import json
import yaml

# Load Checkov results
with open("checkov_results.json") as f:
    checkov_data = json.load(f)

failed_checks = [
    check["check_id"]
    for check in checkov_data["results"]["failed_checks"]
]

# Load control taxonomy
with open("controls/control_taxonomy.yaml") as f:
    control_data = yaml.safe_load(f)

controls = control_data["controls"]

results = []

for control in controls:
    checkov_id = control["enforcement"]["checkov"]

    status = "PASS"
    if checkov_id in failed_checks:
        status = "FAIL"

    results.append({
        "control_id": control["id"],
        "name": control["name"],
        "status": status,
        "frameworks": control["frameworks"],
        "severity": control["severity"]
    })

# Calculate compliance score
total = len(results)
passed = len([r for r in results if r["status"] == "PASS"])
score = (passed / total) * 100

print("\n=== COMPLIANCE REPORT ===\n")

for r in results:
    print(f"{r['control_id']} - {r['name']}: {r['status']} ({r['severity']})")
framework_summary = {}

for r in results:
    for framework, control in r["frameworks"].items():
        if framework not in framework_summary:
            framework_summary[framework] = {"PASS": 0, "FAIL": 0}

        framework_summary[framework][r["status"]] += 1

print("\n=== FRAMEWORK SUMMARY ===\n")

for fw, counts in framework_summary.items():
    print(f"{fw}: {counts}")
print(f"\nCompliance Score: {score:.2f}%")

framework_summary = {}

for r in results:
    for framework, control in r["frameworks"].items():
        if framework not in framework_summary:
            framework_summary[framework] = {"PASS": 0, "FAIL": 0}

        framework_summary[framework][r["status"]] += 1

print("\n=== FRAMEWORK SUMMARY ===\n")

for fw, counts in framework_summary.items():
    print(f"{fw}: {counts}")

# Save evidence
with open("evidence/week2_compliance_report.txt", "w") as f:
    f.write("=== COMPLIANCE REPORT ===\n\n")
    for r in results:
        f.write(f"{r['control_id']} - {r['status']}\n")
    f.write(f"\nScore: {score:.2f}%\n")

