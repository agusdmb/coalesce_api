Implented everything following TDD, checkout the git history for more insight.
I commited often prepending "WIP" to the commit's message to evidence the TDD
process, I don't do that on a regular basis, instead I would wait for the whole
"Red, Green, Refactor" cycle to be finished before commiting.

## TO DO

- Make http calls concurrent (using python async framework)
- Store sources on a DB
- Make a interface to add and remove sources
- Allow the user to change strategy from the endpoint

## How to run

### Running in Docker

To run the app

```bash
docker-compose up --build app
```

Then go to http://localhost:8080/docs

To run the tests

```bash
docker-compose up --build test
```

### Running locally

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
