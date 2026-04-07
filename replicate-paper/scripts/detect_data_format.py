#!/usr/bin/env python3
"""Auto-detect tabular data file format and provide column metadata.

Usage: python detect_data_format.py <path-to-data-file>
Output: JSON to stdout
"""
import json
import sys
from pathlib import Path


def try_csv(path, sep, sep_name):
    """Try reading as CSV with a given separator."""
    import pandas as pd
    try:
        df = pd.read_csv(path, sep=sep, nrows=5, encoding="utf-8")
        if len(df.columns) > 1:
            df_full = pd.read_csv(path, sep=sep, encoding="utf-8")
            return df_full, "csv", sep_name, "utf-8"
    except Exception:
        pass
    # Try latin-1 encoding
    try:
        df = pd.read_csv(path, sep=sep, nrows=5, encoding="latin-1")
        if len(df.columns) > 1:
            df_full = pd.read_csv(path, sep=sep, encoding="latin-1")
            return df_full, "csv", sep_name, "latin-1"
    except Exception:
        pass
    return None, None, None, None


def detect_format(path):
    """Detect file format and return (dataframe, format_name, separator, encoding)."""
    import pandas as pd
    suffix = Path(path).suffix.lower()

    # Try format based on extension first
    if suffix in (".xlsx", ".xls"):
        try:
            df = pd.read_excel(path)
            return df, "excel", None, None
        except Exception:
            pass

    if suffix == ".parquet":
        try:
            df = pd.read_parquet(path)
            return df, "parquet", None, None
        except Exception:
            pass

    if suffix == ".dta":
        try:
            df = pd.read_stata(path)
            return df, "stata", None, None
        except Exception:
            pass

    if suffix == ".sav":
        try:
            df = pd.read_spss(path)
            return df, "spss", None, None
        except Exception:
            pass

    if suffix == ".tsv":
        df, fmt, sep_name, enc = try_csv(path, "\t", "tab")
        if df is not None:
            return df, "tsv", sep_name, enc

    # For .csv or unknown extensions, try separators in order
    for sep, sep_name in [(",", "comma"), ("\t", "tab"), (";", "semicolon"), ("|", "pipe")]:
        df, fmt, sn, enc = try_csv(path, sep, sep_name)
        if df is not None:
            return df, fmt, sn, enc

    # Try binary formats as fallback
    for reader, fmt in [
        (pd.read_excel, "excel"),
        (pd.read_parquet, "parquet"),
        (pd.read_stata, "stata"),
    ]:
        try:
            df = reader(path)
            return df, fmt, None, None
        except Exception:
            pass

    return None, None, None, None


def column_info(df, col):
    """Get metadata for a single column."""
    import numpy as np
    series = df[col]
    info = {
        "name": col,
        "dtype": str(series.dtype),
        "missing": int(series.isna().sum()),
        "unique": int(series.nunique()),
    }
    if np.issubdtype(series.dtype, np.number):
        info["min"] = float(series.min()) if not series.isna().all() else None
        info["max"] = float(series.max()) if not series.isna().all() else None
        info["mean"] = float(series.mean()) if not series.isna().all() else None
        info["std"] = float(series.std()) if not series.isna().all() else None
    sample = series.dropna().head(5).tolist()
    info["sample_values"] = [float(v) if isinstance(v, (int, float)) else str(v) for v in sample]
    return info


def main():
    if len(sys.argv) < 2:
        print("Usage: python detect_data_format.py <path-to-data-file>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    if not Path(path).exists():
        print(json.dumps({"error": f"File not found: {path}"}))
        sys.exit(1)

    df, fmt, separator, encoding = detect_format(path)
    if df is None:
        print(json.dumps({"error": "Could not detect data format", "path": path}))
        sys.exit(1)

    result = {
        "path": str(path),
        "format": fmt,
        "separator": separator,
        "encoding": encoding,
        "rows": len(df),
        "columns": [column_info(df, col) for col in df.columns],
        "head": df.head(5).to_string(index=False),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
