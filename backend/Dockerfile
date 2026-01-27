# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files to the working directory
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install poetry

# Install the dependencies
RUN poetry install --no-root

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port that the FastAPI app will run on
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["poetry", "run", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
