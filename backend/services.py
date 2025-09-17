# services.py
import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

# Get API keys from environment variables
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

def get_weather_for_state(state):
    """Fetches the current weather for a given state."""
    api_url = "http://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": state,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric" # for Celsius
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()
        
        weather_description = data['weather'][0]['description'].capitalize()
        temp = data['main']['temp']
        
        return f"Weather in {state}: {weather_description}. Temp: {temp}°C."
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def send_sms(to_number, body):
    """Sends a text message to a specified number."""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            to=to_number,
            from_=TWILIO_PHONE_NUMBER,
            body=body
        )
        print(f"SMS sent successfully! Message ID: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")