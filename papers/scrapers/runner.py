import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sciencereplication.settings')

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from papers.models import Paper
from papers.scrapers.dataset_spider import DatasetSpider


def run_dataset_spider():
    """Run the dataset discovery spider for all papers with unverified dataset links."""
    papers_with_links = Paper.objects.exclude(dataset_links=[])

    paper_links = []
    for paper in papers_with_links:
        for link in paper.dataset_links:
            if not link.get('verified', False):
                paper_links.append({
                    'paper_id': paper.id,
                    'url': link['url'],
                    'domain': link.get('domain', ''),
                    'description': link.get('description', ''),
                })

    if not paper_links:
        return 'No unverified links to check'

    settings = get_project_settings()
    settings.setmodule('papers.scrapers.settings')

    process = CrawlerProcess(settings)
    process.crawl(DatasetSpider, paper_links=paper_links)
    process.start()

    return f'Processed {len(paper_links)} links'
