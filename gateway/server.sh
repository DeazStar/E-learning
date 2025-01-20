#!/bin/bash

COMMAND=$1

function build_custom_kong_image() {
  echo "Pulling the official Kong image..."
  docker pull kong:3.9.0

  echo "Building the custom Kong image with the middleman plugin..."
  cat > Dockerfile.kong <<EOF
FROM kong:3.9.0

USER root

# Install required build tools
RUN apt-get update && apt-get install -y gcc make musl-dev && rm -rf /var/lib/apt/lists/*

# Install the middleman plugin
RUN luarocks install kong-plugin-the-middleman

USER kong

# Expose necessary ports
EXPOSE 8000 8443 8002 8445
EOF

  docker build -f Dockerfile.kong -t kong-with-middleman .
  if [ $? -eq 0 ]; then
    echo "Custom Kong image built successfully."
  else
    echo "Failed to build the custom Kong image."
    exit 1
  fi

  rm Dockerfile.kong
}



function run() {
  # Step 1: Build the custom Kong image
  build_custom_kong_image

  # Step 2: Create the kong-net network
  echo "Creating Docker network 'kong-net'..."
  docker network create kong-net

  # Step 3: Create rabbit-mq netowrk
  echo "Creating Docker network 'rabit-mq-net"
  docker network create rabbit-mq-net

  # Setp 4: Run rabbit Mq
  echo "Starting rabbit mq" 
  docker run -d --rm --name rabbitmq --network rabbit-mq-net -p 5672:5672 -p 15672:15672 rabbitmq:4.0-management


  # Step 3: Run the kong-dbless container with the custom image
  echo "Starting the Kong container with the middleman plugin pre-installed..."
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
    -e "KONG_PLUGINS=bundled,the-middleman" \
    -p 8000:8000 \
    -p 8443:8443 \
    -p 127.0.0.1:8002:8002 \
    -p 127.0.0.1:8445:8445 \
    kong-with-middleman

  # Wait for Kong to start
  echo "Waiting for Kong to initialize..."
  sleep 5

  # Step 4: Build and run the auth_service container
  echo "Building and starting the auth_service container..."
  cd ../auth_service || exit
  docker build -t auth-service .
  docker run -d --name auth-service \
    --network=kong-net \
    --network=rabbit-mq-net \
    -p 127.0.0.1:8001:8001 \
    auth-service

  echo "Setup completed. Kong and auth_service are running."

  # Step 5: Build and run the course_management_service container
  echo "Building and starting the course_management_service container..."
  cd ../course_management || exit
  docker build -t course-management-service .
  docker run -d --name course-management-service \
    --network=kong-net \
    -p 127.0.0.1:8005:8005 \
    course-management-service
  

  # Step 5: Build and run the notification service container
  echo "Building and starting the notification_service container..."
  cd ../notification_service || exit
  docker build -t notification-service .
  docker run -d --name notification-service \
    --network=rabbit-mq-net \
    -p 127.0.0.1:8007:8007 \
    notification-service
  
  echo "Setup completed. Kong and course_management_service are running."
}

function clean() {
  echo "Stopping and removing the 'kong-dbless' container..."
  docker stop kong-dbless 2>/dev/null
  docker rm kong-dbless 2>/dev/null

  echo "Stopping and removing the 'rabbit-mq-net' container..."
  docker stop rabbit-mq-net 2>/dev/null
  docker rm rabbit-mq-net 2>/dev/null

  echo "Stoppoing and removing rabbit mq conatiner...."
  docker stop rabbitmq 2>/dev/null
  docker rm rabbitmq 2>/dev/null

  echo "Stopping and removing the 'auth_service' container..."
  docker stop auth-service 2>/dev/null
  docker rm auth-service 2>/dev/null

  echo "Stopping and removing the 'course_management_service' container..."
  docker stop course-management-service 2>/dev/null
  docker rm course-management-service 2>/dev/null

  echo "Stopping and removing the 'notification_service' container..."
  docker stop notification-service 2>/dev/null
  docker rm notification-service 2>/dev/null

  echo "Removing the 'kong-net' network..."
  docker network rm kong-net 2>/dev/null

  echo "Removing the 'kong-net' network..."
  docker network rm rabit-mq-net 2>/dev/null

  echo "Clean-up completed for Kong, auth-service, course_management_service, and kong-net."
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
