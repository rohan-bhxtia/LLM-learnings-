import os 
from dotenv import load_dotenv
from google import genai
#from google.genai import types

load_dotenv()
API_key = os.getenv("Gemini_API")

client = genai.Client(api_key=API_key)

prompt = ("explain me bhagwad geeta shlok on focus , keep it in simple language and small "
         "just give the shlok and its explanation in 2-3 lines",
)
count = client.models.count_tokens(
    model="gemini-3.6-flash",
    contents = prompt,
)

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents= prompt,
    config= {"temperature":0},
)

print("prompt Tokens: " , count.total_tokens)
print(response.text)
print("\n---usage---")
print("Input tokens: ", response.usage_metadata.prompt_token_count)
print("Output tokens:", response.usage_metadata.candidates_token_count)
print(response.usage_metadata)
print("total tokens: ",response.usage_metadata.total_token_count)