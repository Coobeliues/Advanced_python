

FROM python:3.9-slim

# RUN apt-get update \
#     && apt-get install -y libpq-dev gcc \
#     && apt-get clean

# # Установка psycopg2
RUN pip install psycopg2-binary
RUN pip install gunicorn
RUN mkdir /app
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app/

RUN chmod a+x docker/*.sh
 
# RUN alembic upgrade head
# EXPOSE 8000

CMD gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000


