import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

Api_key = os.getenv("Gemini_API")
client = genai.Client(api_key= Api_key)


stream = client.models.generate_content_stream(
    model="gemini-3.6-flash",
    contents="can we be job ready in AI in 3 months , if we know the theory of everything and we have to work is on code"
)
for chunk in stream:
    if chunk.text:
        print(chunk.text , end="", flush=True)