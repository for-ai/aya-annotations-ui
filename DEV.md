# Developer Setup

- [Dependencies](#dependencies)
  - [Install Docker](#install-docker)
- [Frontend](#frontend)
  - [How to setup](#how-to-setup)
- [Backend](#backend)
  - [Set up local environment variables](#set-up-local-environment-variables)
  - [Setup the application and database](#setup-the-application-and-database)
  - [Adding alembic migrations](#adding-alembic-migrations)
  - [Interacting with the database container](#interacting-with-the-database-container)
  - [Modifying leaderboard jobs](#modifying-leaderboard-jobs)
  - [Run unit tests](#run-unit-tests)
  - [Run in staging mode](#run-in-staging-mode)
  - [Run in production mode](#run-in-production-mode)
- [Deploying services to GCP Cloud Run (production)](#deploying-services-to-gcp-cloud-run-production)
- [Aya Analytics App](#aya-analytics-app)
  - [Set up local environment variables](#set-up-local-environment-variables-1)
  - [Install Requirements](#install-requirements)
  - [Run the application](#run-the-application)


# Dependencies

## Install Docker

Install Docker Desktop: https://docs.docker.com/get-docker/

# Frontend

## How to setup

1. Set up local environment variables

   For local dev, create a `.env` file at the root of the `frontend/` directory using the `.env.example` file:

   ```console
   cp .env.example .env
   ```

2. Install the dependencies.

   ```
   npm install
   ```

3. Run.
   ```
   npm run develop
   ```

- View the front page: [http://127.0.0.1:80](http://127.0.0.1:80)

# Backend

## Set up local environment variables

For local dev, create a `.env.local` file at the root of the `backend/` directory using the `.env.example` file:

```console
cp .env.example .env.local
```

## Setup the application and database

**NOTE:** You must pass an `ENVIRONMENT` variable to ensure you're running in the right env.

1. Run the app using `docker compose`:
```console
ENVIRONMENT=local docker compose up backend database --build
```
OR
```console
./run.sh
```
  - View the API docs: [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
2. Run all the alembic migrations to load the schema:
```console
ENVIRONMENT=local docker compose exec backend alembic upgrade head
```
3. Seed the local database:
```console
ENVIRONMENT=local docker compose exec backend python -m scripts.seed_db
```
  - This will add a fake user with a language code `spa` and country code `ES`, then create some tasks the user can edit / submit.


### Adding alembic migrations
[Alembic Docs](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

To add a migration run:

```console
alembic revision -m "some_revision_name"
```

Make sure you add an `upgrade()` and `downgrade()` step. Once your migration is added, rebuild the `backend container`, and test that we can upgrade and downgrade a couple times without the DB getting into a broken state:

```console
ENVIRONMENT=local docker compose exec backend alembic upgrade head
ENVIRONMENT=local docker compose exec backend alembic downgrade -1
```

To check the history of migrations run:

```console
ENVIRONMENT=local docker compose exec backend alembic history
```

### Interacting with the database container

The `docker compose` command will spin up the backend along with a postgres container that you can interact with.

To connect to the DB inside of docker, you can run:

```console
ENVIRONMENT=local docker compose exec database psql instruct_multilingual -U backendapp
```

and interactively query data in there such as:

```console
select * from language_code;
```

### Modifying leaderboard jobs

We currently have some Cloud Run Jobs that run on a scheduled basis via Cloud Scheduler. Each of these jobs runs in their own container, and live in the directory `backend/jobs/`, with each type of job in their own subdirectory like `daily/` and their own Dockerfile with a command they run.

They use the `leaderboard_update_job.py` script and have the same dependencies as the FastAPI server.

**Deploying jobs**

To deploy and modify the schedule of the jobs, you can use the ops script:

```console
ops/create-jobs.sh
```

Which will tell you the options you can use. You must pass a job type and a cron expression as a schedule.

**Running jobs locally**

You can run the leaderboard jobs locally with:

```
ENVIRONMENT=local docker compose up <job_type>_leaderboard_job --build
```

replacing `<job_type>` with the available options (see the `docker-compose.yaml` file).

## Run unit tests

Currently, we have a `.env.test` file that gets read in by unit tests. To run the unit tests, you'll need a local postgres database *or* run unit tests in the GitHub Actions workflow.

**Recommended:**
Run the dockerized postgresql instance using:

```
docker compose up database
```

then run unit tests, which will use the dockerized server and a database called `testdb`

```
ENVIRONMENT=test pytest
```

## Run in staging mode

For connecting to the staging database, credentials should be retrieved from GCP Secret Manager, or via a secure message channel.

1. Create a file called `.env.staging` in the root of the `backend/` project:

```console
cp .env.example .env.staging
```

2. Retrieve the staging database URL from GCP Secret Manager
3. Retrieve the staging discord keys from GCP Secret Manager
4. Replace the values in the `.env.staging` file with the staging values
5. Remove `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` fields
6. Start the server with `ENVIRONMENT=staging`:
```console
ENVIRONMENT=staging docker compose up backend --build
```

## Run in production mode

**NOTE:** Only run in production mode for read-operations and debugging.

For connecting to the production database, credentials should be retrieved from GCP Secret Manager, or via a secure message channel.

1. Create a file called `.env.production` in the root of the `backend/` project:

```console
cp .env.example .env.production
```

2. Retrieve the production database URL from GCP Secret Manager
3. Retrieve the production discord keys from GCP Secret Manager
4. Replace the values in the `.env.production` file with the production values
5. Remove `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` fields
6. Start the server with `ENVIRONMENT=production`:
```console
ENVIRONMENT=production docker compose up backend --build
```
  - This will connect to the production database so you don't need to run the local database container

# Deploying services to GCP Cloud Run (production)

To deploy the frontend / backend to GCP Cloud Run (production) there are a few involved steps. Namely:

- Building images
- Pushing to Container Registry
- Deploying the latest image to Cloud Run

This is automated via GCP Cloud Build. `cloudbuild-frontend.yaml` will automatically do the above steps if there are changes to the `frontend/` directory, and `cloudbuild-backend.yaml` will do the same if there are changes to the `backend/` directory.

# Aya Analytics App

## Set up local environment variables

For local dev, create a `.env.analytics-instruct-multilingual-app.local` file at the root of the `analytics/` directory and add the following environment variables to it:

```console
INSTANCE_CONNECTION_NAME="" # Cloud SQL instance connection name
DB_USER="" #user name to access DB
DB_PASS="" #password for DB
DB_NAME="" #name of the DB
C4AI_PROJECT_ID="" #C4AI GCP project ID
GRADIO_SERVER_NAME="0.0.0.0"
GRADIO_SERVER_PORT=8080
APP_ENVIRONMENT="local"
```

## Install Requirements

Create a python virtual environment and install the necessary libraries using `requirements.txt` file

```console
pip install -r requirements.txt
```

## Run the application

Run the app using `app.py`:
```console
python app.py
```

OR

You can also run the app in reload mode using below command:
```console
gradio app.py
```