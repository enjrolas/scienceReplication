# TODO

## Ambiguities and Assumptions

- [library_mismatch] Quantile regression: Paper uses R's quantreg package with Hall-Sheather bandwidth rule for standard errors and t-statistics. Python's statsmodels QuantReg uses the Powell kernel by default. This may cause differences in reported t-statistics and standard errors.
- [approximation_made] Optimal threshold: Paper states threshold is "between $175,000 and $250,000". Since income is bracketed into discrete groups, the threshold falls between two bracket midpoints. Our grid search uses the bracket values directly.
- [data_format_assumption] Income bracketing: The dataset contains pre-bracketed income values (15 groups). We assume log_income in the data corresponds to log of the bracket midpoint values as described in the paper.
- [ambiguous_method] The paper uses $200,000 as the threshold for quantile regression (Section 3.2), described as "suggested by our previous analysis." Since there is no $200,000 bracket, this is likely the midpoint between $175,000 and $250,000, or a round number approximation. We use $200,000 directly.
- [approximation_made] Z-scoring: We use sample standard deviation (ddof=1, Bessel's correction). The paper notation uses (N-1) in the denominator, confirming this choice.
- [missing_implementation] Figure-based results: Regression line slopes and intercepts shown in Figures 1 and 2 are read from the paper text, not extracted from the figures themselves. Some coefficients reported in the figure panels are not available as explicit numbers in the text.
- [library_mismatch] Standard errors: The paper does not specify whether robust standard errors are used for the OLS regression. We use classical (homoskedastic) standard errors as the default in statsmodels.
- [ambiguous_method] The paper mentions quantiles p=15%, 30%, 50%, 70%, 85% but the parsed text shows "p=15%,30%,50%,70%,85%" with a possible dollar sign artifact. We interpret these as the five quantile levels.
