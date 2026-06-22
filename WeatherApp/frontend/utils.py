import requests
from datetime import datetime

# Flask Backend API URL
BACKEND_BASE_URL = "https://weather-app-qqmp.onrender.com"

def get_backend_url():
    """Returns the base URL of the backend API."""
    return BACKEND_BASE_URL

def fetch_weather(city: str):
    """
    Fetch current weather from Flask backend API.
    """
    try:
        response = requests.get(f"{BACKEND_BASE_URL}/weather/{city}", timeout=10)
        if response.status_code == 200:
            return response.json(), None
        else:
            # Try to parse error from JSON response
            try:
                error_msg = response.json().get("error", "Failed to retrieve data.")
            except Exception:
                error_msg = f"HTTP Error {response.status_code}"
            return None, error_msg
    except requests.exceptions.ConnectionError:
        return None, "Unable to connect to Flask backend API. Please make sure the backend is running."
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"

def fetch_forecast(city: str):
    """
    Fetch 5-day forecast from Flask backend API.
    """
    try:
        response = requests.get(f"{BACKEND_BASE_URL}/forecast/{city}", timeout=10)
        if response.status_code == 200:
            return response.json(), None
        else:
            try:
                error_msg = response.json().get("error", "Failed to retrieve data.")
            except Exception:
                error_msg = f"HTTP Error {response.status_code}"
            return None, error_msg
    except requests.exceptions.ConnectionError:
        return None, "Unable to connect to Flask backend API. Please make sure the backend is running."
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"

def c_to_f(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

def format_temp(temp: float, unit: str) -> str:
    """Format temperature based on unit selected ('C' or 'F')."""
    if temp is None:
        return "N/A"
    if unit == "F":
        return f"{c_to_f(temp):.1f}°F"
    return f"{temp:.1f}°C"

def format_timestamp(timestamp: int, timezone_offset: int = 0) -> str:
    """Convert Unix timestamp to readable HH:MM format."""
    if not timestamp:
        return "N/A"
    # Note: timestamp is in UTC.
    try:
        dt = datetime.utcfromtimestamp(timestamp + timezone_offset)
        return dt.strftime("%I:%M %p")
    except Exception:
        # Fallback to local time if math fails
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%I:%M %p")

def get_weather_icon_url(icon_code: str) -> str:
    """Get URL for OpenWeatherMap icons."""
    if not icon_code:
        return ""
    return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
