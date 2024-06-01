# Stage 1: Build the React app
FROM node:14 AS react-build

# Set the working directory
WORKDIR /app

# Copy the React app source code
COPY client/ /app/

# Install the dependencies and build the React app
RUN cd client
RUN npm install
RUN npm run dev
RUN cd ..

# Stage 2: Setup the Flask app
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the Flask app source code
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY app.py /app/

# COPY ./database/database_dump.sql /docker-entrypoint-initdb.d/init.sql

# Expose the port the app runs on
EXPOSE 5000
EXPOSE 5175

# Command to run the Flask app
CMD ["flask", "run"]
CMD ["cd", "client"]
CMD ["npm", "run", "dev"]