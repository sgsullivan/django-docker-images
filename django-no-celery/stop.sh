#!/bin/bash

set -eu

PROJECT_NAME=$1

export COMPOSE_PROJECT_NAME=${PROJECT_NAME} && docker-compose -p ${PROJECT_NAME} down
