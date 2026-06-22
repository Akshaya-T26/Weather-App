# Weather Information Web Application

A modern, responsive, and feature-rich weather dashboard built using a **Flask REST API (Backend)** and a **Streamlit Dashboard (Frontend)**, integrated with the **OpenWeatherMap API**.

---

##  Key Features
- **City Search**: Instant search for any city globally with active loading states and invalid city validation.
- **Detailed Current Conditions**: Displays temperature, feels-like temperature, humidity, wind speed, pressure, visibility, sunrise, and sunset times in clean metrics cards.
- **5-Day Forecast Grid**: Grid displaying daily forecasts including minimum/maximum temperature, weather description, and official OpenWeatherMap icons.
- **Interactive Plotly Charts**: Historical line charts with markers and tooltips tracking temperature, humidity, and wind speed trends over the 5-day span.
- **Imperial / Metric Unit Switcher**: Easily toggle temperatures between Celsius (°C) and Fahrenheit (°F).
- **Search History**: Sidebar list of recent searches for quick re-navigation.
- **CSV Data Download**: Export the raw 5-day forecast data to a CSV file.

---

##  Project Structure

```text
WeatherApp/
│
├── backend/
│   ├── app.py             # Flask application entry point and routes
│   ├── config.py          # Configuration manager utilizing dotenv
│   └── requirements.txt   # Backend dependencies
│
├── frontend/
│   ├── streamlit_app.py   # Main Streamlit dashboard code with styling
│   ├── utils.py           # Helper API client and formatting utilities
│   └── requirements.txt   # Frontend dependencies
│
├── .env                   # Configuration file (API keys & ports)
├── .env.example           # Reference configuration template
├── README.md              # Installation and usage instructions
└── requirements.txt       # Combined project requirements file
```

---

##  Prerequisites

1. **Python 3.8+** installed.
2. **OpenWeatherMap API Key**:
   - Go to [OpenWeatherMap](https://openweathermap.org/) and sign up for a free account.
   - Generate an API key from your profile dashboard under **API keys**.

---

##  Setup & Installation

### 1. Clone or Copy the Project
Ensure all files are placed in your working directory.

### 2. Configure Environment Variables
Copy `.env.example` to a new file named `.env` and insert your API key:
```bash
# Rename the example config
cp .env.example .env
```
Open `.env` in a text editor and update:
```env
OPENWEATHER_API_KEY=your_actual_api_key_here
```

### 3. Install Dependencies
It is highly recommended to use a virtual environment.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install all dependencies (Backend + Frontend)
pip install -r requirements.txt
```

---

##  Running the Application

To run the application, you need to start **both** the backend Flask API and the Streamlit frontend.

### Step 1: Start the Backend (Flask API)
Open a terminal window, activate your environment, and run:
```bash
# From the root directory:
python backend/app.py
```
The backend REST API will start running at `http://127.0.0.1:5000`. You can visit `http://127.0.0.1:5000/health` to verify it is up.

### Step 2: Start the Frontend (Streamlit Dashboard)
Open a **new** terminal window, activate your environment, and run:
```bash
# From the root directory:
streamlit run frontend/streamlit_app.py
```
Streamlit will automatically open the dashboard in your default browser at `http://localhost:8501`.

---

##  API Endpoints (Flask Backend)

### Current Weather Endpoint
- **URL**: `/weather/<city>`
- **Method**: `GET`
- **Response**:
```json
{
  "city": "London",
  "country": "GB",
  "temperature": 15.5,
  "feels_like": 14.8,
  "humidity": 72,
  "wind_speed": 4.1,
  "pressure": 1012,
  "description": "Light Rain",
  "icon": "10d",
  "visibility": 10.0,
  "sunrise": 1623992384,
  "sunset": 1624047482
}
```

### 5-Day Forecast Endpoint
- **URL**: `/forecast/<city>`
- **Method**: `GET`
- **Response**:
```json
[
  {
    "date": "2026-06-20 12:00:00",
    "temp": 15.5,
    "humidity": 72,
    "wind_speed": 4.1,
    "description": "Light Rain",
    "icon": "10d",
    "temp_min": 14.0,
    "temp_max": 16.0
  }
]
```
