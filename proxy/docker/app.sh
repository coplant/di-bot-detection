#!/bin/bash
cd ..

alembic -c proxy/alembic.ini upgrade head

gunicorn proxy.src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:7000
