FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY app.py .

# Create the data folder for the shared volume
RUN mkdir /data

# Default command (can be overridden by Kubernetes)
CMD ["python", "app.py"]
