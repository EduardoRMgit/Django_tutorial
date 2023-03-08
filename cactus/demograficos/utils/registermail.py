import mailchimp_marketing as MailchimpMarketing
import logging
from mailchimp_marketing.api_client import ApiClientError
from cactus.utils import cluster_secret

db_logger = logging.getLogger('db')


def RegistrarMail(email):
    try:
        client = MailchimpMarketing.Client()
        client.set_config({
            "api_key": cluster_secret('server-prefix', 'server'),
            "server": cluster_secret('server-prefix', 'server')
        })

        response = client.lists.add_list_member(
            cluster_secret('list', 'id'), {
                           "email_address": email,
                           "status": "subscribed"})
        db_logger.info(
            f"[Create Customer]: {user}"
            f"response: {response}"
        )
        print(response)
    except ApiClientError as error:
        print("Error: {}".format(error.text))
        msg_mailchimp = (
            f"[Create Customer] Error al crear customer en ubcubo"
            f"para el usuario: {user}. Error: {error}")
        db_logger.warning(msg_mailchimp)

