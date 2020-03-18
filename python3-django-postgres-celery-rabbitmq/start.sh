#!/bin/bash

set -eu

PROJECT_NAME=$1
WEB_PORT=$2

export WEB_PORT=${WEB_PORT}
export COMPOSE_PROJECT_NAME=${PROJECT_NAME}
export POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
export RMQ_CLUSTER='rabbitmq'
export RMQ_USER=${PROJECT_NAME}
export RMQ_PASSWORD=${RMQ_PASSWORD}

docker-compose -p ${PROJECT_NAME} up --build -d
