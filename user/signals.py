""" Use Django's user_logged_out signal to clear the session_key in the User model
 when a session expires. """

from django.contrib.auth import user_logged_out
from django.dispatch import receiver

@receiver(user_logged_out)
def clear_session_key(sender, request, user, **kwargs):
    if user:
        user.session_key = None
        user.save()