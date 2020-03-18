FROM python:3
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /lw
RUN mkdir -p /app
COPY . /lw
WORKDIR /lw
RUN pip install -r requirements.txt
WORKDIR /app
