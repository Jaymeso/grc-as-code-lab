# GRC as Code Lab Demo Script

## Goal

Use this script for a short live walkthrough of the platform with a client, stakeholder, or interviewer.

## Demo Outcome

By the end of the walkthrough, the audience should understand that this project:

- translates infrastructure findings into governance controls
- maps technical issues to regulatory frameworks
- generates a risk-based deployment decision
- produces evidence and a publishable executive dashboard

## Suggested Duration

- 3 minutes for a quick demo
- 7 minutes for a fuller walkthrough

## Demo Flow

### 1. Introduce the platform

Open the repository and explain:

> This is a GRC-as-Code prototype that turns infrastructure misconfigurations into compliance posture, risk scoring, and deployment decisions.

Key points to mention:

- Terraform represents the infrastructure under review
- Checkov produces machine-readable findings
- YAML files define the governance controls
- Python translates technical findings into governance outcomes
- GitHub Actions publishes the results to GitHub Pages

### 2. Show the control library

Open the `controls/` folder and mention the governance coverage:

- Storage Security
- Identity and Access Management
- Data Protection
- Logging and Monitoring
- Cloud Governance
- Network Security
- Resilience and Recovery
- Secure Engineering

Suggested line:

> The platform no longer relies on a single control family. It now evaluates multiple governance domains and rolls them into one release decision.

### 3. Show the engine

Open `grc_engine.py` and explain:

- it loads all control YAML files
- it resolves Checkov mappings
- it supports older and newer control formats
- it marks controls as `PASS`, `FAIL`, or `NOT EVIDENCED`
- it calculates compliance score, evidence coverage, and risk level

Suggested line:

> One of the improvements here is that controls without supporting evidence are no longer treated as false passes. They are surfaced honestly as `NOT EVIDENCED`.

### 4. Show the latest governance output

Open `evidence/week3_risk_report.txt` and highlight:

- Compliance Score: `16.67%`
- Controls Assessed: `6`
- Controls Not Evidenced: `3`
- Risk Level: `HIGH`
- Decision: `BLOCK DEPLOYMENT`

Suggested line:

> This is where the platform becomes useful to leadership. It does not just list scanner findings. It translates them into a release decision with evidence behind it.

### 5. Show the dashboard

Open the GitHub Pages dashboard and point out:

- executive summary
- scorecards
- framework summary
- control detail
- raw evidence section

Suggested line:

> The dashboard gives engineering, GRC, and leadership a shared view of the same assessment without losing technical detail.

### 6. Close with business value

Use a short close like:

> The value of this approach is that governance becomes continuous, testable, and visible in the delivery pipeline instead of being a separate manual checkpoint at the end.

## Optional Command Sequence

If you want to demo the pipeline locally:

```bash
checkov -d terraform --output json > checkov_results.json || true
python3 grc_engine.py
python3 generate_dashboard.py
```

## Strong Closing Lines

Choose one:

- This shows how compliance can move from static documentation into live engineering workflows.
- This is a small prototype of how regulated organisations can build continuous assurance into CI/CD.
- The key idea is that technical findings become governance evidence, not just scanner output.
