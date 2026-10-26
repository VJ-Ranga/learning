# Python Quest — learning roadmap and platform proposal

Status: First foundation chapter implemented. Updated access decision: only the two pre-provisioned learners vjranga and shanesha; public registration is disabled. The longer curriculum below remains the future roadmap.
Date: 2026-10-26
Location: Standalone child folder of Programming_Learning. No dependency on the existing multi-language platform.
Repository: The owner will create the Git repository later. No Git initialization, commits or deployment are part of this plan.
Hosting: Undecided, as requested. Django is the proposed application framework, pending design approval.

## 1. Purpose and learners

Help two learners with general IT knowledge become comfortable reading, explaining, writing and debugging Python. One learner needs practical job readiness; the other needs to understand existing Python AI projects. Begin with strong programming foundations, then build terminal applications, desktop interfaces, database-backed forms and Django web applications.

Teach Python without assuming previous coding fluency. Explain technical words when introduced. Use familiar situations from IT support, teaching and everyday work. Avoid long theory sections before practical work.

Success means each learner can build a small program from a blank file, explain its decisions, handle invalid input, diagnose a traceback and change requirements without copying a complete solution. Scores alone do not establish readiness.

## 2. Learning pace

Planning estimate: 100–140 focused hours for the core route, including independent practice and project revisions. This is a study budget, not a job-readiness guarantee. Reassess after the first five sessions.

- At 2 hours a day, 6 days a week: roughly 9–12 weeks.
- At 3 hours a day, 6 days a week: roughly 6–8 weeks.
- Treat the first 30–40 hours as a foundation sprint, not complete Python mastery.
- Use short daily sessions rather than attempting the entire roadmap in a few weekends.

Suggested 90-minute session:

1. 10 minutes: recall yesterday's concepts without notes.
2. 15 minutes: read a plain-language explanation and trace a worked example.
3. 35 minutes: solve exercises and fix deliberate mistakes.
4. 20 minutes: advance the current project.
5. 10 minutes: explain one solution to the other learner and record an uncertainty.

For additional time, add project practice and review. Do not simply increase the number of new concepts.

## 3. Core learning route

Hours include lessons, challenges and the level project. They are approximate allocations totaling 100–140 hours.

| Level | Focus | Practical outcome | Hours |
| --- | --- | --- | --- |
| 1 — First Mission | Running Python; statements; print; comments; variables; strings; integers; floats; booleans; input; conversion; basic operators; indentation | Terminal profile and bill calculator | 6–8 |
| 2 — Decision Maker | Comparisons; if/elif/else; and/or/not; truth values; for/while; range; break; continue; tracing loops | Support-ticket triage tool and number game | 8–12 |
| 3 — Data Collector | Strings; indexing; slicing; lists; tuples; dictionaries; sets; iteration; choosing a collection | In-memory inventory or student marks tracker | 8–10 |
| 4 — Function Builder | Parameters; arguments; return; scope; decomposition; imports; modules; docstrings; introductory type hints | Refactor the tracker into small reusable functions | 8–12 |
| 5 — Reliable Coder | Reading tracebacks; common exceptions; narrow try/except; validation; paths; text files; JSON; CSV; context managers; debugging; basic automated tests | Terminal expense tracker that survives restarts and invalid input | 10–14 |
| 6 — Project Explorer | venv; pip; dependency files; project structure; Git basics; environment variables; HTTP and JSON; requests with timeouts; simple classes and objects; reading unfamiliar code | API-powered command-line utility and a guided walkthrough of an AI-style project | 8–12 |
| 7 — UI Builder | Tkinter widgets; layout; callbacks; event loop; state; input validation; keeping business logic separate from UI | Desktop calculator, followed by a registration form | 10–14 |
| 8 — Database Keeper | Tables; rows; columns; keys; SQLite; SELECT/INSERT/UPDATE/DELETE; parameterized queries; constraints; transactions; basic relationships | Desktop registration form with persistent records, search, edit and delete | 8–12 |
| 9 — Web Apprentice | Browser/server model; HTTP requests and responses; minimal HTML/forms; Django project/app structure; URLs; views; templates; models; migrations; ORM; admin | First Django application with a database-backed form | 12–16 |
| 10 — Django Builder | Django forms; validation; login/logout; sessions; authorization and ownership; CSRF; tests; configuration; static files; deployment concepts | Private support-ticket or task application with accounts and per-user records | 14–18 |
| Final Mission | Independent requirements; implementation; testing; documentation; explaining and changing code | Build and demonstrate an original small application | 8–12 |

Progression gates:

- Before Level 4: solve a fresh loop/collection problem and explain its output.
- Before Level 7: create a terminal app with functions, validation and file persistence.
- Before Level 9: explain a database operation and safely save/retrieve form input.
- Final gate: implement a new feature and fix a seeded bug without a full solution.
- A learner can revisit any unlocked material. Extra practice is offered when a gate is not yet passed.
- For the two-person initial course, executable challenge checks unlock progression. Explanation/project checklists support peer review, recorded as peer-reviewed rather than instructor-verified mastery; an unavailable reviewer must not indefinitely block learning.

## 4. Later advanced paths

After the core route, choose the path that matches actual job or project needs:

- Django: relationships, query efficiency, pagination, REST APIs and deployment operations.
- AI project literacy: API clients, JSON payloads, configuration, logging, SDK calls, prompt/data flow, failure handling and cost controls. Start with a mock API; paid keys are optional.
- Python depth: comprehensions, iterators, generators, decorators, dataclasses and typing.
- Testing and maintenance: fixtures, mocking, integration tests, refactoring and CI.
- Async and background work only when a project calls for them.

Do not make advanced syntax a prerequisite for building useful beginner applications.

## 5. What each lesson contains

Every lesson follows this sequence:

1. A small real-world problem and a specific learning outcome.
2. A plain-language explanation with any new vocabulary defined.
3. A short working example with line-by-line explanation and expected output.
4. A trace exercise: predict what variables and output will be at each step.
5. A guided change to the example.
6. An independent code challenge with acceptance criteria.
7. A debugging challenge with a realistic error and helpful traceback.
8. A brief explanation prompt: why does this work?
9. A recap and a later recall challenge.

Include common misunderstandings, boundary cases and progressively stronger hints. Avoid dumping a complete solution before the learner attempts the exercise.

Example first coding mission: read a person's name and hours worked, convert the hours from text to a number, calculate pay at a fixed rate, then print a friendly result. Later missions add validation, a reusable function, file storage, a UI and finally a web form. Reusing the problem makes the added abstraction visible.

## 6. Game loop

Working title: Python Quest. Theme and visual design are provisional.

- A world map represents the levels, with short missions and a project at the end of each level.
- Each account has its own dashboard, saved attempts, progress and skill history.
- Mission types include predict output, repair code, write code, explain code and extend an application.
- The main loop is: learn → predict → code → run → receive feedback → revise → complete a mission.
- Feedback distinguishes syntax errors, runtime errors and failed requirements. Where possible it shows a useful failing input and expected behavior.
- Hints progress from conceptual guidance to pseudocode to a worked solution.
- Previously completed work remains available for revision and comparison with the learner's own earlier attempts.
- Daily recall and weekly paired challenges encourage practice. Missing a day does not erase progress.

### Scoring and comparison

Keep competition friendly and make score farming ineffective:

- Mission marks are based on a published rubric, normalized to 100.
- For coding missions: 70 for required behavior and edge cases, 20 for a fresh variation, 10 for a short explanation/review checklist.
- Objective behavior can be checked automatically. Explanations and larger projects are marked as awaiting review until a human reviews them; no claim of automatic understanding assessment.
- Store the best result per mission. Retries can improve it but do not repeatedly add points.
- XP is a motivational completion reward; it is displayed separately from assessed mastery.
- Hints and viewed solutions are recorded. After viewing a solution, a fresh variation is required to demonstrate independent completion.
- Show total completed missions, mastery by topic, project milestones and weekly progress alongside marks.
- Compare both learners on the same completed mission set, as well as overall progress, so an early start does not masquerade as stronger understanding.
- Leaderboard uses server-stored records. Browser-run code results are practice evidence and cannot be treated as tamper-proof grades.
- No speed bonus for beginner exercises. Both learners should be able to explain their own work.

Suggested badges: First Working Program, Bug Detective, Function Builder, Data Keeper, UI Builder and First Django App.

## 7. Execution environments and limits

Beginner lessons should require minimal setup, but the course must also teach normal local Python development.

- Levels 1–5: browser Python runner for supported exercises, plus downloadable/local equivalents.
- Browser execution proposal: Pyodide in a dedicated Web Worker on an isolated runner origin with no platform credentials. Terminate the worker for timeouts; cap output and reset between attempts. A worker keeps the interface responsive but is not by itself a security boundary.
- Provide a controlled input panel for input() exercises. Prototype this early instead of assuming terminal input works unchanged in the browser.
- Test runner isolation, storage access, network policy, input handling, infinite loops, output flooding and runtime compatibility before depending on it.
- Files in browser exercises are temporary/virtual unless explicitly exported. Explain the difference from a learner's local filesystem.
- Level 6 onward: introduce local Python, editor, terminal and environment setup. Show commands appropriate to the learners' operating systems once known.
- Tkinter desktop windows require local Python with Tk support. The browser editor will not promise to display native desktop windows.
- Django projects run locally with their own database before deployment. The learning website and learner-created Django apps are separate applications.
- Local UI and Django projects use test scripts, acceptance checklists and reviewed submissions. Uploading arbitrary code must not execute it on the website server.
- If trustworthy automatic grades are needed later, add a separate isolated execution service with resource limits and independent tests. Do not run learner code inside the Django application process or shell.

## 8. Platform approaches

### Proposed: Django application, PostgreSQL, browser Python runner

Django supplies authentication, sessions, admin tools, forms and database models. PostgreSQL stores shared progress. Templates and a modest JavaScript layer keep the product understandable. The platform becomes a real Python web project the learners can inspect later.

Tradeoffs: browser coding needs careful integration; desktop and full Django exercises still need local tools. Hosting and database operation need a deployment decision.

### Alternative: Static/frontend application with managed authentication and database

Fits frontend-oriented hosting and browser exercises. Adds a separate backend service and access policies, while the product itself teaches less about Django. It remains an option if minimizing backend operation becomes the deciding factor.

### Alternative: Existing learning service plus a separate progress tracker

Fastest route to starting lessons, with less custom platform development. Tradeoff: the curriculum, marking and two-person game experience may be constrained or split across services.

Recommendation: Django for the intended custom platform, subject to approval. Hosting remains undecided. Do not delay the first learning sessions until every game feature exists.

## 9. Proposed product structure

- Accounts: two invite-only learner accounts initially; separate admin account.
- Curriculum: levels, lessons, missions, challenge variants and versioned rubrics.
- Attempts: learner, mission version, submitted answer/code, check results, hint use and timestamps.
- Progress: completed lessons, passed gates and best marks per mission.
- Projects: submission notes, files or repository links, checklist and review status.
- Leaderboard: derived from stored eligible results; do not accept arbitrary XP totals from the browser.
- Administration: edit/publish content and review explanations/projects.

Proposed safeguards: Django password hashing and session authentication, CSRF protection, ownership checks, restricted enrollment, login throttling, secrets kept out of source control, and database backup/export. No learner can modify the other learner's attempts or marks.

Out of scope initially: public enrollment, payments, live chat, AI-generated grading, public tournaments and server execution of untrusted submissions.

## 10. Build sequence and acceptance checks

### Milestone 1 — Prove one complete lesson

Create account/login, a simple mission page, browser editor, run/output/input interaction, a single coding rubric, attempt saving and a two-person progress comparison. Author enough first-level content for an actual study session.

Acceptance: both accounts can complete the same mission independently; results survive logout and server restart; one learner cannot change the other's records; a repeated completion cannot farm XP; the runner handles errors and infinite loops without freezing the page.

### Early shared deployment — after Milestone 1

Once the owner chooses hosting, deploy the first usable slice so both learners can use separate accounts and shared progress immediately. Configure durable storage, HTTPS, secrets and backups, and verify that saved results survive a redeployment. Continue delivering curriculum incrementally. If hosting remains undecided, the first slice remains local and remote shared access is not yet delivered.

### Milestone 2 — Useful foundation course

Complete Levels 1–5 with guided examples, independent variations, debugging work, gates and recall exercises. Add the first terminal project and project submission checklist.

Acceptance: a learner can follow the lessons without an instructor filling in missing prerequisite concepts; every published coding challenge has verified example and edge-case checks.

### Milestone 3 — Practical applications

Add project setup, API literacy, Tkinter and SQLite units with local run guides, starter material and review rubrics.

Acceptance: the calculator works, invalid form inputs are handled, data persists, parameterized queries are used and each learner can demonstrate their own application.

### Milestone 4 — Django and final mission

Add the web progression, authentication/ownership exercises, final project and an annotated walkthrough of the platform's own source.

Acceptance: both learners can build and explain a database-backed web form, restrict access to their own records, run tests and document how to start their project.

### Milestone 5 — Deployment review

Review the early shared deployment after the full learning route is available. Verify backup restoration, both accounts, permission boundaries and saved progress after redeployment. Hosting is selected before the early shared deployment, not postponed until course completion.

No publication or repository creation is included in this planning step.

## 11. Decisions still needed

- Approximate daily study time and any job deadline; the current hour budget is provisional.
- Learner operating systems for local setup instructions.
- Whether English explanations are sufficient or Sinhala support would help.
- Hosting provider and monthly budget, explicitly deferred by the owner.
- Approval of the proposed Django approach and game/scoring design before implementation.

## 12. Sources checked for technical feasibility

- Render Django deployment: https://render.com/docs/deploy-django
- Render free-tier limitations: https://render.com/docs/free
- Vercel Python runtime: https://vercel.com/docs/functions/runtimes/python
- Pyodide usage and Web Workers: https://pyodide.org/en/stable/usage/index.html

Provider capabilities and limits should be rechecked when deployment is actually planned. No specific subscription price or permanent free hosting is assumed.
