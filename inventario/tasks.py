from __future__ import absolute_import, unicode_literals
from django.core.mail import send_mail
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings

logger = get_task_logger(__name__)

@shared_task(name="enviar_email")
def enviar_email(asunto, html, msg, envia):
    logger.info("enviando email")
    send_mail(
        subject=asunto,
        html_message=html,
        message=msg,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[envia],
        fail_silently=False
    )
