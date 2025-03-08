FROM ghcr.io/chroma-core/chroma:latest

COPY requirements.txt .
RUN pip install --upgrade pip

# Install dependencies from requirements file. Turn off pip's cache as docker containers will not make use of it.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variable to change the port
ENV CHROMA_SERVER_HTTP_PORT=5000

# Run the application
CMD ["uvicorn", "chromadb.app:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]