import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if not all([server, database, username, password]):
        raise ValueError("Database environment variables are not fully set")

    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password}"
    )

    return pyodbc.connect(conn_str)


def close_connection(conn):
    if conn:
        conn.close()
