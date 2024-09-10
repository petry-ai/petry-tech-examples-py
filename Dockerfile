# Use Python 3.12 slim image as the base
FROM python:3.12-slim

# Set environment variables
ARG ENV
ARG OPENAI_API_KEY
ARG ALLOWED_HOST

ENV DOCKER_BUILD=1
ENV ENV=${ENV}
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV ALLOWED_HOST=${ALLOWED_HOST}

# Set working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update

# Copy requirements file
COPY ./src /app/src
COPY ./requirements.txt /app/requirements.txt
COPY ./entrypoint.sh /app/entrypoint.sh
COPY ./pyproject.toml /app/pyproject.toml


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]