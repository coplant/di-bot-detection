#!/bin/bash
cd /code

celery -A proxy.src.background.celery worker --loglevel=info
