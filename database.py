import os
import pg8000.dbapi

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "network_diagnostics")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")


# Connect to PostgreSQL
def get_connection():

    if not DB_PASSWORD:
        raise ValueError("DB_PASSWORD is missing. Check your .env file.")

    connection = pg8000.dbapi.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    return connection

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
def search_diagnostics(hostname=None, internet_status=None):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            SELECT id, hostname, local_ip, internet_status,
                   ping_status, response_time, packet_loss,
                   dns_status, created_at
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