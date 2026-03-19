import json

with open("evidence/week3_risk_report.txt") as f:
    report = f.read()

html_content = f"""
<html>
<head>
    <title>GRC Dashboard</title>
    <style>
        body {{
            font-family: Arial;
            background-color: #0d1117;
            color: white;
            padding: 40px;
        }}
        h1 {{
            color: #58a6ff;
        }}
        .card {{
            background: #161b22;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }}
        pre {{
            white-space: pre-wrap;
        }}
    </style>
</head>
<body>

<h1>Calm Resilience Security LTD</h1>
<h2>GRC Compliance Dashboard</h2>

<div class="card">
<pre>{report}</pre>
</div>

</body>
</html>
"""

with open("evidence/dashboard.html", "w") as f:
    f.write(html_content)

print("Dashboard generated: evidence/dashboard.html")
