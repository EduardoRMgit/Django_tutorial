import mailchimp_marketing as MailchimpMarketing
import logging
from cactus.utils import cluster_secret

db_logger = logging.getLogger('db')


def RegistrarMail(user):
    try:
        client = MailchimpMarketing.Client()
        client.set_config({
            "api_key": cluster_secret('mailchimp-apikey', 'key'),
            "server": cluster_secret('server-prefix', 'server')
        })

        response = client.automations.add_workflow_email_subscriber(
            "workflow_id", cluster_secret('workflow', 'key'), {
                "email_address": user.Uprofile.correo_electronico})
        db_logger.info(
            f"[Create Customer]: {user}"
            f"response: {response}"
        )
    except Exception as e:
        msg_mailchimp = (
            f"[Create Customer] Error al crear customer en ubcubo"
            f"para el usuario: {user}. Error: {e}")
        db_logger.warning(msg_mailchimp)
