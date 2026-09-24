import os
import requests
from dotenv import load_dotenv



load_dotenv()

#CALCULATOR TOOL
calculator_tool = {
    "name": "calcy",
    "description": "Calculate two numbers using addition, subtraction, multiplication, or division.",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {
                "type": "number",
                "description": "First number"
            },
            "b": {
                "type": "number",
                "description": "Second number"
            },
            "operation": {
                "type": "string",
                "enum": ["add", "subtract", "multiply","divide"]
            }
        },
        "required": ["a", "b", "operation"]
    }
}


def calcy(a, b, operation):

    if operation == "add":
        return a + b

    elif operation == "subtract":
        return a - b

    elif operation == "multiply":
        return a * b

    elif operation == "divide":
        if b == 0:
            return "Cannot divide by zero"
        return a / b

    return "Invalid operation"


# WEATHER TOOL
weather_tool = {
    "name": "get_weather",
    "description": "Get the current weather of a city. Use this tool when the user asks about weather.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "Name of the city"
            }
        },
        "required": ["city"]
    }
}


def get_weather(city):

    API_KEY = os.getenv("Weather_API")

    url = "https://api.openweathermap.org/data/2.5/weather"

    parameters = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=parameters)

    data = response.json()

    if response.status_code != 200:
        return data.get("message", "Could not get weather")

    return (
    f"City: {data['name']}\n"
    f"Temperature: {data['main']['temp']}°C\n"
    f"Feels Like: {data['main']['feels_like']}°C\n"
    f"Weather: {data['weather'][0]['description']}\n"
    f"Humidity: {data['main']['humidity']}%"
)