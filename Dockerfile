FROM tiangolo/uvicorn-gunicorn:python3.9

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Install redis
RUN set -ex; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        redis-server \
    ; \
    rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["uvicorn", "telegram_bot.app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]
