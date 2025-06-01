FROM python:3.9-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libpcre3-dev \
    libssl-dev \
    nginx \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./templates /app/templates
COPY app.py /app/
COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000
CMD [ "python", "app.py" ]

