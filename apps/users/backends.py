# apps/users/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

class CaseInsensitiveModelBackend(ModelBackend):
    """
    Custom backend to perform case-insensitive authentication.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username:
            logger.error("Username is not provided for authentication.")
            return None
        username = username.lower()
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username__iexact=username)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            logger.warning(f"Password mismatch or inactive user for username: {username}")
        except UserModel.DoesNotExist:
            logger.error(f"No user found with username: {username}")
        return None

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username:
            username = username.lower()
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username__iexact=username)
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
