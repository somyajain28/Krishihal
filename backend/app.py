# app.py
from flask import Flask, request, jsonify
import pymysql.cursors
from dotenv import load_dotenv
import os
from flask_cors import CORS
# Import the functions from your services.py file
from services import get_weather_for_state, send_sms

# Load environment variables from a .env file
load_dotenv()
# app.py
# ... after your load_dotenv() call ...

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

print("Checking credentials:")
print(f"SID: {TWILIO_ACCOUNT_SID}")
print(f"Token: {TWILIO_AUTH_TOKEN}")
print("-" * 20)
# Initialize the Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Database credentials from your .env file
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': os.getenv('DB_PASSWORD'),
    'database': 'krishihal_db'
}

@app.route('/submit-data', methods=['POST'])
def register_farmer():
    connection = None
    try:
        data = request.get_json()
        full_name = data.get('fullName')
        mobile_number = data.get('mobileNumber')
        state = data.get('state')
        crop_type = data.get('cropType')
        address = data.get('address')
        
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        insert_query = """
            INSERT INTO farmers (full_name, mobile_number, state, crop_type, address)
            VALUES (%s, %s, %s, %s, %s)
        """
        farmer_data = (full_name, mobile_number, state, crop_type, address)
        
        cursor.execute(insert_query, farmer_data)
        connection.commit()

        if cursor.rowcount > 0:
            # Get weather and send SMS after successful registration
            weather_info = get_weather_for_state(state)
            if weather_info:
                send_sms(mobile_number, weather_info)
            
            return jsonify({'message': 'Farmer registered successfully!'}), 200
        else:
            return jsonify({'error': 'Registration failed'}), 400

    except pymysql.MySQLError as err:
        print(f"Database error: {err}")
        return jsonify({'error': f'Database error: {err}'}), 500
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
        
    finally:
        if connection and connection.open:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)