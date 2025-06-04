from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class PasswordResetToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return(
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_actia)
        )
password_reset_token = PasswordResetTokenGenerator()

from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def send_password_reset_email(user, request):

    token = password_reset_token.make_token(user)
    uid = user.pk
    reset_link = request.build_absolute_uri(
        reverse('password-reset-confirm', kwargs={'uid':uid, 'token': token})
    )

    subject = 'Reset Your Password'
    message = f'Hi, click the link below to rest your password:\n{reset_link}'

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])