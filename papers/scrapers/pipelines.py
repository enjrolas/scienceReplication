import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sciencereplication.settings')
django.setup()

from papers.models import Paper


class DatasetLinkPipeline:
    """Save enriched dataset link info back to the Paper model."""

    def __init__(self):
        self.updates = {}  # paper_id -> list of enriched links

    def process_item(self, item, spider):
        paper_id = item['paper_id']
        if paper_id not in self.updates:
            self.updates[paper_id] = []

        self.updates[paper_id].append({
            'url': item['url'],
            'domain': item.get('domain', ''),
            'description': item.get('description', ''),
            'verified': item.get('verified', False),
            'size_info': item.get('size_info', ''),
            'content_type': item.get('content_type', ''),
        })
        return item

    def close_spider(self, spider):
        for paper_id, links in self.updates.items():
            try:
                paper = Paper.objects.get(id=paper_id)
                # Merge with existing links, preferring enriched versions
                existing_urls = {l['url'] for l in paper.dataset_links}
                merged = list(paper.dataset_links)
                for link in links:
                    if link['url'] in existing_urls:
                        # Update existing entry
                        for i, existing in enumerate(merged):
                            if existing['url'] == link['url']:
                                merged[i] = link
                                break
                    else:
                        merged.append(link)
                paper.dataset_links = merged
                paper.save(update_fields=['dataset_links'])
                spider.logger.info(f'Updated paper {paper_id}: {len(merged)} dataset links')
            except Paper.DoesNotExist:
                spider.logger.warning(f'Paper {paper_id} not found')
