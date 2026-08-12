import os
from enum import Enum
from typing import List

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()  # loads OPENAI_API_KEY etc. from your .env, same as Day 1
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-5.1-mini"  # check platform.openai.com/docs/models if this string is outdated

# ===========================================================
# EXAMPLE 1 — Flat schema: sentiment classification
# ===========================================================

# Pydantic's `Enum` gives us a *closed* set of allowed values.
# Under the hood this becomes a JSON Schema "enum" — the model
# literally cannot output a 4th option like "mixed".
class Sentiment(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"

# BaseModel = "this Python class also describes a JSON shape."
# Every attribute becomes a required field in strict mode.
class SentimentResult(BaseModel):
    sentiment: Sentiment   # must be one of the 3 enum values above
    confidence: float      # model's own 0.0-1.0 self-rated confidence
    reason: str            # one-sentence justification, forces the model to "show its work"

def classify_sentiment(review: str) -> SentimentResult:
    completion = client.chat.completions.parse(   # note: .parse(), not .create()
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a strict sentiment classifier for product reviews."},
            {"role": "user", "content": review},
        ],
        response_format=SentimentResult,  # <- pass the Pydantic class directly;
                                           #    the SDK converts it to a strict JSON Schema for you
    )
    # .parse() already validated the JSON and built you a real Python object —
    # no json.loads(), no manual validation, no guessing about missing keys.
    return completion.choices[0].message.parsed


# ===========================================================
# EXAMPLE 2 — Nested schema + list: receipt extraction
# ===========================================================

class LineItem(BaseModel):
    name: str
    quantity: int
    unit_price: float

class Receipt(BaseModel):
    store_name: str
    date: str                 # keep as str on Day 3 — real date parsing/validation is a later refinement
    items: List[LineItem]     # a JSON array where every element must match the LineItem schema
    subtotal: float
    tax: float
    total: float

def extract_receipt(raw_text: str) -> Receipt:
    completion = client.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": (
                "Extract structured data from this receipt text. "
                "If a value truly cannot be determined, make your best estimate — "
                "every field in the schema is required."
            )},
            {"role": "user", "content": raw_text},
        ],
        response_format=Receipt,
    )
    return completion.choices[0].message.parsed


# ===========================================================
# Run both examples
# ===========================================================
if __name__ == "__main__":
    review = "The battery life is incredible but the case feels cheap and scratched within a week."
    result = classify_sentiment(review)
    print("\n--- Sentiment classification ---")
    print(result)                    # pretty repr of the Pydantic object
    print("As dict:", result.model_dump())   # convert to a plain dict, e.g. for storing in a DB

    receipt_text = """
    Corner Cafe
    12 Aug 2026
    2x Cappuccino  $4.50 each
    1x Croissant   $3.20
    Subtotal: $12.20
    Tax: $1.10
    Total: $13.30
    """
    receipt = extract_receipt(receipt_text)
    print("\n--- Receipt extraction ---")
    print(receipt)
    for item in receipt.items:
        print(f"  - {item.quantity}x {item.name} @ ${item.unit_price}")