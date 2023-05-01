#!/bin/bash
cd /code

celery -A proxy.src.background.celery flower
