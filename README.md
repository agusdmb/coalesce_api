# How to run

## Running in Docker

To run the app

```bash
docker-compose up --build app
```

Then go to http://localhost:8080/docs

To run the tests

```bash
docker-compose up --build test
```

## Running locally

Install the app and requirements (better to use a virtualenv)

```bash
make init
```

To run the app

```bash
make run
```

Then go to http://localhost:8000/docs

To run the tests

```bash
make test
```
