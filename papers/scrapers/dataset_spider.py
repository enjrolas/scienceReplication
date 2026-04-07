import re

import scrapy

from papers.scrapers.items import DatasetLinkItem

KNOWN_DATA_DOMAINS = [
    'github.com', 'zenodo.org', 'figshare.com', 'osf.io',
    'dataverse', 'dryad', 'kaggle.com', 'data.mendeley.com',
    'openneuro.org', 'huggingface.co/datasets',
]


def match_domain(url):
    url_lower = url.lower()
    for domain in KNOWN_DATA_DOMAINS:
        if domain in url_lower:
            return domain
    return None


class DatasetSpider(scrapy.Spider):
    """Spider that verifies and enriches dataset links for papers.

    For known data repository domains, it fetches the page and extracts
    metadata (size, description). For unknown domains, it does a HEAD
    request to check reachability.
    """
    name = 'dataset_spider'

    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS': 4,
        'DOWNLOAD_DELAY': 1.0,
    }

    def __init__(self, paper_links=None, *args, **kwargs):
        """
        Args:
            paper_links: list of dicts with keys:
                paper_id, url, domain, description
        """
        super().__init__(*args, **kwargs)
        self.paper_links = paper_links or []

    def start_requests(self):
        for link in self.paper_links:
            domain = link.get('domain') or match_domain(link['url'])
            if domain:
                # Known domain: full page fetch for metadata extraction
                yield scrapy.Request(
                    url=link['url'],
                    callback=self.parse_known_domain,
                    cb_kwargs={'paper_id': link['paper_id'], 'domain': domain},
                    errback=self.handle_error,
                    meta={'paper_id': link['paper_id']},
                )
            else:
                # Unknown domain: HEAD request only
                yield scrapy.Request(
                    url=link['url'],
                    method='HEAD',
                    callback=self.parse_head,
                    cb_kwargs={'paper_id': link['paper_id']},
                    errback=self.handle_error,
                    meta={'paper_id': link['paper_id']},
                )

    def parse_known_domain(self, response, paper_id, domain):
        item = DatasetLinkItem(
            paper_id=paper_id,
            url=response.url,
            domain=domain,
            verified=True,
            content_type=response.headers.get('Content-Type', b'').decode('utf-8', errors='ignore'),
        )

        if 'zenodo.org' in domain:
            item['description'] = self._parse_zenodo(response)
            item['size_info'] = self._parse_zenodo_size(response)
        elif 'github.com' in domain:
            item['description'] = self._parse_github(response)
            item['size_info'] = ''
        elif 'figshare.com' in domain:
            item['description'] = self._parse_figshare(response)
            item['size_info'] = self._parse_figshare_size(response)
        elif 'osf.io' in domain:
            item['description'] = self._parse_osf(response)
            item['size_info'] = ''
        else:
            title = response.css('title::text').get('')
            item['description'] = title.strip()[:200] if title else domain
            item['size_info'] = ''

        yield item

    def parse_head(self, response, paper_id):
        yield DatasetLinkItem(
            paper_id=paper_id,
            url=response.url,
            domain=match_domain(response.url),
            description='Verified reachable',
            verified=response.status == 200,
            size_info=response.headers.get('Content-Length', b'').decode('utf-8', errors='ignore'),
            content_type=response.headers.get('Content-Type', b'').decode('utf-8', errors='ignore'),
        )

    def handle_error(self, failure):
        request = failure.request
        paper_id = request.meta.get('paper_id')
        self.logger.warning(f'Failed to fetch {request.url} for paper {paper_id}: {failure.value}')
        yield DatasetLinkItem(
            paper_id=paper_id,
            url=request.url,
            domain=match_domain(request.url),
            description=f'Error: {str(failure.value)[:100]}',
            verified=False,
            size_info='',
            content_type='',
        )

    def _parse_zenodo(self, response):
        title = response.css('h1#record-title::text').get('')
        if not title:
            title = response.css('title::text').get('')
        return title.strip()[:200]

    def _parse_zenodo_size(self, response):
        sizes = response.css('.file-size::text').getall()
        if sizes:
            return ', '.join(s.strip() for s in sizes)
        size_text = response.xpath('//small[contains(text(), "B")]/text()').getall()
        return ', '.join(s.strip() for s in size_text[:5])

    def _parse_github(self, response):
        desc = response.css('p.f4.my-3::text').get('')
        if not desc:
            desc = response.css('[itemprop="about"]::text').get('')
        return desc.strip()[:200] if desc else 'GitHub repository'

    def _parse_figshare(self, response):
        title = response.css('h2.title::text').get('')
        if not title:
            title = response.css('title::text').get('')
        return title.strip()[:200]

    def _parse_figshare_size(self, response):
        size = response.css('.file-size::text').get('')
        return size.strip() if size else ''

    def _parse_osf(self, response):
        title = response.css('h1#nodeTitleEditable::text').get('')
        if not title:
            title = response.css('title::text').get('')
        return title.strip()[:200]
