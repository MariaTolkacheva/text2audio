# 🚀 FastAPI App with Docker Compose

This project runs a **FastAPI application** along with its dependencies (**PostgreSQL/MySQL, Redis, etc.**) using **Docker Compose**.  
It also includes support for running tests inside a containerized environment.

---

## 📦 Requirements

- [Docker](https://docs.docker.com/get-docker/)  
- [Docker Compose](https://docs.docker.com/compose/)

---

## 🏃 Running the Application

To build and start all services (app + dependencies):

```sh
docker-compose up --build
```

To stop everything

```sh
docker compose down
```
---

## 🏃 Testing (without docker-compose)

If you want to test:
1. Start dependencies:
```sh
docker compose up -d db redis
```
2. Run tests in a new container:
```sh
docker compose run --rm fastapi_app pytest
```
3. Shut down dependencies:
```sh
docker compose down
```
