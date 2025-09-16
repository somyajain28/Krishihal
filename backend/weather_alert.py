# We're importing two essential tools (called libraries) that we need.
# 'requests' helps our program ask for information from websites.
# 'twilio' helps our program send text messages.
import requests
from twilio.rest import Client

# --- IMPORTANT: Put your unique secret codes here ---
# This is like a special key from the weather website (OpenWeatherMap) to let you use their service.
WEATHER_API_KEY = "30513d5baa2e66847a45cbe0f65ef6e4"
# This is a special ID for your Twilio account, kind of like your account number.
TWILIO_ACCOUNT_SID = "AC07f7ae57e78d4a2903bc2865ab57042c"
# This is a secret password for your Twilio account.
TWILIO_AUTH_TOKEN = "d49c359eccc21cc5e1fcd5bb494548cd"
# This is the phone number from which the text message will be sent.
TWILIO_PHONE_NUMBER = "+18392755675"
# This is the phone number that will receive the text message.
RECIPIENT_NUMBER = "+919572888593"


# This is a function that does one main job: getting the weather.
def get_weather(city_name):
    # This is the internet address we'll visit to get the weather information.
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    # These are the instructions we send along with our request.
    params = {
        'q': city_name,  # 'q' stands for query; we're asking about this city.
        'appid': WEATHER_API_KEY,  # We show them our special key.
        'units': 'metric'  # We ask for temperature in Celsius.
    }
    
    # We use 'try' to handle potential problems. If something goes wrong, the code inside 'except' will run instead.
    try:
        # This line asks the weather website for the information we want.
        response = requests.get(base_url, params=params)
        # This line checks if we got a good response. If not (like an error), it stops.
        response.raise_for_status() 
        # This line takes the information from the website and turns it into something Python can understand.
        weather_data = response.json()
        
        # We're now picking out the specific pieces of information we want from the weather data.
        description = weather_data['weather'][0]['description'].capitalize()
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        
        # We put all the pieces together into a nice sentence.
        message = (
            f"Weather in {city_name}: {description}. "
            f"Temp: {temp}°C (feels like {feels_like}°C). "
            f"Humidity: {humidity}%. Wind: {wind_speed} m/s."
        )
        
        # This sends the final weather message back to where the function was called.
        return message
    
    except requests.exceptions.RequestException:
        # If there's a problem with the internet, this message is sent instead.
        return "Sorry, I couldn't get the weather data. Please check your internet connection."
    except KeyError:
        # If the city name you typed isn't found, this message is sent instead.
        return "That location wasn't found. Please check the spelling."


# This is a function for sending a text message.
def send_sms(body):
    # Again, we use 'try' to handle possible errors.
    try:
        # We connect to the Twilio service using our account ID and password.
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        # This line tells Twilio to send a new message.
        message = client.messages.create(
            to=RECIPIENT_NUMBER,  # Who the message goes to.
            from_=TWILIO_PHONE_NUMBER,  # Who the message is from.
            body=body  # The actual message content (the weather report).
        )
        # If it works, we print a success message.
        print(f"SMS sent successfully! Message ID: {message.sid}")
    except Exception as e:
        # If something goes wrong while sending the text, we print an error message.
        print(f"Error sending SMS: {e}")


# This is the main part of the program that gets everything started.
def main():
    # We ask the user to type in a city name and save it.
    city = input("Enter a city in Punjab: ")
    
    # We call our 'get_weather' function to get the weather information.
    weather_info = get_weather(city)
    
    # This line checks if the message we got back has an error in it.
    if "Error" in weather_info or "Location not found" in weather_info:
        # If there's an error, we just print the message on the screen.
        print(weather_info)
    else:
        # If there's no error, we send the weather report as a text message.
        send_sms(weather_info)


# This line makes sure our program starts running from the 'main' function.
if __name__ == "__main__":
    main()
