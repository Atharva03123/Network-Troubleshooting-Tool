from database import fetch_diagnostics

records = fetch_diagnostics()

print("Diagnostic History:")

for record in records:
    print(record)