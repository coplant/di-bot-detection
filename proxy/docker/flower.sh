#!/bin/bash
cd /code

celery -A proxy.src.assessment.background.celery flower
