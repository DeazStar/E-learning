#!/bin/bash

COMMAND=$1

function run() {
  # Step 1: Create the kong-net network
  echo "Creating Docker network 'kong-net'..."
  docker network create kong-net

  # Step 2: Run the kong-dbless container
  echo "Starting the Kong container..."
  docker run -d --name kong-dbless \
    --network=kong-net \
    -v "$(pwd):/kong/declarative/" \
    -e "KONG_DATABASE=off" \
    -e "KONG_DECLARATIVE_CONFIG=/kong/declarative/kong.yml" \
    -e "KONG_PROXY_ACCESS_LOG=/dev/stdout" \
    -e "KONG_ADMIN_ACCESS_LOG=/dev/stdout" \
    -e "KONG_PROXY_ERROR_LOG=/dev/stderr" \
    -e "KONG_ADMIN_ERROR_LOG=/dev/stderr" \
    -e "KONG_ADMIN_LISTEN=0.0.0.0:8002, 0.0.0.0:8445 ssl" \
    -e "KONG_ADMIN_GUI_URL=http://localhost:8002" \
    -p 8000:8000 \
    -p 8443:8443 \
    -p 127.0.0.1:8002:8002 \
    -p 127.0.0.1:8445:8445 \
    kong:3.9.0

  # Wait for Kong to start
  echo "Waiting for Kong to initialize..."
  sleep 5

  # Step 3: Build and run the auth_service container
  echo "Building and starting the auth_service container..."
  cd ../auth_service || exit
  docker build -t auth-service .
  docker run -d --name auth-service \
    --network=kong-net \
    -p 127.0.0.1:8001:8001 \
    auth_service

  echo "Setup completed. Kong and auth_service are running."
}

function clean() {
  echo "Stopping and removing the 'kong-dbless' container..."
  docker stop kong-dbless 2>/dev/null
  docker rm kong-dbless 2>/dev/null

  echo "Stopping and removing the 'auth_service' container..."
  docker stop auth-service 2>/dev/null
  docker rm auth-service 2>/dev/null

  echo "Removing the 'kong-net' network..."
  docker network rm kong-net 2>/dev/null

  echo "Clean-up completed for Kong, auth-service, and kong-net."
}

case $COMMAND in
  run)
    run
    ;;
  clean)
    clean
    ;;
  *)
    echo "Usage: $0 {run|clean}"
    exit 1
    ;;
esac
