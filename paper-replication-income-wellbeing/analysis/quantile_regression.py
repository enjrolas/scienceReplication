#!/usr/bin/env python3
"""Quantile regression analysis replicating Section 3.2.

Model (from Equation 3 in the paper):
    Q_{y_i|x_i}(p) = (a + b*x_i) * I(exp(x_i) <= tau) + (c + d*x_i) * I(exp(x_i) > tau)

where:
    y_i = raw wellbeing level (NOT z-scored, unlike OLS section)
    x_i = log-income
    tau = income threshold
    p = quantile level (0.15, 0.30, 0.50, 0.70, 0.85)

Note: The paper uses R's quantreg package with Hall-Sheather bandwidth rule.
Python's statsmodels QuantReg may produce slightly different results.
This is documented in TODO.md as a [library_mismatch].
"""
import numpy as np
from statsmodels.regression.quantile_regression import QuantReg


def piecewise_quantile_reg(y, x, tau, p):
    """Fit piecewise linear quantile regression with threshold tau.

    Args:
        y: raw wellbeing (dependent variable)
        x: log-income (independent variable)
        tau: threshold in income levels (not log-income)
        p: quantile level (e.g. 0.15, 0.30, 0.50, 0.70, 0.85)

    Returns:
        QuantReg results object
    """
    income = np.exp(x)
    above = (income > tau).astype(float)

    # Design matrix: [1, x, D, D*x]
    X = np.column_stack([
        np.ones(len(x)),
        x,
        above,
        above * x,
    ])

    model = QuantReg(y, X)
    # Use default bandwidth (not Hall-Sheather specifically, as statsmodels
    # uses Powell kernel by default). This is a known library_mismatch.
    result = model.fit(q=p)
    return result


def extract_piecewise_params(model):
    """Extract (a, b, c, d) from piecewise quantile regression.

    Same parameterization as OLS:
        a = params[0]
        b = params[1]
        c = params[0] + params[2]
        d = params[1] + params[3]
    """
    a = model.params[0]
    b = model.params[1]
    c = model.params[0] + model.params[2]
    d = model.params[1] + model.params[3]
    return a, b, c, d


def run_analysis(data):
    """Run the quantile regression analysis from Section 3.2.

    Returns a dict of {result_id: computed_value}.
    """
    results = {}

    y = data["wellbeing"].values  # Note: raw wellbeing, not z-scored
    x = data["log_income"].values

    # Quantiles from the paper: p = 15%, 30%, 50%, 70%, 85%
    quantiles = [0.15, 0.30, 0.50, 0.70, 0.85]

    # --- Analysis 1: Pre-specified threshold at $100,000 ---
    for p in quantiles:
        p_label = int(p * 100)
        model = piecewise_quantile_reg(y, x, 100000, p)
        a, b, c, d = extract_piecewise_params(model)

        results[f"3.2_qr_100k_q{p_label}_slope_below"] = b
        results[f"3.2_qr_100k_q{p_label}_slope_above"] = d
        results[f"3.2_qr_100k_q{p_label}_intercept_below"] = a
        results[f"3.2_qr_100k_q{p_label}_intercept_above"] = c

        # t-stats for slope coefficients
        # The paper reports t-stats using Hall-Sheather bandwidth
        results[f"3.2_qr_100k_q{p_label}_tstat_slope_below"] = model.tvalues[1]
        results[f"3.2_qr_100k_q{p_label}_tstat_slope_above"] = (
            model.tvalues[1] + model.tvalues[3]
            if hasattr(model, 'tvalues') else None
        )

        # Slope shift (d-b) and its t-stat
        results[f"3.2_qr_100k_q{p_label}_slope_shift"] = model.params[3]
        results[f"3.2_qr_100k_q{p_label}_tstat_slope_shift"] = model.tvalues[3]

    # --- Analysis 2: Data-driven threshold at $200,000 ---
    # Section 3.2 uses tau = $200,000 "suggested by our previous analysis"
    # Note: The paper uses $200,000 as the round number for the data-driven threshold
    for p in quantiles:
        p_label = int(p * 100)
        model = piecewise_quantile_reg(y, x, 200000, p)
        a, b, c, d = extract_piecewise_params(model)

        results[f"3.2_qr_200k_q{p_label}_slope_below"] = b
        results[f"3.2_qr_200k_q{p_label}_slope_above"] = d
        results[f"3.2_qr_200k_q{p_label}_intercept_below"] = a
        results[f"3.2_qr_200k_q{p_label}_intercept_above"] = c

        # t-stats
        results[f"3.2_qr_200k_q{p_label}_tstat_slope_below"] = model.tvalues[1]
        results[f"3.2_qr_200k_q{p_label}_tstat_slope_shift"] = model.tvalues[3]

        # Slope shift
        results[f"3.2_qr_200k_q{p_label}_slope_shift"] = model.params[3]

    return results
