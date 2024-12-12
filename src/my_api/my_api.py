from datetime import datetime, timedelta
import joblib
import torch
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
import sys
from rag.rag import RAG
from load_llm.load_llm import LLMPretrained, LLMWrapper
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from data_ingestion.retriever import Retriever

sys.path.append("/my_api")
app = FastAPI()

# Secret key et configuration du token
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

rag = None


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)


class Question(BaseModel):
    question: str


class Token(BaseModel):
    access_token: str
    token_type: str


# Fonction pour vérifier l'utilisateur
def verify_user(username: str, password: str):
    if username == "contextor" and password == "robot":  # Remplacez par un vrai hash
        return username
    return None


# Endpoint pour générer un token
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = verify_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {"sub": form_data.username, "exp": datetime.utcnow() + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Vérification du token pour sécuriser les endpoints
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/")
async def root(current_user: str = Depends(get_current_user)):
    return {"message": "Hello World"}

@app.post("/model")
async def get_model(question: Question, current_user: str = Depends(get_current_user)):
    global rag
    try:
        print("Starting to load the model...")
        embedding_model = HuggingFaceEmbeddings(
        model_name="Lajavaness/sentence-camembert-large",
        encode_kwargs={"normalize_embeddings": True},
        model_kwargs = {'device': 'cuda'}
        )

        model = LLMWrapper(llm_pretrained=LLMPretrained.TINY_LLAMA)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=50,
            add_start_index=True,
            strip_whitespace=True
        )

        retriever = Retriever(embedding_model=embedding_model, text_splitter=text_splitter, vector_store_path="./faiss_index")#, documents=RAW_KNOWLEDGE_BASE)
        rag = RAG(vector_store=retriever.vector_store, model=model)
        # rag.model.model.to("cpu")
        print("Model loaded successfully")
        return {"message": "Model loaded"}
    except Exception as e:
        print(f"Error loading model: {e}")
        raise e

@app.post("/question")
async def create_item(question: Question, current_user: str = Depends(get_current_user)):
    print("Post question...")
    global rag
    print("Start answer generation...")
    answer = rag.generate_answer(k=5, query=question.question)
    print("Done generating answer!")
    return {"response": answer}
