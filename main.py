from fastapi import FastAPI
from pydantic import BaseModel
import together
import os

app = FastAPI()

# Load Together API key from environment variable
together.api_key = os.getenv("TOGETHER_API_KEY")

# Request body model
class QueryRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "AgriPal API is running 🚀"}

@app.post("/ask")
def ask_ai(request: QueryRequest):
    response = together.Complete.create(
        prompt=request.query,
        model="togethercomputer/llama-2-70b-chat",
        max_tokens=100,
        temperature=0.7,
        top_p=0.9,
    )
    return {"answer": response["output"]["choices"][0]["text"].strip()}
