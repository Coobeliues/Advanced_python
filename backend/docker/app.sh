#!/bin/bash
alembic revision --autogenerate -m "Recreating tables" &
alembic upgrade head

sleep 5 


cd modules
python3 teleg.py &
cd ..


python3 main.py

