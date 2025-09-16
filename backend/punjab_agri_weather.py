import requests
import sys
import urllib3

# Disable SSL warnings for clean output
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class LocalAgriWeather:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.weatherbit.io/v2.0/forecast/daily"

    def get_weather(self, city=None, lat=None, lon=None, country="IN"):
        try:
            params = {
                "key": self.api_key,
                "units": "M",
                "days": 1
            }

            if city:
                params["city"] = city
                params["country"] = country
            elif lat is not None and lon is not None:
                params["lat"] = lat
                params["lon"] = lon
            else:
                return None, "⚠️ Please provide city name or latitude/longitude."

            response = requests.get(self.base_url, params=params, timeout=10, verify=False)

            # If city/coordinates invalid, return error
            if response.status_code == 400 or response.status_code == 404:
                return None, "⚠️ Location not found or invalid."

            response.raise_for_status()
            data = response.json()
            today = data["data"][0]

            temp = today.get("temp")
            precip = today.get("precip", 0)
            wind = today.get("wind_spd")
            humidity = today.get("rh")
            weather_desc = today["weather"]["description"]

            recommendations = []

            # Temperature
            if temp < 10:
                recommendations.append("⚠️ Temperature is very low – frost risk, protect crops")
            elif 10 <= temp < 15:
                recommendations.append("⚠️ Temperature is low – slow growth possible")
            elif 15 <= temp <= 30:
                recommendations.append("✅ Temperature is optimal for most crops")
            elif 30 < temp <= 35:
                recommendations.append("⚠️ Temperature is high – monitor for heat stress")
            else:
                recommendations.append("⚠️ Temperature is extreme – risk of crop damage")

            # Precipitation
            if precip > 20:
                recommendations.append("⚠️ Heavy rainfall expected – check for waterlogging and soil erosion")
            elif 10 < precip <= 20:
                recommendations.append("⚠️ Moderate rainfall – may require drainage for low-lying fields")
            elif 0 < precip <= 10:
                recommendations.append("✅ Light rainfall – beneficial for crops")
            else:
                recommendations.append("⚠️ No rain expected – irrigation may be needed")

            # Wind
            if wind > 15:
                recommendations.append("⚠️ Strong winds – protect tall or delicate crops")
            elif 10 < wind <= 15:
                recommendations.append("⚠️ Moderate winds – monitor for crop stress")
            else:
                recommendations.append("✅ Wind conditions are suitable for crops")

            # Humidity
            if humidity > 85:
                recommendations.append("⚠️ High humidity – risk of fungal diseases, monitor fields")
            elif humidity < 30:
                recommendations.append("⚠️ Low humidity – risk of dehydration, ensure irrigation")
            else:
                recommendations.append("✅ Humidity is suitable for crop growth")

            # Weather condition alerts
            desc_lower = weather_desc.lower()
            if "rain" in desc_lower:
                recommendations.append("💧 Rain expected – plan fieldwork accordingly")
            if "thunder" in desc_lower or "storm" in desc_lower:
                recommendations.append("⚠️ Thunderstorm alert – avoid outdoor labor and protect crops")
            if "snow" in desc_lower:
                recommendations.append("⚠️ Snow expected – protect sensitive crops and storage")

            output = (
                f"\n📍 Agricultural Weather in {city if city else f'{lat},{lon}'}\n"
                f"🌡 Temperature: {temp}°C\n"
                f"💧 Precipitation: {precip} mm\n"
                f"💨 Wind Speed: {wind} m/s\n"
                f"💦 Humidity: {humidity}%\n"
                f"☁️ Condition: {weather_desc}\n"
                f"📌 Recommendations:\n  - " + "\n  - ".join(recommendations)
            )

            return output, None

        except requests.exceptions.RequestException as e:
            return None, f"⚠️ Error fetching weather data: {e}"
        except KeyError:
            return None, "⚠️ Unable to parse weather data."


def main():
    api_key = "a97a776061274c90a0d5644465ce01a7"  # Free Weatherbit API key
    weather = LocalAgriWeather(api_key)

    print("🌾 Punjab Crop Weather Dashboard")
    print("=" * 50)

    while True:
        city_name = input("\nEnter your city name (Punjab) or leave blank to enter latitude/longitude: ").strip()

        if city_name:
            output, error = weather.get_weather(city=city_name)
        else:
            try:
                lat = float(input("Enter latitude: ").strip())
                lon = float(input("Enter longitude: ").strip())
                output, error = weather.get_weather(lat=lat, lon=lon)
            except ValueError:
                print("⚠️ Invalid latitude/longitude.")
                continue

        if error:
            print(error)
            print("Please try again with a valid city or coordinates.")
            continue
        else:
            print(output)
            break  # Exit after successful fetch


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        sys.exit(0)
