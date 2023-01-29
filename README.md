Implemented everything following TDD, checkout the git history for more insight.
I committed often prepending "WIP" to the commit's message to evidence the TDD
process, I don't do that on a regular basis, instead I would wait for the whole
"Red, Green, Refactor" cycle to be finished before committing.

## Design Decision

To keep things simple (and the examples) I'm using integers for money values. In
the real world I should use decimal numbers, to achieve this in the code I
would actually keep using integers but I would represent the cents with it, (so
basically 100 units would be a dollar and 50 would be 50 cents). Operating this
way is preferred when using currencies.

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
