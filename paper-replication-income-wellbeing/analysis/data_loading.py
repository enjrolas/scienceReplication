#!/usr/bin/env python3
"""Data loading and preprocessing for income-wellbeing replication.

Loads the dataset and computes z-scored wellbeing as described in Section 3.1.
The paper uses:
  z_i = (y_i - mean(y)) / std(y)
where y_i is the raw wellbeing level and std uses sample standard deviation (N-1).
"""
import pandas as pd
import numpy as np
from pathlib import Path


def load_data(data_dir):
    """Load and preprocess the income-wellbeing dataset.

    Args:
        data_dir: Path to the data/ directory containing the CSV file.

    Returns:
        DataFrame with columns: wellbeing, log_income, income, income_above_100,
        and additionally z_wellbeing (z-scored wellbeing).
    """
    data_dir = Path(data_dir)
    csv_path = data_dir / "Income_and_emotional_wellbeing_a_conflict_resolved.csv"

    df = pd.read_csv(csv_path)

    # Verify expected columns
    assert "wellbeing" in df.columns, "Missing 'wellbeing' column"
    assert "log_income" in df.columns, "Missing 'log_income' column"
    assert "income" in df.columns, "Missing 'income' column"

    # Section 3.1: z-score the wellbeing variable
    # z_i = (y_i - y_bar) / s_y
    # where s_y is the sample standard deviation (ddof=1)
    y_bar = df["wellbeing"].mean()
    s_y = df["wellbeing"].std(ddof=1)  # sample std with Bessel's correction
    df["z_wellbeing"] = (df["wellbeing"] - y_bar) / s_y

    return df
