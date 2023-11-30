#!/bin/bash
alembic revision --autogenerate -m "Reconciliation and daily amount tables"
alembic upgrade head
gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
