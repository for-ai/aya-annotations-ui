# Start with the official Python 3.10 image
FROM python:3.10-slim-buster

# Set the working directory to /job
WORKDIR /job

# Copy the backend code into the container
COPY ./ /job/

# Install the dependencies using poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["python", "-m", "jobs.leaderboard_update_job", "--leaderboard", "daily"]