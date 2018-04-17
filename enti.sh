#!/usr/bin/env bash

CMD="$1"
TAG="$2"

if [ "$CMD" = "start" ]; then
  if [ ! -f ".env" ]; then
    echo "Environment file '.env' not found."
    echo "A sample environment file is available at './env.sample'."
    echo "See instructions in README.md to create application environment."
  else
    echo "Loading environment (Note: Stored settings will not be overwritten)."
    source .env
    echo "Starting Enti Server"
    docker-compose up -d
  fi

elif [ "$CMD" = "stop" ]; then
  echo "Stopping Enti Server"
  docker-compose stop

elif [ "$CMD" = "down" ]; then
  echo "Removing Enti Server"
  docker-compose down --remove-orphans

elif [ "$CMD" = "update" ]; then
  docker pull jrgoulet/enti:latest

elif [ "$CMD" = "logs" ]; then
  docker-compose logs -f --tail 200

elif [ "$CMD" = "deploy" ]; then
  if [ -z "$TAG" ]; then
    echo "Usage: ./enti deploy [tag]"
  else
    echo "Deploying jrgoulet/enti:$TAG"
    docker tag enti_ui jrgoulet/enti:$TAG
    docker tag enti_ui jrgoulet/enti:latest
    docker push jrgoulet/enti:$TAG
    docker push jrgoulet/enti:latest
  fi
fi

