# Start with the official Python 3.10 image
FROM python:3.10-slim-bullseye

# Update and install dependencies
RUN apt-get update && apt-get install -y gcc

# Set the working directory to /app
WORKDIR /backend

# Copy the backend code into the container
COPY ./ /backend/

# Install the dependencies using poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# Expose 
EXPOSE 8080

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
