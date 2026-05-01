import ast
from html import escape
from pathlib import Path
from string import Template


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


def display_status(value):
    return value.title()


def display_framework_name(value):
    names = {
        "ISO27001": "ISO 27001",
        "SOC2": "SOC 2",
        "NIST": "NIST",
    }
    return names.get(value, value)


def format_framework_counts(counts):
    try:
        parsed_counts = ast.literal_eval(counts)
    except (SyntaxError, ValueError):
        return counts

    pass_count = parsed_counts.get("PASS", 0)
    fail_count = parsed_counts.get("FAIL", 0)
    not_evidenced = parsed_counts.get("NOT EVIDENCED", 0)
    summary = f"{pass_count} pass / {fail_count} fail"
    if not_evidenced:
        summary = f"{summary} / {not_evidenced} not evidenced"
    return summary


def decision_label(decision):
    labels = {
        "ALLOW": "Allow",
        "REVIEW REQUIRED": "Review",
        "BLOCK DEPLOYMENT": "Block",
        "INSUFFICIENT EVIDENCE": "Insufficient evidence",
    }
    return labels.get(decision, decision.title())


def render_controls_table(controls):
    rows = []
    for control in controls:
        rows.append(
            "\n".join(
                [
                    "                <tr>",
                    '                  <td class="control-id">{control_id}</td>',
                    "                  <td>{name}</td>",
                    '                  <td><span class="badge status-{status_class}">{status}</span></td>',
                    '                  <td><span class="badge severity-{severity_class}">{severity}</span></td>',
                    "                </tr>",
                ]
            ).format(
                control_id=escape(control["id"]),
                name=escape(control["name"]),
                status=escape(display_status(control["status"])),
                severity=escape(display_status(control["severity"])),
                status_class=status_class(control["status"]),
                severity_class=escape(control["severity"].lower()),
            )
        )

    return "\n".join(rows)


def render_framework_cards(frameworks):
    cards = []
    for framework, counts in frameworks.items():
        cards.append(
            "\n".join(
                [
                    "              <div>",
                    "                <span>{framework}</span>",
                    "                <strong>{counts}</strong>",
                    "              </div>",
                ]
            ).format(
                framework=escape(display_framework_name(framework)),
                counts=escape(format_framework_counts(counts)),
            )
        )

    return "\n".join(cards)


def render_action_list(actions):
    items = []
    for action in actions:
        items.append(f"              <li>{escape(action)}</li>")
    return "\n".join(items)


def build_dashboard(report_text, parsed):
    controls = parsed["controls"]
    failed_controls = [control for control in controls if control["status"] == "FAIL"]
    passed_controls = [control for control in controls if control["status"] == "PASS"]
    not_evidenced_controls = [
        control for control in controls if control["status"] == "NOT EVIDENCED"
    ]
    actions = derive_actions(failed_controls)

    html_content = Template(
        """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>GRC as Code Lab | Calm Resilience Security</title>
    <meta
      name="description"
      content="A Calm Resilience Security GRC as Code Lab dashboard showing release risk, control posture, evidence coverage, and executive governance actions."
    />
    <link rel="icon" href="/assets/calm-resilience-security-logo.jpg" type="image/jpeg" />
    <style>
      :root {
        --bg: #f6f8f7;
        --surface: #ffffff;
        --text: #132625;
        --muted: #55615d;
        --line: #dce7e2;
        --accent: #0f6a57;
        --accent-2: #e6f3ef;
        --teal: #2b8975;
        --red: #c84852;
        --gold: #f1b24a;
        --shadow: rgba(19, 38, 37, 0.07);
        --max: 1120px;
      }

      * {
        box-sizing: border-box;
      }

      html {
        scroll-behavior: smooth;
      }

      body {
        margin: 0;
        color: var(--text);
        background: var(--bg);
        font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        line-height: 1.6;
        letter-spacing: 0;
      }

      a {
        color: inherit;
      }

      img {
        display: block;
        max-width: 100%;
      }

      .container {
        width: min(var(--max), calc(100% - 32px));
        margin: 0 auto;
      }

      .site-header {
        position: sticky;
        top: 0;
        z-index: 10;
        border-bottom: 1px solid var(--line);
        background: rgba(246, 248, 247, 0.94);
        backdrop-filter: blur(10px);
      }

      .nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 18px;
        padding: 16px 0;
      }

      .brand {
        display: flex;
        align-items: center;
        gap: 11px;
        text-decoration: none;
      }

      .brand-mark {
        width: 42px;
        height: 42px;
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--surface);
        object-fit: cover;
      }

      .brand-title {
        display: block;
        font-size: 1.05rem;
        font-weight: 850;
      }

      .brand-sub {
        display: block;
        color: var(--muted);
        font-size: 0.84rem;
      }

      nav ul {
        display: flex;
        flex-wrap: wrap;
        gap: 16px;
        margin: 0;
        padding: 0;
        list-style: none;
      }

      nav a {
        color: var(--muted);
        text-decoration: none;
        font-size: 0.95rem;
        font-weight: 700;
      }

      nav a.active,
      nav a:hover {
        color: var(--text);
      }

      .page-hero {
        padding: 78px 0 64px;
        color: #ffffff;
        background:
          linear-gradient(90deg, rgba(19, 38, 37, 0.96), rgba(19, 38, 37, 0.78)),
          url("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1600&q=82")
            center / cover;
      }

      .eyebrow,
      .section-kicker {
        margin: 0 0 14px;
        color: var(--gold);
        font-size: 0.8rem;
        font-weight: 850;
        text-transform: uppercase;
      }

      .section-kicker {
        color: var(--accent);
      }

      h1,
      h2,
      h3,
      p {
        margin-top: 0;
      }

      h1 {
        max-width: 13ch;
        margin-bottom: 22px;
        font-size: 3rem;
        line-height: 1.02;
      }

      h2 {
        margin-bottom: 14px;
        font-size: 2rem;
        line-height: 1.12;
      }

      h3 {
        margin-bottom: 10px;
        font-size: 1.07rem;
      }

      .lead {
        max-width: 690px;
        color: rgba(255, 255, 255, 0.82);
        font-size: 1.1rem;
        line-height: 1.75;
      }

      .section {
        padding: 76px 0;
      }

      .section-white {
        background: var(--surface);
      }

      .section-copy,
      .muted,
      .card p,
      footer {
        color: var(--muted);
      }

      .section-copy {
        font-size: 1.04rem;
        line-height: 1.75;
      }

      .contact-grid {
        display: grid;
        grid-template-columns: 1.05fr 0.95fr;
        gap: 42px;
        align-items: start;
      }

      .card,
      .release-panel,
      .lab-panel,
      .lab-metric {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--surface);
        box-shadow: 0 14px 38px var(--shadow);
      }

      .card {
        min-height: 100%;
        padding: 22px;
      }

      .lab-hero-grid {
        display: grid;
        grid-template-columns: minmax(0, 1.35fr) minmax(280px, 0.65fr);
        gap: 34px;
        align-items: end;
      }

      .release-panel {
        padding: 22px;
        color: var(--text);
      }

      .release-panel p {
        margin-bottom: 0;
        color: var(--muted);
      }

      .release-label,
      .lab-metric span,
      .framework-summary span {
        display: block;
        color: var(--muted);
        font-size: 0.78rem;
        font-weight: 850;
        text-transform: uppercase;
      }

      .release-panel strong {
        display: block;
        margin: 8px 0 10px;
        color: var(--red);
        font-size: 1.45rem;
        line-height: 1.1;
      }

      .lab-metrics,
      .framework-summary,
      .evidence-grid {
        display: grid;
        gap: 16px;
      }

      .lab-metrics {
        grid-template-columns: repeat(4, 1fr);
        margin-top: 24px;
      }

      .lab-metric {
        padding: 22px;
      }

      .lab-metric strong {
        display: block;
        margin: 12px 0 8px;
        color: var(--text);
        font-size: 2rem;
        line-height: 1;
      }

      .lab-metric p {
        margin: 0;
        color: var(--muted);
      }

      .lab-metric.risk-high strong,
      .lab-metric.decision-block strong {
        color: var(--red);
      }

      .lab-layout,
      .evidence-grid {
        display: grid;
        grid-template-columns: minmax(0, 1.25fr) minmax(280px, 0.75fr);
        gap: 18px;
        align-items: start;
      }

      .lab-panel {
        padding: 24px;
      }

      .lab-actions .list-clean li:first-child {
        border-top: 1px solid var(--line);
      }

      .framework-summary {
        grid-template-columns: repeat(3, 1fr);
        margin-top: 24px;
        border-top: 1px solid var(--line);
      }

      .framework-summary div {
        padding: 18px 18px 0 0;
      }

      .framework-summary strong {
        display: block;
        margin-top: 6px;
      }

      .table-wrap {
        overflow-x: auto;
        margin-top: 20px;
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--surface);
      }

      .control-table {
        width: 100%;
        min-width: 760px;
        border-collapse: collapse;
      }

      .control-table th,
      .control-table td {
        padding: 16px;
        text-align: left;
        border-bottom: 1px solid var(--line);
        vertical-align: top;
      }

      .control-table th {
        color: var(--muted);
        background: var(--accent-2);
        font-size: 0.8rem;
        font-weight: 850;
        text-transform: uppercase;
      }

      .control-table tr:last-child td {
        border-bottom: 0;
      }

      .control-id {
        color: var(--accent);
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-weight: 800;
      }

      .badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-height: 28px;
        padding: 5px 10px;
        border-radius: 8px;
        font-size: 0.78rem;
        font-weight: 850;
        text-transform: uppercase;
        white-space: nowrap;
      }

      .status-pass {
        color: #166534;
        background: rgba(22, 101, 52, 0.1);
      }

      .status-fail,
      .severity-high {
        color: var(--red);
        background: rgba(200, 72, 82, 0.12);
      }

      .status-not-evidenced {
        color: var(--muted);
        background: rgba(85, 97, 93, 0.12);
      }

      .severity-medium {
        color: #8a5a00;
        background: rgba(241, 178, 74, 0.22);
      }

      .evidence-block {
        overflow-x: auto;
        margin: 18px 0 0;
        padding: 18px;
        border: 1px solid var(--line);
        border-radius: 8px;
        color: var(--text);
        background: var(--bg);
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 0.9rem;
        line-height: 1.55;
        white-space: pre-wrap;
      }

      .actions {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 30px;
      }

      .button {
        display: inline-flex;
        min-height: 48px;
        align-items: center;
        justify-content: center;
        padding: 13px 18px;
        border: 1px solid var(--line);
        border-radius: 8px;
        color: var(--text);
        background: var(--surface);
        text-decoration: none;
        font-weight: 850;
      }

      .button.primary {
        color: var(--text);
        background: var(--gold);
        border-color: var(--gold);
      }

      .list-clean {
        margin: 16px 0 0;
        padding: 0;
        list-style: none;
      }

      .list-clean li {
        padding: 14px 0;
        border-top: 1px solid var(--line);
      }

      .list-clean li:first-child {
        border-top: 0;
      }

      .cta-panel {
        color: #ffffff;
        background:
          linear-gradient(90deg, rgba(19, 38, 37, 0.96), rgba(19, 38, 37, 0.78)),
          url("https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1600&q=82")
            center / cover;
      }

      .cta-panel .section-kicker {
        color: var(--gold);
      }

      .cta-panel p {
        color: rgba(255, 255, 255, 0.78);
      }

      .dark-card {
        border-color: rgba(255, 255, 255, 0.26);
        background: rgba(255, 255, 255, 0.08);
        box-shadow: none;
      }

      .dark-card p,
      .dark-card a {
        color: #ffffff;
      }

      footer {
        padding: 28px 0;
        border-top: 1px solid var(--line);
        background: var(--bg);
        font-size: 0.95rem;
      }

      .footer-inner {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: flex-start;
        gap: 20px;
      }

      @media (min-width: 720px) {
        h1 {
          font-size: 4.35rem;
        }

        h2 {
          font-size: 2.45rem;
        }
      }

      @media (min-width: 1080px) {
        h1 {
          font-size: 5rem;
        }
      }

      @media (max-width: 920px) {
        .contact-grid,
        .lab-hero-grid,
        .lab-layout,
        .evidence-grid,
        .lab-metrics,
        .framework-summary {
          grid-template-columns: 1fr;
        }

        .nav {
          align-items: flex-start;
          flex-direction: column;
        }
      }

      @media (max-width: 700px) {
        h1 {
          font-size: 2.55rem;
        }

        h2 {
          font-size: 1.8rem;
        }

        .section {
          padding: 56px 0;
        }

        .footer-inner {
          display: grid;
        }
      }
    </style>
  </head>
  <body>
    <header class="site-header">
      <div class="container nav">
        <a class="brand" href="/" aria-label="Calm Resilience Security home">
          <img class="brand-mark" src="/assets/calm-resilience-security-logo.jpg" alt="" aria-hidden="true" />
          <span>
            <span class="brand-title">Calm Resilience Security</span>
            <span class="brand-sub">Calm under pressure. Security by design.</span>
          </span>
        </a>
        <nav aria-label="Primary navigation">
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/about.html">About</a></li>
            <li><a href="/services.html">Services</a></li>
            <li><a class="active" href="/training.html">Training</a></li>
            <li><a href="/contact.html">Contact</a></li>
          </ul>
        </nav>
      </div>
    </header>

    <main>
      <section class="page-hero">
        <div class="container lab-hero-grid">
          <div>
            <p class="eyebrow">GRC as Code Lab</p>
            <h1>Executive governance dashboard.</h1>
            <p class="lead">
              A simulated fintech release view that translates infrastructure control evidence into release risk,
              assurance posture, and leadership action.
            </p>
            <div class="actions">
              <a class="button primary" href="#control-results">Review control results</a>
              <a class="button" href="/contact.html">Discuss a lab</a>
            </div>
          </div>
          <aside class="release-panel" aria-label="Current release decision">
            <span class="release-label">Current decision</span>
            <strong>$decision_short</strong>
            <p>$decision_copy</p>
          </aside>
        </div>
      </section>

      <section class="section section-white">
        <div class="container">
          <p class="section-kicker">Release posture</p>
          <h2>Control evidence converted into an executive decision.</h2>
          <div class="lab-metrics" aria-label="Dashboard summary metrics">
            <article class="lab-metric">
              <span>Compliance score</span>
              <strong>$compliance_score</strong>
              <p>$passed_count of $assessed_count assessed controls passing</p>
            </article>
            <article class="lab-metric risk-high">
              <span>Risk level</span>
              <strong>$risk_level</strong>
              <p>Aggregate risk score: $total_risk_score</p>
            </article>
            <article class="lab-metric decision-block">
              <span>Decision</span>
              <strong>$decision_short</strong>
              <p>$failed_count failed controls require action</p>
            </article>
            <article class="lab-metric">
              <span>Evidence coverage</span>
              <strong>$assessed_count/$total_count</strong>
              <p>$not_evidenced_count controls still lack evidence</p>
            </article>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="container lab-layout">
          <article class="lab-panel">
            <p class="section-kicker">Executive summary</p>
            <h2>Decision context</h2>
            <p class="section-copy">
              The current release candidate remains above acceptable deployment tolerance. This dashboard surfaces
              the specific control failures driving the decision and keeps technical evidence visible for engineering,
              audit, and governance stakeholders.
            </p>
            <div class="framework-summary" aria-label="Framework summary">
$framework_cards
            </div>
          </article>

          <aside class="lab-panel lab-actions">
            <p class="section-kicker">Priority actions</p>
            <h2>Next moves</h2>
            <ul class="list-clean">
$action_items
            </ul>
          </aside>
        </div>
      </section>

      <section class="section section-white" id="control-results">
        <div class="container">
          <p class="section-kicker">Control detail</p>
          <h2>Control results</h2>
          <div class="table-wrap">
            <table class="control-table">
              <thead>
                <tr>
                  <th>Control</th>
                  <th>Description</th>
                  <th>Status</th>
                  <th>Severity</th>
                </tr>
              </thead>
              <tbody>
$control_rows
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="container evidence-grid">
          <article class="lab-panel">
            <p class="section-kicker">Raw governance report</p>
            <h2>Technical evidence</h2>
            <pre class="evidence-block">$raw_report</pre>
          </article>

          <article class="lab-panel">
            <p class="section-kicker">Governance value</p>
            <h2>What the lab demonstrates</h2>
            <p class="section-copy">
              The lab shows how GRC as Code can turn infrastructure evidence into language that engineers,
              auditors, and executives can all use: control status, severity, release tolerance, and actions.
            </p>
            <ul class="list-clean">
              <li>Controls are assessed from evidence rather than assertion.</li>
              <li>Framework summaries are translated into release posture.</li>
              <li>Risk decisions stay visible, explainable, and repeatable.</li>
            </ul>
          </article>
        </div>
      </section>

      <section class="section cta-panel">
        <div class="container contact-grid">
          <div>
            <p class="section-kicker">Build capability</p>
            <h2>Turn governance evidence into decisions people can act on.</h2>
            <p class="section-copy">
              Calm Resilience Security designs practical labs and training for teams that need security governance
              to be clear, evidenced, and resilient.
            </p>
          </div>
          <div class="card dark-card">
            <h3>Discuss a GRC as Code lab</h3>
            <p>Email: <a href="mailto:info@calmsecurity.uk">info@calmsecurity.uk</a></p>
            <a class="button primary" href="mailto:info@calmsecurity.uk">Email Calm Security</a>
          </div>
        </div>
      </section>
    </main>

    <footer>
      <div class="container footer-inner">
        <strong>Calm Resilience Security Ltd</strong>
        <span><a href="mailto:info@calmsecurity.uk">info@calmsecurity.uk</a></span>
        <span>Registered in England with company number 16876614.</span>
        <span>Registered office: 124 City Road, London, EC1V 2NX.</span>
      </div>
    </footer>
  </body>
</html>
"""
    ).substitute(
        decision_copy=escape(decision_copy(parsed["decision"])),
        decision_short=escape(decision_label(parsed["decision"])),
        compliance_score=escape(parsed["compliance_score"]),
        risk_level=escape(display_status(parsed["risk_level"])),
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
