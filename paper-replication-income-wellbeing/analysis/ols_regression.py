#!/usr/bin/env python3
"""OLS regression analysis replicating Section 3.1.

Model (from Equation 1 in the paper):
    E(z_i | x_i) = (a + b*x_i) * I(exp(x_i) <= tau) + (c + d*x_i) * I(exp(x_i) > tau)

where:
    z_i = z-scored wellbeing of individual i
    x_i = log-income of individual i
    tau = income threshold (to be determined)

Approach:
1. For tau = $100,000: replicate KKM2023 analysis (pre-specified threshold)
2. Data-driven threshold: minimize sum of squared residuals (SSR) over candidate thresholds
3. Re-estimate the model using the optimal threshold

The paper finds the optimal threshold between $175,000 and $250,000.
"""
import numpy as np
import statsmodels.api as sm


def piecewise_ols(z, x, tau):
    """Fit piecewise linear OLS model with threshold tau (in income levels).

    The model is:
        E(z_i | x_i) = (a + b*x_i) * I(exp(x_i) <= tau) + (c + d*x_i) * I(exp(x_i) > tau)

    This is equivalent to a single regression with indicator interactions:
        z_i = a + b*x_i + (c-a)*D_i + (d-b)*D_i*x_i + epsilon_i
    where D_i = I(exp(x_i) > tau) = I(income_i > tau)

    Args:
        z: z-scored wellbeing (dependent variable)
        x: log-income (independent variable)
        tau: threshold in income levels (not log-income)

    Returns:
        OLS results object from statsmodels
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

    model = sm.OLS(z, X).fit()
    return model


def extract_piecewise_params(model):
    """Extract (a, b, c, d) from the piecewise OLS model.

    The regression is: z = a + b*x + (c-a)*D + (d-b)*D*x
    So:
        a = params[0]
        b = params[1]
        c-a = params[2]  =>  c = params[0] + params[2]
        d-b = params[3]  =>  d = params[1] + params[3]
    """
    a = model.params[0]
    b = model.params[1]
    c = model.params[0] + model.params[2]
    d = model.params[1] + model.params[3]
    return a, b, c, d


def find_optimal_threshold(z, x, income_values):
    """Find the threshold that minimizes SSR by grid search.

    Section 3.1: "We follow the econometrics literature on detecting 'structural breaks'
    in regression models and propose to choose the threshold tau as the place where the
    sum of squared residuals of the regression analysis is minimized."

    Candidates are the 15 income bracket values from the data.
    We skip extreme values that would leave too few observations in one segment.

    Args:
        z: z-scored wellbeing
        x: log-income
        income_values: sorted unique income bracket values

    Returns:
        (optimal_tau, ssr_by_threshold) where ssr_by_threshold is a dict
    """
    ssr_by_threshold = {}
    best_ssr = np.inf
    best_tau = None

    for tau in income_values:
        income = np.exp(x)
        below = income <= tau
        n_below = below.sum()
        n_above = (~below).sum()

        # Need sufficient observations in each segment
        if n_below < 10 or n_above < 10:
            continue

        model = piecewise_ols(z, x, tau)
        ssr = model.ssr
        ssr_by_threshold[tau] = ssr

        if ssr < best_ssr:
            best_ssr = ssr
            best_tau = tau

    return best_tau, ssr_by_threshold


def run_analysis(data):
    """Run the OLS regression analysis from Section 3.1.

    Returns a dict of {result_id: computed_value}.
    """
    results = {}

    z = data["z_wellbeing"].values
    x = data["log_income"].values
    income = data["income"].values

    # Sample size check (Section 3.1: N = 33,391)
    results["2_sample_size"] = len(data)

    # Get unique income values for threshold search
    unique_incomes = np.sort(data["income"].unique())

    # --- Analysis 1: Pre-specified threshold at $100,000 (replication of KKM2023) ---
    model_100k = piecewise_ols(z, x, 100000)
    a_100, b_100, c_100, d_100 = extract_piecewise_params(model_100k)

    results["3.1_ols_100k_intercept_below"] = a_100
    results["3.1_ols_100k_slope_below"] = b_100
    results["3.1_ols_100k_intercept_above"] = c_100
    results["3.1_ols_100k_slope_above"] = d_100
    results["3.1_ols_100k_ssr"] = model_100k.ssr

    # Standard errors for 100k model
    # The paper parameterization: a, b, (c-a), (d-b) with SEs
    results["3.1_ols_100k_se_intercept"] = model_100k.bse[0]
    results["3.1_ols_100k_se_slope_below"] = model_100k.bse[1]
    results["3.1_ols_100k_se_intercept_shift"] = model_100k.bse[2]
    results["3.1_ols_100k_se_slope_shift"] = model_100k.bse[3]

    # --- Analysis 2: Data-driven optimal threshold ---
    optimal_tau, ssr_dict = find_optimal_threshold(z, x, unique_incomes)

    results["3.1_optimal_threshold"] = optimal_tau

    # The paper says "between $175,000 and $250,000" because the income is bracketed
    # and there are no observations between these two bracket values.
    # The optimal tau should be one of these bracket boundaries.

    # Re-estimate with optimal threshold
    model_opt = piecewise_ols(z, x, optimal_tau)
    a_opt, b_opt, c_opt, d_opt = extract_piecewise_params(model_opt)

    results["3.1_ols_opt_intercept_below"] = a_opt
    results["3.1_ols_opt_slope_below"] = b_opt
    results["3.1_ols_opt_intercept_above"] = c_opt
    results["3.1_ols_opt_slope_above"] = d_opt
    results["3.1_ols_opt_ssr"] = model_opt.ssr

    # Standard errors for optimal model
    results["3.1_ols_opt_se_intercept"] = model_opt.bse[0]
    results["3.1_ols_opt_se_slope_below"] = model_opt.bse[1]
    results["3.1_ols_opt_se_intercept_shift"] = model_opt.bse[2]
    results["3.1_ols_opt_se_slope_shift"] = model_opt.bse[3]

    # R-squared values
    results["3.1_ols_100k_r_squared"] = model_100k.rsquared
    results["3.1_ols_opt_r_squared"] = model_opt.rsquared

    # Percentage of sample above $250,000 (Section 4: "slightly more than 9%")
    pct_above_250k = (income >= 250000).sum() / len(income) * 100
    results["4_pct_above_250k"] = pct_above_250k

    return results
