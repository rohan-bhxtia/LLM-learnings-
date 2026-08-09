import os 
from dotenv import load_dotenv


from google import genai
from openai import OpenAI

load_dotenv()
API_key = os.getenv("Gemini_API")
openai_key = os.getenv("open_ai")
client = genai.Client(api_key=API_key)

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="explain me bhagwad geeta shlok on focus , keep it in simple language and small "
              "just give the shlok and its explanation in 2-3 lines",
    config= {
        "temperature":0
    }
)

print(response.text)

