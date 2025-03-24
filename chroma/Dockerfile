FROM ghcr.io/chroma-core/chroma:latest

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git wget inetutils-ping && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip

# Install dependencies from requirements file. Turn off pip's cache as docker containers will not make use of it.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variable to change the port
#ENV CHROMA_SERVER_HTTP_PORT=5000

# Run the application
CMD ["--host", "0.0.0.0", "--port", "8000", "--reload"]