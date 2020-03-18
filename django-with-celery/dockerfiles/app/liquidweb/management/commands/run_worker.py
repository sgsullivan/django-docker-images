import os
import shlex
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import autoreload


def start_celery():
    cmd = 'celery -B -A {app} worker -l info --max-memory-per-child 180000 --concurrency {num_of_workers} -O fair'.format(
        app=os.environ.get('COMPOSE_PROJECT_NAME', 'site'),num_of_workers=os.environ.get('CELERY_WORKERS', 5))
    subprocess.call(shlex.split(cmd))

class Command(BaseCommand):
    def handle(self, *args, **options):
        start_celery()

