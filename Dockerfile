FROM tiangolo/uvicorn-gunicorn:python3.9

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt --index-url https://pypi.org/simple --default-timeout=1000

COPY . .
CMD ["uvicorn", "telegram_bot.app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]
