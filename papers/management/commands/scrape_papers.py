import re
import time
from datetime import datetime, timedelta
from pathlib import Path

import feedparser
import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from papers.models import Topic, Paper
from papers.latex_processor import process_paper_latex

ARXIV_API = 'http://export.arxiv.org/api/query'
BIORXIV_API = 'https://api.biorxiv.org/details/biorxiv'

KNOWN_DATA_DOMAINS = [
    'github.com', 'zenodo.org', 'figshare.com', 'osf.io',
    'dataverse', 'dryad', 'kaggle.com', 'data.mendeley.com',
    'openneuro.org', 'huggingface.co/datasets',
]


class Command(BaseCommand):
    help = 'Scrape arxiv and biorxiv for papers matching topic search terms'

    def add_arguments(self, parser):
        parser.add_argument('--topic', type=str, help='Slug of a specific topic to scrape')
        parser.add_argument('--max-results', type=int, default=50, help='Max results per source')
        parser.add_argument('--download', action='store_true', help='Download PDFs and LaTeX source')
        parser.add_argument('--skip-biorxiv', action='store_true', help='Skip biorxiv (no LaTeX)')
        parser.add_argument('--discover-datasets', action='store_true',
                            help='Run Scrapy dataset spider after scraping')

    def handle(self, *args, **options):
        topic_slug = options.get('topic')
        max_results = options['max_results']
        download = options['download']
        discover_datasets = options['discover_datasets']

        if topic_slug:
            topics = Topic.objects.filter(slug=topic_slug)
            if not topics.exists():
                self.stderr.write(f'Topic "{topic_slug}" not found')
                return
        else:
            topics = Topic.objects.all()

        if not topics.exists():
            self.stderr.write('No topics configured. Add topics via the management UI or Django admin.')
            return

        for topic in topics:
            self.stdout.write(f'\n=== Scraping for topic: {topic.name} ===')
            self.stdout.write(f'Search terms: {topic.search_terms}')

            self._scrape_arxiv(topic, max_results, download)

            if not options['skip_biorxiv']:
                self._scrape_biorxiv(topic, max_results, download)

        if discover_datasets:
            self._run_dataset_discovery()

        self.stdout.write(self.style.SUCCESS('\nScraping complete.'))

    def _scrape_arxiv(self, topic, max_results, download):
        self.stdout.write(f'\n--- arXiv search ---')
        params = {
            'search_query': f'all:{topic.search_terms}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending',
        }

        try:
            resp = requests.get(ARXIV_API, params=params, timeout=30)
            resp.raise_for_status()
        except requests.RequestException as e:
            self.stderr.write(f'arXiv API error: {e}')
            return

        feed = feedparser.parse(resp.text)
        added = 0
        skipped_no_latex = 0

        for entry in feed.entries:
            arxiv_id = entry.id.split('/abs/')[-1]
            base_id = re.sub(r'v\d+$', '', arxiv_id)

            if Paper.objects.filter(source='arxiv', source_id=base_id, topic=topic).exists():
                self.stdout.write(f'  Skip (exists): {base_id}')
                continue

            # LaTeX source is required — skip papers without it
            has_latex = self._check_arxiv_latex(base_id)
            if not has_latex:
                skipped_no_latex += 1
                self.stdout.write(f'  Skip (no LaTeX): {base_id}')
                time.sleep(0.3)
                continue

            authors = ', '.join(a.get('name', '') for a in entry.get('authors', []))
            published = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published = datetime(*entry.published_parsed[:3]).date()

            # Extract dataset links from abstract, comments, and related links
            all_text = ' '.join([
                entry.get('summary', ''),
                entry.get('title', ''),
                entry.get('arxiv_comment', ''),
                entry.get('arxiv_journal_ref', ''),
            ])

            # Also check arxiv "related" links for dataset pointers
            dataset_links = self._extract_dataset_links_from_text(all_text)
            for link in entry.get('links', []):
                href = link.get('href', '')
                link_type = link.get('type', '')
                title = link.get('title', '')
                if href and any(d in href.lower() for d in KNOWN_DATA_DOMAINS):
                    if href not in {dl['url'] for dl in dataset_links}:
                        dataset_links.append({
                            'url': href,
                            'domain': self._match_domain(href),
                            'description': title or link_type or 'Related link',
                            'verified': False,
                        })

            paper = Paper(
                topic=topic,
                source='arxiv',
                source_id=base_id,
                title=entry.title.replace('\n', ' ').strip(),
                authors=authors,
                abstract=entry.get('summary', '').strip(),
                published_date=published,
                url=entry.link,
                pdf_url=f'https://arxiv.org/pdf/{base_id}',
                latex_url=f'https://arxiv.org/e-print/{base_id}',
                has_latex=True,
                dataset_links=dataset_links,
            )

            if download:
                self._download_arxiv_files(paper, base_id)

            paper.save()

            # Download LaTeX bundle and convert to XML
            if process_paper_latex(paper):
                self.stdout.write(f'    XML generated: {paper.xml_path}')
            else:
                self.stdout.write(f'    XML conversion failed')

            added += 1
            ds = f'({len(dataset_links)} dataset links)' if dataset_links else ''
            self.stdout.write(f'  Added: {base_id} {ds}')
            time.sleep(1)

        self.stdout.write(f'  arXiv: {added} added, {skipped_no_latex} skipped (no LaTeX)')

    def _check_arxiv_latex(self, arxiv_id):
        url = f'https://arxiv.org/e-print/{arxiv_id}'
        try:
            resp = requests.head(url, timeout=10, allow_redirects=True)
            content_type = resp.headers.get('Content-Type', '')
            return resp.status_code == 200 and (
                'gzip' in content_type or 'tar' in content_type or 'x-eprint' in content_type
            )
        except requests.RequestException:
            return False

    def _download_arxiv_files(self, paper, arxiv_id):
        files_dir = Path(settings.PAPER_FILES_DIR) / 'arxiv' / arxiv_id
        files_dir.mkdir(parents=True, exist_ok=True)

        pdf_url = f'https://arxiv.org/pdf/{arxiv_id}.pdf'
        pdf_path = files_dir / f'{arxiv_id.replace("/", "_")}.pdf'
        if self._download_file(pdf_url, pdf_path):
            paper.has_pdf = True
            paper.pdf_path = str(pdf_path.relative_to(settings.BASE_DIR))

        eprint_url = f'https://arxiv.org/e-print/{arxiv_id}'
        latex_path = files_dir / f'{arxiv_id.replace("/", "_")}_source.tar.gz'
        if self._download_file(eprint_url, latex_path):
            paper.latex_path = str(latex_path.relative_to(settings.BASE_DIR))

        time.sleep(1)

    def _scrape_biorxiv(self, topic, max_results, download):
        self.stdout.write(f'\n--- bioRxiv search ---')
        self.stdout.write(f'  Note: bioRxiv papers rarely have LaTeX source.')

        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        cursor = 0
        found = 0
        search_words = topic.search_terms.lower().split()

        while found < max_results:
            api_url = f'{BIORXIV_API}/{start_date}/{end_date}/{cursor}'
            try:
                resp = requests.get(api_url, timeout=30,
                                    headers={'User-Agent': 'ScienceReplication/1.0'})
                resp.raise_for_status()
                data = resp.json()
            except (requests.RequestException, ValueError) as e:
                self.stderr.write(f'  bioRxiv API error: {e}')
                break

            messages = data.get('messages', [{}])
            total = int(messages[0].get('total', 0)) if messages else 0
            collection = data.get('collection', [])

            if not collection:
                break

            for item in collection:
                title = item.get('title', '')
                abstract = item.get('abstract', '')
                text = (title + ' ' + abstract).lower()

                if not any(w in text for w in search_words):
                    continue

                doi = item.get('doi', '')
                if not doi:
                    continue

                if Paper.objects.filter(source='biorxiv', source_id=doi, topic=topic).exists():
                    continue

                pub_date = None
                if item.get('date'):
                    try:
                        pub_date = datetime.strptime(item['date'], '%Y-%m-%d').date()
                    except ValueError:
                        pass

                dataset_links = self._extract_dataset_links_from_text(
                    abstract + ' ' + title
                )

                paper = Paper(
                    topic=topic,
                    source='biorxiv',
                    source_id=doi,
                    title=title,
                    authors=item.get('authors', ''),
                    abstract=abstract,
                    published_date=pub_date,
                    url=f'https://www.biorxiv.org/content/{doi}',
                    pdf_url=f'https://www.biorxiv.org/content/{doi}.full.pdf',
                    has_pdf=True,
                    has_latex=False,
                    dataset_links=dataset_links,
                )

                if download:
                    self._download_biorxiv_pdf(paper, doi)

                paper.save()
                found += 1
                ds = f'({len(dataset_links)} dataset links)' if dataset_links else ''
                self.stdout.write(f'  Added: {doi} {ds}')

                if found >= max_results:
                    break

            cursor += len(collection)
            if cursor >= total:
                break
            time.sleep(1)

        self.stdout.write(f'  bioRxiv: {found} papers added')

    def _download_biorxiv_pdf(self, paper, doi):
        files_dir = Path(settings.PAPER_FILES_DIR) / 'biorxiv' / doi.replace('/', '_')
        files_dir.mkdir(parents=True, exist_ok=True)

        pdf_url = f'https://www.biorxiv.org/content/{doi}.full.pdf'
        pdf_path = files_dir / f'{doi.replace("/", "_")}.pdf'
        if self._download_file(pdf_url, pdf_path):
            paper.pdf_path = str(pdf_path.relative_to(settings.BASE_DIR))

    def _download_file(self, url, path):
        try:
            resp = requests.get(url, timeout=60, stream=True,
                                headers={'User-Agent': 'ScienceReplication/1.0'})
            resp.raise_for_status()
            with open(path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            self.stdout.write(f'    Downloaded: {path.name}')
            return True
        except requests.RequestException as e:
            self.stderr.write(f'    Download failed ({url}): {e}')
            return False

    def _match_domain(self, url):
        url_lower = url.lower()
        for domain in KNOWN_DATA_DOMAINS:
            if domain in url_lower:
                return domain
        return None

    def _extract_dataset_links_from_text(self, text):
        urls = re.findall(r'https?://[^\s<>"\')\]]+', text)
        dataset_links = []
        seen = set()

        for url in urls:
            url = url.rstrip('.,;:')
            if url in seen:
                continue
            domain = self._match_domain(url)
            if domain:
                dataset_links.append({
                    'url': url,
                    'domain': domain,
                    'description': domain,
                    'verified': False,
                })
                seen.add(url)

        return dataset_links

    def _run_dataset_discovery(self):
        """Run Scrapy dataset spider to verify and enrich dataset links."""
        self.stdout.write('\n--- Running dataset discovery spider ---')
        from papers.scrapers.runner import run_dataset_spider
        results = run_dataset_spider()
        self.stdout.write(f'  Dataset discovery complete: {results}')
