import time

from celery import Celery

from proxy.src.config import REDIS_URL

celery = Celery("analyzing", broker=REDIS_URL)


@celery.task
def analyze_fingerprint():
    time.sleep(10)
    return {"hello": "world"}
