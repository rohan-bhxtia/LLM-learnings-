import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
API_key = os.getenv("Gemini_API")
client = genai.Client(api_key=API_key)

SYSTEM_INSTRUCTION = (
    "You are a senior AI engineer "
    "Keep answers under 3 sentences."
)

history = []

def ask(user_text):
    history.append(
        {
        "role": "user",
        "parts": [{"text": user_text}]
     }
    )
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=history,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.4,
        ),
    )

    reply = response.text
    history.append({
        "role": "model",
        "parts": [{"text": reply}]
    })
    return reply

if __name__ == "__main__":
    print("Chatbot ready. Type 'quit' to exit.\`n")
    while True:
        user_text = input("You: ")
        if user_text.lower() == "quit":
            break
        print("Bot:", ask(user_text), "\n")