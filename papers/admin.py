from django.contrib import admin
from .models import Topic, Paper, PaperUpload


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'search_terms', 'created_at')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('title_short', 'source', 'source_id', 'topic', 'has_pdf', 'has_latex', 'published_date')
    list_filter = ('source', 'topic', 'has_pdf', 'has_latex')
    search_fields = ('title', 'authors', 'abstract')

    def title_short(self, obj):
        return obj.title[:80]
    title_short.short_description = 'Title'


@admin.register(PaperUpload)
class PaperUploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'reviewed', 'submitted_at')
    list_filter = ('topic', 'reviewed')
    search_fields = ('title', 'authors')
