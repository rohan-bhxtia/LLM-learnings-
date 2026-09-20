import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from calcy import CALCULATE_TOOL, calculate

load_dotenv()

client = genai.Client(
    api_key=os.getenv("Gemini_API")
)


def run_agent(question):

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=question,
        config=types.GenerateContentConfig(
            tools=[
                types.Tool(
                    function_declarations=[CALCULATE_TOOL]
                )
            ]
        )
    )

    # Did Gemini ask for a tool?
    for function_call in response.function_calls:

        if function_call.name == "calculate":

            # Run our REAL Python function
            result = calculate(**function_call.args)

            # Give result back to Gemini
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=[
                    question,
                    response.candidates[0].content,
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_function_response(
                                name="calculate",
                                response={"result": result}
                            )
                        ]
                    )
                ],
                config=types.GenerateContentConfig(
                    tools=[
                        types.Tool(
                            function_declarations=[CALCULATE_TOOL]
                        )
                    ]
                )
            )

    return response.text


print(run_agent("What's 847 times 39?"))