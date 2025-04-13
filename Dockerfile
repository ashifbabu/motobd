FROM python:3.9-slim

WORKDIR /app

COPY ./functions/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./functions .

ENV PORT=8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"] 