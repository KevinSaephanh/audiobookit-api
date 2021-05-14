from django.core.exceptions import ValidationError
from better_profanity import profanity
import re

class FieldValidator:
    def validateUsername(self, username):
        # Check length of username
        length = len(username)
        if length < 5 or length > 20:
            raise ValidationError('Username length must be between 5 and 20 characters')

        # Check if username contains profanity
        if profanity.contains_profanity(username):
            raise ValidationError('Username cannot contain any profanity')

    def validatePassword(self, password):
        # Check length of password
        length = len(password)
        if length < 7 or length > 100:
            raise ValidationError('Password length must be between 7 and 100 characters')

        # Check if password meets regex standard
        regex = re.compile('^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]$')
        if not regex.match(password):
            raise ValidationError(
                'Password must contain at least one capital letter, one number, and one special character')
