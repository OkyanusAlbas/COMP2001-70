from app.connection import create_connection, close_connection

def test_db_connection():
    print("🔍 Testing database connection...")
    conn = create_connection()

    if conn is None:
        print("⚠️ Database connection failed (expected if VPN is OFF)")
        return

    print("✅ Database connection test passed")
    close_connection(conn)


if __name__ == "__main__":
    test_db_connection()
