from twilio.rest import Client
import os

account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_TOKEN')
headers = {'Accept': 'application/json'}


def send_sms(country, numero, mensaje):
    client = Client(account_sid, auth_token)

    calling_code = "52"
    if country == "US" or str.lower(country) == "other":
        calling_code = "1"

    numero = "{}{}{}".format("+", calling_code, numero)
    message = client.messages.create(body=mensaje,
                                     from_='+12545234463',
                                     to=numero)
    return(message.sid)
