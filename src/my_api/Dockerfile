FROM python:3.9-slim

WORKDIR /my_api

COPY my_api.py /my_api

RUN pip install fastapi uvicorn mlflow

EXPOSE 8085

CMD ["uvicorn", "my_api:app", "--reload", "--host", "0.0.0.0", "--port", "8085"]
