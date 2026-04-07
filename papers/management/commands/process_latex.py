import time

from django.core.management.base import BaseCommand

from papers.models import Paper
from papers.latex_processor import process_paper_latex, download_pdf


class Command(BaseCommand):
    help = 'Download LaTeX bundles and convert to XML for papers in the database'

    def add_arguments(self, parser):
        parser.add_argument('--paper-id', type=int, help='Process a specific paper by ID')
        parser.add_argument('--pending-only', action='store_true',
                            help='Only process papers missing XML')
        parser.add_argument('--download-pdfs', action='store_true',
                            help='Also download PDFs locally')
        parser.add_argument('--limit', type=int, default=0,
                            help='Max papers to process (0 = all)')

    def handle(self, *args, **options):
        if options['paper_id']:
            papers = Paper.objects.filter(id=options['paper_id'])
        elif options['pending_only']:
            papers = Paper.objects.filter(has_latex=True, xml_path='')
        else:
            papers = Paper.objects.filter(has_latex=True)

        if options['limit']:
            papers = papers[:options['limit']]

        total = papers.count()
        self.stdout.write(f'Processing {total} papers...\n')

        success = 0
        failed = 0

        for i, paper in enumerate(papers, 1):
            self.stdout.write(f'[{i}/{total}] {paper.source_id}: {paper.title[:60]}...')

            if options['download_pdfs'] and paper.pdf_url and not paper.pdf_path:
                pdf_path = download_pdf(paper)
                if pdf_path:
                    from django.conf import settings
                    paper.has_pdf = True
                    paper.pdf_path = str(pdf_path.relative_to(settings.BASE_DIR))
                    paper.save(update_fields=['has_pdf', 'pdf_path'])
                    self.stdout.write(f'  PDF downloaded')

            result = process_paper_latex(paper)
            if result:
                success += 1
                self.stdout.write(self.style.SUCCESS(f'  XML generated: {paper.xml_path}'))
            else:
                failed += 1
                self.stdout.write(self.style.WARNING(f'  Failed to convert'))

            time.sleep(0.5)  # Rate limit for downloads

        self.stdout.write(f'\nDone: {success} converted, {failed} failed')
