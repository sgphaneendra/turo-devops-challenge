#!/bin/bash

set -e

export VERSION=$(git rev-parse --short HEAD)

IMAGE_NAME="nginx-static-app"
DOCKER_USER=$1
DOCKER_PWD=$2

echo "Logging into Docker Hub $DOCKER_USER"
echo "$DOCKER_PASSWORD" | docker login --username "$DOCKER_USER" --password "$DOCKER_PWD"


DOCKER_IMAGEREPO=${DOCKER_USER}/${IMAGE_NAME}

echo "Building Docker image: $DOCKER_IMAGEREPO with tag: $VERSION"


docker build -t $DOCKER_IMAGEREPO:$VERSION .

docker push $DOCKER_IMAGEREPO:$VERSION

if [ $? -eq 0 ]; then
    echo "Docker image build was successfull with DOCKER_TAG: $DOCKER_IMAGEREPO:$VERSION"
else
    echo "Failed to build Docker image $DOCKER_IMAGEREPO:$VERSION"
fi

docker logout