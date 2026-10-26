# Python Quest

A small private Python learning game for two learners. This first chapter teaches programming fundamentals through ten lessons and terminal-style programs. Django stores accounts, attempts and best marks. Learner programs execute in an isolated browser frame, not on the Django server.

## Start learning locally

Python 3.12+ is required. From this folder:

```bash
./start.sh
```

Open **http://127.0.0.1:8001/login/**. The only learner accounts are **vjranga** and **shanesha**; there is no registration. Their random initial passwords are in the private `.env.learners` file. Do not commit or publicly share that file. Each learner can change their password using **Change password** in the navigation.

The launcher creates local environment settings once, applies migrations, provisions the two learners and starts the development server. Provisioning preserves existing passwords, so starting the app again does not reset a password you changed. It uses local SQLite, which keeps progress across restarts. It listens only on this computer. Your friend needs the hosted deployment to access it remotely.

On Ubuntu, if creating a virtual environment fails because ensurepip is missing, install the matching `python3-venv` package, then retry. In this workspace a working `.venv` has already been prepared.

Manual setup, including Windows:

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/init_local.py
python manage.py migrate
python manage.py provision_learners
python manage.py runserver 127.0.0.1:8001
```

## Beginner installation help

Open `/help/` or choose **Setup & basic help** from the navigation. This public guide covers installation on Windows/macOS/Ubuntu, version checks, opening a terminal, creating/running a `.py` file, interactive Python and common errors. Setup instructions are also included in the downloadable programs README.

## What is included

1. Output and comments — first message.
2. Variables, integers and f-strings.
3. User input and converting text to numbers.
4. Arithmetic and decimal formatting — bill splitter.
5. Conditions and normalized input — support ticket triage.
6. Loops and running totals.
7. Lists and iteration — inventory.
8. Functions and return values — temperature converter.
9. Exceptions and input validation.
10. A support-cost calculator combining functions, dictionaries and validation.

Each lesson has explanations, a worked example, a trace, a challenge, two hints and an independent code-reasoning checkpoint. Every explanation step, example, trace, challenge and checkpoint has a copyable AI explanation prompt; it includes that step's context and asks for guided understanding rather than an immediate complete solution. Prompts are copied locally for the learner to paste into any AI; nothing is sent automatically. A manual-copy dialog is available when clipboard access is blocked. Checkpoint choices are shuffled. The lesson practice editor and challenge editor keep separate code, input and output, so running a worked example never replaces your challenge draft. Use **Run code** for experiments. Use **Check my answer** for immediate checkpoint feedback without changing marks, then **Check program & save** to run all test inputs and save the complete attempt. Correct/incorrect choices are explicitly labeled, program results show the number of checks passed, and a completed mission offers a large Next mission action. Program input is entered in advance, one value per line; the output panel is terminal-style, not an interactive OS shell.

The editor keeps separate lesson-practice and challenge device drafts per learner and mission. Older device drafts and submitted code containing the exact lesson example are treated as practice code, while other earlier work is preserved as challenge work. Submitted attempt records and marks are retained. Submitted challenge code is also stored in the account and used when no challenge device draft exists. Unsaved device drafts do not sync between computers. Download your program or submit it before changing devices. Lesson examples and reset actions ask before replacing your editor contents.

Download runnable worked programs from the sidebar. The Python files in `terminal-programs/` also run directly on a computer. Local runs do not automatically report results to the website.

## Revisit previous lessons

Every mission has Previous mission / All missions / Next mission links and a numbered map of all ten missions. The current lesson is highlighted; completed and in-progress marks are displayed separately. Use Back to lesson inside a challenge to reread explanations and examples. Navigating does not change marks, and device challenge drafts remain available when you return. Journey cards explicitly open their named lesson; a partial result such as 80/100 is marked In progress, not Completed.

## Scores and honest limits

- Program checks contribute 80 marks; the checkpoint contributes 20.
- A mission completes only when all output checks pass and the checkpoint is correct.
- XP is the sum of each mission's best mark, at most 100 per mission / 1,000 per chapter. Retries cannot farm XP or erase a better result.
- The private leaderboard compares the two active learner accounts; staff are excluded.
- Checks verify output, not that a learner used a particular language construct or understood the solution. Explain your approach to your partner and rebuild worked solutions independently.
- Browser execution reports are **unverified practice evidence**. The server compares reported output against its own expected results and marks the quiz, but a motivated user can forge browser results. This version is unsuitable for hiring exams or formal grading.
- The first slice deliberately omits badges, daily recall scheduling, progression locks, independent challenge variants and automatic explanation/project grading. These remain in the broader roadmap.

## Hosting: Django → Vercel → Neon PostgreSQL

The files are prepared for this target; no Vercel or Neon account/database has been created and no deployment has been performed.

### 1. Create the repository

Create a Git repository **inside this folder** when ready. Keep `.env`, `.venv`, `db.sqlite3`, `artifacts/`, `staticfiles/` and `.vercel/` out of Git. `.gitignore` covers them. The parent multi-language project is independent.

### 2. Create Neon storage

Create a Neon project and choose a region near the Vercel application. Copy its **pooled PostgreSQL connection string**, including `sslmode=require`. Treat it as a secret. Store it as `DATABASE_URL`; never put it in JavaScript or commit it.

For preview deployments, use a separate Neon branch/database. Do not point unreviewed previews at the production database.

### 3. Import into Vercel

Import the repository. The repository root should contain `manage.py`, `requirements.txt`, `pyproject.toml` and `vercel.json`. If importing a larger parent repository instead, set Vercel's Root Directory to `python-learning-game`.

Vercel's current Django integration detects the WSGI entrypoint and handles static collection. The included configuration also names the WSGI entrypoint explicitly. Do not run the development server in production.

Set these environment variables in Vercel:

| Variable | Value |
| --- | --- |
| `DJANGO_DEBUG` | `0` |
| `DJANGO_SECRET_KEY` | A new long random secret, e.g. generated with `python -c "import secrets; print(secrets.token_urlsafe(64))"` |
| `DATABASE_URL` | Neon pooled PostgreSQL URL with SSL |
| `DJANGO_ALLOWED_HOSTS` | Your exact Vercel hostname, e.g. `your-project.vercel.app`; comma-separated if needed |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://your-project.vercel.app` and any actual custom-domain origin, comma-separated |

Vercel's supplied deployment and production hostnames are added to the allowlist automatically. No wildcard host permission is required. Registration is disabled in the application; no invite code is needed.

### 4. Apply database migrations deliberately

Before opening the hosted site, run `python manage.py migrate --noinput` from a trusted terminal with the **target environment's** variables loaded. For example, pull that environment's variables using Vercel's CLI and load the resulting `.env.local` using the explicit environment helper below. `manage.py` itself loads only `.env` automatically; `.env.local` is not loaded implicitly.

For a downloaded `.env.local`, a deliberate command is:

```bash
python scripts/with_env.py .env.local migrate --noinput
```

Check which database/environment you are targeting first. Do not run migrations during every request or run preview migrations against production. Never commit downloaded environment files.

Create the two hosted learners after migrations, using the **same private initial-password file** generated locally:

```bash
python scripts/with_env.py .env.local provision_learners --password-file .env.learners
```

This runs against the selected Neon database, creates only `vjranga` and `shanesha`, and preserves accounts/passwords that already exist. Passwords are hashed by Django and never embedded in source code or exposed in a public registration page. The file stays on your computer; do not upload it to GitHub or Vercel. If the learners have changed their local passwords, this file still holds the original generated passwords; use their own Change password page after first hosted login.

Optional administration: use `python scripts/with_env.py .env.local createsuperuser` with the same target environment. No administrator password ships with the application.

### 5. Deploy and verify

Deploy via Vercel, then verify the real HTTPS URL:

- Log in separately as `vjranga` and `shanesha`; verify that `/join/` is unavailable.
- Verify that each learner can change their own password while preserving progress.
- A solved mission saves after logout/login.
- Both accounts appear on the shared leaderboard.
- A retry does not add duplicate XP.
- Both accounts' progress survives a redeployment.
- One learner cannot see the other's submitted code.

Vercel Hobby and Neon Free have usage allowances. This personal learning project is intended to fit within them initially, not guaranteed to stay free at arbitrary usage. Confirm their current limits at setup. A custom domain is optional.

The local SQLite data is not copied to Neon automatically. Provision the two named learners in Neon, or explicitly plan a data migration if local progress needs preserving.

### Backup progress

Use Neon's available recovery features for the selected plan and keep periodic independent backups. From a trusted terminal with the target environment loaded:

```bash
python manage.py dumpdata auth.user academy --indent 2 --output quest-backup.json
```

This file contains personal data, code and password hashes. Store it privately outside the repository. Validate restoration to a separate test database before relying on the backup. Do not overwrite a live database casually.

## Security and runtime boundaries

- Django password hashing, sessions, CSRF, per-account attempt access and two pre-provisioned learner accounts. Public registration is disabled.
- Login requests are limited to 20 per five-minute source-IP window using shared database state. IP values are hashed in throttle records. The reverse proxy's IP behavior must be checked on the deployed site.
- Hosted configuration fails closed without a secret or PostgreSQL URL, and rejects debug mode on Vercel.
- Learner code runs in a sandboxed iframe with an opaque origin and a fresh disposable worker. The frame has no same-origin privileges, cannot read the host page's cookies/DOM and cannot submit forms or navigate the parent.
- The runner pins Pyodide 0.27.7 because its classic-worker mode works in this opaque-origin sandbox. It uses Python 3.12 in the browser. Do not switch blindly to a module-only Pyodide release; opaque-origin module workers are not compatible with this setup in Chrome.
- Runtime files come from jsDelivr. First run requires internet and downloads a substantial Python runtime. Subsequent fresh workers reuse the browser HTTP cache but still initialize Python again.
- Worker execution is terminated after eight seconds; Python output is capped at 10,000 characters per check. Stop cancels browser execution before submission. There is no server-side exec, subprocess or shell for learner submissions.
- CSP restricts runner scripts/network to the runtime CDN. This is a small private practice runner, not a hardened multi-tenant service or trusted grading sandbox. Do not put secrets into learner programs.

## Development checks

```bash
python manage.py test
python manage.py makemigrations --check --dry-run
python manage.py collectstatic --noinput
# With real production-style settings loaded:
python manage.py check --deploy
```

`academy/tests.py` covers account access, disabled registration, learner provisioning, password changes, shared throttling, score calculation, retry behavior, malformed input, draft privacy, terminal examples and deployment configuration. The only subprocess execution is in tests for the trusted authored terminal examples, never in request handling.

`scripts/browser_check.cjs` is a development-only Playwright journey. Install Playwright separately, set `PLAYWRIGHT_PACKAGE` to its module if necessary, and use a disposable local database. It logs in as a provisioned learner using `.env.learners` or `TEST_USERNAME` / `TEST_PASSWORD`, and submits practice attempts. Use only a disposable database; do not run it against real learner data or production. It exercises input, saved results, missing input, timeouts, output limits, iframe isolation and mobile layouts. Runtime dependency downloads need internet.

## Structure

- `academy/curriculum.py`: lesson content and checked examples.
- `academy/models.py`, `services.py`, `views.py`: accounts/progress integration and practice grading.
- `templates/`, `static/academy/`: interface and isolated runner.
- `terminal-programs/`: runnable local worked examples.
- `LEARNING_PLAN.md`: longer route through desktop UI, databases and Django.

References: [Vercel Django](https://vercel.com/docs/frameworks/full-stack/django), [Neon plans](https://neon.com/pricing), [Django deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/).

`scripts/checkpoint_check.cjs` verifies separate editors, migration of legacy example drafts, challenge draft preservation after tab switches/reloads, separate terminal outputs and mobile layout. It uses a fresh browser context and does not submit attempts. Set `QUEST_BASE_URL` to choose local or hosted verification.

`scripts/feedback_check.cjs` verifies immediate correct/incorrect feedback, stale-result clearing, per-step prompt copying and manual-copy fallback, large next navigation and completion feedback on desktop/mobile. It uses a contract response fixture for program-save feedback so real learner marks are not modified.

`scripts/navigation_check.cjs` verifies exact dashboard-card destinations, previous/next boundaries, all-mission map jumps, back-to-lesson behavior, draft preservation across navigation, mobile layout and unchanged marks. It never submits an attempt.
