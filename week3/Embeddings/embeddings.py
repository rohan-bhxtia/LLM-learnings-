from sentence_transformers import SentenceTransformer
import numpy as np
from cosine import cosine

model = SentenceTransformer("all-MiniLM-L6-v2")


text1 = " python is a programming language"
text2 = " there is a programming language called python "

vector1 = model.encode(text1)
vector2 = model.encode(text2)

similarity = cosine(vector1, vector2)
print("similarity: ",similarity)
