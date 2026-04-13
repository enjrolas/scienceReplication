# Output JSON Schemas

## expected_results.json

Extracted from the paper. Each result has a unique ID traceable to a paper section.

```json
{
  "paper_title": "string",
  "paper_id": "string (e.g. arXiv ID)",
  "results": [
    {
      "result_id": "string (e.g. '3.1_optimal_threshold_lower')",
      "section": "string (e.g. '3.1')",
      "description": "string",
      "paper_value": "number",
      "result_type": "coefficient | statistic | threshold | count | p_value | standard_error | test_statistic | r_squared | other",
      "confidence": "high | low",
      "tolerance": "number (default varies by type)",
      "tolerance_type": "relative | absolute",
      "context": "string (surrounding text from paper)"
    }
  ]
}
```

### Default tolerances by result_type

| result_type      | tolerance | tolerance_type |
|------------------|-----------|----------------|
| coefficient      | 0.05      | relative       |
| statistic        | 0.05      | relative       |
| threshold        | 0.05      | relative       |
| count            | 0.01      | relative       |
| p_value          | 0.01      | absolute       |
| standard_error   | 0.10      | relative       |
| test_statistic   | 0.05      | relative       |
| r_squared        | 0.02      | absolute       |
| other            | 0.05      | relative       |

## computed_results.json

Output by analysis modules. Keys must match `result_id` values in expected_results.json.

```json
{
  "results": {
    "3.1_optimal_threshold_lower": 175000,
    "3.1_optimal_threshold_upper": 250000,
    "3.1_ols_slope_below": 0.234
  },
  "metadata": {
    "python_version": "string",
    "packages": {"statsmodels": "0.14.1"},
    "run_timestamp": "ISO 8601 datetime",
    "run_duration_seconds": "number"
  }
}
```

## comparison_report.json

Unified output combining all three comparison modes.

```json
{
  "paper_title": "string",
  "paper_id": "string",
  "generated_at": "ISO 8601 datetime",
  "summary": {
    "total_results": "integer",
    "passed": "integer",
    "failed": "integer",
    "not_computed": "integer",
    "replication_score": "number (0-100)",
    "overall_correlation": "number | null",
    "overall_rmse": "number | null",
    "mean_absolute_relative_error": "number | null"
  },
  "todo_summary": {
    "total_count": "integer",
    "by_category": {
      "ambiguous_method": "integer",
      "approximation_made": "integer",
      "missing_implementation": "integer",
      "data_format_assumption": "integer",
      "library_mismatch": "integer",
      "other": "integer"
    }
  },
  "per_result": [
    {
      "result_id": "string",
      "section": "string",
      "description": "string",
      "result_type": "string",
      "paper_value": "number",
      "computed_value": "number | null",
      "absolute_difference": "number | null",
      "relative_difference": "number | null",
      "tolerance_used": "number",
      "tolerance_type": "relative | absolute",
      "status": "PASS | FAIL | NOT_COMPUTED | SKIPPED",
      "confidence": "high | low",
      "notes": "string"
    }
  ],
  "statistical_summary": {
    "correlation": "number | null",
    "rmse": "number | null",
    "mean_relative_error": "number | null",
    "max_relative_error": "number | null",
    "by_category": {
      "<result_type>": {
        "count": "integer",
        "passed": "integer",
        "mean_relative_error": "number"
      }
    }
  },
  "side_by_side_table": {
    "headers": ["result_id", "description", "paper_value", "computed_value", "abs_diff", "rel_diff", "status"],
    "rows": [["string", "string", "number", "number|null", "number|null", "number|null", "string"]]
  }
}
```

## TODO Category Enum

| Category                  | Description                                                        |
|---------------------------|--------------------------------------------------------------------|
| `ambiguous_method`        | Paper's method description is unclear or has multiple interpretations |
| `approximation_made`      | Used a close but not identical implementation                       |
| `missing_implementation`  | Could not implement this part of the analysis                       |
| `data_format_assumption`  | Made assumptions about data encoding, types, or structure           |
| `library_mismatch`        | Python library may produce different results than paper's tool      |
| `other`                   | Does not fit other categories                                       |
