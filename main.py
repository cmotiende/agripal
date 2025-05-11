from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import together
import os

app = FastAPI()

# Allow all origins (for frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

together.api_key = os.getenv("TOGETHER_API_KEY")

@app.get("/")
def read_root():
    return {"message": "AgriPal API is running 🚀"}

@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    query = data.get("query")

    response = together.Complete.create(
        prompt=query,
        model="togethercomputer/llama-2-70b-chat",
        max_tokens=100,
        temperature=0.7,
        top_p=0.9,
    )

    answer = response["output"]["choices"][0]["text"]
    return {"answer": answer.strip()}
