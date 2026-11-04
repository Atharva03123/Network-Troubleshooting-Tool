from network_utils import generate_recommendations

internet_status = True

ping_result = {
    "success": True,
    "average_response_ms": 200,
    "packet_loss_percent": 25
}

dns_result = {
    "success": True
}

recommendations = generate_recommendations(
    internet_status,
    ping_result,
    dns_result
)

print("Troubleshooting Recommendations:")

for recommendation in recommendations:
    print("-", recommendation)
    