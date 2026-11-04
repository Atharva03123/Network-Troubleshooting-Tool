from network_utils import check_internet, ping_test, dns_lookup
from network_utils import (
    check_internet,
    ping_test,
    dns_lookup,
    get_hostname,
    get_local_ip
)

print("Internet Connectivity:")

if check_internet():
    print("Connected")
else:
    print("Not Connected")


print("\nPing Test:")

result = ping_test()
print(result)


print("\nDNS Lookup Test:")

dns_result = dns_lookup("google.com")
print(dns_result)
print("\nComputer Information:")

print("Hostname:", get_hostname())
print("Local IP Address:", get_local_ip())