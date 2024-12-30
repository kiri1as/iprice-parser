FROM python:3.13-alpine

WORKDIR /app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    python3-dev \
    libffi-dev \
    build-base \
    tzdata

COPY ../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

ENTRYPOINT ["python", "main.py"]
