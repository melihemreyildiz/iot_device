# iot_device

# IoT Devices Management System

This project is an IoT device management system built using FastAPI, PostgreSQL, RabbitMQ, and Celery. It allows for the creation, deletion, and listing of devices, as well as managing location history and the last known location for all devices.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  1. [Clone the Repository](#1-clone-the-repository)
  2. [Environment Variables](#2-environment-variables)
  3. [Build and Run with Docker Compose](#3-build-and-run-with-docker-compose)
- [Running Tests](#running-tests)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Logging and Monitoring](#logging-and-monitoring)
- [Contribution Guidelines](#contribution-guidelines)
- [License](#license)

## Features
- **Device Management:** Create, delete, and list IoT devices.
- **Location Tracking:** Manage location history and last known location for devices.
- **Asynchronous Task Handling:** Utilize Celery for background task processing.
- **Scalable and Resilient:** Built with scalability and resilience in mind.

## Technologies Used
- **FastAPI:** A modern, fast (high-performance), web framework for building APIs with Python 3.7+.
- **PostgreSQL:** A powerful, open-source object-relational database system.
- **RabbitMQ:** A message broker for handling communication between services.
- **Celery:** An asynchronous task queue/job queue based on distributed message passing.

## Architecture
The architecture consists of a FastAPI application that interacts with a PostgreSQL database for storing device and location data. RabbitMQ is used as a message broker, and Celery handles background tasks.

## Prerequisites
- Docker and Docker Compose installed on your machine.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/melihemreyildiz/iot_device
cd iot_device
```

### 2. Environment Variables
Create a `.env` file in the root directory and add the following environment variables:

```env
DATABASE_URL=postgresql://iot:iot@db:5432/db
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
```

### 3. Build and Run with Docker Compose
```bash
docker-compose up --build
```
This will start the FastAPI application, PostgreSQL, RabbitMQ, and run the tests.

## Running Tests
To run tests, use the following command:

```bash
docker-compose run web tests
```
This will run the tests in the `tests` service defined in the `docker-compose.yml`.

You can also run services locally:
```bash
# Start the TCP server
python app/tcp_server.py

# Test the TCP server
python tests/manual_test_tcp_server.py

# Start Celery worker
celery -A app.tasks worker --loglevel=info

# Start FastAPI application
uvicorn app.main:app --reload
```

Update environment variables for local usage:
```env
DATABASE_URL=postgresql://iot:iot@localhost:5432/db
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
```

## Usage
After starting the services, you can access the FastAPI application at [http://localhost:8000](http://localhost:8000).

## API Documentation
FastAPI provides interactive API documentation at the following endpoints:
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Logging and Monitoring
- **FastAPI logs:** Available in the fastapi container logs.
- **RabbitMQ management UI:** Accessible at [http://localhost:15672](http://localhost:15672) (default credentials: guest/guest).

## Contribution Guidelines
Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests to us.

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.
