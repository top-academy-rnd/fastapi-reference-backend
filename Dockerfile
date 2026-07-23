FROM ghcr.io/astral-sh/uv:latest

COPY . /app

WORKDIR /app

RUN uv sync
