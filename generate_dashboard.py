from html import escape
from pathlib import Path


REPORT_PATH = Path("evidence/week3_risk_report.txt")
DASHBOARD_PATH = Path("evidence/dashboard.html")
PAGES_DIR = Path("site")
PAGES_INDEX = PAGES_DIR / "index.html"


def parse_report(report_text):
    controls = []
    frameworks = {}
    compliance_score = "UNKNOWN"
    risk_level = "UNKNOWN"
    decision = "UNKNOWN"
    total_risk_score = "UNKNOWN"
    controls_assessed = "0"
    controls_not_evidenced = "0"
    section = None

    for raw_line in report_text.splitlines():
        line = raw_line.strip()

        if line == "=== COMPLIANCE REPORT ===":
            section = "controls"
            continue
        if line == "=== FRAMEWORK SUMMARY ===":
            section = "frameworks"
            continue
        if line == "=== EVIDENCE COVERAGE ===":
            section = "coverage"
            continue
        if line == "=== RISK SUMMARY ===":
            section = "risk"
            continue
        if not line:
            continue

        if line.startswith("Compliance Score:"):
            compliance_score = line.split(":", 1)[1].strip()
            continue
        if line.startswith("Risk Level:"):
            risk_level = line.split(":", 1)[1].strip()
            continue
        if line.startswith("Decision:"):
            decision = line.split(":", 1)[1].strip()
            continue
        if line.startswith("Total Risk Score:"):
            total_risk_score = line.split(":", 1)[1].strip()
            continue
        if line.startswith("Controls Assessed:"):
            controls_assessed = line.split(":", 1)[1].strip()
            continue
        if line.startswith("Controls Not Evidenced:"):
            controls_not_evidenced = line.split(":", 1)[1].strip()
            continue

        if section == "controls" and " - " in line and ": " in line:
            control_id, remainder = line.split(" - ", 1)
            name, outcome = remainder.rsplit(": ", 1)
            status, severity = outcome.split(" (", 1)
            controls.append(
                {
                    "id": control_id,
                    "name": name,
                    "status": status,
                    "severity": severity.rstrip(")"),
                }
            )
            continue

        if section == "frameworks" and ": " in line:
            framework, counts = line.split(": ", 1)
            frameworks[framework] = counts
            continue

    return {
        "controls": controls,
        "frameworks": frameworks,
        "compliance_score": compliance_score,
        "risk_level": risk_level,
        "decision": decision,
        "total_risk_score": total_risk_score,
        "controls_assessed": controls_assessed,
        "controls_not_evidenced": controls_not_evidenced,
    }


def decision_copy(decision):
    messages = {
        "ALLOW": "Governance thresholds are satisfied and the release can proceed.",
        "REVIEW REQUIRED": (
            "The change set is partially compliant and needs manual governance review "
            "before release."
        ),
        "BLOCK DEPLOYMENT": (
            "The current control posture exceeds release tolerance and should be "
            "stopped pending remediation."
        ),
        "INSUFFICIENT EVIDENCE": (
            "The current evidence set is too thin to support a reliable release decision."
        ),
    }
    return messages.get(decision, "The release status could not be determined.")


def derive_actions(failed_controls):
    action_map = {
        "GRC-101": "Remove wildcard IAM permissions and tighten least-privilege boundaries.",
        "GRC-201": "Apply KMS-backed encryption to S3 storage used for regulated data.",
        "GRC-301": "Enable S3 access logging to improve monitoring and audit visibility.",
        "GRC-002": "Turn on S3 versioning to support rollback, recovery, and retention needs.",
        "GRC-501": "Strengthen recovery controls to improve resilience and restore capability.",
        "GRC-601": "Limit public network exposure and verify ingress restrictions.",
        "GRC-701": "Document secure development requirements and enforce them in delivery workflows.",
    }

    ordered_actions = []
    seen = set()
    for control in failed_controls:
        action = action_map.get(control["id"])
        if action and action not in seen:
            ordered_actions.append(action)
            seen.add(action)

    if not ordered_actions:
        ordered_actions.append(
            "Maintain the current posture and continue monitoring control drift in CI/CD."
        )

    return ordered_actions[:5]


def status_class(value):
    return value.lower().replace(" ", "-")


def render_controls_table(controls):
    rows = []
    for control in controls:
        rows.append(
            """
            <tr>
              <td class="control-id">{control_id}</td>
              <td>{name}</td>
              <td><span class="badge status {status_class}">{status}</span></td>
              <td><span class="badge severity severity-{severity_class}">{severity}</span></td>
            </tr>
            """.format(
                control_id=escape(control["id"]),
                name=escape(control["name"]),
                status=escape(control["status"]),
                severity=escape(control["severity"]),
                status_class=status_class(control["status"]),
                severity_class=escape(control["severity"].lower()),
            )
        )

    return "\n".join(rows)


def render_framework_cards(frameworks):
    cards = []
    for framework, counts in frameworks.items():
        cards.append(
            """
            <div class="mini-card">
              <div class="mini-label">{framework}</div>
              <div class="mini-value">{counts}</div>
            </div>
            """.format(framework=escape(framework), counts=escape(counts))
        )

    return "\n".join(cards)


def render_action_list(actions):
    items = []
    for action in actions:
        items.append(f"<li>{escape(action)}</li>")
    return "\n".join(items)


def build_dashboard(report_text, parsed):
    controls = parsed["controls"]
    failed_controls = [control for control in controls if control["status"] == "FAIL"]
    passed_controls = [control for control in controls if control["status"] == "PASS"]
    not_evidenced_controls = [
        control for control in controls if control["status"] == "NOT EVIDENCED"
    ]
    actions = derive_actions(failed_controls)

    html_content = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Calm Resilience Security LTD - Executive Governance Dashboard</title>
    <style>
        :root {{
            --bg: #f4efe6;
            --surface: rgba(255, 252, 246, 0.78);
            --surface-strong: #fffaf2;
            --ink: #172126;
            --muted: #59646b;
            --line: rgba(23, 33, 38, 0.12);
            --accent: #0f766e;
            --accent-deep: #0d5f62;
            --warn: #b45309;
            --danger: #9f1239;
            --good: #166534;
            --shadow: 0 24px 60px rgba(30, 41, 59, 0.10);
        }}
        * {{
            box-sizing: border-box;
        }}
        body {{
            margin: 0;
            font-family: "Avenir Next", "Helvetica Neue", sans-serif;
            color: var(--ink);
            background:
                radial-gradient(circle at top left, rgba(15, 118, 110, 0.18), transparent 34%),
                radial-gradient(circle at top right, rgba(180, 83, 9, 0.16), transparent 28%),
                linear-gradient(180deg, #f7f2ea 0%, #efe7db 100%);
            min-height: 100vh;
        }}
        .shell {{
            max-width: 1180px;
            margin: 0 auto;
            padding: 48px 20px 72px;
        }}
        .hero {{
            position: relative;
            overflow: hidden;
            background: linear-gradient(145deg, rgba(13, 95, 98, 0.92), rgba(23, 33, 38, 0.96));
            color: #f7f5ef;
            border-radius: 30px;
            padding: 32px;
            box-shadow: var(--shadow);
            isolation: isolate;
        }}
        .hero::after {{
            content: "";
            position: absolute;
            inset: auto -70px -90px auto;
            width: 220px;
            height: 220px;
            border-radius: 999px;
            background: rgba(244, 239, 230, 0.10);
            filter: blur(2px);
            z-index: -1;
        }}
        .eyebrow {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 8px 14px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.10);
            border: 1px solid rgba(255, 255, 255, 0.18);
            font-size: 13px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }}
        .hero-grid {{
            display: grid;
            grid-template-columns: minmax(0, 1.5fr) minmax(280px, 0.9fr);
            gap: 24px;
            align-items: end;
            margin-top: 18px;
        }}
        h1 {{
            font-family: "Iowan Old Style", "Palatino Linotype", serif;
            font-size: clamp(2.2rem, 5vw, 4.5rem);
            line-height: 0.98;
            margin: 12px 0;
            max-width: 10ch;
        }}
        .lede {{
            max-width: 58ch;
            color: rgba(247, 245, 239, 0.82);
            font-size: 1.02rem;
            line-height: 1.6;
            margin: 0;
        }}
        .hero-note {{
            background: rgba(255, 255, 255, 0.10);
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: 24px;
            padding: 22px;
            backdrop-filter: blur(6px);
        }}
        .hero-note-label {{
            color: rgba(247, 245, 239, 0.68);
            font-size: 0.88rem;
            margin-bottom: 10px;
        }}
        .hero-note p {{
            margin: 0;
            line-height: 1.6;
            color: #fffdf7;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 16px;
            margin-top: 22px;
        }}
        .metric-card,
        .panel,
        .mini-card {{
            background: var(--surface);
            border: 1px solid var(--line);
            backdrop-filter: blur(10px);
            box-shadow: var(--shadow);
        }}
        .metric-card {{
            border-radius: 22px;
            padding: 20px;
            animation: rise 0.55s ease both;
        }}
        .metric-label {{
            color: var(--muted);
            font-size: 0.86rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}
        .metric-value {{
            margin-top: 12px;
            font-size: clamp(1.5rem, 2.5vw, 2.2rem);
            font-weight: 700;
            line-height: 1;
        }}
        .metric-subtle {{
            margin-top: 10px;
            color: var(--muted);
            font-size: 0.95rem;
        }}
        .content-grid {{
            display: grid;
            grid-template-columns: minmax(0, 1.25fr) minmax(280px, 0.75fr);
            gap: 18px;
            margin-top: 22px;
        }}
        .panel {{
            border-radius: 26px;
            padding: 24px;
            animation: rise 0.65s ease both;
        }}
        .panel h2 {{
            margin: 0 0 14px;
            font-family: "Iowan Old Style", "Palatino Linotype", serif;
            font-size: 1.8rem;
            font-weight: 600;
        }}
        .panel-copy {{
            color: var(--muted);
            line-height: 1.7;
            margin: 0 0 16px;
        }}
        .badge {{
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            padding: 7px 12px;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }}
        .status.pass {{
            background: rgba(22, 101, 52, 0.10);
            color: var(--good);
        }}
        .status.fail {{
            background: rgba(159, 18, 57, 0.10);
            color: var(--danger);
        }}
        .status.not-evidenced {{
            background: rgba(89, 100, 107, 0.12);
            color: var(--muted);
        }}
        .severity-high {{
            background: rgba(159, 18, 57, 0.10);
            color: var(--danger);
        }}
        .severity-medium {{
            background: rgba(180, 83, 9, 0.12);
            color: var(--warn);
        }}
        .framework-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
        }}
        .mini-card {{
            border-radius: 20px;
            padding: 18px;
        }}
        .mini-label {{
            color: var(--muted);
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}
        .mini-value {{
            margin-top: 10px;
            font-size: 1.1rem;
            line-height: 1.4;
            font-weight: 600;
        }}
        .actions {{
            margin: 0;
            padding-left: 18px;
            color: var(--ink);
        }}
        .actions li {{
            margin: 0 0 12px;
            line-height: 1.55;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        thead th {{
            text-align: left;
            font-size: 0.82rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--muted);
            padding: 0 0 12px;
            border-bottom: 1px solid var(--line);
        }}
        tbody td {{
            padding: 14px 0;
            border-bottom: 1px solid rgba(23, 33, 38, 0.08);
            vertical-align: top;
        }}
        tbody tr:last-child td {{
            border-bottom: none;
        }}
        .control-id {{
            font-family: "SFMono-Regular", "Menlo", monospace;
            font-size: 0.9rem;
            color: var(--accent-deep);
        }}
        .report {{
            margin-top: 22px;
        }}
        .report pre {{
            margin: 0;
            white-space: pre-wrap;
            font-family: "SFMono-Regular", "Menlo", monospace;
            font-size: 0.92rem;
            line-height: 1.55;
            color: #223038;
            background: rgba(255, 255, 255, 0.46);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 18px;
            overflow-x: auto;
        }}
        .topline {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 10px;
        }}
        .topline .badge {{
            background: rgba(15, 118, 110, 0.10);
            color: var(--accent-deep);
        }}
        @keyframes rise {{
            from {{
                opacity: 0;
                transform: translateY(10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        @media (max-width: 920px) {{
            .hero-grid,
            .content-grid,
            .metrics,
            .framework-grid {{
                grid-template-columns: 1fr;
            }}
            .shell {{
                padding: 20px 14px 48px;
            }}
            .hero,
            .panel,
            .metric-card {{
                border-radius: 22px;
            }}
        }}
    </style>
</head>
<body>
    <main class="shell">
        <section class="hero">
            <div class="eyebrow">Calm Resilience Security LTD</div>
            <div class="hero-grid">
                <div>
                    <h1>Executive Governance Dashboard</h1>
                    <p class="lede">
                        A live governance snapshot for a simulated fintech deployment,
                        translating infrastructure findings into release risk, control posture,
                        and executive action.
                    </p>
                </div>
                <div class="hero-note">
                    <div class="hero-note-label">Release Status</div>
                    <p>{decision_copy}</p>
                </div>
            </div>
        </section>

        <section class="metrics">
            <article class="metric-card">
                <div class="metric-label">Compliance Score</div>
                <div class="metric-value">{compliance_score}</div>
                <div class="metric-subtle">{passed_count} of {assessed_count} assessed controls passing</div>
            </article>
            <article class="metric-card">
                <div class="metric-label">Risk Level</div>
                <div class="metric-value">{risk_level}</div>
                <div class="metric-subtle">Aggregate risk score: {total_risk_score}</div>
            </article>
            <article class="metric-card">
                <div class="metric-label">Decision</div>
                <div class="metric-value">{decision}</div>
                <div class="metric-subtle">{failed_count} failed controls require action</div>
            </article>
            <article class="metric-card">
                <div class="metric-label">Evidence Coverage</div>
                <div class="metric-value">{assessed_count}/{total_count}</div>
                <div class="metric-subtle">{not_evidenced_count} controls still lack evidence</div>
            </article>
        </section>

        <section class="content-grid">
            <article class="panel">
                <div class="topline">
                    <span class="badge">Executive Summary</span>
                    <span class="badge">Fintech Governance Scenario</span>
                </div>
                <h2>Decision Context</h2>
                <p class="panel-copy">
                    The current release candidate remains above acceptable deployment
                    tolerance. This dashboard surfaces the specific control failures
                    driving the decision and keeps the technical evidence visible for
                    engineering, audit, and governance stakeholders.
                </p>
                <div class="framework-grid">
                    {framework_cards}
                </div>
            </article>

            <aside class="panel">
                <div class="topline">
                    <span class="badge">Priority Actions</span>
                </div>
                <h2>Next Moves</h2>
                <ul class="actions">
                    {action_items}
                </ul>
            </aside>
        </section>

        <section class="panel report">
            <div class="topline">
                <span class="badge">Control Detail</span>
            </div>
            <h2>Control Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Control</th>
                        <th>Description</th>
                        <th>Status</th>
                        <th>Severity</th>
                    </tr>
                </thead>
                <tbody>
                    {control_rows}
                </tbody>
            </table>
        </section>

        <section class="panel report">
            <div class="topline">
                <span class="badge">Technical Evidence</span>
            </div>
            <h2>Raw Governance Report</h2>
            <pre>{raw_report}</pre>
        </section>
    </main>
</body>
</html>
""".format(
        decision_copy=escape(decision_copy(parsed["decision"])),
        compliance_score=escape(parsed["compliance_score"]),
        risk_level=escape(parsed["risk_level"]),
        decision=escape(parsed["decision"]),
        total_risk_score=escape(parsed["total_risk_score"]),
        passed_count=len(passed_controls),
        failed_count=len(failed_controls),
        assessed_count=escape(parsed["controls_assessed"]),
        total_count=len(controls),
        not_evidenced_count=len(not_evidenced_controls),
        framework_cards=render_framework_cards(parsed["frameworks"]),
        action_items=render_action_list(actions),
        control_rows=render_controls_table(controls),
        raw_report=escape(report_text),
    )

    return html_content


PAGES_DIR.mkdir(exist_ok=True)
report_text = REPORT_PATH.read_text()
parsed_report = parse_report(report_text)
html = build_dashboard(report_text, parsed_report)

DASHBOARD_PATH.write_text(html)
PAGES_INDEX.write_text(html)

print(f"Dashboard generated: {DASHBOARD_PATH}")
print(f"Pages site generated: {PAGES_INDEX}")
