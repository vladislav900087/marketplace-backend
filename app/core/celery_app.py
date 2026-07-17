import os
from celery import Celery

broker_url = os.getenv('CELERY_BROKER_URL') or os.getenv('REDIS_URL')
result_backend = os.getenv('CELERY_RESULT_BACKEND') or broker_url

if not broker_url:
    raise RuntimeError('CELERY_BROKER_URL OR REDIS_URL is not configured')
celery_app = Celery('marketplace', broker=broker_url, backend=result_backend)

# ssl parameters enabled

if broker_url.startswith('rediss://'):
    celery_app.conf.update(
        broker_use_ssl={"ssl_cert_reqs": "none"},
        redis_backend_use_ssl={"ssl_cert_reqs": "none"}
    )

import app.tasks.email_tasks
import app.tasks.result_tasks
celery_app.autodiscover_tasks(['app.tasks'])
print('ACTIVE REDIS URL:', broker_url)
print(celery_app.tasks.keys())
