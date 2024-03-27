FROM python:3.12-slim

COPY . /app

WORKDIR /app

COPY requirements.txt /tmp/

RUN pip install --no-cache-dir -r /tmp/requirements.txt


CMD ["python", "main.py"]
