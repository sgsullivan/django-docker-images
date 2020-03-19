#!/bin/bash

set -eu

PROJECT_NAME=$1
WEB_PORT=$2
SSH_PORT=$3

export WEB_PORT=${WEB_PORT}
export SSH_PORT=${SSH_PORT}
export COMPOSE_PROJECT_NAME=${PROJECT_NAME}
export POSTGRES_PASSWORD=${POSTGRES_PASSWORD}

[[ -d /var/sites/${PROJECT_NAME}/django ]] || mkdir -p /var/sites/${PROJECT_NAME}/django

useradd ${PROJECT_NAME} -d /home/${PROJECT_NAME} -s /bin/bash

[[ -n ${SSH_PUB_KEY:-} ]] && {
  mkdir -p /var/sites/${PROJECT_NAME}/django/.ssh
  chmod 700 /var/sites/${PROJECT_NAME}/django/.ssh
  echo "${SSH_PUB_KEY}" > /var/sites/${PROJECT_NAME}/django/.ssh/authorized_keys
}

cat << EOF > /var/sites/${PROJECT_NAME}/django/.profile
export POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
export COMPOSE_PROJECT_NAME=${PROJECT_NAME}

alias ls="ls --color"
alias ll="ls -la --color"
EOF

chown -R ${PROJECT_NAME}.${PROJECT_NAME} /var/sites/${PROJECT_NAME}/django

docker-compose -p ${PROJECT_NAME} up --build -d
