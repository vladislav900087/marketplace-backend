from celery import Celery


celery_app = Celery('marketplace', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

import app.tasks.email_tasks
import app.tasks.result_tasks
celery_app.autodiscover_tasks(['app.tasks'])
print(celery_app.tasks.keys())
