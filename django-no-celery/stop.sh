#!/bin/bash

set -eu

PROJECT_NAME=$1
WEB_PORT=$2

export WEB_PORT=${WEB_PORT} && export COMPOSE_PROJECT_NAME=${PROJECT_NAME} && docker-compose -p ${PROJECT_NAME} down
