# FROM python:3.9

# RUN mkdir /fastapi_app

# WORKDIR /fastapi_app

# COPY requirements.txt .

# RUN pip install -r requirements.txt

# COPY . .

# COPY .env .

# CMD gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

FROM python:3.9-slim

RUN pip install gunicorn

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

# Use the official PostgreSQL image as a parent image
# FROM postgres:latest

# # Set the environment variables
# ENV POSTGRES_DB=egov
# ENV POSTGRES_USER=postgres
# ENV POSTGRES_PASSWORD=601246

# # Expose the PostgreSQL port
# EXPOSE 5432

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
# CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "-b", "0.0.0.0:8000", "--reload"]
CMD gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000


