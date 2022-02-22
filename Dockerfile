FROM python:3.8-slim

RUN pip install poetry
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

COPY mailroom mailroom

ENTRYPOINT ["poetry", "run"]

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "mailroom.app"]
