import os 
from dotenv import load_dotenv


from google import genai
from google.genai import types

load_dotenv()
API_key = os.getenv("Gemini_API")

client = genai.Client(api_key=API_key)


response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="explain me bhagwad geeta shlok on focus , keep it in simple language and small "
              "just give the shlok and its explanation in 2-3 lines",
              config= types.GenerateContentConfig(
                  temperature = 0,
                
              )
    )


print(response.text)
