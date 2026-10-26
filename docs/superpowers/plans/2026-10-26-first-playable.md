# Python Quest First Playable Implementation Plan

> **For agentic workers:** Execute inline with superpowers:executing-plans. The user authorized building the first slice immediately.

**Goal:** Two learners can study Python fundamentals, run terminal-style programs, save practice results and compare progress.
**Architecture:** Django owns authentication and persisted attempts. An opaque-origin sandbox iframe owns a disposable Pyodide worker, never server-side learner execution. PostgreSQL is required on Vercel; SQLite is local development only.
**Tech Stack:** Django 5.2 LTS, templates/CSS/JavaScript, Pyodide, Neon PostgreSQL, Vercel.
**Spec:** ../../../LEARNING_PLAN.md, narrowed by the user's request to first-step basics and terminal programs.

## Global Constraints

- Work only inside python-learning-game; no Git initialization, push or publication.
- Hosting target is Django → Vercel → Neon PostgreSQL, now selected by the owner.
- Invite-only learner enrollment, individual saved attempts and server-derived comparison.
- Browser coding results are practice evidence, not tamper-proof assessments.
- No desktop UI or advanced Django curriculum in this initial slice.

## Review Focus

- Anonymous submissions and cross-account changes must be rejected.
- Retrying a mission must not accumulate duplicate XP.
- Malformed and oversized submissions must return useful errors without saving marks.
- Infinite loops, missing input, runtime errors and output flooding must not freeze the interface.
- Hosted configuration must not silently fall back to a temporary SQLite database.

## Task 1 — Accounts and persisted practice

Files: questgame/settings.py, questgame/urls.py, academy/models.py, academy/forms.py, academy/views.py, academy/tests.py, migrations.
Interfaces: mission identifiers from academy.curriculum; POST attempts accepts code, quiz answer and browser case output. Server derives marks from expected outputs and quiz answer.
- [x] Write/run failing tests for invite enrollment, ownership, malformed payloads, grading and no duplicate completion reward.
- [x] Implement settings, accounts, attempt storage, grading and routes.
- [x] Run Django tests and migrations.

## Task 2 — Beginner lessons and safe coding workspace

Files: academy/curriculum.py, templates/academy/*, static/academy/*, terminal-programs/*.
Interfaces: mission JSON contains case inputs, expected outputs and starter code; sandbox sends run/check results through a restricted message bridge.
- [x] Add curriculum tests for required explanations, real case sets and download access.
- [x] Author ten short lessons, examples, hints, quizzes and independent coding challenges.
- [x] Build dashboard, mission workspace, practice terminal and leaderboard.
- [x] Browser-test input, changed test inputs, errors, retries, timeout/stop, isolation and mobile layout.

## Task 3 — Deployment preparation and handoff

Files: README.md, requirements.txt, .env.example, .gitignore, vercel.json, start.sh, management commands.
- [x] Verify deploy checks fail closed without database/secret/invite settings.
- [x] Prepare Vercel entrypoint and Neon connection settings; document explicit migrations and separate preview databases.
- [x] Run full tests, static collection, production checks and browser journey; review once and fix material defects.
- [x] Deliver local preview, startup instructions and remaining hosting/account setup requirements.

No commits: user will create the Git repository later.

## Completion record

- User approved immediate implementation on 2026-10-26; Django/Vercel/Neon selected.
- All work confined to the requested standalone folder; no Git or deployment actions.
- Database and browser-grade scoring verified; browser reports are explicitly practice evidence.
- Browser-tested input/output, all-input check saving, missing input, infinite-loop timeout, output flood, opaque iframe isolation and desktop/mobile layouts.
- Review finding fixed: compare invitation codes as UTF-8 bytes so Sinhala input cannot crash signup.
- Ruling: first slice uses 80 output marks + 20 quiz marks, with no locked progression or independent challenge generator, to deliver useful foundation practice now. Larger game mechanics remain in the roadmap.
- Ruling: Pyodide 0.27.7 classic worker is pinned after Chrome proved module workers fail in opaque-origin frames. Worker handshake has a request/response to avoid load-order races.
- Ruling: existing standalone folder is the isolated workspace; no worktree can be created because the owner has not yet created the repository.
- Actual Vercel/Neon deployment remains unverified until the owner provides/configures hosting and repository access.
