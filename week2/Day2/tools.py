import os
import requests
from dotenv import load_dotenv
import currencyapicom



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
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(API_KEY, params=params)

    data = response.json()

    if response.status_code != 200:
        return data.get("message", "Could not get weather")

    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "weather": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"]
    }


# CURRENCY CONVERTER TOOL
currency_tool = {
    "name": "convert_currency",
    "description": "Convert an amount from one currency to another.",
    "parameters": {
        "type": "object",
        "properties": {
            "amount": {
                "type": "number",
                "description": "Amount to convert"
            },
            "from_currency": {
                "type": "string",
                "description": "Currency to convert from, such as USD"
            },
            "to_currency": {
                "type": "string",
                "description": "Currency to convert to, such as INR"
            }
        },
        "required": ["amount", "from_currency", "to_currency"]
    }
}


def convert_currency(amount, from_currency, to_currency):
# this block is i found in documentation of currency conversion API 
    client = currencyapicom.Client('Currency_API')
    result = client.historical('01-01-2022')
    print(result)


print(convert_currency())