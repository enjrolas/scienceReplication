"""Download LaTeX bundles, store locally, and convert to XML via LaTeXML."""
import os
import shutil
import subprocess
import tarfile
import tempfile
import zipfile
from pathlib import Path

import requests
from django.conf import settings


def get_paper_dir(paper):
    """Get the local directory for a paper's files."""
    safe_id = paper.source_id.replace('/', '_')
    paper_dir = Path(settings.PAPER_FILES_DIR) / paper.source / safe_id
    paper_dir.mkdir(parents=True, exist_ok=True)
    return paper_dir


def download_latex_bundle(paper):
    """Download the LaTeX source bundle for a paper. Returns the local path or None."""
    if not paper.latex_url:
        return None

    paper_dir = get_paper_dir(paper)
    safe_id = paper.source_id.replace('/', '_')
    bundle_path = paper_dir / f'{safe_id}_source.tar.gz'

    if bundle_path.exists():
        return bundle_path

    try:
        resp = requests.get(paper.latex_url, timeout=60, stream=True,
                            headers={'User-Agent': 'ScienceReplication/1.0'})
        resp.raise_for_status()
        with open(bundle_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return bundle_path
    except requests.RequestException:
        return None


def download_pdf(paper):
    """Download the PDF for a paper. Returns the local path or None."""
    if not paper.pdf_url:
        return None

    paper_dir = get_paper_dir(paper)
    safe_id = paper.source_id.replace('/', '_')
    pdf_path = paper_dir / f'{safe_id}.pdf'

    if pdf_path.exists():
        return pdf_path

    try:
        resp = requests.get(paper.pdf_url, timeout=60, stream=True,
                            headers={'User-Agent': 'ScienceReplication/1.0'})
        resp.raise_for_status()
        with open(pdf_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return pdf_path
    except requests.RequestException:
        return None


def find_main_tex(directory):
    """Find the main .tex file in a directory."""
    tex_files = list(Path(directory).rglob('*.tex'))
    if not tex_files:
        return None

    # Prefer known main file names
    for name in ('main.tex', 'paper.tex', 'manuscript.tex', 'article.tex'):
        for f in tex_files:
            if f.name.lower() == name:
                return f

    # Look for \documentclass in the file
    for f in tex_files:
        try:
            content = f.read_text(errors='replace')
            if '\\documentclass' in content:
                return f
        except Exception:
            continue

    # Fall back to largest
    return max(tex_files, key=lambda f: f.stat().st_size)


def extract_latex_bundle(bundle_path, dest_dir):
    """Extract a LaTeX bundle (.tar.gz, .zip, .gz, .tex) into dest_dir. Returns the main .tex path."""
    bundle_path = Path(bundle_path)
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    name = bundle_path.name.lower()

    try:
        if name.endswith('.zip'):
            with zipfile.ZipFile(bundle_path, 'r') as zf:
                zf.extractall(dest_dir)
        elif name.endswith('.tar.gz') or name.endswith('.tgz') or name.endswith('.tar'):
            with tarfile.open(bundle_path, 'r:*') as tf:
                tf.extractall(dest_dir)
        elif name.endswith('.gz'):
            # Single gzipped file — might be a .tex or a tar
            import gzip
            with gzip.open(bundle_path, 'rb') as gz:
                content = gz.read(512)
                gz.seek(0)
                # Check if it's a tar inside
                if content[:5] == b'\\docu' or content[:1] == b'%':
                    # It's a gzipped .tex file
                    tex_path = dest_dir / bundle_path.stem
                    if not str(tex_path).endswith('.tex'):
                        tex_path = tex_path.with_suffix('.tex')
                    tex_path.write_bytes(gz.read())
                else:
                    # Try as tar
                    gz.close()
                    with tarfile.open(bundle_path, 'r:gz') as tf:
                        tf.extractall(dest_dir)
        elif name.endswith('.tex'):
            shutil.copy2(bundle_path, dest_dir / bundle_path.name)
        else:
            # Try tar, then just copy
            try:
                with tarfile.open(bundle_path, 'r:*') as tf:
                    tf.extractall(dest_dir)
            except tarfile.TarError:
                shutil.copy2(bundle_path, dest_dir / bundle_path.name)
    except Exception:
        return None

    return find_main_tex(dest_dir)


def convert_to_xml(tex_path, output_path=None):
    """Convert a .tex file to XML using LaTeXML. Returns the XML path or None."""
    tex_path = Path(tex_path)
    if output_path is None:
        output_path = tex_path.with_suffix('.xml')
    else:
        output_path = Path(output_path)

    try:
        result = subprocess.run(
            ['latexml', '--dest', str(output_path), str(tex_path)],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(tex_path.parent),
        )
        if output_path.exists() and output_path.stat().st_size > 0:
            return output_path
        return None
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return None


def process_paper_latex(paper):
    """Full pipeline: download LaTeX bundle, extract, convert to XML.
    Updates the paper model fields. Returns True on success."""

    paper_dir = get_paper_dir(paper)
    safe_id = paper.source_id.replace('/', '_')

    # Step 1: Get the LaTeX bundle
    bundle_path = None
    if paper.latex_path and Path(settings.BASE_DIR / paper.latex_path).exists():
        bundle_path = Path(settings.BASE_DIR / paper.latex_path)
    elif paper.source == 'upload' and paper.latex_path:
        # Uploaded files are in MEDIA_ROOT
        media_path = Path(settings.MEDIA_ROOT) / paper.latex_path
        if media_path.exists():
            bundle_path = media_path
    else:
        bundle_path = download_latex_bundle(paper)

    if not bundle_path:
        return False

    # Update latex_path if we just downloaded
    rel_path = str(bundle_path.relative_to(settings.BASE_DIR))
    if paper.latex_path != rel_path:
        paper.latex_path = rel_path
        paper.has_latex = True

    # Step 2: Extract to a working directory
    extract_dir = paper_dir / 'latex_extracted'
    if extract_dir.exists():
        shutil.rmtree(extract_dir)

    main_tex = extract_latex_bundle(bundle_path, extract_dir)
    if not main_tex:
        return False

    # Step 3: Convert to XML
    xml_output = paper_dir / f'{safe_id}.xml'
    xml_path = convert_to_xml(main_tex, xml_output)
    if xml_path:
        paper.xml_path = str(xml_path.relative_to(settings.BASE_DIR))

    paper.save()
    return xml_path is not None
