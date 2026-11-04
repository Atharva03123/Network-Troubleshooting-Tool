
import socket
import subprocess
import platform
import re


def check_internet():
    """Check internet connectivity using HTTPS."""

    try:
        socket.create_connection(
            ("google.com", 443),
            timeout=5
        )
        return True

    except OSError:
        return False

def ping_test(host="8.8.8.8"):
    """Ping a server and calculate response time and packet loss."""

    param = "-n" if platform.system().lower() == "windows" else "-c"

    command = ["ping", param, "4", host]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=20
        )

        output = result.stdout

        # Extract response times
        times = re.findall(r"time[=<]\s*(\d+)ms", output, re.IGNORECASE)

        # Calculate packet loss
        loss_match = re.search(r"(\d+)%\s*loss", output, re.IGNORECASE)

        packet_loss = int(loss_match.group(1)) if loss_match else 100

        if times:
            average_response = round(
                sum(map(int, times)) / len(times), 2
            )
        else:
            average_response = None

        return {
            "host": host,
            "success": result.returncode == 0,
            "average_response_ms": average_response,
            "packet_loss_percent": packet_loss
        }

    except (subprocess.TimeoutExpired, OSError) as error:
        return {
            "host": host,
            "success": False,
            "average_response_ms": None,
            "packet_loss_percent": 100,
            "error": str(error)
        }
def dns_lookup(domain="google.com"):
    """Resolve a domain name into an IP address."""
    try:
        ip_address = socket.gethostbyname(domain)

        return {
            "domain": domain,
            "ip_address": ip_address,
            "success": True
        }

    except socket.gaierror as error:
        return {
            "domain": domain,
            "ip_address": None,
            "success": False,
            "error": str(error)
        }
def get_hostname():
    return socket.gethostname()

def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        return local_ip

    except socket.gaierror:
        return "Unable to detect local IP"
def generate_recommendations(internet_status, ping_result, dns_result):

    recommendations = []

    # Check Internet Connectivity
    if not internet_status:

        recommendations.append(
            "Internet connection is unavailable. "
            "Check Wi-Fi or Ethernet connectivity."
        )

    # Check Ping Result
    if not ping_result["success"]:

        recommendations.append(
            "Ping test failed. Check network connectivity "
            "and whether ICMP traffic is blocked."
        )

    # Check Packet Loss
    packet_loss = ping_result.get("packet_loss_percent")

    if packet_loss is not None and packet_loss > 0:

        recommendations.append(
            f"Packet loss detected ({packet_loss}%). "
            "Check Wi-Fi stability, router connectivity "
            "and network congestion."
        )

    # Check High Response Time
    response_time = ping_result.get("average_response_ms")

    if response_time is not None and response_time > 150:

        recommendations.append(
            f"High ping response time detected ({response_time} ms). "
            "Investigate network latency and congestion."
        )

    # Check DNS
    if not dns_result["success"]:

        recommendations.append(
            "DNS lookup failed. Check DNS configuration "
            "or try another DNS resolver."
        )

    # No Issues Found
    if not recommendations:

        recommendations.append(
            "No issues detected by the current diagnostic tests."
        )

    return recommendations
            

    
