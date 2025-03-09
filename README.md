# MCP Weather API - Server-Sent Events Demo

A modern Python application demonstrating the use of Message Passing Channel (MCP) with Server-Sent Events for real-time weather data from the Seniverse Weather API.

## Features

- Real-time weather data streaming via Server-Sent Events (SSE)
- Integration with Seniverse Weather API (心知天气)
- MCP server implementation with Starlette
- Modern Python project structure with clean separation of concerns
- Chinese UI interface for displaying weather data

## Project Structure

```
mcp-weather/
├── server/                   # Server components
│   └── weather.py            # Seniverse Weather API client
├── templates/                # HTML templates
│   └── index.html            # Main UI for weather display
├── static/                   # Static assets (if needed)
├── .env                      # Environment variables
├── main.py                   # Application entry point
├── pyproject.toml            # Project dependencies
└── README.md                 # Project documentation
```

## Requirements

- Python 3.12 or higher
- Dependencies:
  - mcp[cli]
  - starlette
  - uvicorn
  - python-dotenv
  - httpx
  - pydantic

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mcp-weather
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

3. Get an API key from Seniverse (心知天气):
   - Register at https://seniverse.com/
   - Create a new application to get an API key

4. Configure your environment variables in the `.env` file:
   ```
   # Replace with your actual API key from Seniverse
   SENIVERSE_API_KEY=your_api_key
   ```

## Running the Application

Start the server:

```bash
python main.py
```

The server will start on http://localhost:8000 by default.

## API Endpoints

- `/sse`: Connect to the Server-Sent Events stream
- `/messages`: POST endpoint for sending messages to the server
- `/`: Main web interface for the weather app

## MCP Methods

- `weather.current`: Get current weather data for a location
  - Parameters:
    - `location`: City name (e.g., "beijing", "shanghai")
    - `language`: Response language (optional, default: "zh-Hans")
    - `unit`: Temperature unit (optional, default: "c")

- `weather.subscribe`: Subscribe to weather updates

## Seniverse Weather API

This application uses the Seniverse Weather API (心知天气) to retrieve real-time weather data. The API provides:

- Current weather conditions
- Temperature, humidity, and wind data
- Weather forecasts

For more information about the API, visit: https://seniverse.com/api

## Example Client Usage

The application includes a web interface accessible at http://localhost:8000/ that demonstrates:

1. Fetching current weather data for a specified location
2. Subscribing to weather updates
3. Displaying weather data in a user-friendly interface

## License

MIT License
