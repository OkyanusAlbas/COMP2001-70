import pyodbc
import os

def create_connection():
    """
    Establish and return a SQL Server connection.
    """
    try:
        conn = pyodbc.connect(
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=dist-6-505.uopnet.plymouth.ac.uk;"
            "Database=COMP2001_OAlbas;"
            "UID=OAlbas;"
            "PWD=DtlJ855;"
            "Trusted_Connection=no;",
            timeout=5
        )
        return conn
    except pyodbc.Error as e:
        print("Database connection failed:", e)
        return None


def close_connection(conn):
    if conn:
        conn.close()
