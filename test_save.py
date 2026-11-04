from database import save_diagnostic

result = save_diagnostic(
    hostname="TEST-PC",
    local_ip="192.168.1.10",
    internet_status=True,
    ping_status=True,
    response_time=45.5,
    packet_loss=0,
    dns_status=True
)

if result:
    print("Diagnostic record saved successfully!")