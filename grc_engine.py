import json
import sys
from pathlib import Path

import yaml


REPORT_PATH = Path("evidence/week3_risk_report.txt")
CHECKOV_RESULTS_PATH = Path("checkov_results.json")
CONTROLS_DIR = Path("controls")


def load_check_sets():
    with CHECKOV_RESULTS_PATH.open() as file_handle:
        checkov_data = json.load(file_handle)

    failed_checks = {
        check["check_id"]
        for check in checkov_data["results"]["failed_checks"]
    }
    passed_checks = {
        check["check_id"]
        for check in checkov_data["results"]["passed_checks"]
    }

    return failed_checks, passed_checks


def resolve_checkov_id(control):
    enforcement = control.get("enforcement", {})

    if "checkov" in enforcement:
        return enforcement["checkov"]

    # Older baseline controls used OPA policy references without a direct
    # Checkov ID. Keep known mappings here so both control formats work.
    legacy_policy_map = {
        "policies/s3_public.rego": "CKV_AWS_20",
        "policies/s3_versioning.rego": "CKV_AWS_21",
    }

    return legacy_policy_map.get(enforcement.get("opa_policy"))


def score_control_definition(control):
    enforcement = control.get("enforcement", {})

    return (
        3 * int("checkov" in enforcement)
        + 2 * int("severity" in control)
        + int("objective" in control)
        + len(control)
    )


def load_controls():
    controls_by_id = {}

    for file_path in sorted(CONTROLS_DIR.glob("*.yaml")):
        with file_path.open() as file_handle:
            control_data = yaml.safe_load(file_handle) or {}

        for control in control_data.get("controls", []):
            control_copy = dict(control)
            control_copy["source_file"] = file_path.name
            control_id = control_copy["id"]
            existing_control = controls_by_id.get(control_id)

            if existing_control is None:
                controls_by_id[control_id] = control_copy
                continue

            existing_score = score_control_definition(existing_control)
            current_score = score_control_definition(control_copy)

            if current_score >= existing_score:
                controls_by_id[control_id] = control_copy

    return list(controls_by_id.values())


failed_checks, passed_checks = load_check_sets()
controls = load_controls()
results = []
framework_summary = {}
total_risk_score = 0
max_possible_risk = 0

for control in controls:
    checkov_id = resolve_checkov_id(control)
    status = "NOT EVIDENCED"

    if checkov_id in failed_checks:
        status = "FAIL"
    elif checkov_id in passed_checks:
        status = "PASS"

    risk_weight = control.get("risk_weight", 0)
    severity = control.get("severity", "MEDIUM")
    frameworks = control.get("frameworks", {})

    if status in {"PASS", "FAIL"}:
        max_possible_risk += risk_weight
    if status == "FAIL":
        total_risk_score += risk_weight

    for framework in frameworks:
        if framework not in framework_summary:
            framework_summary[framework] = {
                "PASS": 0,
                "FAIL": 0,
                "NOT EVIDENCED": 0,
            }
        framework_summary[framework][status] += 1

    results.append(
        {
            "control_id": control["id"],
            "name": control["name"],
            "status": status,
            "frameworks": frameworks,
            "severity": severity,
            "risk_weight": risk_weight,
            "checkov_id": checkov_id or "UNMAPPED",
            "source_file": control["source_file"],
        }
    )

assessed_results = [result for result in results if result["status"] in {"PASS", "FAIL"}]
total = len(assessed_results)
passed = len([result for result in assessed_results if result["status"] == "PASS"])
not_evidenced = len([result for result in results if result["status"] == "NOT EVIDENCED"])
score = (passed / total) * 100 if total > 0 else 0

if total_risk_score >= 50:
    risk_level = "HIGH"
elif total_risk_score >= 20:
    risk_level = "MEDIUM"
else:
    risk_level = "LOW"

if total == 0:
    decision = "INSUFFICIENT EVIDENCE"
elif risk_level == "HIGH":
    decision = "BLOCK DEPLOYMENT"
elif risk_level == "MEDIUM":
    decision = "REVIEW REQUIRED"
else:
    decision = "ALLOW"

print("\n=== COMPLIANCE REPORT ===\n")
for result in results:
    print(
        f"{result['control_id']} - {result['name']}: "
        f"{result['status']} ({result['severity']})"
    )

print("\n=== FRAMEWORK SUMMARY ===\n")
for framework, counts in framework_summary.items():
    print(f"{framework}: {counts}")

print(f"\nCompliance Score: {score:.2f}%")

print("\n=== EVIDENCE COVERAGE ===\n")
print(f"Controls Assessed: {total}")
print(f"Controls Not Evidenced: {not_evidenced}")

print("\n=== RISK SUMMARY ===\n")
print(f"Total Risk Score: {total_risk_score}")
print(f"Risk Level: {risk_level}")
print(f"\nDecision: {decision}")

with REPORT_PATH.open("w") as file_handle:
    file_handle.write("=== COMPLIANCE REPORT ===\n\n")
    for result in results:
        file_handle.write(
            f"{result['control_id']} - {result['name']}: "
            f"{result['status']} ({result['severity']})\n"
        )

    file_handle.write("\n=== FRAMEWORK SUMMARY ===\n\n")
    for framework, counts in framework_summary.items():
        file_handle.write(f"{framework}: {counts}\n")

    file_handle.write(f"\nCompliance Score: {score:.2f}%\n")
    file_handle.write("\n=== EVIDENCE COVERAGE ===\n\n")
    file_handle.write(f"Controls Assessed: {total}\n")
    file_handle.write(f"Controls Not Evidenced: {not_evidenced}\n")
    file_handle.write("\n=== RISK SUMMARY ===\n\n")
    file_handle.write(f"Total Risk Score: {total_risk_score}\n")
    file_handle.write(f"Risk Level: {risk_level}\n")
    file_handle.write(f"Decision: {decision}\n")

if decision == "BLOCK DEPLOYMENT":
    sys.exit(1)
