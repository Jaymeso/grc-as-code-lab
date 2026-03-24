from pathlib import Path

report_path = Path("evidence/week3_risk_report.txt")
dashboard_path = Path("evidence/dashboard.html")
pages_dir = Path("site")
pages_dir.mkdir(exist_ok=True)
pages_index = pages_dir / "index.html"

report = report_path.read_text()

risk_level = "UNKNOWN"
decision = "UNKNOWN"
compliance_score = "UNKNOWN"

for line in report.splitlines():
    if line.startswith("Compliance Score:"):
        compliance_score = line.split(":", 1)[1].strip()
    elif line.startswith("Risk Level:"):
        risk_level = line.split(":", 1)[1].strip()
    elif line.startswith("Decision:"):
        decision = line.split(":", 1)[1].strip()

recommended_actions = """
<ul>
  <li>Review failed controls and prioritise remediation by severity.</li>
  <li>Remove overly permissive IAM access.</li>
  <li>Enable KMS-backed encryption for S3 storage.</li>
  <li>Enable S3 access logging and versioning.</li>
  <li>Re-run the governance pipeline before release.</li>
</ul>
"""

html_content = f"""
<html>
<head>
    <title>Calm Resilience Security LTD - Executive Governance Dashboard</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #0d1117;
            color: #e6edf3;
            padding: 40px;
            max-width: 1100px;
            margin: auto;
        }}
        h1 {{
            color: #58a6ff;
            margin-bottom: 4px;
        }}
        h2 {{
            color: #8b949e;
            font-weight: normal;
            margin-top: 0;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin: 24px 0;
        }}
        .card {{
            background: #161b22;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #30363d;
        }}
        .label {{
            color: #8b949e;
            font-size: 14px;
            margin-bottom: 8px;
        }}
        .value {{
            font-size: 24px;
            font-weight: bold;
        }}
        .section {{
            background: #161b22;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #30363d;
            margin-top: 20px;
        }}
        pre {{
            white-space: pre-wrap;
            margin: 0;
        }}
        ul {{
            margin: 0;
            padding-left: 20px;
        }}
    </style>
</head>
<body>
    <h1>Calm Resilience Security LTD</h1>
    <h2>Executive Governance Dashboard</h2>

    <div class="grid">
        <div class="card">
            <div class="label">Compliance Score</div>
            <div class="value">{compliance_score}</div>
        </div>
        <div class="card">
            <div class="label">Risk Level</div>
            <div class="value">{risk_level}</div>
        </div>
        <div class="card">
            <div class="label">Decision</div>
            <div class="value">{decision}</div>
        </div>
    </div>

    <div class="section">
        <h3>Executive Summary</h3>
        <p>
            This dashboard summarises the governance posture of a simulated fintech infrastructure deployment.
            The platform evaluates controls across storage, identity, data protection, and logging domains,
            then produces a compliance score, risk level, and release decision.
        </p>
    </div>

    <div class="section">
        <h3>Recommended Actions</h3>
        {recommended_actions}
    </div>

    <div class="section">
        <h3>Detailed Technical Report</h3>
        <pre>{report}</pre>
    </div>
</body>
</html>
"""

dashboard_path.write_text(html_content)
pages_index.write_text(html_content)
print(f"Dashboard generated: {dashboard_path}")
print(f"Pages site generated: {pages_index}")
