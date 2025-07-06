# ---- Minimal Python image ----
FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bots/slayer/main.py"]
