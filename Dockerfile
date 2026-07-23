FROM ubuntu

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY . /app

WORKDIR /app

RUN /root/.local/bin/uv sync
