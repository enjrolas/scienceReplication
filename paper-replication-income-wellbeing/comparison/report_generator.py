#!/usr/bin/env python3
"""Generate comparison reports in JSON and Markdown formats.

Reads comparator output and TODO.md to produce:
- comparison_report.json (machine-readable, consistent schema)
- comparison_report.md (human-readable summary)

Usage: python report_generator.py <comparator_output.json> <output_dir> [--todo <TODO.md>] [--title <paper_title>] [--paper-id <id>]
Output: Writes comparison_report.json and comparison_report.md to output_dir
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

TODO_CATEGORIES = [
    "ambiguous_method",
    "approximation_made",
    "missing_implementation",
    "data_format_assumption",
    "library_mismatch",
    "other",
]


def parse_todo_md(todo_path):
    """Parse TODO.md and count items by category.

    Counts all bullet points at any nesting depth that have a [category] tag.
    """
    counts = {cat: 0 for cat in TODO_CATEGORIES}
    total = 0

    if not Path(todo_path).exists():
        return {"total_count": 0, "by_category": counts}

    text = Path(todo_path).read_text(encoding="utf-8")
    # Match lines like: - [category] description or  - [category] description
    pattern = re.compile(r"^\s*[-*]\s*\[(\w+)\]", re.MULTILINE)
    for m in pattern.finditer(text):
        cat = m.group(1)
        if cat in counts:
            counts[cat] += 1
        else:
            counts["other"] += 1
        total += 1

    return {"total_count": total, "by_category": counts}


def generate_markdown(report):
    """Generate a human-readable Markdown summary."""
    s = report["summary"]
    lines = [
        f"# Replication Report: {report.get('paper_title', 'Unknown')}",
        "",
        f"**Paper ID**: {report.get('paper_id', 'N/A')}",
        f"**Generated**: {report.get('generated_at', 'N/A')}",
        "",
        "## Summary",
        "",
        f"- **Replication Score**: {s['replication_score']}/100",
        f"- **Results**: {s['passed']}/{s['total_results']} passed, "
        f"{s['failed']} failed, {s['not_computed']} not computed",
    ]

    if s.get("overall_correlation") is not None:
        lines.append(f"- **Correlation**: {s['overall_correlation']:.4f}")
    if s.get("overall_rmse") is not None:
        lines.append(f"- **RMSE**: {s['overall_rmse']:.6f}")
    if s.get("mean_absolute_relative_error") is not None:
        lines.append(f"- **Mean Relative Error**: {s['mean_absolute_relative_error']:.4f}")

    # TODO summary
    todo = report.get("todo_summary", {})
    if todo.get("total_count", 0) > 0:
        lines.extend([
            "",
            "## Implementation Notes (TODO items)",
            "",
            f"**Total items**: {todo['total_count']}",
            "",
        ])
        for cat, count in todo.get("by_category", {}).items():
            if count > 0:
                lines.append(f"- {cat}: {count}")

    # Side-by-side table
    lines.extend([
        "",
        "## Results Comparison",
        "",
        "| Result | Description | Paper | Computed | Abs Diff | Rel Diff | Status |",
        "|--------|-------------|-------|----------|----------|----------|--------|",
    ])
    for row in report.get("side_by_side_table", {}).get("rows", []):
        result_id, desc, paper_val, comp_val, abs_d, rel_d, status = row
        comp_str = f"{comp_val}" if comp_val is not None else "N/A"
        abs_str = f"{abs_d:.6f}" if abs_d is not None else "N/A"
        rel_str = f"{rel_d:.4f}" if rel_d is not None else "N/A"
        emoji = "PASS" if status == "PASS" else "FAIL" if status == "FAIL" else "N/A"
        lines.append(f"| {result_id} | {desc[:30]} | {paper_val} | {comp_str} | {abs_str} | {rel_str} | {emoji} |")

    # Statistical breakdown by category
    by_cat = report.get("statistical_summary", {}).get("by_category", {})
    if by_cat:
        lines.extend([
            "",
            "## Results by Category",
            "",
        ])
        for cat, info in by_cat.items():
            lines.append(f"- **{cat}**: {info['passed']}/{info['count']} passed "
                         f"(mean relative error: {info.get('mean_relative_error', 0):.4f})")

    lines.append("")
    return "\n".join(lines)


def generate_report(comparison_data, output_dir, paper_title="", paper_id="", todo_path=None):
    """Generate both JSON and Markdown reports.

    Args:
        comparison_data: dict from comparator.compare()
        output_dir: path to write reports
        paper_title: paper title string
        paper_id: paper identifier string
        todo_path: path to TODO.md (optional)
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "paper_title": paper_title,
        "paper_id": paper_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        **comparison_data,
    }

    # Parse TODO.md if provided
    if todo_path:
        report["todo_summary"] = parse_todo_md(todo_path)
    elif "todo_summary" not in report:
        report["todo_summary"] = {"total_count": 0, "by_category": {cat: 0 for cat in TODO_CATEGORIES}}

    # Write JSON
    json_path = output_dir / "comparison_report.json"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    # Write Markdown
    md_path = output_dir / "comparison_report.md"
    md_path.write_text(generate_markdown(report), encoding="utf-8")

    return report


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate comparison reports")
    parser.add_argument("comparator_json", help="Path to comparator output JSON")
    parser.add_argument("output_dir", help="Directory to write reports")
    parser.add_argument("--todo", help="Path to TODO.md", default=None)
    parser.add_argument("--title", help="Paper title", default="")
    parser.add_argument("--paper-id", help="Paper ID", default="")
    args = parser.parse_args()

    with open(args.comparator_json) as f:
        comparison_data = json.load(f)

    report = generate_report(
        comparison_data, args.output_dir,
        paper_title=args.title, paper_id=args.paper_id,
        todo_path=args.todo,
    )
    print(f"Reports written to {args.output_dir}/")
    print(f"  - comparison_report.json")
    print(f"  - comparison_report.md")
    print(f"Replication score: {report['summary']['replication_score']}/100")


if __name__ == "__main__":
    main()
