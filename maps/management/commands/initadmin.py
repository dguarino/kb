__author__ = 'dkarchmer@gmail.com'

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core import management
from django.contrib.auth.management.commands import changepassword


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Creating account for admin')
        management.call_command('createsuperuser', interactive=False, username="admin", email="xxx@xxx.com")
        command = changepassword.Command()
        command._get_pass = lambda *args: 'password'
        command.execute(username="admin")
