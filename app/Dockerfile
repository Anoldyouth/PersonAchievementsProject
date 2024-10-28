FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Устанавливаем переменную окружения для Poetry
ENV PATH="/root/.local/bin:$PATH"

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем зависимости через Poetry
RUN /root/.local/bin/poetry install --no-dev

# Копируем остальную часть кода приложения
COPY . /app

# Команда для запуска вашего приложения
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
