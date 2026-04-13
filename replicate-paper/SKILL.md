---
name: replicate-paper
description: "Replicate a scientific paper's analysis as a standalone Python project. Use this skill whenever a user wants to replicate, reproduce, or verify the quantitative results of a scientific paper. Trigger when: the user provides a LaTeXML XML file and dataset(s) in a folder and wants to build a replication project; the user says 'replicate this paper', 'reproduce these results', 'verify this analysis', or 'check these findings'; the user has a paper and data files and wants automated analysis code generated. Also trigger when the user mentions replication, reproduction, or independent verification of scientific findings alongside data files. This skill handles the full pipeline: parsing the paper, understanding the methods, generating Python code, running it, and comparing results. Do NOT trigger for: simply reading or summarizing papers without replication, general data analysis without a specific paper to replicate, or LaTeX formatting/conversion tasks."
---

# Replicate Paper

Convert a scientific paper (LaTeXML XML) and its dataset into a standalone Python project that replicates the paper's analysis, then compare computed results against the paper's reported values.

## Workflow

Follow these steps in order. The skill bundles reusable scripts in `scripts/` (relative to this SKILL.md) for parsing and comparison. Analysis code is generated fresh for each paper.

### Step 1: Identify Inputs

Locate the input folder. It should contain:
- One `.xml` file (LaTeXML format)
- One or more data files (CSV, TSV, Excel, Parquet, Stata .dta, SPSS .sav, or other tabular)

If the user hasn't specified a folder, ask them. If the folder contains multiple XML files, ask which is the paper.

### Step 2: Parse the Paper

Run the bundled parser to extract the paper's structure:

```bash
python <skill-dir>/scripts/parse_latexml.py <path-to-xml>
```

This outputs JSON with `title`, `authors`, `abstract`, `sections` (with `paragraphs`, `equations`, `reported_numbers`), `figures`, and `bibliography_keys`.

Read the output carefully. Pay attention to:
- **Equations**: The `tex` field contains the original LaTeX. This is the authoritative specification of each model. See `references/latexml_elements.md` for parsing details.
- **Reported numbers**: Automatically extracted dollar amounts, percentages, counts, and decimal numbers with surrounding context.
- **Figure captions**: Often contain key results, threshold values, and statistical details.

### Step 3: Detect Data Format

Run the bundled detector on each data file:

```bash
python <skill-dir>/scripts/detect_data_format.py <path-to-data-file>
```

This outputs column names, types, statistics, and sample values. If the user provided format-specific instructions, apply those instead.

### Step 4: Understand the Methods

Read through the parsed sections to identify each distinct analysis. For each analysis, determine:

1. **The statistical model** from equations (use the `tex` field)
2. **Dependent and independent variables** from the prose surrounding equations
3. **Variable-to-column mapping**: Match the paper's mathematical notation (e.g., $z_i$, $x_i$) to dataset column names (e.g., `wellbeing`, `log_income`) using the Data section of the paper
4. **Key parameters**: thresholds, quantile levels, sample sizes, bandwidth rules
5. **The paper's software**: note if it mentions R, Stata, MATLAB, etc. — Python equivalents may produce slightly different results

Consult `references/common_methods.md` for standard statistical method -> Python library mappings.

**When to ask the user**: Only use AskUserQuestion when there is genuine ambiguity that would change the analysis outcome — for example, when column names don't clearly map to the paper's variables, or when the paper describes a method that has multiple valid Python implementations with materially different results. Do not ask about straightforward implementations. Aim for 1-3 questions maximum per paper.

### Step 5: Extract Expected Results

From the parsed output, identify all quantitative results the paper reports:
- Regression coefficients and standard errors
- Test statistics (t-stats, F-stats, chi-squared)
- Model fit measures (R², SSR, AIC, BIC)
- Threshold values, breakpoints
- Sample sizes and counts
- P-values and confidence intervals
- Any numerical values in figure captions or tables

Build `expected_results.json` following the schema in `references/output_schema.md`. For each result:
- Assign a unique `result_id` using the pattern `<section_number>_<description_slug>` (e.g., `3.1_optimal_threshold`, `3.2_quantile_50_slope_below`)
- Set `result_type` from the enum: `coefficient`, `statistic`, `threshold`, `count`, `p_value`, `standard_error`, `test_statistic`, `r_squared`, `other`
- Set `confidence` to `high` if the value is explicitly stated in text, `low` if inferred from figures or context
- Use default tolerances from `references/output_schema.md` unless the paper's precision suggests otherwise

### Step 6: Generate the Project

Create the project directory `paper-replication-<slug>/` where `<slug>` is a short URL-safe name derived from the paper title.

#### 6a: Initialize with uv

```bash
mkdir -p paper-replication-<slug>
cd paper-replication-<slug>
uv init
```

Then update the generated `pyproject.toml` based on the template in `assets/pyproject_template.toml`, adjusting dependencies for the specific methods needed. Add extra dependencies as needed (e.g., `linearmodels` for panel data, `arch` for GARCH, `scikit-learn` for ML methods, `openpyxl` for Excel reading, `pyreadstat` for Stata/SPSS).

#### 6b: Copy data and comparison scripts

```
data/              <- copy dataset files here
comparison/
├── __init__.py
├── comparator.py  <- copy from <skill-dir>/scripts/comparator.py
└── report_generator.py <- copy from <skill-dir>/scripts/report_generator.py
```

#### 6c: Generate analysis code

Create `analysis/` with:

- `__init__.py`
- `data_loading.py` — shared data loading and preprocessing:
  - Load data using pandas with auto-detected format
  - Apply any transformations described in the paper (z-scoring, log transforms, indicator creation)
  - Return a clean DataFrame ready for analysis

- One module per analysis section (e.g., `ols_regression.py`, `quantile_regression.py`):
  - Each module has a `run_analysis(data)` function that returns a dict of `{result_id: computed_value}`
  - The code should follow the paper's equations exactly, using the `tex` field as specification
  - Add comments citing the paper section for each major step
  - When making a best-effort approximation, add a comment explaining the approximation

Use the Python implementations from `references/common_methods.md` as starting points.

#### 6d: Generate main.py

The orchestrator that:
1. Loads data via `analysis.data_loading`
2. Imports and calls each analysis module's `run_analysis()`
3. Collects all results into `computed_results.json`
4. Runs `comparison.comparator.compare()` with expected and computed results
5. Calls `comparison.report_generator.generate_report()` to write reports
6. Prints a summary to stdout

```python
#!/usr/bin/env python3
"""Replication of: <paper title>"""
import json
import sys
from pathlib import Path

def main():
    project_dir = Path(__file__).parent
    
    # Load data
    from analysis.data_loading import load_data
    data = load_data(project_dir / "data")
    
    # Run analyses
    results = {}
    from analysis.<module> import run_analysis as run_<name>
    results.update(run_<name>(data))
    # ... repeat for each analysis module
    
    # Write computed results
    results_dir = project_dir / "results"
    results_dir.mkdir(exist_ok=True)
    computed = {"results": results, "metadata": {"python_version": sys.version}}
    (results_dir / "computed_results.json").write_text(
        json.dumps(computed, indent=2, default=str))
    
    # Compare
    from comparison.comparator import compare
    from comparison.report_generator import generate_report
    expected = json.loads((project_dir / "expected_results.json").read_text())
    comparison = compare(expected, computed)
    generate_report(comparison, results_dir,
                    paper_title="<title>", paper_id="<id>",
                    todo_path=project_dir / "TODO.md")
    
    # Summary
    s = comparison["summary"]
    print(f"\nReplication Score: {s['replication_score']:.1f}/100")
    print(f"Results: {s['passed']}/{s['total_results']} passed, "
          f"{s['failed']} failed, {s['not_computed']} not computed")
    return 0 if s['replication_score'] >= 80 else 1

if __name__ == "__main__":
    sys.exit(main())
```

#### 6e: Write expected_results.json

Write the file built in Step 5 to the project root.

### Step 7: Write TODO.md

Create `TODO.md` at the project root documenting all ambiguities and assumptions. Every item must be tagged with a category from the fixed enum:

```markdown
# TODO

## Ambiguities and Assumptions

- [category] Description of the issue
  - [category] Sub-detail if needed
```

**Categories**: `ambiguous_method`, `approximation_made`, `missing_implementation`, `data_format_assumption`, `library_mismatch`, `other`

Common items to flag:
- Library differences (R vs Python implementations)
- Bandwidth or kernel choices that aren't fully specified
- Standard error methods with multiple valid implementations
- Assumptions about data preprocessing not stated in the paper
- Results that could only be estimated from figures

### Step 8: Run the Project

```bash
cd paper-replication-<slug>
uv run python main.py
```

If it fails:
1. Read the error carefully
2. Fix the issue in the generated code
3. Retry (up to 3 attempts total)

Common failures:
- Missing dependencies → add to `pyproject.toml`
- Column name mismatches → fix in `data_loading.py`
- Numerical convergence issues → adjust solver parameters or initial values
- Import errors → check module structure

### Step 9: Report Results

After successful execution, read `results/comparison_report.json` and summarize to the user:

1. **Replication score** (0-100)
2. **Pass/fail breakdown** by result type
3. **Notable discrepancies** — any FAIL results with context on why they might differ
4. **TODO item count** — how many implementation assumptions were flagged
5. **Recommendation** — whether the replication supports or challenges the paper's findings

If the replication score is low, investigate whether it's a code issue or a genuine discrepancy before reporting.

## Project Structure Reference

The generated project always has this layout:

```
paper-replication-<slug>/
├── pyproject.toml              # uv-managed, Python 3.12+
├── main.py                     # Orchestrator
├── TODO.md                     # Tagged ambiguities and assumptions
├── expected_results.json       # Extracted from paper
├── data/                       # Dataset files
├── analysis/
│   ├── __init__.py
│   ├── data_loading.py         # Shared data loading
│   └── <method>.py             # One per analysis section
├── comparison/
│   ├── __init__.py
│   ├── comparator.py           # Copied from skill
│   └── report_generator.py     # Copied from skill
└── results/                    # Generated at runtime
    ├── computed_results.json
    ├── comparison_report.json
    └── comparison_report.md
```

## Key Principles

- **Equations are the spec**: The LaTeX equations (from `tex` attributes) are the authoritative definition of each model. Generate code that implements them directly.
- **Best-effort, not perfect**: When an exact Python equivalent doesn't exist, use the closest available and document the difference in TODO.md. A working approximation is better than a blocked pipeline.
- **Consistency matters**: Every paper gets the same JSON output schema, the same comparison metrics, the same project layout. This enables automated cross-paper analysis.
- **Don't over-ask**: Only interrupt the user for genuinely ambiguous decisions. Standard methods, obvious variable mappings, and well-documented techniques should just work.
