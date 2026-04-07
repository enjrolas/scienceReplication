# Common Statistical Methods: Paper -> Python Mapping

Reference for translating statistical methods described in papers to Python implementations.

## Regression Models

### Ordinary Least Squares (OLS)
```python
import statsmodels.api as sm
X = sm.add_constant(X)  # add intercept
model = sm.OLS(y, X).fit()
# model.params, model.bse, model.rsquared, model.ssr
```

### Piecewise / Segmented Linear Regression
Construct indicator variables for each segment:
```python
import numpy as np
def piecewise_ols(x, y, threshold):
    below = x <= np.log(threshold)  # or however threshold is defined
    X = np.column_stack([
        np.ones(len(x)),
        x,
        (~below).astype(float),          # intercept shift
        x * (~below).astype(float)       # slope shift
    ])
    # Or equivalently, separate intercepts and slopes:
    X_below = np.column_stack([np.ones(below.sum()), x[below]])
    X_above = np.column_stack([np.ones((~below).sum()), x[~below]])
```

### Quantile Regression
```python
from statsmodels.regression.quantile_regression import QuantReg
model = QuantReg(y, X).fit(q=0.5)  # median regression
# For multiple quantiles:
quantiles = [0.15, 0.25, 0.50, 0.75, 0.85]
results = {q: QuantReg(y, X).fit(q=q) for q in quantiles}
```

Standard errors: statsmodels uses the Powell kernel by default. For Hall-Sheather bandwidth (as used in R's quantreg), use:
```python
model.fit(q=q, bandwidth="hsheather")  # if available
# Otherwise note in TODO.md as [library_mismatch]
```

### Panel Data / Fixed Effects
```python
from linearmodels.panel import PanelOLS
model = PanelOLS(y, X, entity_effects=True).fit()
```

### Instrumental Variables (2SLS)
```python
from linearmodels.iv import IV2SLS
model = IV2SLS(y, X_exog, X_endog, Z_instruments).fit()
```

## Structural Break Detection

### Grid Search (minimize SSR)
The most common data-driven approach:
```python
import numpy as np
from scipy.optimize import minimize_scalar

def find_threshold(x, y, candidates):
    best_ssr = np.inf
    best_tau = None
    for tau in candidates:
        below = np.exp(x) <= tau  # or x <= np.log(tau)
        if below.sum() < 10 or (~below).sum() < 10:
            continue  # skip degenerate splits
        ssr = ssr_piecewise(x, y, below)
        if ssr < best_ssr:
            best_ssr = ssr
            best_tau = tau
    return best_tau, best_ssr
```

### Bai-Perron Test
For formal structural break testing. No standard Python package; implement via:
```python
# Manual F-test comparing restricted vs unrestricted models
# Or use ruptures package for change point detection
import ruptures as rpt
```

## Standard Errors

| Type | statsmodels | Notes |
|------|-------------|-------|
| Classical | `model.fit()` | Default, assumes homoskedasticity |
| HC0 (White) | `model.fit(cov_type='HC0')` | Heteroskedasticity-robust |
| HC1 | `model.fit(cov_type='HC1')` | Small-sample correction |
| HC3 | `model.fit(cov_type='HC3')` | Most conservative |
| HAC (Newey-West) | `model.fit(cov_type='HAC', cov_kwds={'maxlags': L})` | Autocorrelation-robust |
| Clustered | `model.fit(cov_type='cluster', cov_kwds={'groups': g})` | Cluster-robust |
| Bootstrap | Manual implementation | `from scipy.stats import bootstrap` for CIs |

## Common Transformations

### Z-scoring
```python
z = (y - y.mean()) / y.std(ddof=1)  # sample std (ddof=1)
# Or population std (ddof=0) -- check paper's convention
```

### Log Transform
```python
log_income = np.log(income)
# Papers often use natural log unless "log10" is specified
```

### Indicator / Dummy Variables
```python
income_above_threshold = (income > threshold).astype(int)
# For interaction terms:
x_above = x * income_above_threshold
```

## Hypothesis Testing

### t-test
```python
from scipy import stats
t_stat, p_value = stats.ttest_ind(group1, group2)
```

### F-test (nested models)
```python
from scipy.stats import f as f_dist
f_stat = ((ssr_restricted - ssr_unrestricted) / df_diff) / (ssr_unrestricted / df_resid)
p_value = 1 - f_dist.cdf(f_stat, df_diff, df_resid)
```

### Chi-squared
```python
from scipy.stats import chi2_contingency
chi2, p, dof, expected = chi2_contingency(observed_table)
```

## Optimization

```python
from scipy.optimize import minimize, minimize_scalar
# For 1D threshold search:
result = minimize_scalar(objective, bounds=(low, high), method='bounded')
# For general optimization:
result = minimize(objective, x0, method='L-BFGS-B', bounds=bounds)
```

## Key Libraries by Domain

| Domain | Primary Package | Alternative |
|--------|----------------|-------------|
| General regression | statsmodels | sklearn |
| Quantile regression | statsmodels | quantreg (via rpy2) |
| Panel data | linearmodels | - |
| Time series | statsmodels | arch, pmdarima |
| Survival analysis | lifelines | scikit-survival |
| Machine learning | scikit-learn | - |
| Bayesian | pymc, arviz | emcee |
| Causal inference | dowhy, econml | - |
| Meta-analysis | pymare | - |

## Tips for Replication

1. **Check sample sizes first** - if your N differs from the paper, data filtering is wrong
2. **Match the paper's software** when possible - R packages may use different defaults than Python
3. **Watch for log vs ln** - most econ papers use natural log; some use log10
4. **Standard errors matter** - papers in economics almost always use robust SEs
5. **Random seeds** - for any stochastic method, results will differ without the same seed
6. **Floating point** - very small differences (~1e-10) are expected across implementations
