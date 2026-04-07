#!/usr/bin/env python3
"""Replication of: Income and emotional well-being: Evidence for well-being
plateauing around $200,000 per year (Bennedsen, 2024, arXiv:2401.05347)"""
import json
import sys
import time
from pathlib import Path


def main():
    start_time = time.time()
    project_dir = Path(__file__).parent

    # Load data
    from analysis.data_loading import load_data
    data = load_data(project_dir / "data")
    print(f"Loaded {len(data)} observations")
    print(f"  wellbeing: mean={data['wellbeing'].mean():.3f}, std={data['wellbeing'].std():.3f}")
    print(f"  z_wellbeing: mean={data['z_wellbeing'].mean():.6f}, std={data['z_wellbeing'].std():.6f}")
    print(f"  income range: ${data['income'].min():,.0f} - ${data['income'].max():,.0f}")

    # Run analyses
    results = {}

    print("\n--- OLS Regression (Section 3.1) ---")
    from analysis.ols_regression import run_analysis as run_ols
    ols_results = run_ols(data)
    results.update(ols_results)
    print(f"  Sample size: {ols_results['2_sample_size']}")
    print(f"  Optimal threshold: ${ols_results['3.1_optimal_threshold']:,.0f}")
    print(f"  OLS 100k - slope below: {ols_results['3.1_ols_100k_slope_below']:.4f}")
    print(f"  OLS 100k - slope above: {ols_results['3.1_ols_100k_slope_above']:.4f}")
    print(f"  OLS opt  - slope below: {ols_results['3.1_ols_opt_slope_below']:.4f}")
    print(f"  OLS opt  - slope above: {ols_results['3.1_ols_opt_slope_above']:.4f}")
    print(f"  Pct above $250k: {ols_results['4_pct_above_250k']:.2f}%")

    print("\n--- Quantile Regression (Section 3.2) ---")
    from analysis.quantile_regression import run_analysis as run_qr
    qr_results = run_qr(data)
    results.update(qr_results)
    for p in [15, 30, 50, 70, 85]:
        b_100 = qr_results[f"3.2_qr_100k_q{p}_slope_below"]
        d_100 = qr_results[f"3.2_qr_100k_q{p}_slope_above"]
        b_200 = qr_results[f"3.2_qr_200k_q{p}_slope_below"]
        d_200 = qr_results[f"3.2_qr_200k_q{p}_slope_above"]
        print(f"  Q{p}: 100k slope below={b_100:.3f}, above={d_100:.3f} | "
              f"200k slope below={b_200:.3f}, above={d_200:.3f}")

    # Write computed results
    results_dir = project_dir / "results"
    results_dir.mkdir(exist_ok=True)

    duration = time.time() - start_time
    computed = {
        "results": results,
        "metadata": {
            "python_version": sys.version,
            "run_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "run_duration_seconds": round(duration, 2),
        },
    }
    (results_dir / "computed_results.json").write_text(
        json.dumps(computed, indent=2, default=str))
    print(f"\nComputed results written to {results_dir / 'computed_results.json'}")

    # Compare
    from comparison.comparator import compare
    from comparison.report_generator import generate_report
    expected = json.loads((project_dir / "expected_results.json").read_text())
    comparison = compare(expected, computed)
    generate_report(
        comparison, results_dir,
        paper_title="Income and emotional well-being: Evidence for well-being plateauing around $200,000 per year",
        paper_id="2401.05347",
        todo_path=project_dir / "TODO.md",
    )

    # Summary
    s = comparison["summary"]
    print(f"\n{'='*60}")
    print(f"Replication Score: {s['replication_score']:.1f}/100")
    print(f"Results: {s['passed']}/{s['total_results']} passed, "
          f"{s['failed']} failed, {s['not_computed']} not computed")
    if s.get("overall_correlation") is not None:
        print(f"Correlation: {s['overall_correlation']:.4f}")
    if s.get("overall_rmse") is not None:
        print(f"RMSE: {s['overall_rmse']:.6f}")
    print(f"{'='*60}")

    return 0 if s["replication_score"] >= 80 else 1


if __name__ == "__main__":
    sys.exit(main())
