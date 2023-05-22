import mailchimp_marketing as MailchimpMarketing
import logging
from mailchimp_marketing.api_client import ApiClientError
from cactus.settings import cluster_secret

db_logger = logging.getLogger('db')


def RegistrarMail(user):
    try:
        client = MailchimpMarketing.Client()
        client.set_config({
            "api_key": cluster_secret('mailchimp-credentials', 'key'),
            "server": cluster_secret('mailchimp-credentials', 'server')
        })

        response = client.lists.add_list_member(
            cluster_secret('mailchimp-credentials', 'id'), {
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
