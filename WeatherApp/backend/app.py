import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config

# Initialize Flask App
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# Validate config
Config.validate()

OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    if not Config.OPENWEATHER_API_KEY or Config.OPENWEATHER_API_KEY == "your_api_key_here":
        return jsonify({
            "status": "warning",
            "message": "OpenWeatherMap API Key is not set or using default placeholder."
        }), 200
    return jsonify({"status": "healthy", "message": "Backend server is running."}), 200

@app.route('/weather/<city>', methods=['GET'])
def get_current_weather(city):
    """
    Fetch current weather data for a given city.
    Returns details like temperature, feels like, humidity, etc.
    """
    if not Config.OPENWEATHER_API_KEY or Config.OPENWEATHER_API_KEY == "your_api_key_here":
        return jsonify({"error": "OpenWeatherMap API Key is not configured on the backend. Please add it to your .env file."}), 500

    params = {
        "q": city,
        "appid": Config.OPENWEATHER_API_KEY,
        "units": "metric"  # Defaulting to metric on backend, unit conversion handled on frontend
    }

    try:
        response = requests.get(f"{OPENWEATHER_BASE_URL}/weather", params=params, timeout=10)
        
        if response.status_code == 404:
            return jsonify({"error": f"City '{city}' not found."}), 404
        elif response.status_code != 200:
            return jsonify({"error": f"Failed to fetch weather data from OpenWeatherMap API. (Status Code: {response.status_code})"}), response.status_code

        data = response.json()
        
        # Format current weather response according to requirements and UI needs
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
            "visibility": data.get("visibility", 0) / 1000.0,  # Convert meters to km
            "sunrise": data.get("sys", {}).get("sunrise"),
            "sunset": data.get("sys", {}).get("sunset")
        }
        return jsonify(formatted_weather), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Network error or request timeout: {str(e)}"}), 503
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/forecast/<city>', methods=['GET'])
def get_forecast(city):
    """
    Fetch 5-day weather forecast (3-hour intervals) for a given city.
    """
    if not Config.OPENWEATHER_API_KEY or Config.OPENWEATHER_API_KEY == "your_api_key_here":
        return jsonify({"error": "OpenWeatherMap API Key is not configured on the backend. Please add it to your .env file."}), 500

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
            return jsonify({"error": f"Failed to fetch forecast data from OpenWeatherMap API. (Status Code: {response.status_code})"}), response.status_code

        data = response.json()
        forecast_list = data.get("list", [])
        
        # Format the 5-day forecast response
        formatted_forecast = []
        for item in forecast_list:
            formatted_item = {
                "date": item.get("dt_txt"),
                "temp": item.get("main", {}).get("temp"),
                "humidity": item.get("main", {}).get("humidity"),
                "wind_speed": item.get("wind", {}).get("speed"),
                "description": item.get("weather", [{}])[0].get("description", "N/A").title(),
                "icon": item.get("weather", [{}])[0].get("icon", ""),
                "temp_min": item.get("main", {}).get("temp_min"),
                "temp_max": item.get("main", {}).get("temp_max")
            }
            formatted_forecast.append(formatted_item)
            
        return jsonify(formatted_forecast), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Network error or request timeout: {str(e)}"}), 503
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    # Start Flask API
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=Config.FLASK_ENV == "development")
