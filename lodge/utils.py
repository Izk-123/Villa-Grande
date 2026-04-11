# lodge/utils.py
import os
from twilio.rest import Client
from django.conf import settings
from django.core.mail import send_mail

def send_whatsapp_message(to_phone, message):
    """Send a WhatsApp message via Twilio."""
    if not settings.TWILIO_ACCOUNT_SID:
        # For development: fallback to print
        print(f"WhatsApp message to {to_phone}: {message}")
        return
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=settings.TWILIO_WHATSAPP_FROM,
        to=f'whatsapp:{to_phone}'
    )

def send_email_message(to_email, subject, message):
    """Send an email using Django's email backend."""
    if not to_email:
        return
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        fail_silently=False,
    )