import ast
import os
import sys

violations = []

# Policy 1: No hardcoded API keys
with open("config.py", "r") as file:
    config_tree = ast.parse(file.read())

for node in ast.walk(config_tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "API_KEY":
                if not isinstance(node.value, ast.Call):
                    violations.append("Hardcoded API key detected")

# Policy 2: Debug mode must be disabled
debug_found = False

for node in ast.walk(config_tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "DEBUG":
                debug_found = True
                if not (
                    isinstance(node.value, ast.Constant)
                    and node.value.value is False
                ):
                    violations.append("Debug mode must be disabled")

if not debug_found:
    violations.append("DEBUG setting is missing")

# Policy 3: Logging must use a separate file
with open("app.py", "r") as file:
    app_tree = ast.parse(file.read())

file_logging = False

for node in ast.walk(app_tree):
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "basicConfig":
                if any(keyword.arg == "filename" for keyword in node.keywords):
                    file_logging = True

        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "FileHandler":
                file_logging = True

if not file_logging:
    violations.append("Application logging to a separate file is not enabled")

# Generate compliance report
os.makedirs("reports", exist_ok=True)

with open("reports/compliance-report.txt", "w") as report:
    report.write("COMPLIANCE CHECK REPORT\n")
    report.write("=======================\n\n")

    if violations:
        report.write("STATUS: NON-COMPLIANT\n\n")
        for violation in violations:
            report.write("[FAIL] " + violation + "\n")
    else:
        report.write("STATUS: COMPLIANT\n\n")
        report.write("[PASS] No hardcoded API keys\n")
        report.write("[PASS] Debug mode disabled\n")
        report.write("[PASS] Separate application logging enabled\n")

if violations:
    print("Compliance check FAILED")
    for violation in violations:
        print("[FAIL]", violation)
    sys.exit(1)

print("Compliance check PASSED")
print("All compliance policies satisfied.")
