from getpass import getpass

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create a user'

    def handle(self, *args, **kwargs):
        username = input('Username: ')
        password = getpass('Password: ')
        User = get_user_model()
        user = User.objects.create_user(username=username)
        user.set_password(password)
        user.save()

        print('\nUser created.\n')
