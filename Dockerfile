
FROM python:3.8-slim-buster

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install Firefox binary
RUN apt-get update \
    && apt-get install -y firefox-esr --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install --upgrade pip 
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY ./wunderground/ ./

ENTRYPOINT [ "python3", "main.py" ]
