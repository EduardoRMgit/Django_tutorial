from cactus.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def mandar_email(correo, username):

    receptor = correo
    user = username
    print(correo, username)
    subject = 'Bienvenido a Inguz'
    html_message = render_to_string(f'mail/correo.html',
                                   {'username': user})
    body = strip_tags(html_message)


    send_mail(
        subject,
        body,
        EMAIL_HOST_USER,
        [receptor],
        auth_password='pipweonnrzertwfv',
        fail_silently=False,
        html_message=html_message
    )
