import mysql.connector
from mysql.connector import Error
from database import get_db_connection

def update_database():
    try:
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            
            # 1. Add is_active column to users if not exists
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT FALSE")
                print("Column 'is_active' added to users table.")
            except Error as err:
                if err.errno == 1060: # Duplicate column name
                    print("Column 'is_active' already exists.")
                else:
                    print(f"Error adding column: {err}")

            # 2. Create otp_codes table
            create_otp_table = """
            CREATE TABLE IF NOT EXISTS otp_codes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(100) NOT NULL,
                otp_code VARCHAR(10) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + INTERVAL 10 MINUTE)
            )
            """
            cursor.execute(create_otp_table)
            print("Table 'otp_codes' checked/created.")
            
            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_database()
