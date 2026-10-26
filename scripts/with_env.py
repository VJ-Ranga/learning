"""Run a management command with a deliberately selected environment file."""
import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

if len(sys.argv) < 3:
    raise SystemExit('Usage: python scripts/with_env.py ENV_FILE MANAGEMENT_COMMAND [OPTIONS]')
environment_file = Path(sys.argv[1]).resolve()
if not environment_file.is_file():
    raise SystemExit('Environment file does not exist. No command was run.')
load_dotenv(environment_file, override=True)
root = Path(__file__).resolve().parent.parent
raise SystemExit(subprocess.call([sys.executable, str(root / 'manage.py'), *sys.argv[2:]], cwd=root, env=os.environ))
