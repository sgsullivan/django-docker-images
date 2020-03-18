from __future__ import absolute_import

from django.conf import settings
from celery import Celery

import os

projectName = os.environ.get('COMPOSE_PROJECT_NAME')

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', projectName + '.settings')

app = Celery(projectName)

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    broker_url=settings.RMQ_AMQP_CONNECTION_STRING,
    result_backend='rpc://',
    result_persistent=True,
    result_expires=30,
    beat_schedule={},
    task_acks_late=True,
)

