from django.contrib.auth.backends import ModelBackend
from .models import Account

class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = Account.objects.get(email=email)
            if user.check_password(password):
                request.session['user_id'] = user.id  # Set user_id in the session
                
                return user
        except Account.DoesNotExist:
            return None
        return None
