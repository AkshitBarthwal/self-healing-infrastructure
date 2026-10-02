FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir docker

COPY receiver.py /app/receiver.py

CMD ["python", "/app/receiver.py"]
