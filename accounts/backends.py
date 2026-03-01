from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

TASUser = get_user_model()


class DualAuthenticationBackend(ModelBackend):
    """
    Custom authentication backend that can authenticate TAS School Management System users.
    Since we've swapped the user model, all users are now TASUser instances.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        # Try to authenticate as a TAS user by username
        try:
            tas_user = TASUser.objects.get(username=username)
            if tas_user.check_password(password):
                return tas_user
        except TASUser.DoesNotExist:
            pass
        
        # Try authentication by email for TAS users
        try:
            tas_user = TASUser.objects.get(email=username)
            if tas_user.check_password(password):
                return tas_user
        except TASUser.DoesNotExist:
            pass
        
        return None
    
    def get_user(self, user_id):
        """Get TAS user by ID."""
        try:
            return TASUser.objects.get(pk=user_id)
        except TASUser.DoesNotExist:
            return None


class TASUserBackend(ModelBackend):
    """
    Authentication backend specifically for TAS School Management System users.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        # Try to authenticate as a TAS user by username
        try:
            tas_user = TASUser.objects.get(username=username)
            if tas_user.check_password(password):
                return tas_user
        except TASUser.DoesNotExist:
            pass
        
        # Try authentication by email for TAS users
        try:
            tas_user = TASUser.objects.get(email=username)
            if tas_user.check_password(password):
                return tas_user
        except TASUser.DoesNotExist:
            pass
        
        return None
    
    def get_user(self, user_id):
        """Get TAS user by ID."""
        try:
            return TASUser.objects.get(pk=user_id)
        except TASUser.DoesNotExist:
            return None 