import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel ,Field


load_dotenv()

Api_key = os.getenv("Gemini_API")
client = genai.Client(api_key=Api_key)

class AI_response(BaseModel):
     brain : str = Field(
          description="Be honest and abusive , u can say anything u want to say "
     )
     heart: str = Field(
          description="be polite , like u r agod , be super polite and helpful"
     )
     mouth: str  = Field(
          description=" combination of both , that'll be my style"
     )


history=[]
def ask_gemini_stream(prompt: str) -> str:
    history.append(types.Content(
         role="user",
         parts=[types.Part(text=prompt)]
        )
    )

    stream = client.models.generate_content_stream(
        model="gemini-3.6-flash",
        contents=history,
        config= types.GenerateContentConfig(
            temperature=0.2,
            system_instruction= " You are Gemini , and u r supposed to give precise answers",
            response_mime_type="application/json",
            response_schema=AI_response
            )
    )

    full_text = ""
    for chunk in stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                full_text += chunk.text
    result = AI_response.model_validate_json(full_text) # this "result" is used just to use this variable to seperate the output paragraphs
    print("\n---------brain--------------")
    print(result.brain)
    print("\n-------------------heart-------------------")
    print(result.heart)

    print("\n-------------------mouth-------------------")
    print(result.mouth)
                

    history.append(types.Content(
                    role="model", 
                    parts=[types.Part(text=full_text)]
                )
            )
    return full_text


if __name__ == "__main__":
    text = str(input("what u wanna ask? : "))
    ask_gemini_stream(text)

