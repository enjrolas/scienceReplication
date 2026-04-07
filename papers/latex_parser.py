import re
import tarfile
import zipfile
import tempfile
from pathlib import Path


def parse_latex(file_path):
    """Parse a LaTeX file or archive and extract title, abstract, authors.

    Accepts .tex files, .zip, .tar.gz, or .gz archives.
    Returns dict with 'title', 'abstract', 'authors' keys.
    """
    path = Path(file_path)
    tex_content = _read_tex_content(path)
    if not tex_content:
        return {'title': '', 'abstract': '', 'authors': ''}

    return {
        'title': _extract_title(tex_content),
        'abstract': _extract_abstract(tex_content),
        'authors': _extract_authors(tex_content),
    }


def _read_tex_content(path):
    """Read .tex content from a file or archive."""
    suffix = path.suffix.lower()
    name = path.name.lower()

    if suffix == '.tex':
        return path.read_text(errors='replace')

    if suffix == '.zip':
        return _read_from_zip(path)

    if suffix == '.gz' or name.endswith('.tar.gz'):
        return _read_from_tar(path)

    if suffix == '.tar':
        return _read_from_tar(path)

    # Try reading as plain text
    try:
        return path.read_text(errors='replace')
    except Exception:
        return None


def _read_from_zip(path):
    """Find and read the main .tex file from a zip archive."""
    try:
        with zipfile.ZipFile(path, 'r') as zf:
            tex_files = [f for f in zf.namelist() if f.endswith('.tex')]
            if not tex_files:
                return None
            # Prefer main.tex or the largest .tex file
            main = _pick_main_tex(tex_files, lambda f: len(zf.read(f)))
            return zf.read(main).decode('utf-8', errors='replace')
    except Exception:
        return None


def _read_from_tar(path):
    """Find and read the main .tex file from a tar/tar.gz archive."""
    try:
        with tarfile.open(path, 'r:*') as tf:
            tex_members = [m for m in tf.getmembers() if m.name.endswith('.tex') and m.isfile()]
            if not tex_members:
                return None
            main = _pick_main_tex(
                tex_members,
                lambda m: m.size,
            )
            f = tf.extractfile(main)
            if f:
                return f.read().decode('utf-8', errors='replace')
    except Exception:
        return None


def _pick_main_tex(items, size_fn):
    """Pick the main .tex file — prefer 'main.tex', 'paper.tex', or the largest."""
    for item in items:
        name = item if isinstance(item, str) else item.name
        basename = Path(name).name.lower()
        if basename in ('main.tex', 'paper.tex', 'manuscript.tex', 'article.tex'):
            return item
    # Fall back to largest file
    return max(items, key=size_fn)


def _extract_title(tex):
    """Extract \\title{...} from LaTeX source."""
    # Handle \title{...} possibly spanning multiple lines
    match = re.search(r'\\title\s*(?:\[.*?\])?\s*\{', tex)
    if not match:
        return ''
    return _extract_braced(tex, match.end() - 1)


def _extract_abstract(tex):
    """Extract \\begin{abstract}...\\end{abstract} from LaTeX source."""
    match = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.DOTALL)
    if match:
        return _clean_latex(match.group(1).strip())
    # Try \abstract{...}
    match = re.search(r'\\abstract\s*\{', tex)
    if match:
        return _clean_latex(_extract_braced(tex, match.end() - 1))
    return ''


def _extract_authors(tex):
    """Extract author names from LaTeX source."""
    # Try \author{...}
    match = re.search(r'\\author\s*(?:\[.*?\])?\s*\{', tex)
    if match:
        raw = _extract_braced(tex, match.end() - 1)
        return _clean_authors(raw)
    return ''


def _extract_braced(tex, open_pos):
    """Extract content between matched braces starting at open_pos."""
    if open_pos >= len(tex) or tex[open_pos] != '{':
        return ''
    depth = 0
    start = open_pos + 1
    for i in range(open_pos, len(tex)):
        if tex[i] == '{':
            depth += 1
        elif tex[i] == '}':
            depth -= 1
            if depth == 0:
                return _clean_latex(tex[start:i])
    return _clean_latex(tex[start:])


def _clean_latex(text):
    """Remove common LaTeX commands and clean up text."""
    # Remove comments
    text = re.sub(r'(?<!\\)%.*$', '', text, flags=re.MULTILINE)
    # Remove common formatting commands
    text = re.sub(r'\\(?:textbf|textit|emph|textrm|textsc|textsf)\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\(?:bf|it|em|rm|sc|sf)\b', '', text)
    # Remove \\ and ~
    text = text.replace('\\\\', ' ').replace('~', ' ')
    # Remove remaining simple commands
    text = re.sub(r'\\[a-zA-Z]+\*?(?:\[.*?\])?(?:\{([^}]*)\})?', r'\1', text)
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _clean_authors(raw):
    """Clean up author text from LaTeX."""
    # Remove \and, \AND, etc.
    raw = re.sub(r'\\and\b', ',', raw, flags=re.IGNORECASE)
    # Remove affiliations in \inst{}, \affiliation{}, etc.
    raw = re.sub(r'\\(?:inst|affiliation|institution|email|address|thanks)\{[^}]*\}', '', raw)
    # Remove footnote marks
    raw = re.sub(r'\\(?:footnote|footnotemark|thanksref)\{[^}]*\}', '', raw)
    raw = re.sub(r'\\\w+\{[^}]*\}', '', raw)
    # Clean up
    raw = _clean_latex(raw)
    # Normalize separators
    raw = re.sub(r'\s*,\s*,\s*', ', ', raw)
    raw = re.sub(r'\s+', ' ', raw).strip().strip(',').strip()
    return raw
