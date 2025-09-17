import pymysql.cursors
from dotenv import load_dotenv
import os

load_dotenv()

try:
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password=os.getenv('DB_PASSWORD'),
        database='krishihal_db',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Success! The PyMySQL connection works.")
    connection.close()

except pymysql.MySQLError as err:
    print(f"Error: {err}")