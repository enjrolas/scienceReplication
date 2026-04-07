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
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='papers')
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES)
    source_id = models.CharField(max_length=100, help_text="e.g. arxiv ID like 2301.12345")
    title = models.TextField()
    authors = models.TextField()
    abstract = models.TextField()
    published_date = models.DateField(null=True, blank=True)
    url = models.URLField(max_length=500)

    # File availability
    has_pdf = models.BooleanField(default=False)
    pdf_path = models.CharField(max_length=500, blank=True)
    has_latex = models.BooleanField(default=False)
    latex_path = models.CharField(max_length=500, blank=True)

    # Dataset links (not downloaded, just collected)
    dataset_links = models.JSONField(default=list, blank=True,
        help_text="List of dicts: [{'url': '...', 'description': '...'}]")

    scraped_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('source', 'source_id', 'topic')
        ordering = ['-published_date']

    def __str__(self):
        return f"[{self.source}] {self.title[:80]}"
