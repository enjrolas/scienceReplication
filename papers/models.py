from django.db import models
from django.utils.text import slugify


class Topic(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    search_terms = models.TextField(help_text="Search query for arxiv/biorxiv APIs")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Paper(models.Model):
    SOURCE_CHOICES = [
        ('arxiv', 'arXiv'),
        ('biorxiv', 'bioRxiv'),
        ('upload', 'User Upload'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='papers')
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES)
    source_id = models.CharField(max_length=100, help_text="e.g. arxiv ID like 2301.12345")
    title = models.TextField()
    authors = models.TextField()
    abstract = models.TextField()
    published_date = models.DateField(null=True, blank=True)
    url = models.URLField(max_length=500)

    # Remote URLs for paper resources
    pdf_url = models.URLField(max_length=500, blank=True, help_text="Direct link to PDF")
    latex_url = models.URLField(max_length=500, blank=True, help_text="Direct link to LaTeX source")

    # Local file paths (when downloaded)
    has_pdf = models.BooleanField(default=False)
    pdf_path = models.CharField(max_length=500, blank=True)
    has_latex = models.BooleanField(default=False)
    latex_path = models.CharField(max_length=500, blank=True)

    # LaTeXML-converted XML
    xml_path = models.CharField(max_length=500, blank=True, help_text="Path to LaTeXML-converted XML file")

    # Dataset links (not downloaded, just collected)
    dataset_links = models.JSONField(default=list, blank=True,
        help_text="List of dicts: [{'url': '...', 'description': '...'}]")

    scraped_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('source', 'source_id', 'topic')
        ordering = ['-published_date']

    def __str__(self):
        return f"[{self.source}] {self.title[:80]}"


class PaperUpload(models.Model):
    """User-submitted paper with uploaded files."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='uploads')
    title = models.CharField(max_length=500)
    authors = models.CharField(max_length=500, blank=True)
    paper_url = models.URLField(max_length=500, blank=True, help_text="Link to the paper (optional)")

    # Files
    latex_file = models.FileField(upload_to='uploads/latex/')
    pdf_file = models.FileField(upload_to='uploads/pdf/', blank=True)

    # Links
    code_url = models.URLField(max_length=500, blank=True, help_text="Link to code repository (optional)")
    dataset_url = models.URLField(max_length=500, blank=True, help_text="Link to dataset (optional)")

    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Upload: {self.title[:80]}"
