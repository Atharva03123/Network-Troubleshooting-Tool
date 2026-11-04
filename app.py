
import streamlit as st
import pandas as pd

from database import (
    fetch_diagnostics,
    save_diagnostic,
    search_diagnostics
)

from network_utils import (
    check_internet,
    ping_test,
    dns_lookup,
    get_hostname,
    get_local_ip,
    generate_recommendations
)


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Network Troubleshooting Tool",
    page_icon="🌐",
    layout="wide"
)

# Initialize session state

if "diagnostics" not in st.session_state:
    st.session_state.diagnostics = None

if "save_message" not in st.session_state:
    st.session_state.save_message = None

if "history_records" not in st.session_state:
    st.session_state.history_records = None


# --------------------------------------------------
# 2. DASHBOARD HEADER
# --------------------------------------------------

st.title("🌐 Network Troubleshooting & Diagnostic Tool")

st.write(
    "A simple tool to check network connectivity "
    "and identify common network problems."
)

st.divider()


# --------------------------------------------------
# 3. NETWORK DIAGNOSTIC OVERVIEW
# --------------------------------------------------

st.subheader("Network Diagnostic Overview")

diagnostics = st.session_state.diagnostics

col1, col2, col3 = st.columns(3)

with col1:

    if diagnostics is None:
        internet_value = "Not Checked"
    else:
        internet_value = (
            "Connected" if diagnostics["internet"]
            else "Disconnected"
        )

    st.metric("Internet Status", internet_value)


with col2:

    if diagnostics is None:
        ping_value = "Not Checked"
    else:
        ping_value = (
            "Successful" if diagnostics["ping"]["success"]
            else "Failed"
        )

    st.metric("Ping Response", ping_value)


with col3:

    if diagnostics is None:
        packet_loss_value = "Not Checked"
    else:
        loss = diagnostics["ping"]["packet_loss_percent"]

        packet_loss_value = (
            f"{loss}%" if loss is not None
            else "Unknown"
        )

    st.metric("Packet Loss", packet_loss_value)

st.divider()


# --------------------------------------------------
# 4. RUN NETWORK DIAGNOSTICS
# --------------------------------------------------

st.subheader("Run Network Diagnostics")

if st.button("🚀 Run Network Diagnostics", width="stretch"):

    with st.spinner("Running network diagnostics..."):

        internet_status = check_internet()

        ping_result = ping_test()

        dns_result = dns_lookup("google.com")

        hostname = get_hostname()

        local_ip = get_local_ip()

        # Store diagnostic results

        diagnostics_data = {
            "internet": internet_status,
            "ping": ping_result,
            "dns": dns_result,
            "hostname": hostname,
            "local_ip": local_ip
        }

        st.session_state.diagnostics = diagnostics_data

        # Save results in PostgreSQL

        try:

            save_diagnostic(
                hostname=hostname,
                local_ip=local_ip,
                internet_status=internet_status,
                ping_status=ping_result["success"],
                response_time=ping_result.get("average_response_ms"),
                packet_loss=ping_result.get("packet_loss_percent"),
                dns_status=dns_result["success"]
            )

            st.session_state.save_message = (
                "Diagnostic results saved successfully!"
            )

            # Refresh history after a new diagnostic

            st.session_state.history_records = None

        except Exception as error:

            st.session_state.save_message = (
                f"Unable to save diagnostic results: {error}"
            )

    st.rerun()


# --------------------------------------------------
# 5. DISPLAY SAVE MESSAGE
# --------------------------------------------------

if st.session_state.save_message:

    if st.session_state.save_message.startswith(
        "Diagnostic results saved"
    ):
        st.success(st.session_state.save_message)

    else:
        st.error(st.session_state.save_message)


# --------------------------------------------------
# 6. DISPLAY DIAGNOSTIC RESULTS
# --------------------------------------------------

diagnostics = st.session_state.diagnostics

if diagnostics is not None:

    st.success("Network diagnostics completed!")

    st.subheader("Diagnostic Results")

    # Internet status

    if diagnostics["internet"]:
        st.success("Internet: Connected")
    else:
        st.error("Internet: Not Connected")

    # Ping results

    ping_result = diagnostics["ping"]

    if ping_result["success"]:

        st.success("Ping: Successful")

    else:

        st.error("Ping: Failed")

        if ping_result.get("error"):
            st.write("Error:", ping_result["error"])

    st.write(
        "Average Response Time:",
        (
            f'{ping_result["average_response_ms"]} ms'
            if ping_result["average_response_ms"] is not None
            else "Unknown"
        )
    )

    loss = ping_result.get("packet_loss_percent")

    st.write(
        "Packet Loss:",
        f"{loss}%" if loss is not None else "Unknown"
    )

    # DNS results

    dns_result = diagnostics["dns"]

    if dns_result["success"]:

        st.success("DNS Lookup: Successful")

        st.write("Domain:", dns_result["domain"])

        st.write("IP Address:", dns_result["ip_address"])

    else:

        st.error("DNS Lookup: Failed")

        st.write(dns_result.get("error", "Unknown DNS error"))

    st.divider()


    # --------------------------------------------------
    # 7. COMPUTER INFORMATION
    # --------------------------------------------------

    st.subheader("Computer Information")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Computer Name",
            diagnostics["hostname"]
        )

    with col2:

        st.metric(
            "Local IP Address",
            diagnostics["local_ip"]
        )

    st.divider()


    # --------------------------------------------------
    # 8. TROUBLESHOOTING RECOMMENDATIONS
    # --------------------------------------------------

    st.subheader("🔧 Troubleshooting Recommendations")

    recommendations = generate_recommendations(
        diagnostics["internet"],
        diagnostics["ping"],
        diagnostics["dns"]
    )

    for recommendation in recommendations:
        st.info(recommendation)

    st.divider()


# --------------------------------------------------
# 9. DIAGNOSTIC HISTORY AND SQL FILTERING
# --------------------------------------------------

st.subheader("📋 Diagnostic History")

col1, col2 = st.columns(2)

with col1:

    hostname_filter = st.text_input(
        "Search by Hostname",
        placeholder="Enter hostname..."
    )

with col2:

    status_filter = st.selectbox(
        "Filter by Internet Status",
        ["All", "Connected", "Disconnected"]
    )


# Search records

if st.button("🔍 Search Records", width="stretch"):

    if status_filter == "All":
        internet_status = None

    elif status_filter == "Connected":
        internet_status = True

    else:
        internet_status = False

    try:

        records = search_diagnostics(
            hostname=hostname_filter.strip() or None,
            internet_status=internet_status
        )

        st.session_state.history_records = records

    except Exception as error:

        st.error(f"Unable to search records: {error}")

        st.session_state.history_records = []


# Load all records initially

if st.session_state.history_records is None:

    try:

        st.session_state.history_records = fetch_diagnostics()

    except Exception as error:

        st.error(f"Unable to fetch diagnostic history: {error}")

        st.session_state.history_records = []


# --------------------------------------------------
# 10. DISPLAY HISTORY AND CSV EXPORT
# --------------------------------------------------

records = st.session_state.history_records

columns = [
    "ID",
    "Hostname",
    "Local IP",
    "Internet Status",
    "Ping Status",
    "Response Time (ms)",
    "Packet Loss (%)",
    "DNS Status",
    "Created At"
]

if records:

    history_df = pd.DataFrame(
        records,
        columns=columns
    )

    st.success(
        f"{len(history_df)} diagnostic records found."
    )

    st.dataframe(
        history_df,
        width="stretch",
        hide_index=True
    )

    # CSV Export

    csv_data = history_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Diagnostic History (CSV)",
        data=csv_data,
        file_name="network_diagnostic_history.csv",
        mime="text/csv",
        width="stretch"
    )

else:

    st.warning("No matching diagnostic records found.")

st.divider()

st.caption(
    "Network Troubleshooting & Diagnostic Tool | "
    "Python • Streamlit • PostgreSQL"
)
