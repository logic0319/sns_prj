import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
User = get_user_model()
CONF_DIR = settings.CONF_DIR
config = json.loads(open(os.path.join(CONF_DIR, 'settings_deploy.json')).read())


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = config['defaultSuperuser']['username']
        password = config['defaultSuperuser']['password']
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email='a@a.com',
                password=password
            )
        else:
            print('default superuser exist')