# Use official Python slim image for smaller footprint
FROM python:3.11-slim

# Set environment variables
COPY .env .

# Set work directory
WORKDIR /app

# Install system dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Use uvicorn for running the application
CMD ["uvicorn", "--reload", "app.main:app", "--host", "0.0.0.0", "--port", "7171"]