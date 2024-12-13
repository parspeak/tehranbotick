import requests
from celery import shared_task
from django.conf import settings


@shared_task
def send_otp(phone_number, otp):
    try:
        response = requests.post(settings.SMS_PANEL_API, headers={
            "apikey": settings.SMS_PANEL_API_KEY,
            "content-type": "application/x-www-form-urlencoded"
        }, data={
            "receptor": phone_number,
            "type": 1,
            "template": settings.SMS_PANEL_TEMPLATE_NAME,
            "param1": str(otp)
        })
    except:
        pass
