FROM python:3.12.2-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./gpt_server /app

# CMD ["uvicorn", "gpt_server:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "gpt_server:app", "--bind", "0.0.0.0:8000"]
