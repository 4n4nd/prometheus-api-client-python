FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir pytest

CMD ["pytest", "-q"]
