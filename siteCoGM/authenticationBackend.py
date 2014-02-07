from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

# So I can invoked authenticate recursively below
django_authenticate = authenticate

class SuperuserLoginAuthenticationBackend(object):
    """ Let superusers login as regular users. """
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        # The password should be name/password
        if "@" not in password:
            return None
        supername, superpass = password.split("@", 1)
        superuser = django_authenticate(username=supername, password=superpass)
        if superuser and superuser.is_superuser:
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
            