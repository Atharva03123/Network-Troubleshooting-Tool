# 🌐 Network Troubleshooting & Diagnostic Tool

A Python-based network troubleshooting application built using Streamlit and PostgreSQL. This tool helps users diagnose common network connectivity issues, monitor network performance, and maintain diagnostic history.

## 🚀 Project Overview

The Network Troubleshooting & Diagnostic Tool performs basic network tests to identify connectivity problems, check ping response time, detect packet loss, resolve DNS information, and provide rule-based troubleshooting recommendations.

It also stores diagnostic results in a PostgreSQL database, allowing users to search, filter, and export historical diagnostic records.

## ✨ Features

- **Internet Connectivity Check:** Checks internet availability using an HTTPS connection.
- **Ping Test:** Tests connectivity with a remote server.
- **Packet Loss Detection:** Identifies packet loss during ping tests.
- **Response Time Measurement:** Calculates average ping response time.
- **DNS Lookup:** Resolves domain names into IP addresses.
- **Computer Information:** Displays hostname and local IP address.
- **Troubleshooting Recommendations:** Provides basic recommendations based on diagnostic results.
- **PostgreSQL Integration:** Saves diagnostic records in a database.
- **SQL Search & Filtering:** Searches records by hostname and internet connection status.
- **CSV Export:** Downloads diagnostic history for further analysis.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| PostgreSQL | Database management |
| SQL | Data storage, retrieval and filtering |
| pg8000 | PostgreSQL database connectivity |
| Pandas | Data handling and CSV export |
| Socket | Network connectivity and DNS checks |
| Subprocess | Executing ping commands |

## 📂 Project Structure

```text
Network_Troubleshooting_Tool/
│
├── app.py
├── network_utils.py
├── database.py
├── requirements.txt
├── test_network.py
├── test_database.py
├── test_fetch.py
├── test_save.py
├── test_search.py
├── test_recommendations.py
├── .gitignore
└── README.md
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Atharva03123/Network-Troubleshooting-Tool.git
```

### 2. Navigate to the project folder

```bash
cd Network-Troubleshooting-Tool
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## 🗄️ Database Configuration

This project uses PostgreSQL to store diagnostic history.

### 1. Create a PostgreSQL database

Create a database using pgAdmin or PostgreSQL.

### 2. Create the diagnostic history table

```sql
CREATE TABLE diagnostic_history (
    id SERIAL PRIMARY KEY,
    hostname VARCHAR(100),
    local_ip VARCHAR(50),
    internet_status BOOLEAN,
    ping_status BOOLEAN,
    response_time FLOAT,
    packet_loss FLOAT,
    dns_status BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=postgres
DB_PASSWORD=your_password
```

Replace the database name and credentials with your own PostgreSQL configuration.

**Important:** Never upload your `.env` file or database credentials to GitHub.

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal.

## 🧪 Testing

The project includes separate Python test files for checking network utilities, database connectivity, saving and retrieving records, and troubleshooting recommendations.

Example:

```bash
python test_network.py
python test_search.py
python test_recommendations.py
```

## 📊 Learning Outcomes

Through this project, I gained practical experience in:

- Network connectivity troubleshooting.
- Python socket programming.
- Executing system commands using subprocess.
- PostgreSQL database integration.
- Writing SQL queries for searching and filtering.
- Building interactive applications using Streamlit.
- Managing environment variables and database credentials.
- Exporting data using Pandas.

## 👨‍💻 Author

**Atharva Shivangi**

GitHub: [Atharva03123](https://github.com/Atharva03123)

---

*This project was developed as a practical learning project focused on Python programming, network troubleshooting, database management, and IT support fundamentals.*