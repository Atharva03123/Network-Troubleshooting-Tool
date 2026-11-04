from database import search_diagnostics

print("\n--- All Records ---")
records = search_diagnostics()

for record in records:
    print(record)

print("\n--- Search by Hostname ---")
records = search_diagnostics(hostname="TEST-PC")

for record in records:
    print(record)

print("\n--- Search Failed Internet Records ---")
records = search_diagnostics(internet_status=False)

for record in records:
    print(record)