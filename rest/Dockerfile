# Use a base image with Python (e.g., Python 3.9)
FROM python:3.11

# Install system dependencies required for some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /rest

COPY . /rest

# Install Poetry
RUN pip install --no-cache-dir poetry

# Install app dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Expose the port that your app will listen to (if applicable)
EXPOSE 8000

# Define the command to run your app
CMD ["python", "api/main.py"]