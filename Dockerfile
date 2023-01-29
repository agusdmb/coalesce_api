FROM python:3.10.6-slim-bullseye as prod

RUN pip3 install poetry==1.1.15

RUN useradd -m -s /bin/bash api && mkdir -p /code && chown api:api /code
USER api
WORKDIR /code

COPY pyproject.toml poetry.lock /code/
RUN poetry install --no-dev

COPY . /code

CMD "poetry", "run", "uvicorn", "coalesce_api.api:app"

FROM prod as dev

RUN poetry install

CMD ["poetry", "run", "uvicorn", "coalesce_api:app", "--reload"]
