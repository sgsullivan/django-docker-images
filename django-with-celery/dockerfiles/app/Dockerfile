FROM python:3
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client vim \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /lw
RUN mkdir -p /app
COPY . /lw
WORKDIR /lw
RUN pip install -r initial-requirements.txt
RUN pip freeze --local > requirements.txt
WORKDIR /app
