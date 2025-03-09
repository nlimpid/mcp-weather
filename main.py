import os

import uvicorn
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.responses import FileResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

# Import our Seniverse weather client
from server.weather import SeniverseWeatherClient

# Load environment variables
load_dotenv()

# Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
API_KEY = os.getenv("SENIVERSE_API_KEY")

# Initialize the MCP server
app = Server("mcp-weather")
sse = SseServerTransport("/messages")

# Initialize the Seniverse weather client
weather_client = SeniverseWeatherClient(
    api_key=API_KEY or "your_api_key",  # Replace with your actual API key from environment
    default_language="zh-Hans",
    default_unit="c",
)


# MCP method handlers
@app.method("weather.current")
async def handle_current_weather(params):
    """
    Handle request for current weather data from Seniverse API.

    Args:
        params: Dictionary containing location parameter

    Returns:
        Weather data as a dictionary
    """
    location = params.get("location", "beijing")
    language = params.get("language", "zh-Hans")
    unit = params.get("unit", "c")

    try:
        weather_data = await weather_client.get_current_weather(
            location=location, language=language, unit=unit
        )

        # Return the weather data as a dictionary
        return weather_data.model_dump()
    except Exception as e:
        # Log the error and return an error response
        print(f"Error fetching weather data: {e}")
        return {"error": "Failed to fetch weather data", "message": str(e)}


@app.method("weather.subscribe")
async def handle_weather_subscription(_, context):
    """
    Handle subscription to weather updates.

    Args:
        _: Parameters (not used)
        context: MCP context object

    Returns:
        Initial response with subscription ID
    """
    # Generate a unique subscription ID
    subscription_id = context.generate_id()

    # For demo purposes, just acknowledge the subscription
    return {"subscriptionId": subscription_id, "message": "Subscribed to weather updates"}


# Starlette route handlers
async def handle_sse(scope, receive, send):
    async with sse.connect_sse(scope, receive, send) as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())


async def handle_messages(scope, receive, send):
    await sse.handle_post_message(scope, receive, send)


# Create the Starlette application with routes
starlette_app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Route("/messages", endpoint=handle_messages, methods=["POST"]),
        # Serve static files
        Mount("/static", StaticFiles(directory="static"), name="static"),
        # Add a route for the index.html template
        Route("/", endpoint=lambda scope, receive, send: FileResponse("templates/index.html")),
    ]
)


if __name__ == "__main__":
    print(f"Starting MCP Weather API server on {HOST}:{PORT}")
    print(f"Open http://{HOST if HOST != '0.0.0.0' else 'localhost'}:{PORT} in your browser")

    # Run the Starlette application using Uvicorn
    uvicorn.run(starlette_app, host=HOST, port=PORT, log_level="info")
