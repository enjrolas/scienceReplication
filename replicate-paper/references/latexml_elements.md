# LaTeXML XML Element Reference

## Namespace

All elements use the default namespace: `http://dlmf.nist.gov/LaTeXML`

When using Python's `xml.etree.ElementTree`, prefix all tag names:
```python
NS = "{http://dlmf.nist.gov/LaTeXML}"
root.findall(f".//{NS}section")
```

## Document Structure

```
document
├── title                    # Paper title (may contain <break/> elements)
├── creator[@role="author"]
│   ├── personname           # Author name
│   └── contact              # Affiliation, email
├── abstract
│   └── p                    # Abstract paragraphs
├── section[@xml:id="S1"]    # Top-level sections
│   ├── tags/tag[@role="refnum"]  # Section number (e.g. "1")
│   ├── title                # Section title (contains <tag> child to strip)
│   ├── para[@xml:id="S1.p1"]
│   │   └── p               # Paragraph text with inline elements
│   └── subsection[@xml:id="S3.SS1"]
│       ├── tags/tag[@role="refnum"]
│       ├── title
│       └── para/p
├── figure[@xml:id="S4.F1"]  # Figures (often after all sections)
│   ├── tags/tag[@role="refnum"]
│   ├── caption              # Full caption text
│   ├── toccaption           # Short caption for TOC
│   └── graphics[@graphic]   # Image references
└── bibliography
    └── biblist/bibitem      # Bibliography entries
```

## Key Elements

### Math

The most important element for understanding equations. Has two representations:

1. **`tex` attribute** (USE THIS): Contains the original LaTeX source
   ```xml
   <Math mode="inline" tex="E(z_{i}|x_{i})" text="..." xml:id="S3.SS1.p1.m6">
   ```

2. **`XMath` child tree** (AVOID): Verbose MathML-like representation with `XMApp`, `XMTok`, `XMWrap` etc.

Always prefer the `tex` attribute. Clean it by:
- Removing `\displaystyle`
- Replacing `&#10;` with space
- Decoding HTML entities (`&gt;` -> `>`, `&lt;` -> `<`)

### Equations (numbered/display)

```
equationgroup[@xml:id="S3.E1"]
└── equation[@labels="LABEL:eq:OLS"]
    └── MathFork
        └── MathBranch
            └── td
                └── Math[@tex="..."]  # The equation's LaTeX
```

The `labels` attribute on `equation` contains the LaTeX label (e.g. `LABEL:eq:OLS`).
The equation number is in `tags/tag[@role="refnum"]` on the equationgroup.

### Inline Math

Directly inside `p` elements:
```xml
<Math mode="inline" tex="\tau" text="tau" xml:id="S3.SS1.p2.m3">
```

### Figures

```xml
<figure labels="LABEL:fig:full" xml:id="S4.F1">
  <caption>Full caption text with <Math> and <ref> elements...</caption>
  <graphics graphic="filename.eps" xml:id="S4.F1.g1"/>
</figure>
```

### Citations

```xml
<cite class="ltx_citemacro_cite">
  <bibref bibrefs="KKM2023" show="Authors Phrase1YearPhrase2">
```

The `bibrefs` attribute contains the citation key(s).

### Cross-references

```xml
<ref labelref="LABEL:eq:OLS"/>
```

## Extracting Text Content

To get clean text from a `p` element, recursively collect `.text` and `.tail` from all children. Replace `Math` elements with their `tex` attribute value (wrapped in `$...$` for inline). Skip `tags`, `cite` internal structure.

## Common ID Patterns

| Pattern     | Meaning                    |
|-------------|----------------------------|
| `S1`        | Section 1                  |
| `S3.SS1`    | Section 3, Subsection 1    |
| `S3.E1`     | Section 3, Equation 1      |
| `S4.F1`     | Section 4, Figure 1        |
| `S3.SS1.p1` | Section 3.1, Paragraph 1   |
| `S3.SS1.p1.m1` | Inline math in that para |
