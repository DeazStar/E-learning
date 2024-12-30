# Use an official Python image as the base
FROM python:3.11-slim

# Set environment variables to avoid interactive prompts
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory inside the container
WORKDIR /usr/src/auth_service

# Copy requirements.txt into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

COPY .env /usr/src/auth_service/.env

# Expose the port your application runs on (e.g., 8000 for Django)
EXPOSE 8000

# Default command to run manage.py
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
