from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE","artisan.settings")


app = Celery('artisan')

app.config_from_object("django.conf:settings",namespace="CELERY")

app.autodiscover_tasks()