FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

RUN apt-get update && apt-get install -y curl

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose API port
EXPOSE 8000

# Start application (seed DB then run API)
CMD ["bash", "-c", "python seed.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]