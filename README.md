# GRC as Code Lab

![Terraform](https://img.shields.io/badge/Terraform-IaC-blue)
![OPA](https://img.shields.io/badge/OpenPolicyAgent-PolicyEngine-green)
![Checkov](https://img.shields.io/badge/Checkov-ComplianceScanner-orange)
![Security](https://img.shields.io/badge/Security-GRC%20as%20Code-red)





# GRC as Code Lab

Hands-on training environment demonstrating how governance, risk, and compliance can be implemented as code using modern cloud security tools.

## Tools Used

- Terraform
- Open Policy Agent (OPA)
- Checkov

## Repository Structure

terraform/  → example cloud infrastructure  
policies/   → governance policy rules  
controls/   → control library definitions  
evidence/   → audit evidence from exercises  

## Purpose

This lab demonstrates how traditional governance controls can be translated into machine-enforced rules for continuous compliance.

## Training

See: docs/grc-as-code-training-manual.md


# GRC as Code Lab

A hands-on training environment demonstrating how governance, risk and compliance controls can be implemented as code using modern cloud security tools.

## Tools Used

- Terraform
- Open Policy Agent (OPA)
- Checkov

## Architecture

Terraform Infrastructure  
↓  
Checkov Compliance Scanner  
↓  
OPA Policy Engine  
↓  
Control Library  
↓  
Evidence

## Repository Structure

terraform/  → infrastructure examples  
policies/   → governance policy rules  
controls/   → control definitions  
evidence/   → audit evidence  

## Example Controls

- Public S3 buckets prohibited
- S3 versioning required

## Training

Instructor manual available in:

docs/grc-as-code-training-manual.md

## Purpose

This project demonstrates how traditional governance controls can be translated into machine-enforced rules enabling continuous compliance.

