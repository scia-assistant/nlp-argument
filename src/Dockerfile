FROM python:3.9-slim

WORKDIR /my_api

RUN pip install fastapi uvicorn mlflow python-jose python-multipart
RUN pip install torch langchain langchain-community transformers>=4.30.0 langchain_huggingface faiss-cpu

COPY my_api/my_api.py /my_api
COPY rag /my_api/rag
COPY load_llm /my_api/load_llm
# COPY model /my_api/model
COPY faiss_index /my_api/faiss_index
COPY data_ingestion /my_api/data_ingestion

EXPOSE 8085

CMD ["uvicorn", "my_api:app", "--reload", "--host", "0.0.0.0", "--port", "8085"]
