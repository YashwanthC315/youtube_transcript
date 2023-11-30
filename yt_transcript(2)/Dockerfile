# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg

# Install Python dependencies
RUN pip install --no-cache-dir pytube pydub assemblyai

# Command to run on container start
CMD ["python", "script.py"]
