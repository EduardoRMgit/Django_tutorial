from cactus.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from cactus.settings import AUTH_PWD
import logging

db_logger = logging.getLogger('db')


def mandar_email(correo, username):

    receptor = correo
    subject = 'Bienvenido a Inguz'
    html_message = render_to_string('mail/correo.html',
                                    {'username': username})
    body = strip_tags(html_message)
    try:
        send_mail(
            subject,
            body,
            EMAIL_HOST_USER,
            [receptor],
            auth_password=AUTH_PWD,
            fail_silently=False,
            html_message=html_message
        )
    except Exception as e:
        msg_mail = "[Send Mail] Error al mandar mail" \
                   f"para el usuario: {username}"
        db_logger.warning(f"{msg_mail}:error {e}")
