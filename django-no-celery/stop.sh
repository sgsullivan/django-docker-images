#!/bin/bash

set -eu

PROJECT_NAME=$1

export COMPOSE_PROJECT_NAME=${PROJECT_NAME} && export POSTGRES_PASSWORD=${POSTGRES_PASSWORD} && docker-compose -p ${PROJECT_NAME} down
