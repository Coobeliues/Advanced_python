# FROM python:3.9-slim

# ENV PYTHONPATH "${PYTHONPATH}:/appp"
# RUN pip install psycopg2-binary
# RUN pip install gunicorn

# RUN mkdir /appp
# WORKDIR /appp

# COPY requirements.txt .
# RUN pip install -r requirements.txt

# COPY . /appp

# COPY DejaVuSans.ttf /app/modules/DejaVuSans.ttf

# RUN chmod a+x docker/*.sh

# WORKDIR /appp
# CMD gunicorn appp:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
FROM python:3.9-slim

RUN mkdir /appp
ENV PYTHONPATH "${PYTHONPATH}:/appp"
WORKDIR /appp
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /appp

COPY DejaVuSans.ttf /appp/modules/DejaVuSans.ttf
RUN pip install aiogram 
RUN chmod a+x docker/*.sh

# CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000","./docker/app.sh"]
CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker--bind=0.0.0.0:8000
