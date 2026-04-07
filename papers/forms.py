from django import forms
from .models import Topic, PaperUpload


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'search_terms', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Developmental Psychology'}),
            'search_terms': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. developmental psychology'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Optional description'}),
        }


class PaperUploadForm(forms.ModelForm):
    class Meta:
        model = PaperUpload
        fields = ['topic', 'title', 'authors', 'paper_url', 'latex_file', 'pdf_file', 'code_url', 'dataset_url']
        widgets = {
            'topic': forms.Select(attrs={'class': 'form-input'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Paper title'}),
            'authors': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Author names (optional)'}),
            'paper_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://arxiv.org/abs/... (optional)'}),
            'latex_file': forms.ClearableFileInput(attrs={'class': 'form-input', 'accept': '.tex,.zip,.tar,.tar.gz,.gz'}),
            'pdf_file': forms.ClearableFileInput(attrs={'class': 'form-input', 'accept': '.pdf'}),
            'code_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://github.com/... (optional)'}),
            'dataset_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://zenodo.org/... (optional)'}),
        }


class LoginForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter password'}),
    )
