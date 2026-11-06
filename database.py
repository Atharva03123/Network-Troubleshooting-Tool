
import os
import ssl
import pg8000.dbapi
import streamlit as st

from dotenv import load_dotenv

# Load local environment variables
load_dotenv()


# Read configuration from Streamlit Cloud Secrets
# or local .env file
def get_config(key, default=None):
    try:
        value = st.secrets.get(key)
        if value:
            return value
    except Exception:
        pass

    return os.getenv(key, default)


# Database configuration
DB_HOST = get_config("DB_HOST", "localhost")
DB_PORT = int(get_config("DB_PORT", "5432"))
DB_NAME = get_config("DB_NAME", "network_diagnostics")
DB_USER = get_config("DB_USER", "postgres")
DB_PASSWORD = get_config("DB_PASSWORD")


# Connect to Neon PostgreSQL
def get_connection():

    if not DB_PASSWORD:
        raise ValueError(
            "DB_PASSWORD is missing. Check your .env file or Streamlit Secrets."
        )

    connection = pg8000.dbapi.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        ssl_context=ssl.create_default_context()
    )

    return connection


# Save diagnostic record
def save_diagnostic(
    hostname,
    local_ip,
    internet_status,
    ping_status,
    response_time,
    packet_loss,
    dns_status
):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO diagnostic_history (
                hostname,
                local_ip,
                internet_status,
                ping_status,
                response_time,
                packet_loss,
                dns_status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            hostname,
            local_ip,
            internet_status,
            ping_status,
            response_time,
            packet_loss,
            dns_status
        )

        cursor.execute(query, values)
        connection.commit()

        return True

    finally:
        cursor.close()
        connection.close()


# Fetch all diagnostic records
def fetch_diagnostics():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                id,
                hostname,
                local_ip,
                internet_status,
                ping_status,
                response_time,
                packet_loss,
                dns_status,
                created_at
            FROM diagnostic_history
            ORDER BY created_at DESC
        """

        cursor.execute(query)
        records = cursor.fetchall()

        return records

    finally:
        cursor.close()
        connection.close()


# Search diagnostic records
def search_diagnostics(hostname=None, internet_status=None):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                id,
                hostname,
                local_ip,
                internet_status,
                ping_status,
                response_time,
                packet_loss,
                dns_status,
                created_at
            FROM diagnostic_history
            WHERE 1=1
        """

        values = []

        if hostname:
            query += " AND hostname ILIKE %s"
            values.append(f"%{hostname}%")

        if internet_status is not None:
            query += " AND internet_status = %s"
            values.append(internet_status)

        query += " ORDER BY created_at DESC"

        cursor.execute(query, tuple(values))
        records = cursor.fetchall()

        return records

    finally:
        cursor.close()
        connection.close()
