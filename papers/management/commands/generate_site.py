import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from papers.models import Topic, Paper


class Command(BaseCommand):
    help = 'Generate static HTML site from paper database'

    def add_arguments(self, parser):
        parser.add_argument('--output', type=str, help='Output directory (default: STATIC_SITE_DIR from settings)')

    def handle(self, *args, **options):
        output_dir = Path(options.get('output') or settings.STATIC_SITE_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)

        topics = Topic.objects.prefetch_related('papers').all()

        # Generate index page
        index_html = render_to_string('papers/index.html', {
            'topics': topics,
            'total_papers': Paper.objects.count(),
        })
        (output_dir / 'index.html').write_text(index_html)
        self.stdout.write(f'Generated: index.html')

        # Generate topic pages
        for topic in topics:
            papers = topic.papers.all()
            topic_html = render_to_string('papers/topic.html', {
                'topic': topic,
                'papers': papers,
                'papers_with_latex': papers.filter(has_latex=True).count(),
                'papers_with_datasets': papers.exclude(dataset_links=[]).count(),
            })
            topic_dir = output_dir / topic.slug
            topic_dir.mkdir(parents=True, exist_ok=True)
            (topic_dir / 'index.html').write_text(topic_html)
            self.stdout.write(f'Generated: {topic.slug}/index.html ({papers.count()} papers)')

        # Copy static assets
        assets_src = Path(__file__).resolve().parent.parent.parent / 'static' / 'papers'
        assets_dst = output_dir / 'static'
        if assets_src.exists():
            if assets_dst.exists():
                shutil.rmtree(assets_dst)
            shutil.copytree(assets_src, assets_dst)
            self.stdout.write(f'Copied static assets')

        self.stdout.write(self.style.SUCCESS(f'\nSite generated in: {output_dir}'))
