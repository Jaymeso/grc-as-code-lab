# GRC as Code Training Lab
Instructor Manual – Week 1

## Overview

This training lab introduces the concept of **GRC as Code**.  
Participants learn how governance controls can be translated into machine-enforced policies using modern cloud security tools.

Duration: 2–3 hours

Audience:
- Security engineers
- GRC analysts
- DevSecOps engineers
- Cloud engineers


---

## Learning Objectives

By the end of this lab participants will:

1. Understand the concept of GRC as Code
2. Learn the difference between controls and enforcement tools
3. Build infrastructure using Terraform
4. Create governance rules using Open Policy Agent (OPA)
5. Detect cloud misconfigurations using Checkov
6. Map controls to regulatory frameworks
7. Understand continuous compliance pipelines


---

## Lab Architecture

Participants will build the following governance pipeline:

Terraform Infrastructure  
↓  
Checkov Compliance Scan  
↓  
OPA Policy Engine  
↓  
Control Library  
↓  
Evidence

This mirrors the architecture used by modern security platforms such as:

- Prisma Cloud
- Wiz
- Lacework
- Bridgecrew
- Drata


---

## Prerequisites

Participants require:

- Mac or Linux laptop
- Terminal access
- Internet connection


---

## Tools Used

Git – version control  
Terraform – infrastructure as code  
Open Policy Agent – policy engine  
Checkov – compliance scanning tool


---

## Exercise 1 – Create Project Structure

Create the repository structure:

mkdir -p grc-as-code-lab/{terraform,policies,controls,evidence}



Expected structure:

terraform/  
policies/  
controls/  
evidence/


---

## Exercise 2 – Create Insecure Infrastructure

Create an intentionally insecure S3 bucket:

nano terraform/insecure_s3.tf

Add:

resource "aws_s3_bucket" "bad_bucket" {
bucket = "grc-test-public-bucket"
acl = "public-read"
}


This resource intentionally violates multiple security controls.


---

## Exercise 3 – Create Governance Policy

Create an OPA rule:

nano policies/s3_public.rego


Add:

package security

deny contains msg if {
input.resource_type == "aws_s3_bucket"
input.acl == "public-read"
msg := "Public S3 buckets are not allowed"
}



This converts a governance control into executable policy.


---

## Exercise 4 – Test the Policy

Create test input:
nano test.json

Add:
{
"resource_type": "aws_s3_bucket",
"acl": "public-read"
}




Run evaluation:
opa eval --format pretty --data policies/s3_public.rego --input test.json "data.security.deny"

Expected result:

[
"Public S3 buckets are not allowed"
]





---

## Exercise 5 – Run Compliance Scan

Run Checkov:

checkov -d terraform/


Checkov will detect multiple misconfigurations including:

- public bucket access
- missing versioning
- missing encryption
- missing logging

This demonstrates that **one resource can violate multiple governance controls**.


---

## Exercise 6 – Create Secure Configuration

Create a secure bucket configuration:

nano terraform/secure_s3.tf


Add:

resource "aws_s3_bucket" "secure_bucket" {
bucket = "grc-test-secure-bucket"
}

resource "aws_s3_bucket_public_access_block" "secure_bucket_block" {
bucket = aws_s3_bucket.secure_bucket.id

block_public_acls = true
block_public_policy = true
ignore_public_acls = true
restrict_public_buckets = true
}


Re-run Checkov to observe improved security posture.


---

## Exercise 7 – Create Control Library

Define the governance control:

nano controls/s3_baseline.yaml

Example control:


control_family:
id: AWS-S3-BASELINE
name: S3 Baseline Security Controls

controls:

id: GRC-001
name: Public S3 Buckets Prohibited
frameworks:
ISO27001: A.8.20
SOC2: CC6
NIST: AC-3
enforcement:
opa_policy: policies/s3_public.rego
scanner: checkov



---

## Exercise 8 – Capture Evidence

Create evidence record:


nano evidence/week1_notes.txt


Example:


OPA policy successfully enforced rule.

Checkov detected multiple S3 misconfigurations.

Secure configuration improved compliance posture.




---

## Final Repository Structure


grc-as-code-lab
│
├ terraform/
├ policies/
├ controls/
├ evidence/
├ docs/
└ README.md




---

## Key Takeaways

1. Cloud misconfigurations often violate multiple controls.
2. Governance controls should be separated from enforcement tools.
3. Infrastructure as Code enables preventative compliance.
4. Policy engines allow continuous governance enforcement.


---

## Next Module (Week 2)

Participants will learn:

- framework mapping engines
- automated control evaluation
- risk scoring
- CI/CD compliance pipelines
