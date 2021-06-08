from django.core.mail import EmailMessage
from better_profanity import profanity
import re


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            to=[data['to_email']],
            body=data['email_body']
        )
        email.send()

    @staticmethod
    def is_valid_username(username):
        regex = re.compile('^[a-zA-Z0-9_-]{5, 20}*$')
        has_profanity = profanity.contains_profanity(username)
        return not has_profanity and regex.match(username)

    @staticmethod
    def is_valid_password(password):
        regex = re.compile(
            '^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{7, 100}$')
        return regex.match(password)
