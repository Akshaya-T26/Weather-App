import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Validate config
Config.validate()

OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"


# ✅ HOME ROUTE (FIX for "Not Found")
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Weather API is running successfully 🚀",
        "status": "active",
        "endpoints": {
            "health": "/health",
            "current_weather": "/weather/<city>",
            "forecast": "/forecast/<city>"
        }
    }), 200


@app.route('/health', methods=['GET'])
def health_check():
    if not Config.OPENWEATHER_API_KEY or Config.OPENWEATHER_API_KEY == "your_api_key_here":
        return jsonify({
            "status": "warning",
            "message": "OpenWeatherMap API Key is not set or using default placeholder."
        }), 200
    return jsonify({"status": "healthy", "message": "Backend server is running."}), 200


@app.route('/weather/<city>', methods=['GET'])
def get_current_weather(city):

    if not Config.OPENWEATHER_API_KEY or Config.OPENWEATHER_API_KEY == "your_api_key_here":
        return jsonify({"error": "API Key not configured"}), 500

    params = {
        "q": city,
        "appid": Config.OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(f"{OPENWEATHER_BASE_URL}/weather", params=params, timeout=10)

        if response.status_code == 404:
            return jsonify({"error": f"City '{city}' not found."}), 404
        elif response.status_code != 200:
            return jsonify({"error": "Failed to fetch weather data"}), response.status_code

        data = response.json()

        formatted_weather = {
            "city": data.get("name", city),
            "country": data.get("sys", {}).get("country", ""),
            "temperature": data.get("main", {}).get("temp"),
            "feels_like": data.get("main", {}).get("feels_like"),
            "humidity": data.get("main", {}).get("humidity"),
            "wind_speed": data.get("wind", {}).get("speed"),
            "pressure": data.get("main", {}).get("pressure"),
            "description": data.get("weather", [{}])[0].get("description", "N/A").title(),
            "icon": data.get("weather", [{}])[0].get("icon", ""),
            "visibility": data.get("visibility", 0) / 1000.0,
            "sunrise": data.get("sys", {}).get("sunrise"),
            "sunset": data.get("sys", {}).get("sunset")
        }

        return jsonify(formatted_weather), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/forecast/<city>', methods=['GET'])
def get_forecast(city):

    if not Config.OPENWEATHER_API_KEY or Config.OPENWEATHER_API_KEY == "your_api_key_here":
        return jsonify({"error": "API Key not configured"}), 500

    params = {
        "q": city,
        "appid": Config.OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(f"{OPENWEATHER_BASE_URL}/forecast", params=params, timeout=10)

        if response.status_code == 404:
            return jsonify({"error": f"City '{city}' not found."}), 404
        elif response.status_code != 200:
            return jsonify({"error": "Failed to fetch forecast data"}), response.status_code

        data = response.json()

        forecast_list = []
        for item in data.get("list", []):
            forecast_list.append({
                "date": item.get("dt_txt"),
                "temp": item.get("main", {}).get("temp"),
                "humidity": item.get("main", {}).get("humidity"),
                "wind_speed": item.get("wind", {}).get("speed"),
                "description": item.get("weather", [{}])[0].get("description", "N/A").title(),
                "icon": item.get("weather", [{}])[0].get("icon", ""),
                "temp_min": item.get("main", {}).get("temp_min"),
                "temp_max": item.get("main", {}).get("temp_max")
            })

        return jsonify(forecast_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=Config.FLASK_ENV == "development")
