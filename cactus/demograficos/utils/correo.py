from django.core.mail import EmailMultiAlternatives
from cactus.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def mandar_email(correo, username):

    receptor = correo
    user = username
    print(correo, username)
    d = {'username': user}
    subject = 'Bienvenido a Inguz'
    html_content = render_to_string("mail/correo1.html",{'username': user})
    print(html_content)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject,
        text_content,
        EMAIL_HOST_USER,
        [receptor]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    # send_mail(
    #     subject,
    #     body,
    #     EMAIL_HOST_USER,
    #     [receptor],
    #     auth_password='pipweonnrzertwfv',
    #     fail_silently=False
    # )
