from pathlib import Path

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

BASE_DIR = str(Path(__file__).resolve().parent.parent.parent.parent) + '/import_file/'


class Command(BaseCommand):
    def add_user(self, parser):
        parser.add_argument('filename', nargs='+', type=str)

    def handle(self, *args, **options):
        with open(BASE_DIR + options['filename'][0]) as file:
            content = file.readlines()
            for user in content:
                first_name, last_name, username, email, password = user.strip().split(',')
                User.objects.create(first_name=username, last_name=last_name, username=username, email=email,
                                    password=password)
        self.stdout.write(self.style.SUCCESS('Successfully added tags'))
