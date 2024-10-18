import os
from celery import Celery
import django
from django.conf import settings
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sedreh.settings")
django.setup()
app = Celery("sedreh")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.broker_connection_retry_on_startup = True
app.conf.imports = ["user.tasks"]
app.conf.result_backend = settings.CELERY_BROKER_URL
app.conf.task_serializer = settings.CELERY_TASK_SERIALIZER
app.conf.result_serializer = settings.CELERY_RESULT_BACKEND
app.conf.accept_content = ["json"]
app.conf.result_expires = timedelta(days=1)
app.conf.task_always_eager = False
app.conf.worker_prefetch_multiplier = 8
