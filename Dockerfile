FROM python:3.6-slim

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN pip install flask==1.0.2 requests==2.19.1

COPY app.py /app/app.py

WORKDIR /app
CMD ["python", "app.py"]