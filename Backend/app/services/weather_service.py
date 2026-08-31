from pathlib import Path
import os

import pandas as pd
import requests
from dotenv import load_dotenv


load_dotenv()


# ==================================================
# Paths
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

WEATHER_CSV = (
    BASE_DIR
    / "data"
    / "sri_lanka_weather.csv"
)


# ==================================================
# Load historical dataset once
# ==================================================

weather_df = pd.read_csv(
    WEATHER_CSV
)

weather_df["time"] = pd.to_datetime(
    weather_df["time"]
)

weather_df["year"] = (
    weather_df["time"].dt.year
)

weather_df["month"] = (
    weather_df["time"].dt.month
)


# ==================================================
# Historical weather
# ==================================================

def get_historical_weather_features(
    district: str,
    month: int
):

    # Find district/city
    location_data = weather_df[
        weather_df["city"]
        .astype(str)
        .str.lower()
        == district.lower()
    ].copy()

    if location_data.empty:

        raise ValueError(
            f"No historical weather data found for {district}."
        )

    # ----------------------------------------------
    # Annual historical calculations
    # ----------------------------------------------

    yearly = (
        location_data
        .groupby("year")
        .agg(
            annual_temperature_c=(
                "temperature_2m_mean",
                "mean"
            ),
            annual_rainfall_mm=(
                "rain_sum",
                "sum"
            ),
            annual_et0_mm=(
                "et0_fao_evapotranspiration",
                "sum"
            )
        )
    )

    annual_temperature_c = float(
        yearly["annual_temperature_c"].mean()
    )

    annual_rainfall_mm = float(
        yearly["annual_rainfall_mm"].mean()
    )

    annual_et0_mm = float(
        yearly["annual_et0_mm"].mean()
    )

    # ----------------------------------------------
    # Selected month historical calculations
    # ----------------------------------------------

    month_data = location_data[
        location_data["month"] == month
    ]

    if month_data.empty:

        raise ValueError(
            f"No historical data for month {month} in {district}."
        )

    # Calculate values per year first
    monthly_by_year = (
        month_data
        .groupby("year")
        .agg(
            monthly_temperature_c=(
                "temperature_2m_mean",
                "mean"
            ),
            monthly_rainfall_mm=(
                "rain_sum",
                "sum"
            ),
            monthly_et0_mm=(
                "et0_fao_evapotranspiration",
                "sum"
            ),
            monthly_wind_max_kmh=(
                "windspeed_10m_max",
                "mean"
            ),
            monthly_radiation=(
                "shortwave_radiation_sum",
                "mean"
            ),
            precipitation_hours=(
                "precipitation_hours",
                "sum"
            )
        )
    )

    monthly_temperature_c = float(
        monthly_by_year[
            "monthly_temperature_c"
        ].mean()
    )

    monthly_rainfall_mm = float(
        monthly_by_year[
            "monthly_rainfall_mm"
        ].mean()
    )

    monthly_et0_mm = float(
        monthly_by_year[
            "monthly_et0_mm"
        ].mean()
    )

    monthly_wind_max_kmh = float(
        monthly_by_year[
            "monthly_wind_max_kmh"
        ].mean()
    )

    monthly_radiation = float(
        monthly_by_year[
            "monthly_radiation"
        ].mean()
    )

    precipitation_hours = float(
        monthly_by_year[
            "precipitation_hours"
        ].mean()
    )

    water_balance_mm = (
        monthly_rainfall_mm
        - monthly_et0_mm
    )

    elevation = float(
        location_data["elevation"].median()
    )

    return {
        "annual_temperature_c": annual_temperature_c,
        "annual_rainfall_mm": annual_rainfall_mm,
        "annual_et0_mm": annual_et0_mm,

        "monthly_temperature_c": monthly_temperature_c,
        "monthly_rainfall_mm": monthly_rainfall_mm,
        "monthly_et0_mm": monthly_et0_mm,

        "monthly_wind_max_kmh": monthly_wind_max_kmh,
        "monthly_radiation": monthly_radiation,

        "precipitation_hours": precipitation_hours,
        "water_balance_mm": water_balance_mm,

        "elevation": elevation,
        "month": month
    }


# ==================================================
# Current weather API
# ==================================================

def get_current_weather(
    district: str
):

    api_key = os.getenv(
        "OPENWEATHER_API_KEY"
    )

    if not api_key:

        raise ValueError(
            "OPENWEATHER_API_KEY is missing from .env"
        )

    url = (
        "https://api.openweathermap.org/"
        "data/2.5/weather"
    )

    params = {
        "q": f"{district},LK",
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    if response.status_code != 200:

        raise ValueError(
            f"Could not retrieve current weather for {district}."
        )

    data = response.json()

    rain = data.get(
        "rain",
        {}
    ).get(
        "1h",
        0
    )

    return {
        "district": district,

        "temperature_c": data["main"]["temp"],

        "feels_like_c": data["main"]["feels_like"],

        "humidity": data["main"]["humidity"],

        "wind_speed_mps": data["wind"]["speed"],

        "rainfall_1h_mm": rain,

        "condition": data["weather"][0]["main"],

        "description": data["weather"][0]["description"]
    }