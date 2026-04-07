import subprocess
import threading

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TopicForm, LoginForm, PaperUploadForm
from .latex_parser import parse_latex
from .latex_processor import process_paper_latex
from .models import Topic, Paper, PaperUpload


def _check_auth(request):
    return request.session.get('manage_authenticated', False)


def manage_login(request):
    if _check_auth(request):
        return redirect('manage_dashboard')

    form = LoginForm()
    error = None

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == settings.MANAGE_PASSWORD:
                request.session['manage_authenticated'] = True
                return redirect('manage_dashboard')
            else:
                error = 'Incorrect password.'

    return render(request, 'papers/login.html', {'form': form, 'error': error})


def manage_logout(request):
    request.session.pop('manage_authenticated', None)
    return redirect('manage_login')


def manage_dashboard(request):
    if not _check_auth(request):
        return redirect('manage_login')

    topics = Topic.objects.prefetch_related('papers').all()
    return render(request, 'papers/manage.html', {
        'topics': topics,
        'total_papers': Paper.objects.count(),
    })


def manage_topic_add(request):
    if not _check_auth(request):
        return redirect('manage_login')

    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_dashboard')
    else:
        form = TopicForm()

    return render(request, 'papers/topic_form.html', {'form': form, 'action': 'Add'})


def manage_topic_edit(request, slug):
    if not _check_auth(request):
        return redirect('manage_login')

    topic = get_object_or_404(Topic, slug=slug)

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('manage_dashboard')
    else:
        form = TopicForm(instance=topic)

    return render(request, 'papers/topic_form.html', {'form': form, 'action': 'Edit', 'topic': topic})


def manage_topic_delete(request, slug):
    if not _check_auth(request):
        return redirect('manage_login')

    topic = get_object_or_404(Topic, slug=slug)
    if request.method == 'POST':
        topic.delete()
    return redirect('manage_dashboard')


def _run_command_background(args):
    """Run a management command in a background thread."""
    def _run():
        subprocess.run(
            ['python3', 'manage.py'] + args,
            cwd=str(settings.BASE_DIR),
            capture_output=True,
        )
    thread = threading.Thread(target=_run, daemon=True)
    thread.start()


def manage_scrape(request):
    if not _check_auth(request):
        return JsonResponse({'error': 'Not authenticated'}, status=403)

    if request.method == 'POST':
        topic_slug = request.POST.get('topic', '')
        args = ['scrape_papers', '--max-results', '50']
        if topic_slug:
            args += ['--topic', topic_slug]
        _run_command_background(args)
        return JsonResponse({'status': 'Scraping started'})

    return JsonResponse({'error': 'POST required'}, status=405)


def manage_generate(request):
    if not _check_auth(request):
        return JsonResponse({'error': 'Not authenticated'}, status=403)

    if request.method == 'POST':
        _run_command_background(['generate_site'])
        return JsonResponse({'status': 'Site generation started'})

    return JsonResponse({'error': 'POST required'}, status=405)


def upload_paper(request):
    success = False

    if request.method == 'POST':
        form = PaperUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save()

            # Parse the LaTeX file to extract metadata
            parsed = parse_latex(upload.latex_file.path)

            # Build dataset_links from the provided URL
            dataset_links = []
            if upload.dataset_url:
                dataset_links.append({
                    'url': upload.dataset_url,
                    'domain': '',
                    'description': 'User-submitted dataset',
                    'verified': False,
                })

            # Create a Paper model entry from the parsed data
            paper = Paper.objects.create(
                topic=upload.topic,
                source='upload',
                source_id=f'upload-{upload.id}',
                title=parsed['title'] or upload.title,
                authors=parsed['authors'] or upload.authors,
                abstract=parsed['abstract'],
                url=upload.paper_url or '',
                pdf_url=upload.paper_url if upload.pdf_file else '',
                latex_url='',
                has_pdf=bool(upload.pdf_file),
                pdf_path=upload.pdf_file.name if upload.pdf_file else '',
                has_latex=True,
                latex_path=upload.latex_file.name,
                dataset_links=dataset_links,
            )

            # Convert LaTeX to XML via LaTeXML
            process_paper_latex(paper)

            success = True
            form = PaperUploadForm()
    else:
        form = PaperUploadForm()

    return render(request, 'papers/upload.html', {'form': form, 'success': success})
