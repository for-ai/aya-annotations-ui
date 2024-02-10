#!/bin/bash

if [ $# -ne 2 ]; then
  echo "Usage: $0 <SERVICE> <TAG>"
  exit 1
fi

SERVICE=$1
TAG=$2

PROJECT_ID=$(gcloud config get-value project)

docker tag instruct-multilingual-web-app_${SERVICE} \
  us-east1-docker.pkg.dev/${PROJECT_ID}/web-app/${SERVICE}:${TAG}

docker push us-east1-docker.pkg.dev/${PROJECT_ID}/web-app/${SERVICE}:${TAG}
