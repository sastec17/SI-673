import json
import logging
import os
import re
from datetime import datetime, timedelta, timezone

import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

HEADERS = {
    "User-Agent": "SI673-Weather-Dashboard (educational project)",
    "Accept": "application/geo+json",
}


def get_weather_data(path, params=None):
    """Retrieve weather data from the National Weather Service."""

    # TODO 2: Read WEATHER_API_BASE_URL from the Lambda environment.
    # Remove a trailing slash with .rstrip("/")
    base_url = os

    url = f"{base_url}{path}"

    logger.info("Requesting weather data from %s", url)

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=8,
    )

    response.raise_for_status()
    return response.json()


def get_value(properties, field):
    """Extract a temperature measurement in Fahrenheit."""
    measurement = properties.get(field) or {}
    value = measurement.get("value")

    if value is None:
        return None

    return value


def get_history(airport):
    """Retrieve up to 10 temperatures from the past 3 days."""
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=3)

    data = get_weather_data(
        f"/stations/{airport}/observations",
        {
            "start": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "limit": 100,
        },
    )

    temperatures = []

    for observation in data.get("features", []):
        properties = observation.get("properties") or {}
        temperature = get_value(properties, "temperature")

        if temperature is not None:
            temperatures.append(temperature)

        if len(temperatures) >= 10:
            break

    return list(reversed(temperatures))


def lambda_handler(event, context):

    # TODO 1: Read the airport code from the query parameters.
    # Convert the code to uppercase and remove surrounding whitespace.
    # Example URL: ?airport=KDTW
    #
    # Hint:
    # params = event.get("queryStringParameters") or {}
    # airport = ...
    airport = "REPLACE_ME"

    if not re.fullmatch(r"[A-Z]{4}", airport):
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json",
            },
            "body": json.dumps(
                {"error": "Provide a four-letter airport code, such as KDTW."}
            ),
        }

    try:
        logger.info("Fetching weather for airport: %s", airport)

        current = get_weather_data(f"/stations/{airport}/observations/latest")

        properties = current.get("properties") or {}
        history = get_history(airport)

        # TODO 3: Complete the response dictionary.
        # The dashboard expects these exact keys:
        # temp, dewpoint, date, history, airport
        #
        # Use get_value(properties, "temperature") for temp.
        # Use get_value(properties, "dewpoint") for dewpoint.
        # Date comes from properties.get("timestamp").

        body = {
            "temp": None,  # TODO
            "dewpoint": None,  # TODO
            "date": None,  # TODO
            "history": history,
            "airport": None,  # TODO
        }

        logger.info(
            "Weather retrieved for %s: %d historical readings",
            airport,
            len(history),
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json",
            },
            "body": json.dumps(body),
        }

    except requests.exceptions.RequestException:
        logger.exception("Weather service request failed")

        return {
            "statusCode": 502,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json",
            },
            "body": json.dumps({"error": "Unable to retrieve weather data."}),
        }

    except Exception:
        logger.exception("Unexpected Lambda error")

        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json",
            },
            "body": json.dumps({"error": "An unexpected error occurred."}),
        }
