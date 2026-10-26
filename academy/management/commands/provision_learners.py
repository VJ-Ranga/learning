"""Create the two private learners once without resetting changed passwords."""
import os
import secrets
from pathlib import Path
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from dotenv import dotenv_values


class Command(BaseCommand):
    help = 'Create vjranga and shanesha with private random initial passwords; preserve existing accounts.'

    def add_arguments(self, parser):
        parser.add_argument('--password-file', default=str(settings.BASE_DIR / '.env.learners'))

    def handle(self, *args, **options):
        path = Path(options['password_file']).resolve()
        if not path.exists():
            try:
                descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                with os.fdopen(descriptor, 'w') as file:
                    for username in ('vjranga', 'shanesha'):
                        file.write(f'{username.upper()}_PASSWORD={secrets.token_urlsafe(18)}\n')
            except OSError as error:
                raise CommandError('Could not create the private password file.') from error
        values = dotenv_values(path)
        for username in ('vjranga', 'shanesha'):
            value = values.get(username.upper() + '_PASSWORD')
            if not value or len(value) < 20:
                raise CommandError('Password file must contain VJRANGA_PASSWORD and SHANESHA_PASSWORD, each at least 20 characters.')
        with transaction.atomic():
            for username in ('vjranga', 'shanesha'):
                user, created = get_user_model().objects.get_or_create(username=username)
                if created:
                    user.set_password(values[username.upper() + '_PASSWORD'])
                    user.save(update_fields=['password'])
                    self.stdout.write(f'Created learner: {username}')
                else:
                    self.stdout.write(f'Kept existing account and password: {username}')
        self.stdout.write(f'Initial credentials are stored privately in {path}. Do not commit this file.')
