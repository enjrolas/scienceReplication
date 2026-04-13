#!/usr/bin/env python3
"""Generate interactive HTML visualization of replication results.

Creates a single-page web view with:
1. OLS with $100k threshold + fit lines
2. OLS with optimal $175k threshold + fit lines
3. SSR optimization curve
4. Quantile regression with $100k threshold (5 quantiles)
5. Quantile regression with $200k threshold (5 quantiles)
6. Comparison report summary
"""
import json
import math
import webbrowser
from pathlib import Path

import numpy as np
import pandas as pd


def main():
    project_dir = Path(__file__).parent

    # Load data
    df = pd.read_csv(project_dir / "data" / "Income_and_emotional_wellbeing_a_conflict_resolved.csv")
    y_bar = df["wellbeing"].mean()
    s_y = df["wellbeing"].std(ddof=1)
    df["z_wellbeing"] = (df["wellbeing"] - y_bar) / s_y

    # Load computed results
    with open(project_dir / "results" / "computed_results.json") as f:
        computed = json.load(f)["results"]

    # Load comparison report
    with open(project_dir / "results" / "comparison_report.json") as f:
        report = json.load(f)

    # Compute bracket-level means for scatter points
    bracket_stats = df.groupby("income").agg(
        mean_z=("z_wellbeing", "mean"),
        mean_wb=("wellbeing", "mean"),
        count=("wellbeing", "count"),
        log_income=("log_income", "first"),
        q15=("wellbeing", lambda x: x.quantile(0.15)),
        q30=("wellbeing", lambda x: x.quantile(0.30)),
        q50=("wellbeing", lambda x: x.quantile(0.50)),
        q70=("wellbeing", lambda x: x.quantile(0.70)),
        q85=("wellbeing", lambda x: x.quantile(0.85)),
    ).reset_index()

    unique_incomes = sorted(df["income"].unique())
    log_incomes = [math.log(inc) for inc in unique_incomes]
    income_labels = [f"${int(inc/1000)}k" for inc in unique_incomes]

    # --- Generate fit line data ---

    # Fine x grid for smooth lines
    x_min, x_max = min(log_incomes) - 0.1, max(log_incomes) + 0.1
    x_grid = np.linspace(x_min, x_max, 200)

    def piecewise_line(x, a, b, c, d, log_tau):
        y = np.where(x <= log_tau, a + b * x, c + d * x)
        return y

    # OLS $100k
    ols100_a = computed["3.1_ols_100k_intercept_below"]
    ols100_b = computed["3.1_ols_100k_slope_below"]
    ols100_c = computed["3.1_ols_100k_intercept_above"]
    ols100_d = computed["3.1_ols_100k_slope_above"]
    log_100k = math.log(100000)
    ols100_y = piecewise_line(x_grid, ols100_a, ols100_b, ols100_c, ols100_d, log_100k)

    # OLS optimal ($175k)
    opt_tau = computed["3.1_optimal_threshold"]
    ols_opt_a = computed["3.1_ols_opt_intercept_below"]
    ols_opt_b = computed["3.1_ols_opt_slope_below"]
    ols_opt_c = computed["3.1_ols_opt_intercept_above"]
    ols_opt_d = computed["3.1_ols_opt_slope_above"]
    log_opt = math.log(opt_tau)
    ols_opt_y = piecewise_line(x_grid, ols_opt_a, ols_opt_b, ols_opt_c, ols_opt_d, log_opt)

    # SSR values - recompute for the curve
    from analysis.data_loading import load_data
    from analysis.ols_regression import piecewise_ols
    data_full = load_data(project_dir / "data")
    z = data_full["z_wellbeing"].values
    x_data = data_full["log_income"].values

    ssr_values = {}
    for tau in unique_incomes:
        below = np.exp(x_data) <= tau
        if below.sum() < 10 or (~below).sum() < 10:
            continue
        from statsmodels.api import OLS as sm_OLS
        above_flag = (~below).astype(float)
        X_mat = np.column_stack([np.ones(len(x_data)), x_data, above_flag, above_flag * x_data])
        model = sm_OLS(z, X_mat).fit()
        ssr_values[tau] = model.ssr

    # Quantile regression fit lines
    quantiles = [0.15, 0.30, 0.50, 0.70, 0.85]
    qr_colors = ["#e41a1c", "#ff7f00", "#4daf4a", "#377eb8", "#984ea3"]
    qr_labels = ["15th", "30th", "50th", "70th", "85th"]

    def qr_fit_data(threshold_key, log_tau):
        lines = []
        for i, p in enumerate(quantiles):
            p_label = int(p * 100)
            a = computed[f"3.2_qr_{threshold_key}_q{p_label}_intercept_below"]
            b = computed[f"3.2_qr_{threshold_key}_q{p_label}_slope_below"]
            c = computed[f"3.2_qr_{threshold_key}_q{p_label}_intercept_above"]
            d = computed[f"3.2_qr_{threshold_key}_q{p_label}_slope_above"]
            y_line = piecewise_line(x_grid, a, b, c, d, log_tau)
            lines.append({"label": qr_labels[i], "color": qr_colors[i], "y": y_line.tolist()})
        return lines

    qr_100k_lines = qr_fit_data("100k", log_100k)
    qr_200k_lines = qr_fit_data("200k", math.log(200000))

    # --- Build HTML ---
    x_grid_list = x_grid.tolist()

    # Convert bracket data to JSON-serializable lists
    bracket_json = {
        "log_income": bracket_stats["log_income"].tolist(),
        "income": bracket_stats["income"].tolist(),
        "income_labels": income_labels,
        "mean_z": bracket_stats["mean_z"].tolist(),
        "mean_wb": bracket_stats["mean_wb"].tolist(),
        "count": bracket_stats["count"].tolist(),
        "q15": bracket_stats["q15"].tolist(),
        "q30": bracket_stats["q30"].tolist(),
        "q50": bracket_stats["q50"].tolist(),
        "q70": bracket_stats["q70"].tolist(),
        "q85": bracket_stats["q85"].tolist(),
    }

    ssr_json = {
        "thresholds": [f"${int(k/1000)}k" for k in sorted(ssr_values.keys())],
        "threshold_values": sorted(ssr_values.keys()),
        "ssr": [ssr_values[k] for k in sorted(ssr_values.keys())],
    }

    chart_data = json.dumps({
        "bracket": bracket_json,
        "x_grid": x_grid_list,
        "ols100": {"y": ols100_y.tolist(), "log_tau": log_100k, "tau": 100000,
                   "a": ols100_a, "b": ols100_b, "c": ols100_c, "d": ols100_d,
                   "ssr": computed["3.1_ols_100k_ssr"], "r2": computed["3.1_ols_100k_r_squared"]},
        "ols_opt": {"y": ols_opt_y.tolist(), "log_tau": log_opt, "tau": opt_tau,
                    "a": ols_opt_a, "b": ols_opt_b, "c": ols_opt_c, "d": ols_opt_d,
                    "ssr": computed["3.1_ols_opt_ssr"], "r2": computed["3.1_ols_opt_r_squared"]},
        "ssr_curve": ssr_json,
        "qr_100k": qr_100k_lines,
        "qr_200k": qr_200k_lines,
        "report": report,
    })

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Replication Results: Income and Emotional Well-being</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f1117; color: #e0e0e0; }}
  .header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 32px 40px; border-bottom: 1px solid #2a2a4a; }}
  .header h1 {{ font-size: 22px; font-weight: 600; color: #f0f0f0; margin-bottom: 4px; }}
  .header .subtitle {{ font-size: 14px; color: #888; }}
  .score-banner {{ display: flex; gap: 24px; padding: 20px 40px; background: #141420; border-bottom: 1px solid #2a2a4a; }}
  .score-card {{ background: #1a1a2e; border-radius: 8px; padding: 16px 24px; min-width: 160px; }}
  .score-card .label {{ font-size: 11px; text-transform: uppercase; color: #888; letter-spacing: 0.5px; }}
  .score-card .value {{ font-size: 28px; font-weight: 700; margin-top: 4px; }}
  .score-card .value.pass {{ color: #4ade80; }}
  .score-card .value.warn {{ color: #fbbf24; }}
  .score-card .value.neutral {{ color: #60a5fa; }}
  .content {{ padding: 24px 40px; }}
  .chart-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }}
  .chart-row {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-bottom: 24px; }}
  .chart-box {{ background: #1a1a2e; border-radius: 10px; border: 1px solid #2a2a4a; padding: 20px; }}
  .chart-box h3 {{ font-size: 14px; font-weight: 600; margin-bottom: 4px; color: #f0f0f0; }}
  .chart-box .desc {{ font-size: 12px; color: #888; margin-bottom: 12px; }}
  .chart-box canvas {{ width: 100% !important; height: 300px !important; }}
  .chart-box.wide canvas {{ height: 350px !important; }}
  .params {{ display: flex; gap: 16px; flex-wrap: wrap; margin-top: 8px; font-size: 11px; }}
  .params .param {{ background: #22223a; border-radius: 4px; padding: 4px 8px; }}
  .params .param .k {{ color: #888; }}
  .params .param .v {{ color: #60a5fa; font-family: monospace; }}
  .todo-section {{ background: #1a1a2e; border-radius: 10px; border: 1px solid #2a2a4a; padding: 20px; margin-top: 20px; }}
  .todo-section h3 {{ font-size: 14px; font-weight: 600; margin-bottom: 12px; }}
  .todo-bar {{ display: flex; gap: 12px; flex-wrap: wrap; }}
  .todo-chip {{ background: #22223a; border-radius: 4px; padding: 4px 10px; font-size: 12px; }}
  .todo-chip .cat {{ color: #888; }}
  .todo-chip .cnt {{ color: #fbbf24; font-weight: 600; margin-left: 4px; }}
  .legend {{ display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 8px; }}
  .legend-item {{ display: flex; align-items: center; gap: 4px; font-size: 11px; color: #ccc; }}
  .legend-swatch {{ width: 14px; height: 3px; border-radius: 2px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 12px; }}
  th {{ text-align: left; padding: 8px 12px; border-bottom: 1px solid #2a2a4a; color: #888; text-transform: uppercase; font-size: 10px; letter-spacing: 0.5px; }}
  td {{ padding: 8px 12px; border-bottom: 1px solid #1e1e30; }}
  tr:hover {{ background: #22223a; }}
  .status-pass {{ color: #4ade80; font-weight: 600; }}
  .status-fail {{ color: #f87171; font-weight: 600; }}
</style>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
</head>
<body>
<div class="header">
  <h1>Replication Results: Income and Emotional Well-being</h1>
  <div class="subtitle">Bennedsen (2024) &mdash; arXiv:2401.05347 &mdash; Piecewise regression with structural break detection</div>
</div>

<div class="score-banner" id="scoreBanner"></div>

<div class="content">
  <!-- Row 1: SSR curve + two OLS panels -->
  <div class="chart-row">
    <div class="chart-box">
      <h3>SSR Optimization</h3>
      <div class="desc">Sum of squared residuals by threshold &tau;</div>
      <canvas id="chartSSR"></canvas>
    </div>
    <div class="chart-box">
      <h3>OLS: &tau; = $100k (KKM2023)</h3>
      <div class="desc">Piecewise linear fit &mdash; monotonically increasing</div>
      <canvas id="chartOLS100"></canvas>
      <div class="params" id="params100"></div>
    </div>
    <div class="chart-box">
      <h3>OLS: &tau; = $175k (Data-driven)</h3>
      <div class="desc">Piecewise linear fit &mdash; plateau above threshold</div>
      <canvas id="chartOLSOpt"></canvas>
      <div class="params" id="paramsOpt"></div>
    </div>
  </div>

  <!-- Row 2: Quantile regressions -->
  <div class="chart-grid">
    <div class="chart-box wide">
      <h3>Quantile Regression: &tau; = $100k</h3>
      <div class="desc">Fit lines across 5 quantiles of the well-being distribution</div>
      <div class="legend" id="qrLegend"></div>
      <canvas id="chartQR100"></canvas>
    </div>
    <div class="chart-box wide">
      <h3>Quantile Regression: &tau; = $200k</h3>
      <div class="desc">All quantiles plateau above the data-driven threshold</div>
      <div class="legend" id="qrLegend2"></div>
      <canvas id="chartQR200"></canvas>
    </div>
  </div>

  <!-- Comparison table -->
  <div class="chart-box">
    <h3>Result Comparison: Paper vs. Computed</h3>
    <table id="compTable"></table>
  </div>

  <!-- TODO summary -->
  <div class="todo-section">
    <h3>Implementation Notes (TODO items)</h3>
    <div class="todo-bar" id="todoBar"></div>
  </div>
</div>

<script>
const D = {chart_data};

// --- Score banner ---
const s = D.report.summary;
const todo = D.report.todo_summary || {{}};
document.getElementById('scoreBanner').innerHTML = `
  <div class="score-card"><div class="label">Replication Score</div><div class="value pass">${{s.replication_score}}/100</div></div>
  <div class="score-card"><div class="label">Results Passed</div><div class="value pass">${{s.passed}}/${{s.total_results}}</div></div>
  <div class="score-card"><div class="label">Correlation</div><div class="value neutral">${{s.overall_correlation ? s.overall_correlation.toFixed(4) : 'N/A'}}</div></div>
  <div class="score-card"><div class="label">Mean Rel. Error</div><div class="value neutral">${{s.mean_absolute_relative_error ? (s.mean_absolute_relative_error * 100).toFixed(1) + '%' : 'N/A'}}</div></div>
  <div class="score-card"><div class="label">TODO Items</div><div class="value warn">${{todo.total_count || 0}}</div></div>
`;

// --- Chart defaults ---
Chart.defaults.color = '#aaa';
Chart.defaults.borderColor = '#2a2a4a';
Chart.defaults.font.size = 11;
const bracket = D.bracket;

function incomeAxis() {{
  return {{
    title: {{ display: true, text: 'log(income)', color: '#888' }},
    grid: {{ color: '#1e1e30' }},
  }};
}}

// --- SSR chart ---
new Chart(document.getElementById('chartSSR'), {{
  type: 'line',
  data: {{
    labels: D.ssr_curve.thresholds,
    datasets: [{{
      data: D.ssr_curve.ssr,
      borderColor: '#60a5fa',
      borderWidth: 2,
      pointBackgroundColor: D.ssr_curve.threshold_values.map(v => v === D.ols_opt.tau ? '#4ade80' : '#60a5fa'),
      pointRadius: D.ssr_curve.threshold_values.map(v => v === D.ols_opt.tau ? 6 : 3),
      tension: 0.3,
    }}]
  }},
  options: {{
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{ callbacks: {{ label: ctx => 'SSR: ' + ctx.parsed.y.toFixed(2) }} }}
    }},
    scales: {{
      x: {{ title: {{ display: true, text: 'Income threshold \\u03C4', color: '#888' }}, grid: {{ color: '#1e1e30' }} }},
      y: {{ title: {{ display: true, text: 'SSR', color: '#888' }}, grid: {{ color: '#1e1e30' }} }},
    }}
  }}
}});

// --- OLS helper ---
function olsChart(canvasId, paramsId, olsData, label) {{
  const ctx = document.getElementById(canvasId);
  new Chart(ctx, {{
    type: 'scatter',
    data: {{
      datasets: [
        {{
          label: 'Bracket means',
          data: bracket.log_income.map((x, i) => ({{ x, y: bracket.mean_z[i] }})),
          backgroundColor: '#60a5fa',
          pointRadius: 5,
          order: 2,
        }},
        {{
          label: 'Below \\u03C4',
          data: D.x_grid.filter(x => x <= olsData.log_tau).map((x, i) => {{
            const idx = D.x_grid.indexOf(x);
            return {{ x, y: olsData.y[idx] }};
          }}),
          type: 'line',
          borderColor: '#4ade80',
          borderWidth: 2.5,
          pointRadius: 0,
          order: 1,
        }},
        {{
          label: 'Above \\u03C4',
          data: D.x_grid.filter(x => x > olsData.log_tau).map(x => {{
            const idx = D.x_grid.indexOf(x);
            return {{ x, y: olsData.y[idx] }};
          }}),
          type: 'line',
          borderColor: '#f87171',
          borderWidth: 2.5,
          pointRadius: 0,
          order: 1,
        }},
      ]
    }},
    options: {{
      plugins: {{
        legend: {{ display: true, position: 'bottom', labels: {{ boxWidth: 12, padding: 8 }} }},
        annotation: {{ annotations: {{}} }}
      }},
      scales: {{
        x: incomeAxis(),
        y: {{ title: {{ display: true, text: 'z(well-being)', color: '#888' }}, grid: {{ color: '#1e1e30' }} }},
      }}
    }}
  }});

  const p = document.getElementById(paramsId);
  p.innerHTML = `
    <span class="param"><span class="k">slope below:</span> <span class="v">${{olsData.b.toFixed(4)}}</span></span>
    <span class="param"><span class="k">slope above:</span> <span class="v">${{olsData.d.toFixed(4)}}</span></span>
    <span class="param"><span class="k">SSR:</span> <span class="v">${{olsData.ssr.toFixed(1)}}</span></span>
    <span class="param"><span class="k">R\u00B2:</span> <span class="v">${{olsData.r2.toFixed(6)}}</span></span>
  `;
}}

olsChart('chartOLS100', 'params100', D.ols100, '$100k');
olsChart('chartOLSOpt', 'paramsOpt', D.ols_opt, '$' + (D.ols_opt.tau / 1000) + 'k');

// --- QR helper ---
function qrChart(canvasId, legendId, qrLines, log_tau) {{
  // Build legend
  const legendEl = document.getElementById(legendId);
  legendEl.innerHTML = qrLines.map(l =>
    `<div class="legend-item"><div class="legend-swatch" style="background:${{l.color}}"></div>${{l.label}} percentile</div>`
  ).join('');

  const datasets = [];
  // Scatter: bracket quantile dots
  const qCols = ['q15','q30','q50','q70','q85'];
  qrLines.forEach((line, i) => {{
    datasets.push({{
      label: line.label + ' data',
      data: bracket.log_income.map((x, j) => ({{ x, y: bracket[qCols[i]][j] }})),
      backgroundColor: line.color + '88',
      pointRadius: 4,
      pointStyle: 'circle',
      order: 3,
    }});
  }});

  // Fit lines split at threshold
  qrLines.forEach((line, i) => {{
    // Below
    datasets.push({{
      label: line.label + ' fit (below)',
      data: D.x_grid.map((x, j) => x <= log_tau ? {{ x, y: line.y[j] }} : null).filter(Boolean),
      type: 'line',
      borderColor: line.color,
      borderWidth: 2,
      pointRadius: 0,
      order: 1,
    }});
    // Above
    datasets.push({{
      label: line.label + ' fit (above)',
      data: D.x_grid.map((x, j) => x > log_tau ? {{ x, y: line.y[j] }} : null).filter(Boolean),
      type: 'line',
      borderColor: line.color,
      borderWidth: 2,
      borderDash: [4, 3],
      pointRadius: 0,
      order: 1,
    }});
  }});

  new Chart(document.getElementById(canvasId), {{
    type: 'scatter',
    data: {{ datasets }},
    options: {{
      plugins: {{ legend: {{ display: false }} }},
      scales: {{
        x: incomeAxis(),
        y: {{ title: {{ display: true, text: 'Well-being', color: '#888' }}, grid: {{ color: '#1e1e30' }} }},
      }}
    }}
  }});
}}

qrChart('chartQR100', 'qrLegend', D.qr_100k, {log_100k});
qrChart('chartQR200', 'qrLegend2', D.qr_200k, {math.log(200000)});

// --- Comparison table ---
const table = document.getElementById('compTable');
let thtml = '<thead><tr><th>Result</th><th>Section</th><th>Paper</th><th>Computed</th><th>Rel. Diff</th><th>Status</th></tr></thead><tbody>';
(D.report.per_result || []).forEach(r => {{
  const cls = r.status === 'PASS' ? 'status-pass' : 'status-fail';
  const cv = r.computed_value != null ? (typeof r.computed_value === 'number' ? r.computed_value.toFixed(4) : r.computed_value) : 'N/A';
  const rd = r.relative_difference != null ? (r.relative_difference * 100).toFixed(2) + '%' : 'N/A';
  thtml += `<tr><td>${{r.description}}</td><td>${{r.section}}</td><td>${{r.paper_value}}</td><td>${{cv}}</td><td>${{rd}}</td><td class="${{cls}}">${{r.status}}</td></tr>`;
}});
thtml += '</tbody>';
table.innerHTML = thtml;

// --- TODO bar ---
const todoBar = document.getElementById('todoBar');
if (todo.by_category) {{
  todoBar.innerHTML = Object.entries(todo.by_category).filter(([,v]) => v > 0).map(([k,v]) =>
    `<span class="todo-chip"><span class="cat">${{k.replace(/_/g, ' ')}}:</span><span class="cnt">${{v}}</span></span>`
  ).join('');
}}
</script>
</body>
</html>"""

    out_path = project_dir / "results" / "replication_dashboard.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"Dashboard written to: {out_path}")
    webbrowser.open(f"file://{out_path.resolve()}")


if __name__ == "__main__":
    main()
