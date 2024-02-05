# create a gcp cloud run job for the backend service
# with max retries 3 and timeout 5 minutes

# provide a set of options to the script, since there are 4 different
# leaderboard update jobs that need to be created:
# update_daily_leaderboard, update_weekly_leaderboard, 
# update_leaderboard_by_language (runs hourly), update_leaderboard_overall (runs hourly)

# usage: ./create-leaderboard-job.sh <JOB_TYPE> <schedule>
# example: ./create-leaderboard-job.sh daily "30 0 * * *"

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  echo "Usage: $0 <JOB_TYPE> [SCHEDULE]"
  echo "JOB_TYPE: daily, weekly, by_language, overall"
  echo "SCHEDULE (optional): cron schedule for the job in the format: '<minute> <hour> <day-of-month> <month> <day-of-week>'"
  exit 1
fi

JOB_TYPE=$1
SCHEDULE=$2

PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects list --filter="$(gcloud config get-value project)" --format="value(PROJECT_NUMBER)")
TAG=latest
# # replace underscores with dashes for the job type
JOB_TYPE=${JOB_TYPE//_/-}
JOB_NAME=${JOB_TYPE}-leaderboard-job
SERVICE_NAME=${JOB_NAME//-/_}
# replace dashes with underscores for the job name
IMAGE_NAME=instruct-multilingual-web-app-${SERVICE_NAME}
REGION=us-east1

GCR_IMAGE=gcr.io/$PROJECT_ID/$JOB_NAME:$TAG

echo "Creating job $JOB_NAME with schedule $SCHEDULE"

# build the docker image based on the job that needs to be created
echo "Building docker image for $SERVICE_NAME"
ENVIRONMENT=local docker-compose build $SERVICE_NAME

echo "Tagging docker image $IMAGE_NAME with gcr image name $GCR_IMAGE"
docker tag $IMAGE_NAME $GCR_IMAGE

if [ $? -ne 0 ]; then
    echo "Tagging failed. Exiting..."
    # Exit the script with a non-zero status code to indicate failure
    exit 1
fi


echo "Pushing docker image to gcr"
docker push $GCR_IMAGE

# NOTE: the job must be created first before it can be updated
echo "Creating job $JOB_NAME in cloud run"
gcloud run jobs update $JOB_NAME \
  --image $GCR_IMAGE \
  --max-retries 2 \
  --task-timeout 5m \
  --region us-east1 \
  --set-cloudsql-instances $PROJECT_ID:$REGION:instruct-multilingual-app-db \
  --vpc-connector $(gcloud secrets versions access latest --secret=VPC_CONNECTOR_BACKEND_PROD) \
  --set-secrets "INSTRUCT_MULTILINGUAL_APP_DB_URI=INSTRUCT_MULTILINGUAL_APP_DB_URI_PROD:latest" \
  --set-env-vars PROJECT_ID=$PROJECT_ID,ENVIRONMENT=production,DISCORD_API_BASE_URL=blank,DISCORD_CLIENT_ID=blank,DISCORD_CLIENT_SECRET=blank,DISCORD_REDIRECT_URI=blank,FRONTEND_URL=temp-placeholder-until-updated,FOR_AI_URL=blank,APP_NAME=${JOB_NAME},JWT_SECRET=SECRET_KEY,JWT_ALGORITHM=blank,JWT_EXPIRATION_TIME=30,GOOGLE_CLIENT_ID=blank,GOOGLE_CLIENT_SECRET=blank,GOOGLE_REDIRECT_URI=blank\
  --memory 512Mi \
  --cpu 2 \
  --execute-now \

#!/bin/bash

create_scheduler_job() {
    local SCHEDULER_URI="https://${REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${PROJECT_ID}/jobs/${JOB_NAME}:run"

    echo "Creating scheduler job for ${JOB_NAME} on schedule ${SCHEDULE} to trigger ${SCHEDULER_URI}"

    gcloud scheduler jobs update http scheduler-${SERVICE_NAME} \
        --location="${REGION}" \
        --schedule="${SCHEDULE}" \
        --uri="${SCHEDULER_URI}" \
        --http-method='POST' \
        --oauth-service-account-email="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
        --time-zone=UTC \
        --oauth-token-scope="https://www.googleapis.com/auth/cloud-platform"
}

# Call the function only if the --schedule flag is provided
# else, print that the job was created without a schedule
if [ -z "$SCHEDULE" ]; then
    echo "Created job ${JOB_NAME} without a schedule"
else
    create_scheduler_job
fi
