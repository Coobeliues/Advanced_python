#!/bin/bash
alembic revision --autogenerate -m "Reconciliation and daily amount tables" &
alembic upgrade head

sleep 5 


# cd modules
# python3 teleg.py &
# cd ..


python3 main.py

