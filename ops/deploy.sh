#!/bin/bash

# Parse command-line arguments
while getopts i:t:p:r: option
do
case "${option}"
in
i) SERVICE_IMAGE_NAME=${OPTARG};;
t) IMAGE_TAG=${OPTARG};;
p) PORT=${OPTARG};;
r) REGION=${OPTARG};;
esac
done

# Set default values
REGION=${REGION:-us-east1}
CPU=2
MEMORY=2Gi
CONCURRENCY=5
ENVIRONMENT=production
MIN_INSTANCES=2
MAX_INSTANCES=10
VPC_CONNECTOR=$(gcloud secrets versions access latest --secret=VPC_CONNECTOR_BACKEND_PROD)

PROJECT_ID=$(gcloud config get-value project)
IMAGE_URI="us-east1-docker.pkg.dev/$PROJECT_ID/web-app/$SERVICE_IMAGE_NAME:$IMAGE_TAG"

# Deploy the image to Cloud Run
gcloud run deploy $SERVICE_IMAGE_NAME \
    --image $IMAGE_URI \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --concurrency $CONCURRENCY \
    --cpu $CPU \
    --memory $MEMORY \
    --port $PORT \
    --set-cloudsql-instances $PROJECT_ID:$REGION:instruct-multilingual-app-db \
    --vpc-connector $VPC_CONNECTOR \
    --min-instances $MIN_INSTANCES \
    --max-instances $MAX_INSTANCES \
    --update-secrets "INSTRUCT_MULTILINGUAL_APP_DB_URI=INSTRUCT_MULTILINGUAL_APP_DB_URI_PROD:latest,\
DISCORD_CLIENT_ID=DISCORD_CLIENT_ID:latest,\
DISCORD_CLIENT_SECRET=DISCORD_CLIENT_SECRET:latest,\
DISCORD_REDIRECT_URI=DISCORD_REDIRECT_URI:latest, \
FRONTEND_URL=FRONTEND_URL:latest" \
    --set-env-vars "ENVIRONMENT=${ENVIRONMENT}"

if [ $? -eq 0 ]; then
  SERVICE_URL=$(gcloud run services describe $SERVICE_IMAGE_NAME --platform managed --region $REGION --format "value(status.url)")
  echo "Deployment successful. Service URL: $SERVICE_URL"
else
  echo "Deployment failed. Please check the UI or Log Analytics to troubleshoot."
fi