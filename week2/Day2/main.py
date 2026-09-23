import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools import (
    calculator_tool,
    calcy,
    weather_tool,
    get_weather,
)


load_dotenv()

client = genai.Client(
    api_key=os.getenv("Gemini_API")
)


# Map Gemini's tool name to the actual Python function
TOOL_FUNCTIONS = {
    "calcy": calcy,
    "get_weather": get_weather,
}


def run_agent(question):

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=question,
        config=types.GenerateContentConfig(
            tools=[
                types.Tool(
                    function_declarations=[
                        calculator_tool,
                        weather_tool,
                    ]
                )
            ]
        )
    )

    # Check whether Gemini requested any tools
    if response.function_calls:

        tool_results = []

        for function_call in response.function_calls:

            tool_name = function_call.name
            args = function_call.args

            # Find the actual Python function
            tool_function = TOOL_FUNCTIONS[tool_name]

            # Execute the tool
            result = tool_function(**args)

            tool_results.append(
                types.Part.from_function_response(
                    name=tool_name,
                    response={"result": result}
                )
            )

        # Send tool results back to Gemini
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[
                question,
                response.candidates[0].content,
                types.Content(
                    role="user",
                    parts=tool_results
                )
            ],
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        function_declarations=[
                            calculator_tool,
                            weather_tool,
                        ]
                    )
                ]
            )
        )

    return response.text


if __name__ == "__main__":

    question = input("You: ")

    answer = run_agent(question)

    print("\nGemini:", answer)