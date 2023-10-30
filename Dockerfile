FROM tiangolo/uvicorn-gunicorn:python3.9

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt --default-timeout=3000

COPY . .
CMD ["uvicorn", "telegram_bot.app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]
