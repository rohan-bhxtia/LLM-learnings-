from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("Gemini_API"))

def generate_answer(query, context):

    prompt = f"""
    Answer the user's question using the context below.

    Context:
    {context}

    Question:
    {query}

    If the answer is not available in the context,
    say that you don't have enough information.
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text