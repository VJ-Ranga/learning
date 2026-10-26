"""Create private local settings once, never overwrite an existing environment."""
from pathlib import Path
import secrets

root = Path(__file__).resolve().parent.parent
environment = root / '.env'
if not environment.exists():
    secret = secrets.token_urlsafe(64)
    with environment.open('x') as file:
        file.write(f'DJANGO_DEBUG=1\nDJANGO_SECRET_KEY={secret}\n')
    environment.chmod(0o600)
    print('Created private .env for local development.')
print('Open http://127.0.0.1:8001/login/ and use your assigned learner account.')
print('Initial passwords are kept in the private .env.learners file after provisioning.')
