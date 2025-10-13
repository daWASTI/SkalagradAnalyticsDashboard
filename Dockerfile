FROM python:3.11-bullseye

# Set working directory inside the container
WORKDIR /app
ENV PYTHONPATH=/app

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt python-dotenv

# Copy source code and environment file
COPY src/ ./src/
COPY .env .

# Set environment variables
ENV PORT=8050
EXPOSE 8050

# Run app
CMD ["python", "src/dashboard/app.py"]