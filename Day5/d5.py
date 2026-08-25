import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

Api_key = os.getenv("Gemini_API")
client = genai.Client(api_key=Api_key)

history=[]


def ask_gemini_stream(prompt: str) -> str:
    history.append(types.Content(role="user",parts=[types.Part(text=prompt)]))

    stream = client.models.generate_content_stream(
        model="gemini-3.6-flash",
        contents=history,
        config= types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=300,
            response_mime_type="application/json",
            response_schema=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "answer": types.Schema(type=types.Type.STRING),
                    "confidence": types.Schema(type=types.Type.NUMBER),
                },
                required=["answer"],
            ),
            )
    )

    full_text = ""
    finish_reason = None
    for chunk in stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                full_text += chunk.text
            if chunk.candidates and chunk.candidates[0].finish_reason:
                finish_reason = chunk.candidates[0].finish_reason

    history.append(types.Content(role="model", parts=[types.Part(text=full_text)]))
    return full_text


if __name__ == "__main__":
    ask_gemini_stream(
        "can we be job ready in AI in 3 months, if we know the theory of everything and we have to work is on code"
    )
