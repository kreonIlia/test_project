FROM python:3.11-slim

# Устанавливаем зависимости ОС
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

# Устанавливаем зависимости Python проекта
WORKDIR /app
COPY pyproject.toml /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY . /app

EXPOSE 8000

CMD alembic upgrade head && uvicorn src.application:app --host 0.0.0.0 --port 8000
