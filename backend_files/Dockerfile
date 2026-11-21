FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all backend files including model and requirements
COPY . /app

# Install system build dependencies and python requirements
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove build-essential && \
    rm -rf /var/lib/apt/lists/*

# Expose the API port
EXPOSE 7860

# Command to run the Flask application
CMD ["python", "app.py"]
