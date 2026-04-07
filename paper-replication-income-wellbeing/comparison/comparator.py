#!/usr/bin/env python3
"""Compare computed results against expected results from a paper.

Three comparison modes:
1. Tolerance-based: per-result PASS/FAIL
2. Statistical summary: correlation, RMSE, replication score
3. Side-by-side table

Usage: python comparator.py <expected_results.json> <computed_results.json>
Output: JSON to stdout
"""
import json
import math
import sys

# Default tolerances by result type
DEFAULT_TOLERANCES = {
    "coefficient": (0.05, "relative"),
    "statistic": (0.05, "relative"),
    "threshold": (0.05, "relative"),
    "count": (0.01, "relative"),
    "p_value": (0.01, "absolute"),
    "standard_error": (0.10, "relative"),
    "test_statistic": (0.05, "relative"),
    "r_squared": (0.02, "absolute"),
    "other": (0.05, "relative"),
}


def check_tolerance(paper_value, computed_value, tolerance, tolerance_type):
    """Check if computed value is within tolerance of paper value."""
    if computed_value is None:
        return "NOT_COMPUTED", None, None

    abs_diff = abs(computed_value - paper_value)
    if paper_value != 0:
        rel_diff = abs_diff / abs(paper_value)
    else:
        rel_diff = abs_diff  # fallback for zero paper value

    if tolerance_type == "relative":
        passed = rel_diff <= tolerance
    else:  # absolute
        passed = abs_diff <= tolerance

    status = "PASS" if passed else "FAIL"
    return status, abs_diff, rel_diff


def compute_statistical_summary(per_result):
    """Compute aggregate statistics across all results."""
    paired = [(r["paper_value"], r["computed_value"])
              for r in per_result
              if r["computed_value"] is not None and r["status"] != "SKIPPED"]

    if not paired:
        return {
            "correlation": None,
            "rmse": None,
            "mean_relative_error": None,
            "max_relative_error": None,
            "by_category": {},
        }

    paper_vals = [p for p, c in paired]
    comp_vals = [c for p, c in paired]

    # RMSE
    sq_diffs = [(p - c) ** 2 for p, c in paired]
    rmse = math.sqrt(sum(sq_diffs) / len(sq_diffs))

    # Relative errors
    rel_errors = []
    for p, c in paired:
        if p != 0:
            rel_errors.append(abs(c - p) / abs(p))
        else:
            rel_errors.append(abs(c - p))
    mean_rel_error = sum(rel_errors) / len(rel_errors) if rel_errors else None
    max_rel_error = max(rel_errors) if rel_errors else None

    # Correlation
    correlation = None
    if len(paired) >= 2:
        n = len(paired)
        mean_p = sum(paper_vals) / n
        mean_c = sum(comp_vals) / n
        cov = sum((p - mean_p) * (c - mean_c) for p, c in paired) / n
        std_p = math.sqrt(sum((p - mean_p) ** 2 for p in paper_vals) / n)
        std_c = math.sqrt(sum((c - mean_c) ** 2 for c in comp_vals) / n)
        if std_p > 0 and std_c > 0:
            correlation = cov / (std_p * std_c)

    # By category
    by_category = {}
    for r in per_result:
        rt = r["result_type"]
        if rt not in by_category:
            by_category[rt] = {"count": 0, "passed": 0, "rel_errors": []}
        by_category[rt]["count"] += 1
        if r["status"] == "PASS":
            by_category[rt]["passed"] += 1
        if r["relative_difference"] is not None:
            by_category[rt]["rel_errors"].append(r["relative_difference"])

    for rt in by_category:
        errs = by_category[rt].pop("rel_errors")
        by_category[rt]["mean_relative_error"] = sum(errs) / len(errs) if errs else 0.0

    return {
        "correlation": round(correlation, 6) if correlation is not None else None,
        "rmse": round(rmse, 6),
        "mean_relative_error": round(mean_rel_error, 6) if mean_rel_error is not None else None,
        "max_relative_error": round(max_rel_error, 6) if max_rel_error is not None else None,
        "by_category": by_category,
    }


def build_side_by_side(per_result):
    """Build a side-by-side comparison table."""
    headers = ["result_id", "description", "paper_value", "computed_value",
               "abs_diff", "rel_diff", "status"]
    rows = []
    for r in per_result:
        rows.append([
            r["result_id"],
            r["description"],
            r["paper_value"],
            r["computed_value"],
            r["absolute_difference"],
            r["relative_difference"],
            r["status"],
        ])
    return {"headers": headers, "rows": rows}


def compare(expected, computed):
    """Run all three comparison modes.

    Args:
        expected: dict with "results" list from expected_results.json
        computed: dict with "results" dict from computed_results.json
    """
    computed_results = computed.get("results", {})
    per_result = []

    for exp in expected.get("results", []):
        result_id = exp["result_id"]
        paper_value = exp["paper_value"]
        result_type = exp.get("result_type", "other")
        confidence = exp.get("confidence", "high")

        # Get tolerance
        tolerance = exp.get("tolerance")
        tolerance_type = exp.get("tolerance_type")
        if tolerance is None or tolerance_type is None:
            default_tol, default_type = DEFAULT_TOLERANCES.get(
                result_type, (0.05, "relative"))
            tolerance = tolerance if tolerance is not None else default_tol
            tolerance_type = tolerance_type if tolerance_type is not None else default_type

        computed_value = computed_results.get(result_id)
        status, abs_diff, rel_diff = check_tolerance(
            paper_value, computed_value, tolerance, tolerance_type)

        per_result.append({
            "result_id": result_id,
            "section": exp.get("section", ""),
            "description": exp.get("description", ""),
            "result_type": result_type,
            "paper_value": paper_value,
            "computed_value": computed_value,
            "absolute_difference": round(abs_diff, 8) if abs_diff is not None else None,
            "relative_difference": round(rel_diff, 8) if rel_diff is not None else None,
            "tolerance_used": tolerance,
            "tolerance_type": tolerance_type,
            "status": status,
            "confidence": confidence,
            "notes": exp.get("context", ""),
        })

    # Summary
    total = len(per_result)
    passed = sum(1 for r in per_result if r["status"] == "PASS")
    failed = sum(1 for r in per_result if r["status"] == "FAIL")
    not_computed = sum(1 for r in per_result if r["status"] == "NOT_COMPUTED")

    # Replication score: weighted by confidence
    if total > 0:
        weights = [2.0 if r["confidence"] == "high" else 1.0 for r in per_result]
        weighted_pass = sum(w for w, r in zip(weights, per_result) if r["status"] == "PASS")
        replication_score = 100.0 * weighted_pass / sum(weights)
    else:
        replication_score = 0.0

    statistical_summary = compute_statistical_summary(per_result)
    side_by_side = build_side_by_side(per_result)

    return {
        "summary": {
            "total_results": total,
            "passed": passed,
            "failed": failed,
            "not_computed": not_computed,
            "replication_score": round(replication_score, 1),
            "overall_correlation": statistical_summary["correlation"],
            "overall_rmse": statistical_summary["rmse"],
            "mean_absolute_relative_error": statistical_summary["mean_relative_error"],
        },
        "per_result": per_result,
        "statistical_summary": statistical_summary,
        "side_by_side_table": side_by_side,
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python comparator.py <expected_results.json> <computed_results.json>",
              file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        expected = json.load(f)
    with open(sys.argv[2]) as f:
        computed = json.load(f)

    result = compare(expected, computed)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
