import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

db_config = {
    'user': 'root',
    'password': os.getenv('DB_PASSWORD'),
    'host': '127.0.0.1',
    'database': 'krishihal_db'
}

print("Attempting to connect to the database...")
try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print("Success! The database connection works.")
    else:
        print("Connection failed, but no exception was raised.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    
finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed.")