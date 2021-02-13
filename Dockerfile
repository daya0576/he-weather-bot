####################
#    How To Use    #
####################
# 1. docker build -t he_weather_image ./
# 2. docker run -d -p 80:80 -e  MODULE_NAME="app" -v /var/www/unswco:/unswco --name=he_weather he_weather_image

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

RUN poetry install --no-root --no-dev

COPY ./telegram_bot /app