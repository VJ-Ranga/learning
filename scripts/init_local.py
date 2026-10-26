"""Create private local settings once, never overwrite an existing environment."""
from pathlib import Path
import secrets

root = Path(__file__).resolve().parent.parent
environment = root / '.env'
if not environment.exists():
    secret = secrets.token_urlsafe(64)
    invite = secrets.token_urlsafe(12)
    with environment.open('x') as file:
        file.write(f'DJANGO_DEBUG=1\nDJANGO_SECRET_KEY={secret}\nENROLLMENT_CODE={invite}\n')
    environment.chmod(0o600)
    print('Created private .env for local development.')
print('Open http://127.0.0.1:8001/join/ and create your account.')
print('Find your room invite in .env under ENROLLMENT_CODE. Share it only with your learning partner.')
