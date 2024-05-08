# myapp/authentication.py
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class ExampleAuthentication(BaseAuthentication):
    def authenticate(self, request):
        username = request.headers.get('ShahadAlkamli')
        password = request.headers.get('SH9920')

        if not username or not password:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed('No such user')

        if not user.check_password(password):
            raise AuthenticationFailed('Invalid password')

        return (user, None)
