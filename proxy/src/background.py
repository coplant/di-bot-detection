import time

from celery import Celery

from proxy.src.config import REDIS_URL
from proxy.src.service.schemas import FingerprintSchema

celery = Celery("analyzing", broker=REDIS_URL, backend=REDIS_URL)


@celery.task
def analyze_fingerprint(fingerprint: FingerprintSchema):
    fingerprint = FingerprintSchema.parse_obj(fingerprint)
    time.sleep(10)
    return fingerprint.webRTC.value
