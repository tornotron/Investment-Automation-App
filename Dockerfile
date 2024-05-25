# Use the official Python base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . /code/

# Expose the port that the FastAPI application will run on
EXPOSE 8000

# Set the command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]