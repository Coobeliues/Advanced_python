FROM python:3.9-slim

RUN pip install psycopg2-binary
RUN pip install gunicorn
RUN mkdir /app
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app/

COPY DejaVuSans.ttf /app/modules/DejaVuSans.ttf
COPY dbase /app/modules/dbase
COPY modules /app/modules
RUN chmod a+x docker/*.sh


WORKDIR /app
CMD ["gunicorn", "app:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
