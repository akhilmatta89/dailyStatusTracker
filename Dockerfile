# Use an official Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy application files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask runs on
EXPOSE 9000

# Set environment variables to disable buffering (helps with logs)
ENV PYTHONUNBUFFERED=1

# Command to run the Flask application
CMD ["python", "main.py"]
