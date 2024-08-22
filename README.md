# Authentication Service For Outfit Finder

This service is responsible for authenticating users and authorizing them to access the outfit finder services.

## Features

- User registration
- User login
- User logout
- User password reset
- User profile update
- User profile retrieval
- User profile deletion

## Libraries


## Setup

1. Clone the repository
2. Create a `.env` file in the root directory and add the following environment variables:
    ```bash
    MYSQL_ROOT_PASSWORD=<root_password>
    MYSQL_DATABASE=<database_name
    MYSQL_USER=<user>
    MYSQL_PASSWORD=<password>
    MYSQL_HOST=<host>
    MYSQL_PORT=<port>
    MINIO_ROOT_USER=<root_user>
    MINIO_ROOT_PASSWORD=<root_password
    MINIO_HOST=<host>
    MINIO_PORT=<port>
    MINIO_BUCKET=<bucket>
    ```
   
3. Run the following command to start the services:
    ```bash
    docker-compose up
    ```
