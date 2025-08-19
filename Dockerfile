# ./Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Scrapy needs a few system libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libssl-dev libxml2-dev libxslt1-dev zlib1g-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements layer caching
WORKDIR /app
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Copy the whole repo, but we’ll run from /app/books
COPY . /app

# Default working dir is the Scrapy project
WORKDIR /app/books

# Default command (overriden in compose file)
CMD ["scrapy", "list"]