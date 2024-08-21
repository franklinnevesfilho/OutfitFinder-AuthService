# Use an official Python runtime as a parent image
FROM python:3.12.4-slim

# Set the working directory to /auth-service
WORKDIR /auth-service

# Copy the current directory contents into the container at /auth-service
COPY ../app /auth-service/app
COPY ../requirements.txt /auth-service
COPY ../main.py /auth-service

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

RUN useradd -m myuser
USER myuser


# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
