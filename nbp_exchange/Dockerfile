# Base image
FROM python:3.9-alpine

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Create the working directory
RUN mkdir /app
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Collect static files
RUN python manage.py migrate --noinput \
    && python manage.py collectstatic --noinput

# Expose the port
EXPOSE 8000

# Start the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

