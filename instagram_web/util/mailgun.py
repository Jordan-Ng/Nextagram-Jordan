from authlib.flask.client import OAuth
from config import mailgun_config
import config
import os
import requests


def send_simple_message(donater):
    return requests.post(
        f"https://api.mailgun.net/v3/{mailgun_config.MAILGUN_DOMAIN_NAME}/messages",
        auth=("api", mailgun_config.MAILGUN_API_KEY),
        data={"from": f"mailgun@{mailgun_config.MAILGUN_DOMAIN_NAME}",
              "to": [donater],
              "subject": "Hello boss",
              "text": "Testing some Mailgun awesomness!"})
