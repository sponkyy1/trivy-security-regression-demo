FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    python2.7 \
    libssl1.0-dev \
    && rm -rf /var/lib/apt/lists/*
