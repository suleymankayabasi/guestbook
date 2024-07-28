# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables for Python buffering and Docker image optimizations
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /code

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gettext \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the Django project code into the container
COPY . /code/

# Expose the port that Django runs on
EXPOSE 8000

RUN chmod +x runserver.sh

# Run Django development server
CMD ["/bin/sh", "runserver.sh"]
