from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)


class Question(BaseModel):
    question: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/question")
def create_item(question: Question):
    if question.question == "hello":
        return {"response": "hello my boy"}
    else:
        return {"response": "I don't understand"}
