import logging, random
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from threading import Thread
from django.contrib.auth.hashers import make_password
from authentication.models import OTP
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q

# to send email in parallel thread
def execute_in_background(function):
    def start_thread(*args, **kwargs):
        thread = Thread(target=function, args=args, kwargs=kwargs)
        thread.start()
    return start_thread

# to send email & handle logs
logger = logging.getLogger(__name__)

@execute_in_background
def send_email(html_template, context):
    from_email = settings.SERVER_EMAIL
    subject = context.get('subject')
    to_email = context.get('to_email')
    cc = context.get('cc')
    bcc = context.get('bcc')
    attachments = context.get('attachments')

    if not to_email:
        raise ValueError("The 'to_email' address must be provided and cannot be empty.")
    elif not isinstance(to_email, list):
        to_email = [to_email]

    try:
        html_message = render_to_string(html_template, context)
        message = EmailMessage(subject=subject, body=html_message, from_email=from_email, to=to_email, cc=cc, bcc=bcc,
                               attachments=attachments)
        message.content_subtype = 'html'
        result = message.send()
        logger.info(f"Sending email to {', '.join(to_email)} with subject: {subject} - Status {result}")
    except Exception as e:
        logger.info(f"Sending email to {', '.join(to_email)} with subject: {subject} - Status 0")
        logger.exception(e)

# to generate otp
def generate_otp(email):
    otp = 0
    while otp == 0:
        otp = str(random.randint(100000, 999999))

        # save otp to validate
        hashed_otp = make_password(otp)
        otp_exist = OTP.objects.filter(
            Q(otp_hash=hashed_otp),
            Q(expires_at__gt = timezone.now())
        )
        if not otp_exist.exists():
            new_otp = OTP(
                email = email,
                otp_hash = hashed_otp,
                expires_at = timezone.now() + timedelta(minutes=5)
            )
            new_otp.save()
            return otp
        otp = 0