import requests
import sys

class PunjabWeather:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city, state="Punjab", country="IN"):
        try:
            params = {
                "q": f"{city},{state},{country}",
                "appid": self.api_key,
                "units": "metric",
                "lang": "en"
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Parse response
            city_name = data.get("name", "Unknown")
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            weather_desc = data["weather"][0]["description"].capitalize()
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            return (
                f"\n📍 Weather in {city_name}, Punjab\n"
                f"🌡 Temperature: {temp}°C (Feels like {feels_like}°C)\n"
                f"☁️ Condition: {weather_desc}\n"
                f"💧 Humidity: {humidity}%\n"
                f"🌬 Wind Speed: {wind_speed} m/s\n"
            )

        except requests.exceptions.RequestException as e:
            return f"Error fetching weather data: {e}"
        except KeyError:
            return "⚠️ Unable to parse weather data."


def main():
    api_key = "30513d5baa2e66847a45cbe0f65ef6e4"  # <-- Your API key here
    weather = PunjabWeather(api_key)

    punjab_cities = [
        "Chandigarh", "Ludhiana", "Amritsar",
        "Jalandhar", "Patiala", "Bathinda",
        "Mohali", "Pathankot"
    ]

    print("🌍 Punjab Weather Dashboard")
    print("=" * 50)
    print("Select a city:")
    for i, city in enumerate(punjab_cities, start=1):
        print(f"{i}. {city}")
    print(f"{len(punjab_cities)+1}. Enter custom city name")

    try:
        user_input = input("\nEnter your choice (1-9 or city name): ").strip()

        # If input is a number → handle by index
        if user_input.isdigit():
            choice = int(user_input)

            if 1 <= choice <= len(punjab_cities):
                selected_city = punjab_cities[choice - 1]
                print(f"\nFetching weather for {selected_city}...")
                print(weather.get_weather(selected_city))
            elif choice == len(punjab_cities) + 1:
                custom_city = input("Enter city name: ").strip()
                print(f"\nFetching weather for {custom_city}...")
                print(weather.get_weather(custom_city))
            else:
                print("⚠️ Invalid choice!")

        else:
            # Treat input directly as a city name
            print(f"\nFetching weather for {user_input}...")
            print(weather.get_weather(user_input))

    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        sys.exit(0)


if __name__ == "__main__":
    main()
