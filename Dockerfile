FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /paNET_Extractor

# Install the application dependencies.
WORKDIR /paNET_Extractor
RUN uv sync --frozen --no-cache

# Run the application.
CMD ["/paNET_Extractor/.venv/bin/fastapi", "run", "panetextractor/api/main.py", "--port", "80", "--host", "0.0.0.0"]