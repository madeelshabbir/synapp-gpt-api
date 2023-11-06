# SynappGPT

- It is like a replica of ChatGPT

## Technology

- python-3.9.15

- pip-23.3.1

- django-4.2.1

- psql-14.5 (PostgreSQL)

## Development

### 1. Prerequisites

**For Linux**

- Install [Docker Engine](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/).

**For Mac**

- Install [Docker Desktop](https://docs.docker.com/desktop/install/mac-install/).

### 2. Initial Setup

Clone the project repository

      $ git clone https://<TOKEN>@github.com/Alishba-Saeed/synapp-gpt-api.git

Get into the project directory

      $ cd synapp-gpt-api

Copy `.env.example` to `.env`

      cp .env.example .env

- Update all missing values.

#### For Linux Only

- Update `DB_HOST` with the IP value of `inet ip` of `<BROADCAST,MULTICAST,UP,LOWER_UP>` received from following command

      ip a

### 3. Create Database

- Run DB container

      docker-compose -f docker-compose.dev.yml up --build db

- Open psql console

      docker exec -it <CONTAINER NAME> psql -U postgres

- Update password for user postgres

      \password postgres

- Run SQL query to create database

      CREATE DATABASE synappgpt;
      \q

- Stop the continer.

      docker stop <CONTAINER NAME>

### 4. Run the server

      docker-compose -f docker-compose.yml up --build

### 5. Create superuser and seed dummy data

- Open bash for app container

      docker exec -it <CONTAINER NAME> bash

- Create superuser

      python manage.py createsuperuser
