"""
Seniverse Weather API client for accessing weather data.
"""

from typing import Any, Dict, Optional

import httpx
from pydantic import BaseModel


class WeatherData(BaseModel):
    """Model for weather data returned by the Seniverse API."""

    temperature: float
    feels_like: Optional[float] = None
    humidity: Optional[float] = None
    wind_direction: Optional[str] = None
    wind_speed: Optional[float] = None
    wind_scale: Optional[int] = None
    conditions: str
    location: str
    last_update: Optional[str] = None


class SeniverseWeatherClient:
    """
    Client for accessing the Seniverse Weather API.

    API Documentation: https://seniverse.com/api
    """

    BASE_URL = "https://api.seniverse.com/v3"

    def __init__(
        self,
        api_key: str,
        default_language: str = "zh-Hans",
        default_unit: str = "c",
        timeout: int = 10,
    ):
        """
        Initialize the Seniverse Weather API client.

        Args:
            api_key: Your Seniverse API key
            default_language: Default language for responses (e.g., 'zh-Hans', 'en')
            default_unit: Default temperature unit ('c' for Celsius, 'f' for Fahrenheit)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.default_language = default_language
        self.default_unit = default_unit
        self.timeout = timeout

    async def get_current_weather(
        self, location: str, language: Optional[str] = None, unit: Optional[str] = None
    ) -> WeatherData:
        """
        Get current weather data for a specified location.

        Args:
            location: Location name (city name) or ID
            language: Response language (defaults to instance default)
            unit: Temperature unit (defaults to instance default)

        Returns:
            WeatherData object containing current weather information

        Raises:
            httpx.HTTPError: If the API request fails
        """
        # Use instance defaults if parameter not specified
        language = language or self.default_language
        unit = unit or self.default_unit

        # Build query parameters
        params = {"key": self.api_key, "location": location, "language": language, "unit": unit}

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Make API request
            response = await client.get(f"{self.BASE_URL}/weather/now.json", params=params)
            response.raise_for_status()

            # Parse JSON response
            data = response.json()

            # Extract relevant data from the response
            try:
                result = data["results"][0]
                now = result["now"]

                return WeatherData(
                    temperature=float(now["temperature"]),
                    feels_like=float(now.get("feels_like", 0)) if "feels_like" in now else None,
                    humidity=float(now.get("humidity", 0)) if "humidity" in now else None,
                    wind_direction=now.get("wind_direction"),
                    wind_speed=float(now.get("wind_speed", 0)) if "wind_speed" in now else None,
                    wind_scale=int(now.get("wind_scale", 0)) if "wind_scale" in now else None,
                    conditions=now.get("text", "Unknown"),
                    location=result["location"]["name"],
                    last_update=now.get("last_update"),
                )
            except (KeyError, IndexError) as e:
                # Re-raise with more informative message
                raise ValueError(f"Failed to parse Seniverse API response: {e}") from e

    async def get_weather_with_raw_response(
        self, location: str, language: Optional[str] = None, unit: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get the raw weather data from the API.

        This method returns the complete API response as a dictionary,
        which can be useful for accessing additional data not captured
        in the WeatherData model.

        Args:
            location: Location name (city name) or ID
            language: Response language (defaults to instance default)
            unit: Temperature unit (defaults to instance default)

        Returns:
            Complete API response as a dictionary
        """
        language = language or self.default_language
        unit = unit or self.default_unit

        params = {"key": self.api_key, "location": location, "language": language, "unit": unit}

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.BASE_URL}/weather/now.json", params=params)
            response.raise_for_status()
            return response.json()


# Example usage:
"""
async def main():
    # Create client with your API key
    client = SeniverseWeatherClient(api_key="your_api_key")
    
    # Get weather for Beijing
    try:
        weather = await client.get_current_weather("beijing")
        print(f"Temperature in {weather.location}: {weather.temperature}°C")
        print(f"Conditions: {weather.conditions}")
    except Exception as e:
        print(f"Error getting weather: {e}")

# Run with asyncio
# import asyncio
# asyncio.run(main())
"""
