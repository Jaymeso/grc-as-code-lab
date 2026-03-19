import json
import yaml

# -----------------------------
# Risk counters
# -----------------------------
total_risk_score = 0
max_possible_risk = 0

# -----------------------------
# Load Checkov results
# -----------------------------
with open("checkov_results.json") as f:
    checkov_data = json.load(f)

failed_checks = [
    check["check_id"]
    for check in checkov_data["results"]["failed_checks"]
]

# -----------------------------
# Load control definitions
# -----------------------------
with open("controls/control_taxonomy.yaml") as f:
    control_data = yaml.safe_load(f)

controls = control_data["controls"]

results = []

# -----------------------------
# Evaluate controls
# -----------------------------
for control in controls:
    checkov_id = control["enforcement"]["checkov"]

    status = "PASS"
    if checkov_id in failed_checks:
        status = "FAIL"

    risk_weight = control.get("risk_weight", 0)
    max_possible_risk += risk_weight

    if status == "FAIL":
        total_risk_score += risk_weight

    results.append({
        "control_id": control["id"],
        "name": control["name"],
        "status": status,
        "frameworks": control["frameworks"],
        "severity": control["severity"],
        "risk_weight": risk_weight
    })

# -----------------------------
# Compliance score
# -----------------------------
total = len(results)
passed = len([r for r in results if r["status"] == "PASS"])
score = (passed / total) * 100 if total > 0 else 0

# -----------------------------
# Print compliance report
# -----------------------------
print("\n=== COMPLIANCE REPORT ===\n")

for r in results:
    print(f"{r['control_id']} - {r['name']}: {r['status']} ({r['severity']})")

# -----------------------------
# Framework summary
# -----------------------------
framework_summary = {}

for r in results:
    for framework in r["frameworks"]:
        if framework not in framework_summary:
            framework_summary[framework] = {"PASS": 0, "FAIL": 0}

        framework_summary[framework][r["status"]] += 1

print("\n=== FRAMEWORK SUMMARY ===\n")

for fw, counts in framework_summary.items():
    print(f"{fw}: {counts}")

print(f"\nCompliance Score: {score:.2f}%")

# -----------------------------
# Risk summary
# -----------------------------
print("\n=== RISK SUMMARY ===\n")
print(f"Total Risk Score: {total_risk_score}")

if total_risk_score >= 50:
    risk_level = "HIGH"
elif total_risk_score >= 20:
    risk_level = "MEDIUM"
else:
    risk_level = "LOW"

print(f"Risk Level: {risk_level}")

if risk_level == "HIGH":
    decision = "BLOCK DEPLOYMENT"
elif risk_level == "MEDIUM":
    decision = "REVIEW REQUIRED"
else:
    decision = "ALLOW"

print(f"\nDecision: {decision}")

# -----------------------------
# Save evidence file
# -----------------------------
with open("evidence/week3_risk_report.txt", "w") as f:
    f.write("=== COMPLIANCE REPORT ===\n\n")

    for r in results:
        f.write(f"{r['control_id']} - {r['name']}: {r['status']} ({r['severity']})\n")

    f.write("\n=== FRAMEWORK SUMMARY ===\n\n")

    for fw, counts in framework_summary.items():
        f.write(f"{fw}: {counts}\n")

    f.write(f"\nCompliance Score: {score:.2f}%\n")

    f.write("\n=== RISK SUMMARY ===\n\n")
    f.write(f"Total Risk Score: {total_risk_score}\n")
    f.write(f"Risk Level: {risk_level}\n")
    f.write(f"Decision: {decision}\n")
