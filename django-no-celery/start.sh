#!/bin/bash

export COMPOSE_PROJECT_NAME=erste && export POSTGRES_PASSWORD=p455w0rd && docker-compose -p erste up --build -d

