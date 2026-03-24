<p align="center">
  <img src="assets/calm.png" width="160"/>
</p>

<p align="center">
  <b>Calm Resilience Security LTD</b><br>
  <i>Engineering calm through resilient security</i>
</p>

# GRC as Code Lab

## What This Is

A production-style GRC-as-Code platform prototype that converts cloud misconfigurations into control failures, framework impacts, risk scores, and deployment decisions.

Built to demonstrate how modern organisations can move from manual audits to continuous assurance.

## Enterprise Control Coverage

This platform currently evaluates multiple governance domains:

- Storage Security
- Identity & Access Management
- Data Protection
- Logging & Monitoring

It produces a unified compliance score, risk score, and deployment decision across all control families.

## Fintech Governance Scenario

This platform simulates a pre-deployment governance gate for a fintech environment.

### Example Scenario

A trading platform is preparing to deploy cloud infrastructure changes. Before release, the GRC engine automatically evaluates whether the environment meets baseline governance expectations across:

- Storage Security
- Identity & Access Management
- Data Protection
- Logging & Monitoring

The engine then determines whether the change should be:

- **ALLOW**
- **REVIEW REQUIRED**
- **BLOCK DEPLOYMENT**

This demonstrates how regulated organisations can move from manual review to continuous, automated assurance.

## Live Dashboard

View the published executive governance dashboard here:

[Executive Governance Dashboard](https://jaymeso.github.io/grc-as-code-lab/)

## Why This Matters

In regulated cloud environments, technical misconfigurations are not just engineering issues — they can become governance, audit, and operational risk issues.

This prototype demonstrates how infrastructure findings can be translated into:

- control failures
- framework impact
- compliance posture
- risk score
- deployment decision

This allows security and GRC teams to embed governance directly into delivery pipelines.

## Why This Matters

In regulated cloud environments, technical misconfigurations are not just engineering issues — they can become governance, audit, and operational risk issues.

This prototype demonstrates how infrastructure findings can be translated into:

- control failures
- framework impact
- compliance posture
- risk score
- deployment decision

This allows security and GRC teams to embed governance directly into delivery pipelines.

## What the Platform Produces

For each infrastructure evaluation, the platform produces:

- Control-level pass/fail results
- Framework summaries across ISO 27001, SOC 2, and NIST
- Compliance score
- Risk score and risk level
- Deployment decision
- Evidence reports
- Executive summary

## Example Outcome

### Medium-Risk Scenario
- Compliance Score: 50.00%
- Risk Level: MEDIUM
- Decision: REVIEW REQUIRED

### High-Risk Scenario
- Compliance Score: 20.00%
- Risk Level: HIGH
- Decision: BLOCK DEPLOYMENT

These scenarios show how the platform supports graduated governance decisions rather than binary pass/fail reporting.

## Who This Is For

This prototype is relevant to:

- Fintech and regulated cloud platforms
- Security and GRC leaders
- DevSecOps teams
- Internal audit and assurance functions
- Organisations aligning to ISO 27001, SOC 2, and NIST

## Implementation Use Cases

This architecture can be adapted for organisations that want to:

- gate infrastructure changes through governance policy
- automate control evaluation across cloud environments
- generate machine-readable assurance evidence
- introduce risk-based release decisions into CI/CD
- prototype internal compliance engineering capabilities

![Terraform](https://img.shields.io/badge/Terraform-IaC-blue)
![OPA](https://img.shields.io/badge/OpenPolicyAgent-PolicyEngine-green)
![Checkov](https://img.shields.io/badge/Checkov-ComplianceScanner-orange)
![Security](https://img.shields.io/badge/Security-GRC%20as%20Code-red)

## Overview

This repository demonstrates how **Governance, Risk, and Compliance (GRC)** controls can be implemented as code using modern cloud security tools.

The project shows how traditional governance controls can be translated into **machine-enforced policies** enabling continuous compliance.

### Course Roadmap
This repository is structured as a progressive GRC engineering training programme.

### Week 1 – Foundations: GRC as Code

- Infrastructure as Code (Terraform)
- Policy as Code (OPA)
- Compliance Scanning (Checkov)
- Control Definition (YAML)
- Evidence capture

Outcome:
- Detect misconfigurations
- Understand control enforcement

---

### Week 2 – Compliance Engine & Automation

- Checkov JSON parsing
- Control mapping engine (Python)
- Framework mapping (ISO27001 / SOC2 / NIST)
- Compliance scoring
- GitHub Actions integration
- Automated evidence generation

Outcome:
- Translate technical findings into compliance posture
- Generate audit-ready evidence automatically

---

### Week 3 – Risk Engine

- Risk weighting per control
- Total risk score calculation
- Risk classification (LOW / MEDIUM / HIGH)
- Deployment decision logic

Outcome:
- Move from compliance reporting to risk-based governance

---

### Week 4 – Enterprise GRC Architecture

- Expanded from single-family controls to multi-family governance
- Added IAM control family
- Added Data Protection control family
- Added Logging & Monitoring control family
- Unified enterprise risk scoring across multiple domains

Outcome:
- Aggregate risk across storage, identity, data protection, and logging
- Produce a single governance decision across multiple control families

---

### Week 5 – Client-Ready Fintech Use Case

- Fintech governance scenario
- Executive-style reporting
- Product-style repo positioning
- Business-value framing

Outcome:
- Turn the lab into a client-ready governance product prototype

## Evidence Trail

The `evidence/` folder captures the progression of the platform:

- Week 1 – Foundations of GRC as Code
- Week 2 – Compliance Evaluation Report
- Week 3 – Risk Engine Evidence
- Week 4 – Enterprise Governance Evidence

---
## Business Value

This platform demonstrates how organisations can:

- move from manual compliance checks to continuous assurance
- enforce governance through CI/CD pipelines
- translate technical findings into executive-level risk decisions
- generate machine-readable evidence for audit and assurance
- apply one governance engine across multiple cloud control families

For fintech and regulated environments, this supports faster release cycles without sacrificing governance discipline.

## Example Outcomes

This lab demonstrates multiple governance states depending on infrastructure configuration.

### Scenario A – Medium Risk

- GRC-001 Public S3 Buckets Prohibited: PASS  
- GRC-002 S3 Versioning Required: FAIL  
- Compliance Score: 50.00%  
- Risk Level: MEDIUM  
- Decision: REVIEW REQUIRED  

This scenario reflects a partially compliant environment where issues exist but do not require immediate deployment blocking.

---

### Scenario B – High Risk

- GRC-001 Public S3 Buckets Prohibited: FAIL  
- GRC-002 S3 Versioning Required: FAIL  
- Compliance Score: 0.00%  
- Risk Level: HIGH  
- Decision: BLOCK DEPLOYMENT  

This scenario demonstrates a critical misconfiguration where deployment must be stopped.

---
## Fintech Use Case

This platform simulates a fintech cloud governance gate for infrastructure changes.

### Scenario

A trading platform is preparing to deploy infrastructure updates. Before release, the platform automatically evaluates:

- Storage Security
- Identity & Access Management
- Data Protection
- Logging & Monitoring

The engine then determines whether the release should be:

- **ALLOW**
- **REVIEW REQUIRED**
- **BLOCK DEPLOYMENT**

### Example Governance Outcome

A partially compliant deployment may produce:

- Compliance Score: 50.00%
- Risk Level: MEDIUM
- Decision: REVIEW REQUIRED

A high-risk deployment may produce:

- Compliance Score: 20.00%
- Risk Level: HIGH
- Decision: BLOCK DEPLOYMENT

---

### Why This Matters

Modern GRC systems should not operate on binary pass/fail logic.

This lab demonstrates:

- Partial compliance handling  
- Risk-based decision making  
- Automated enforcement of governance thresholds  

This repository is structured as a progressive GRC engineering training programme.

### Week 1 – Foundations: GRC as Code

- Infrastructure as Code (Terraform)
- Policy as Code (OPA)
- Compliance Scanning (Checkov)
- Control Definition (YAML)
- Evidence capture

Outcome:
- Detect misconfigurations
- Understand control enforcement

---

### Week 2 – Compliance Engine & Automation

- Checkov JSON parsing
- Control mapping engine (Python)
- Framework mapping (ISO27001 / SOC2 / NIST)
- Compliance scoring
- GitHub Actions integration
- Automated evidence generation

Outcome:
- Translate technical findings into compliance posture
- Generate audit-ready evidence automatically

---

### Week 3 – Risk Engine (Coming Next)

- Risk scoring (HIGH / MEDIUM weighting)
- Control criticality
- Compliance thresholds
- Risk-based decision making
- Dashboard-style output

Outcome:
- Move from compliance → risk intelligence

---

### Week 4 – Enterprise GRC Architecture

- Expanded from single-family controls to multi-family governance
- Added IAM control family
- Added Data Protection control family
- Unified enterprise risk scoring across multiple domains

Control families now include:
- Storage Security
- Identity & Access Management
- Data Protection

Example outcome:
- Compliance Score: 25.00%
- Risk Level: HIGH
- Decision: BLOCK DEPLOYMENT

---

- Added Logging / Monitoring control family

Control families now include:
- Storage Security
- Identity & Access Management
- Data Protection
- Logging / Monitoring

---

## What This Project Demonstrates

This lab simulates how modern cloud governance platforms operate:

- Continuous compliance (every commit is evaluated)
- Control abstraction (technical → governance)
- Framework alignment (ISO27001, SOC2, NIST)
- Automated evidence generation
- DevSecOps integration

The system evolves from:
Misconfiguration detection

to:

Compliance as Code


and ultimately to:

Risk-based governance


## Tools Used

- Terraform (Infrastructure as Code)
- Open Policy Agent (Policy Engine)
- Checkov (Compliance Scanner)

## Architecture

```mermaid
flowchart TD

A[Terraform Infrastructure]
B[Checkov Compliance Scan]
C[OPA Policy Engine]
D[Control Library]
E[Evidence]

A --> B
B --> C
C --> D
D --> E
``` 

This diagram illustrates how governance controls are enforced through automated scanning and policy evaluation.


## Repository Structure

grc-as-code-lab
│
├ terraform/ Infrastructure examples
├ policies/ Governance policy rules
├ controls/ Control definitions
├ evidence/ Audit evidence
├ diagrams/ Architecture diagrams
├ docs/ Training documentation
└ README.md


## Example Controls

This lab demonstrates several governance controls including:

- Public S3 buckets prohibited
- S3 versioning required
- Secure storage configuration

## Evidence Trail

The `evidence/` folder captures the progression of the platform:

- Week 1 – Foundations of GRC as Code
- Week 2 – Compliance Evaluation Report
- Week 3 – Risk Engine Evidence
- Week 4 – Enterprise Governance Evidence



## Training Manual

A full instructor guide for running this lab in a training environment is available here: docs/grc-as-code-training-manual.md



## About

This training lab is developed and maintained by **Calm Resilience Security LTD**, a consultancy focused on:

- Cloud governance and security
- GRC automation
- ISO27001 / SOC2 alignment
- DevSecOps integration

The goal is to demonstrate how modern organisations can move from manual compliance processes to **automated, continuous assurance**.

## Who This Is For

This prototype is relevant to:

- Fintech platforms
- Cloud-native regulated businesses
- Security and GRC leaders
- DevSecOps teams
- Organisations aligning to ISO 27001, SOC 2, and NIST

---

## Commercial Use & Services

This project is released under the MIT License and is free to use, modify, and distribute.

However, this repository represents a **reference implementation of a GRC-as-Code architecture** developed by **Calm Resilience Security LTD**.

For organisations looking to:

- Implement enterprise-grade GRC automation
- Integrate compliance into CI/CD pipelines
- Build ISO 27001 / SOC 2 / NIST-aligned control frameworks
- Operationalise risk-based deployment decisions

We offer consulting, advisory, and implementation services.

📩 Contact: enquiries@calmresilience.security  
🌐 Company: Calm Resilience Security LTD

---

## Disclaimer

This project is provided for educational and demonstration purposes.  
It does not constitute legal, regulatory, or compliance advice.
