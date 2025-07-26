FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    curl \
    python2.7 \
    && rm -rf /var/lib/apt/lists/*
