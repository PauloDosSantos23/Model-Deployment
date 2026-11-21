FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all frontend files
COPY . /app

# Install python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Streamlit web interface port
EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
