import os
from celery import Celery

redis_url = os.getenv('REDIS_URL')
if not redis_url:
    raise RuntimeError('REDIS_URL is not configured')
celery_app = Celery('marketplace', broker=redis_url, backend=redis_url)

# ssl parameters enabled
if redis_url is not None:
    if redis_url.startswith('rediss://'):
        celery_app.conf.update(
            broker_use_ssl={"ssl_cert_reqs": "none"},
            redis_backend_use_ssl={"ssl_cert_reqs": "none"}
        )

import app.tasks.email_tasks
import app.tasks.result_tasks
celery_app.autodiscover_tasks(['app.tasks'])
print('ACTIVE REDIS URL:', redis_url)
print(celery_app.tasks.keys())
