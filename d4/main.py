from google import genai
from google.genai import types

def ask_gemini_stream(prompt: str, system: str = None, max_output_tokens: int = 300) -> str:
    """
    Streams a Gemini reply token-by-token to the console, then returns
    the full accumulated text (for saving into chat history afterward).
    """
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    config = types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=max_output_tokens,
        system_instruction=system,
    )

    full_text = ""
    stream = client.models.generate_content_stream(
        model="gemini-3-flash",
        contents=prompt,
        config=config,
    )

    for chunk in stream:
        if chunk.text:
            print(chunk.text, end="", flush=True)
            full_text += chunk.text

    print()
    return full_text

if __name__ == "__main__":
    ask_gemini_stream("Explain what a vector database is, in 3 sentences.")