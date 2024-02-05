# Use an official Node.js runtime as a parent image
FROM node:16.11.0-alpine3.14

ARG ENVIRONMENT
ENV ENVIRONMENT=${ENVIRONMENT}

ARG GOOGLE_ANALYTICS_ID
ENV GOOGLE_ANALYTICS_ID=${GOOGLE_ANALYTICS_ID}

# Set the working directory to /frontend
WORKDIR /frontend

# Copy the frontend code into the container
COPY ./ /frontend/

# Install dependencies using npm
RUN npm install

# Build the production version of the app
RUN npm run build

EXPOSE 80

# Define the command to start the app
CMD ["npm", "start"]
