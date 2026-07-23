FROM ubuntu

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY . /app

WORKDIR /app

RUN uv sync
