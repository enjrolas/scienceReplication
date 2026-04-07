#!/usr/bin/env python3
"""Parse a LaTeXML XML file and extract structured information for replication.

Usage: python parse_latexml.py <path-to-xml>
Output: JSON to stdout
"""
import json
import re
import sys
import xml.etree.ElementTree as ET

NS = "{http://dlmf.nist.gov/LaTeXML}"


def extract_text(elem):
    """Recursively extract text from an element, replacing Math with $tex$."""
    if elem is None:
        return ""
    parts = []
    if elem.tag == f"{NS}Math":
        tex = elem.get("tex", "")
        tex = clean_tex(tex)
        mode = elem.get("mode", "inline")
        if mode == "inline":
            parts.append(f"${tex}$")
        else:
            parts.append(f"$${tex}$$")
        if elem.tail:
            parts.append(elem.tail)
        return "".join(parts)

    # Skip tag elements inside titles (they contain the section number)
    if elem.tag in (f"{NS}tag", f"{NS}tags"):
        if elem.tail:
            parts.append(elem.tail)
        return "".join(parts)

    # Handle citations: just output "[Author Year]" placeholder
    if elem.tag == f"{NS}cite":
        if elem.tail:
            parts.append(elem.tail)
        return "[citation]" + "".join(parts)

    # Skip bibref internal structure
    if elem.tag in (f"{NS}bibref", f"{NS}bibrefphrase"):
        if elem.tail:
            parts.append(elem.tail)
        return "".join(parts)

    if elem.text:
        parts.append(elem.text)
    for child in elem:
        parts.append(extract_text(child))
    if elem.tail:
        parts.append(elem.tail)
    return "".join(parts)


def clean_tex(tex):
    """Clean a TeX string from a Math element's tex attribute."""
    tex = tex.replace("\\displaystyle", "")
    tex = tex.replace("&#10;", " ")
    tex = tex.replace("&gt;", ">")
    tex = tex.replace("&lt;", "<")
    tex = tex.replace("&amp;", "&")
    tex = re.sub(r"\s+", " ", tex).strip()
    # Remove trailing/leading % (LaTeXML artifacts)
    tex = tex.strip("%").strip()
    return tex


def extract_numbers(text):
    """Extract notable numbers from paragraph text."""
    numbers = []

    # Dollar amounts: $75,000 or $175,000 or $15000
    for m in re.finditer(r"\$(\d{1,3}(?:,\d{3})+|\d{4,})", text):
        val = int(m.group(1).replace(",", ""))
        ctx_start = max(0, m.start() - 40)
        ctx_end = min(len(text), m.end() + 40)
        numbers.append({
            "value": val,
            "raw": m.group(0),
            "context": text[ctx_start:ctx_end].strip(),
        })

    # Percentages: 75% or 0.05%
    for m in re.finditer(r"(\d+(?:\.\d+)?)\s*%", text):
        val = float(m.group(1))
        ctx_start = max(0, m.start() - 40)
        ctx_end = min(len(text), m.end() + 40)
        numbers.append({
            "value": val,
            "raw": m.group(0),
            "context": text[ctx_start:ctx_end].strip(),
        })

    # Large integers (sample sizes, counts): standalone numbers >= 100
    for m in re.finditer(r"(?<!\$)\b(\d{3,}(?:,\d{3})*)\b(?!%)", text):
        raw = m.group(1)
        val = int(raw.replace(",", ""))
        if val < 100:
            continue
        ctx_start = max(0, m.start() - 40)
        ctx_end = min(len(text), m.end() + 40)
        numbers.append({
            "value": val,
            "raw": raw,
            "context": text[ctx_start:ctx_end].strip(),
        })

    # Decimal numbers (coefficients, p-values): e.g., 0.234, -1.56
    for m in re.finditer(r"(?<!\w)-?\d+\.\d+(?!\w)", text):
        val = float(m.group(0))
        ctx_start = max(0, m.start() - 40)
        ctx_end = min(len(text), m.end() + 40)
        numbers.append({
            "value": val,
            "raw": m.group(0),
            "context": text[ctx_start:ctx_end].strip(),
        })

    return numbers


def _find_ancestor_section(root, target):
    """Find the nearest section/subsection ancestor of target within root.

    Returns None if target is a direct descendant of root without any
    intervening section/subsection.
    """
    parent_map = {child: parent for parent in root.iter() for child in parent}
    current = target
    while current in parent_map:
        current = parent_map[current]
        if current is root:
            return None
        if current.tag in (f"{NS}section", f"{NS}subsection"):
            return current
    return None


def parse_section(elem, depth=0):
    """Parse a section or subsection element."""
    section = {
        "id": elem.get("{http://www.w3.org/XML/1998/namespace}id", ""),
        "number": "",
        "title": "",
        "paragraphs": [],
        "equations": [],
        "figures": [],
        "reported_numbers": [],
        "subsections": [],
    }

    # Extract section number
    tags = elem.find(f"{NS}tags")
    if tags is not None:
        refnum = tags.find(f"{NS}tag[@role='refnum']")
        if refnum is not None and refnum.text:
            section["number"] = refnum.text.strip()

    # Extract title
    title_elem = elem.find(f"{NS}title")
    if title_elem is not None:
        section["title"] = extract_text(title_elem).strip()

    # Extract paragraphs
    for para in elem.findall(f"{NS}para"):
        for p in para.findall(f"{NS}p"):
            text = extract_text(p).strip()
            if text:
                section["paragraphs"].append(text)
                section["reported_numbers"].extend(extract_numbers(text))

    # Extract equations (may be nested inside para/p elements)
    for eqgroup in elem.iter(f"{NS}equationgroup"):
        # Skip equations that belong to a child subsection
        parent_section = _find_ancestor_section(elem, eqgroup)
        if parent_section is not None and parent_section is not elem:
            continue

        eq_id = eqgroup.get("{http://www.w3.org/XML/1998/namespace}id", "")
        eq_num = ""
        eq_tags = eqgroup.find(f"{NS}tags")
        if eq_tags is not None:
            eq_refnum = eq_tags.find(f"{NS}tag[@role='refnum']")
            if eq_refnum is not None and eq_refnum.text:
                eq_num = eq_refnum.text.strip()

        for eq in eqgroup.findall(f"{NS}equation"):
            labels = eq.get("labels", "")
            # Find Math elements with tex attribute
            for math in eq.iter(f"{NS}Math"):
                tex = math.get("tex", "")
                if tex:
                    section["equations"].append({
                        "id": eq_id,
                        "label": labels,
                        "tex": clean_tex(tex),
                        "number": eq_num,
                    })
                    break  # one tex per equation is enough

    # Extract subsections
    for sub in elem.findall(f"{NS}subsection"):
        section["subsections"].append(parse_section(sub, depth + 1))

    return section


def parse_figure(elem):
    """Parse a figure element."""
    fig = {
        "id": elem.get("{http://www.w3.org/XML/1998/namespace}id", ""),
        "label": elem.get("labels", ""),
        "caption": "",
        "graphics": [],
        "reported_numbers": [],
    }

    caption_elem = elem.find(f"{NS}caption")
    if caption_elem is not None:
        fig["caption"] = extract_text(caption_elem).strip()
        fig["reported_numbers"] = extract_numbers(fig["caption"])

    for g in elem.findall(f"{NS}graphics"):
        graphic = g.get("graphic", "")
        if graphic:
            fig["graphics"].append(graphic)

    return fig


def parse_document(xml_path):
    """Parse a full LaTeXML XML document."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    doc = {
        "title": "",
        "authors": [],
        "abstract": "",
        "sections": [],
        "figures": [],
        "bibliography_keys": [],
    }

    # Title
    title_elem = root.find(f"{NS}title")
    if title_elem is not None:
        doc["title"] = extract_text(title_elem).strip()

    # Authors
    for creator in root.findall(f"{NS}creator[@role='author']"):
        name_elem = creator.find(f"{NS}personname")
        if name_elem is not None and name_elem.text:
            doc["authors"].append(name_elem.text.strip())

    # Abstract
    abstract_elem = root.find(f"{NS}abstract")
    if abstract_elem is not None:
        parts = []
        for p in abstract_elem.findall(f"{NS}p"):
            text = extract_text(p).strip()
            if text:
                parts.append(text)
        doc["abstract"] = "\n\n".join(parts)

    # Sections
    for section in root.findall(f"{NS}section"):
        doc["sections"].append(parse_section(section))

    # Figures (may be at document level, outside sections)
    for figure in root.findall(f"{NS}figure"):
        doc["figures"].append(parse_figure(figure))

    # Also look for figures inside sections
    for figure in root.iter(f"{NS}figure"):
        fig_id = figure.get("{http://www.w3.org/XML/1998/namespace}id", "")
        if not any(f["id"] == fig_id for f in doc["figures"]):
            doc["figures"].append(parse_figure(figure))

    # Bibliography keys
    for bibitem in root.iter(f"{NS}bibitem"):
        key = bibitem.get("key", "")
        if key:
            doc["bibliography_keys"].append(key)
    # Also from bibref elements
    for bibref in root.iter(f"{NS}bibref"):
        refs = bibref.get("bibrefs", "")
        for ref in refs.split(","):
            ref = ref.strip()
            if ref and ref not in doc["bibliography_keys"]:
                doc["bibliography_keys"].append(ref)

    return doc


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_latexml.py <path-to-xml>", file=sys.stderr)
        sys.exit(1)

    xml_path = sys.argv[1]
    doc = parse_document(xml_path)
    print(json.dumps(doc, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
