FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

WORKDIR /bot

ADD pyproject.toml .
ADD uv.lock .

RUN uv sync --locked --no-install-project --no-dev

ADD *.py /bot

ENTRYPOINT ["uv", "run", "python", "main.py"]
