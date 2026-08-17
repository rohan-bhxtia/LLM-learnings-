
import os
from enum import Enum
from typing import List
 
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
 
load_dotenv()  # loads GOOGLE_API_KEY from your .env, same as Day 1
client = genai.Client(api_key=os.getenv("Gemini_API"))
 
MODEL = "gemini-3.6-flash"  # check ai.google.dev/models if this string is outdated
 
class Sentiment(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"
 
class SentimentResult(BaseModel):
    sentiment: Sentiment
    confidence: float
    reason: str
 
def classify_sentiment(review: str) -> SentimentResult:
    response = client.models.generate_content(
        model=MODEL,
        contents=review,  # Gemini takes the user turn as `contents` directly
        config=types.GenerateContentConfig(
            system_instruction="You are a strict sentiment classifier for product reviews.",
            response_mime_type="application/json",  # tells Gemini "the reply body IS json"
            response_schema=SentimentResult,          # <- pass the Pydantic class directly,
                                                        #    same convenience as OpenAI's .parse()
        ),
    )

    return response.parsed
 
 
# ===========================================================
# EXAMPLE 2 — Nested schema + list: receipt extraction
# ===========================================================
 
# class LineItem(BaseModel):
#     name: str
#     quantity: int
#     unit_price: float
 
# class Receipt(BaseModel):
#     store_name: str
#     date: str
#     items: List[LineItem]
#     subtotal: float
#     tax: float
#     total: float
 
# def extract_receipt(raw_text: str) -> Receipt:
#     response = client.models.generate_content(
#         model=MODEL,
#         contents=raw_text,
#         config=types.GenerateContentConfig(
#             system_instruction=(
#                 "Extract structured data from this receipt text. "
#                 "If a value truly cannot be determined, make your best estimate — "
#                 "every field in the schema is required."
#             ),
#             response_mime_type="application/json",
#             response_schema=Receipt,
#         ),
#     )
#     return response.parsed
 
 
# ===========================================================
# Run both examples
# ===========================================================
if __name__ == "__main__":
    review = "The battery life is incredible but the case feels cheap and scratched within a week."
    result = classify_sentiment(review)
    print("\n--- Sentiment classification ---")
    print(result)
    print("As dict:", result.model_dump())
 
    # receipt_text = """
    # Corner Cafe
    # 12 Aug 2026
    # 2x Cappuccino  $4.50 each
    # 1x Croissant   $3.20
    # Subtotal: $12.20
    # Tax: $1.10
    # Total: $13.30
    # """
    # receipt = extract_receipt(receipt_text)
    # print("\n--- Receipt extraction ---")
    # print(receipt)
    # for item in receipt.items:
    #     print(f"  - {item.quantity}x {item.name} @ ${item.unit_price}")
 