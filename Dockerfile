# Use a small, official Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt python-dotenv

# Copy source code and environment file
COPY src/ ./src/
COPY .env .

# Set environment variables
ENV PORT=8050
EXPOSE 8050

# Move to app folder
WORKDIR /app/src/dashboard

# Run app
CMD ["python", "app.py"]