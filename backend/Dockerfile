

FROM python:3.9-slim

RUN pip install gunicorn


WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app/

# EXPOSE 8000

CMD gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000


