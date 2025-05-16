FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create static and media directories
RUN mkdir -p /app/staticfiles /app/media

# Run as non-root user
RUN useradd -m myuser
RUN chown -R myuser:myuser /app
USER myuser

# Command to run on container start
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "theater_system.wsgi:application"]
