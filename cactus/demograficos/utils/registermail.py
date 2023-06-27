import mailchimp_marketing as MailchimpMarketing
import logging
from mailchimp_marketing.api_client import ApiClientError
from django.conf import settings

db_logger = logging.getLogger('db')


def RegistrarMail(user):
    # Marketing
    try:
        client = MailchimpMarketing.Client()
        client.set_config({
            "api_key": settings.MAILCHIMP_KEY,
            "server": settings.MAILCHIMP_SERVER
        })

        response = client.lists.add_list_member(
            settings.MAILCHIMP_ID, {
                           "email_address": user.email,
                           "status": "subscribed"})
        db_logger.info(
            f"[Subcription mailchimp]: {user}"
            f"response: {response}"
        )
    except ApiClientError as error:
        print("Error: {}".format(error.text))
        msg_mailchimp = (
            f"[Error mailchimp] Error al suscribir al usuario"
            f"con el email: {user.email}. Error: {error.text}")
        db_logger.warning(msg_mailchimp)
    # Clientes
    if settings.SITE == "prod":
        try:
            client = MailchimpMarketing.Client()
            client.set_config({
                "api_key": settings.MAILCHIMP_KEY_C,
                "server": settings.MAILCHIMP_SERVER_c
            })

            response = client.lists.add_list_member(
                settings.MAILCHIMP_ID_C, {
                               "email_address": user.email,
                               "status": "subscribed"})
            db_logger.info(
                f"[Subcription mailchimp]: {user}"
                f"response: {response}"
            )
        except ApiClientError as error:
            print("Error: {}".format(error.text))
            msg_mailchimp = (
                f"[Error mailchimp] Error al suscribir al usuario"
                f"con el email: {user.email}. Error: {error.text}")
            db_logger.warning(msg_mailchimp)
