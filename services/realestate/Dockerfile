# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files to the working directory
COPY ./pyproject.toml ./poetry.lock ./

# Install Poetry
RUN pip install poetry

# Install the dependencies
RUN poetry install --no-root

# Copy the rest of the application code to the working directory
COPY ./app /app

# Expose the port that the gRPC server will run on
EXPOSE 50052

# Run the gRPC server
CMD ["poetry", "run", "python", "main.py"]
