FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app .

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload & python /app/tcp_server.py"]
