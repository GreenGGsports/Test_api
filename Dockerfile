# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Gunicorn will run on
EXPOSE 8888

# Command to run the app with Gunicorn, listening on port 8888
CMD exec gunicorn --bind :8888 app:app
