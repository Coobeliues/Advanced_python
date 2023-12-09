#!/bin/bash

alembic revision --autogenerate -m "Reconciliation and daily amount tables"
alembic upgrade head
cd modules
python3 teleg.py
cd ..
python3 main.py
# gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
