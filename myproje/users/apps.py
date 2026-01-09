
from django.apps import AppConfig
from django.db.utils import OperationalError
from django.db.models.signals import post_migrate
from django.apps import AppConfig
from django.contrib.auth.hashers import make_password
class YourAppConfig(AppConfig):
    name = 'users'  # Your app name
    def ready(self):
        from .models import CustomUser  # Import inside the ready method
        post_migrate.connect(create_default_user)

def create_default_user(sender, **kwargs):
    from .models import CustomUser  # Import here to avoid AppRegistryNotReady
    try:
        if not CustomUser.objects.filter(username='henok').exists():
            CustomUser.objects.create_user(
                username='henok',
                email='defaultuser@example.com',
                password='12341234',
                phone='0934567890',
                fname='Default',
                lname='User',
                gender='Other'  # Adjust as needed
            )
    except OperationalError:
        pass

"""
def create_default_user(sender, **kwargs):
    from .models import CustomUser  # Import here to avoid AppRegistryNotReady
    try:
        if not CustomUser.objects.filter(username='henok').exists():
            CustomUser.objects.create_user(
                username='henok',
                email='defaultuser@example.com',
                password=make_password('12341234'),  # Ensure password is hashed
                phone='0934567890',
                fname='Default',
                lname='User',
                gender='Other'  # Adjust as needed
            )
    except OperationalError:
        pass
"""
