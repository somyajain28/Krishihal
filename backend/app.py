# app.py
from flask import Flask, request, jsonify
import pymysql.cursors
from dotenv import load_dotenv
import os
from flask_cors import CORS

# Load environment variables from a .env file
load_dotenv()

# Initialize the Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Database credentials from your .env file
db_config = {
    'user': 'root',
    'password': os.getenv('DB_PASSWORD'),
    'host': '127.0.0.1',
    'database': 'krishihal_db'
}

# A simple GET route to confirm the server is running
@app.route('/')
def home():
    return "The backend server is running!"

@app.route('/submit-data', methods=['POST'])
def register_farmer():
    connection = None
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        # Get the JSON data from the frontend
        data = request.get_json()
        full_name = data.get('fullName')
        mobile_number = data.get('mobileNumber')
        state = data.get('state')
        crop_type = data.get('cropType')
        address = data.get('address')
        

        # SQL query to insert all form fields
        insert_query = """
            INSERT INTO farmers (full_name, mobile_number, state, crop_type, address)
            VALUES (%s, %s, %s, %s, %s)
        """
        farmer_data = (full_name, mobile_number, state, crop_type, address)
        
        cursor.execute(insert_query, farmer_data)
        connection.commit()

        # Check if the row was successfully inserted
        if cursor.rowcount > 0:
            return jsonify({'message': 'Farmer registered successfully!'}), 200
        else:
            return jsonify({'error': 'Registration failed'}), 400

    except pymysql.MySQLError as err:
        # Catch specific MySQL errors and return them to the frontend
        print(f"Database error: {err}")
        return jsonify({'error': f'Database error: {err.msg}'}), 500
        
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
        
    finally:
        # Always close the connection and cursor to free up resources
        if connection and connection.open:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)