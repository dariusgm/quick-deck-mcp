FROM ubuntu:24.04
LABEL maintainer="Darius Murawski"
LABEL description="Docker image for Quick Deck MCP Server"
LABEL version="1.0"

WORKDIR /app
COPY pyproject.toml /app/pyproject.toml
# Update the package list
RUN apt-get update
# Install dependencies
RUN apt-get install -y texlive-latex-base texlive-latex-recommended
RUN apt-get install -y pandoc
# Install Python and pip
RUN apt-get install -y python3 python3-pip
# Install uv package manager, whith --break-system-packages to enforce the glboal installation
RUN pip install uv --break-system-packages
# Install the required Python packages
RUN uv venv --python=3.13 --seed && . .venv/bin/activate && uv sync
# Copy the rest of the application code
COPY . /app
# Add exposed port
EXPOSE 8000
# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src
# Set the working directory to the virtual environment
CMD ["/app/.venv/bin/uvicorn", "main:app",  "--host",  "0.0.0.0", "--port", "8000", "--workers", "4"]
