# FROM python:3.9-slim

# WORKDIR /my_api

# RUN pip install fastapi uvicorn mlflow python-jose python-multipart
# RUN pip install torch langchain langchain-community transformers>=4.30.0 langchain_huggingface faiss-cpu

# COPY my_api/my_api.py /my_api
# COPY rag /my_api/rag
# COPY load_llm /my_api/load_llm
# # COPY model /my_api/model
# COPY faiss_index /my_api/faiss_index
# COPY data_ingestion /my_api/data_ingestion

# EXPOSE 8085

# CMD ["uvicorn", "my_api:app", "--reload", "--host", "0.0.0.0", "--port", "8085"]


# Use an NVIDIA CUDA base image with Python
FROM nvidia/cuda:12.5.0-base-ubuntu22.04


ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Paris

# Set a working directory
WORKDIR /my_api

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install required Python packages
RUN pip install --upgrade pip
RUN pip install fastapi uvicorn mlflow python-jose python-multipart
RUN pip install torch transformers>=4.30.0
RUN pip install langchain langchain-community langchain_huggingface faiss-cpu

# Copy application files
COPY my_api/my_api.py /my_api
COPY rag /my_api/rag
COPY load_llm /my_api/load_llm
# COPY model /my_api/model
COPY faiss_index /my_api/faiss_index
COPY data_ingestion /my_api/data_ingestion

# Expose the application port
EXPOSE 8085

# Set the default command to start the app
CMD ["uvicorn", "my_api:app", "--reload", "--host", "0.0.0.0", "--port", "8085"]
