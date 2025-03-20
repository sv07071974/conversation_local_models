# Use a base Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code and the model files to the container
COPY app.py .
COPY models/ /app/models/

# Set environment variables if needed (adjust as necessary)
ENV MODEL_PATH="/app/models/llama3.2_latest"

# Expose a port for the application (adjust if needed)
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]
