import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import utils

# Set page configurations
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS for premium look and feel (cards, styling, gradients)
st.markdown("""
<style>
    /* Main container styling */
    .reportview-container {
        background: #f0f2f6;
    }
    
    /* Title style */
    .title-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .title-container h1 {
        margin: 0;
        font-family: 'Outfit', 'Segoe UI', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
    }
    .title-container p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }

    /* Metric card design */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #eef2f5;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        text-align: center;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }
    .metric-title {
        color: #64748b;
        font-size: 0.9rem;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        color: #1e293b;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .metric-sub {
        color: #94a3b8;
        font-size: 0.8rem;
        margin-top: 0.25rem;
    }

    /* Weather card main */
    .weather-main-card {
        background: linear-gradient(135deg, #3a7bd5 0%, #3a6073 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .weather-main-card h2 {
        margin: 0 0 0.5rem 0;
        font-size: 2.2rem;
        font-weight: 600;
    }
    .weather-main-card .temp-val {
        font-size: 4rem;
        font-weight: 800;
        margin: 1rem 0;
    }
    
    /* Forecast Card Grid */
    .forecast-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #f1f5f9;
        margin: 0.2rem;
    }
    .forecast-date {
        font-weight: 600;
        color: #334155;
        font-size: 0.95rem;
    }
    .forecast-temp {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0.5rem 0;
    }
    .forecast-desc {
        color: #64748b;
        font-size: 0.8rem;
        text-transform: capitalize;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'search_history' not in st.session_state:
    st.session_state['search_history'] = []
if 'current_city' not in st.session_state:
    st.session_state['current_city'] = "London"
if 'last_refreshed' not in st.session_state:
    st.session_state['last_refreshed'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Header Section
st.markdown("""
    <div class="title-container">
        <h1>☀️ Weather Insights Dashboard</h1>
        <p>Real-time current weather & 5-day predictive forecasts</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar implementation
st.sidebar.image("https://openweathermap.org/img/wn/02d@2x.png", width=100)
st.sidebar.title("Configuration")

# City Search Box
search_input = st.sidebar.text_input("Enter City Name:", value=st.session_state['current_city'])

# Unit Settings
unit_choice = st.sidebar.radio("Temperature Unit:", options=["Celsius (°C)", "Fahrenheit (°F)"], index=0)
unit = "C" if "Celsius" in unit_choice else "F"

# Buttons: Search and Refresh
col_search, col_refresh = st.sidebar.columns(2)
with col_search:
    search_clicked = st.button("Search", use_container_width=True)
with col_refresh:
    refresh_clicked = st.button("🔄 Refresh", use_container_width=True)

if search_clicked and search_input:
    st.session_state['current_city'] = search_input.strip()
    if st.session_state['current_city'] not in st.session_state['search_history']:
        st.session_state['search_history'].insert(0, st.session_state['current_city'])
        st.session_state['search_history'] = st.session_state['search_history'][:5] # Limit history to last 5
    st.session_state['last_refreshed'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if refresh_clicked:
    st.session_state['last_refreshed'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Search History
if st.session_state['search_history']:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Recent Searches")
    for hist_city in st.session_state['search_history']:
        if st.sidebar.button(hist_city, key=f"hist_{hist_city}", use_container_width=True):
            st.session_state['current_city'] = hist_city
            st.session_state['last_refreshed'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.rerun()

# Clear History
if st.session_state['search_history'] and st.sidebar.button("Clear History", use_container_width=True):
    st.session_state['search_history'] = []
    st.rerun()

# Fetch Weather Data
city = st.session_state['current_city']

with st.spinner(f"Fetching weather details for {city}..."):
    weather_data, weather_err = utils.fetch_weather(city)
    forecast_data, forecast_err = utils.fetch_forecast(city)

# Render Dashboard
if weather_err or forecast_err:
    st.error(f"⚠️ Error: {weather_err or forecast_err}")
    st.info("💡 Please verify the Flask backend server is running and that you have entered a valid city name.")
else:
    # ------------------ CURRENT WEATHER ------------------
    col_main, col_metrics = st.columns([1, 2])

    with col_main:
        icon_url = utils.get_weather_icon_url(weather_data.get("icon"))
        temp_str = utils.format_temp(weather_data.get("temperature"), unit)
        feels_like_str = utils.format_temp(weather_data.get("feels_like"), unit)
        
        st.markdown(f"""
            <div class="weather-main-card">
                <h2>{weather_data.get('city')}, {weather_data.get('country')}</h2>
                <p style="font-size:1.1rem; margin-top:-0.5rem; opacity:0.8;">Current Conditions</p>
                <img src="{icon_url}" style="width:120px; filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.2));" />
                <div class="temp-val">{temp_str}</div>
                <p style="font-size:1.4rem; font-weight:600; margin:0;">{weather_data.get('description')}</p>
                <p style="font-size:0.95rem; margin-top:0.5rem; opacity:0.9;">Feels Like: {feels_like_str}</p>
            </div>
        """, unsafe_allow_html=True)

    with col_metrics:
        # 2x3 Grid for metrics
        m_row1_col1, m_row1_col2, m_row1_col3 = st.columns(3)
        m_row2_col1, m_row2_col2, m_row2_col3 = st.columns(3)

        # Humidity
        m_row1_col1.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">💧 Humidity</div>
                <div class="metric-value">{weather_data.get('humidity')}%</div>
                <div class="metric-sub">Moisture level</div>
            </div>
        """, unsafe_allow_html=True)

        # Wind Speed
        m_row1_col2.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">💨 Wind Speed</div>
                <div class="metric-value">{weather_data.get('wind_speed')} m/s</div>
                <div class="metric-sub">Directional velocity</div>
            </div>
        """, unsafe_allow_html=True)

        # Pressure
        m_row1_col3.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🎈 Pressure</div>
                <div class="metric-value">{weather_data.get('pressure')} hPa</div>
                <div class="metric-sub">Atmospheric pressure</div>
            </div>
        """, unsafe_allow_html=True)

        # Visibility
        m_row2_col1.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">👁️ Visibility</div>
                <div class="metric-value">{weather_data.get('visibility'):.1f} km</div>
                <div class="metric-sub">Clear sight range</div>
            </div>
        """, unsafe_allow_html=True)

        # Sunrise
        sunrise_time = utils.format_timestamp(weather_data.get("sunrise"))
        m_row2_col2.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🌅 Sunrise</div>
                <div class="metric-value">{sunrise_time}</div>
                <div class="metric-sub">Dawn starts</div>
            </div>
        """, unsafe_allow_html=True)

        # Sunset
        sunset_time = utils.format_timestamp(weather_data.get("sunset"))
        m_row2_col3.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🌇 Sunset</div>
                <div class="metric-value">{sunset_time}</div>
                <div class="metric-sub">Dusk ends</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------ 5-DAY FORECAST ------------------
    st.subheader("🗓️ 5-Day Weather Forecast")
    
    # Process forecast data (Get 1 sample per day at 12:00 PM to show in grid cards)
    df_forecast = pd.DataFrame(forecast_data)
    df_forecast['datetime'] = pd.to_datetime(df_forecast['date'])
    
    # Filter to select 1 data point per day (approx 12:00 PM)
    df_daily = df_forecast[df_forecast['datetime'].dt.hour == 12].copy()
    if df_daily.empty:
        # Fallback to daily uniques if 12:00 is missing
        df_forecast['day'] = df_forecast['datetime'].dt.date
        df_daily = df_forecast.groupby('day').first().reset_index()

    cols_forecast = st.columns(len(df_daily))
    for i, (_, row) in enumerate(df_daily.iterrows()):
        date_obj = pd.to_datetime(row['date'])
        day_name = date_obj.strftime("%A")
        date_str = date_obj.strftime("%b %d")
        icon_f_url = utils.get_weather_icon_url(row['icon'])
        temp_val = utils.format_temp(row['temp'], unit)
        min_max_temp = f"Min: {utils.format_temp(row['temp_min'], unit)} / Max: {utils.format_temp(row['temp_max'], unit)}"
        
        with cols_forecast[i]:
            st.markdown(f"""
                <div class="forecast-card">
                    <div class="forecast-date">{day_name}</div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">{date_str}</div>
                    <img src="{icon_f_url}" style="width: 60px;" />
                    <div class="forecast-temp">{temp_val}</div>
                    <div style="font-size: 0.75rem; color: #64748b; font-weight: 500; margin-bottom: 0.5rem;">{min_max_temp}</div>
                    <div class="forecast-desc">{row['description']}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------ INTERACTIVE CHARTS ------------------
    st.subheader("📈 Weather Trends (Next 5 Days)")
    
    # Format Temperature in selected unit for chart
    if unit == "F":
        df_forecast['temp_chart'] = df_forecast['temp'].apply(utils.c_to_f)
        y_title = "Temperature (°F)"
    else:
        df_forecast['temp_chart'] = df_forecast['temp']
        y_title = "Temperature (°C)"

    chart_tabs = st.tabs(["🌡️ Temperature Trend", "💧 Humidity Trend", "💨 Wind Speed Trend"])
    
    with chart_tabs[0]:
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(
            x=df_forecast['date'], 
            y=df_forecast['temp_chart'],
            mode='lines+markers',
            name='Temperature',
            line=dict(color='#3a7bd5', width=3),
            marker=dict(size=6, color='#1e3c72'),
            hovertemplate="<b>Date:</b> %{x}<br><b>Temp:</b> %{y:.1f}°" + f"{unit}<extra></extra>"
        ))
        fig_temp.update_layout(
            title=f"5-Day Temperature Forecast for {weather_data.get('city')}",
            xaxis_title="Date & Time",
            yaxis_title=y_title,
            template="plotly_white",
            hovermode="x unified",
            height=400
        )
        st.plotly_chart(fig_temp, use_container_width=True)

    with chart_tabs[1]:
        fig_hum = go.Figure()
        fig_hum.add_trace(go.Scatter(
            x=df_forecast['date'], 
            y=df_forecast['humidity'],
            mode='lines+markers',
            name='Humidity',
            line=dict(color='#00c6ff', width=3),
            marker=dict(size=6, color='#0072ff'),
            hovertemplate="<b>Date:</b> %{x}<br><b>Humidity:</b> %{y}%<extra></extra>"
        ))
        fig_hum.update_layout(
            title=f"5-Day Humidity Forecast for {weather_data.get('city')}",
            xaxis_title="Date & Time",
            yaxis_title="Humidity (%)",
            template="plotly_white",
            hovermode="x unified",
            height=400
        )
        st.plotly_chart(fig_hum, use_container_width=True)

    with chart_tabs[2]:
        fig_wind = go.Figure()
        fig_wind.add_trace(go.Scatter(
            x=df_forecast['date'], 
            y=df_forecast['wind_speed'],
            mode='lines+markers',
            name='Wind Speed',
            line=dict(color='#f46b45', width=3),
            marker=dict(size=6, color='#ee0979'),
            hovertemplate="<b>Date:</b> %{x}<br><b>Wind Speed:</b> %{y} m/s<extra></extra>"
        ))
        fig_wind.update_layout(
            title=f"5-Day Wind Speed Forecast for {weather_data.get('city')}",
            xaxis_title="Date & Time",
            yaxis_title="Wind Speed (m/s)",
            template="plotly_white",
            hovermode="x unified",
            height=400
        )
        st.plotly_chart(fig_wind, use_container_width=True)

    # ------------------ DOWNLOAD & DATA TABLE ------------------
    st.markdown("---")
    st.subheader("📊 Raw Forecast Data")
    
    # Download as CSV button
    csv_data = df_forecast[['date', 'temp', 'humidity', 'wind_speed', 'description', 'temp_min', 'temp_max']].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download 5-Day Forecast as CSV",
        data=csv_data,
        file_name=f"{city.replace(' ', '_')}_weather_forecast.csv",
        mime="text/csv",
    )
    
    st.dataframe(df_forecast[['date', 'temp', 'humidity', 'wind_speed', 'description']].rename(columns={
        "date": "Date & Time",
        "temp": "Temp (°C)",
        "humidity": "Humidity (%)",
        "wind_speed": "Wind (m/s)",
        "description": "Condition"
    }), use_container_width=True)

    st.caption(f"Last updated: {st.session_state['last_refreshed']}")
