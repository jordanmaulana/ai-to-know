# AI to Know

A public, plain-English list of things AI made possible. Each entry answers three questions:
what is it, what can you make with it, and what did you have to do before it existed. The
public site is a React SPA; behind it sits a Django backend, a superuser-only CMS, and a
nightly Hacker News crawl that proposes new entries and files them as drafts for a human to
review.

## The editorial bar

> Only add something that unlocks work which was impossible or wildly impractical before.

"Faster", "cheaper", "a nicer version of an existing tool", model releases, benchmark results
and funding news do not qualify. The full rules — what qualifies, what disqualifies, and the
verbatim rubric the crawler judges against — live in one file,
[syllabus/editorial.py](syllabus/editorial.py). That file is the source of truth: it is
rendered for humans at `/dashboard/editorial/` and fed to the model as its system prompt. Edit
it there, nowhere else.

Entries are filed under six categories (`syllabus/models.py`): **build** (writing software),
**automate** (routine work), **agents** (multi-step action), **media** (image/audio/video),
**interface** (voice, vision, the screen), **infra** (running and serving models).

## How it works

```
Hacker News (Algolia API)
        │  make crawl  →  syllabus/management/commands/crawl_hn.py
        ▼
  free prefilter          points floor (--min-points 40) + AI keyword hit
        │                 + skip any hn_id already in CrawlCandidate
        ▼
  Claude judge            one API call per survivor; system = RUBRIC + index of
        │                 existing subjects; json_schema output
        │                 → accepted / rejected_llm / duplicate
        ▼
  Subject(status=draft)  ──►  /dashboard/subjects/?status=draft   (superuser review)
                                        │  publish  →  Subject.publish()
                                        ▼
                              GET /api/v1/syllabus/subjects/   (AllowAny, published only)
                                        ▼
                              React SPA:  /   and   /subjects/<slug>
```

Every story the crawler looks at is recorded as a `CrawlCandidate` keyed by a unique `hn_id`,
so no story is ever fetched, judged, or paid for twice. The prefilter is free — only survivors
cost an API call. `make crawl-dry` runs the prefilter alone: no API calls, nothing written.
Without `ANTHROPIC_API_KEY` the crawl still fetches and prefilters, leaves the survivors
unjudged, and picks them up on the next run once the key is set.

**Nothing the crawler produces is public.** Accepted stories become drafts. A draft reaches
the site only when a superuser publishes it in the CMS.

Hand-written entries are different: they live in [syllabus/seed_data.py](syllabus/seed_data.py)
(23 of them), load with `make seed`, and are published immediately.

## Two front doors

The repo serves two distinct UIs, with two distinct auth systems. Keep them straight.

| | Public site | CMS |
|---|---|---|
| Where | `frontend/` — React SPA on :5173 | `/dashboard/` — Django templates |
| Routes | `/`, `/subjects/<slug>`, `/login`, `/dashboard` | dashboard, subjects, queue, editorial |
| Auth | DRF token in `localStorage` | Django session, **superuser only** |
| JS | Vite + TanStack Router + Jotai + React Query | none at all |

- **SPA** — `/` is the syllabus itself, `/subjects/<slug>` the detail page. Both are public;
  redirects are centralized in `AuthGate`
  ([frontend/src/features/auth/components/auth-gate.tsx](frontend/src/features/auth/components/auth-gate.tsx)),
  which is the only place routing decisions are made. `isPublicPath` in that file decides what
  an anonymous visitor may see.
- **CMS** — server-rendered, gated by `SuperuserRequiredMixin` ([core/views.py](core/views.py)):
  anonymous → `/login/?next=…`, signed-in non-superuser → 403. Filters, search and pagination
  are plain `GET` querystrings, so every view of the list is a URL you can bookmark or paste to
  someone. `/dashboard/queue/` shows every HN story the crawler has judged and why.
  `/admin/` stays wired as the escape hatch.

Note the Django side redirects its own `/` to `/dashboard/`. The public `/` is served by Vite
in dev and by whatever hosts `frontend/dist` in production — Django never renders it.

## Repo layout

| Path | What's in it |
|---|---|
| [core/](core/) | Project config (`settings.py`, `urls.py`, wsgi) plus shared abstractions only: `BaseModel` (ObjectId PK, timestamps, `actor`), `AppSetting`, Mayar payments. **No domain models here.** |
| [api/v1/](api/v1/) | DRF layer — `auth_api.py`, `syllabus_api.py`, `payments_api.py`, `serializers.py`, `urls.py` |
| [syllabus/](syllabus/) | The product app: `models.py`, `views.py` (CMS), `forms.py`, `selectors.py` (dashboard queries), `editorial.py`, `seed_data.py`, `management/commands/` |
| [templates/](templates/) | CMS templates (`cms/*`) and shared partials (`_partials/*`) |
| [static/](static/) | `input.css` → `output.css`, the CMS's own Tailwind build |
| [frontend/](frontend/) | The React SPA — `src/routes/` (file-based), `src/features/{auth,syllabus}/` |

## Getting started

Prerequisites: [uv](https://docs.astral.sh/uv/), [pnpm](https://pnpm.io/), Node.

```bash
cp .env.example .env          # SECRET_KEY can stay blank while DEBUG=True
uv sync
make migrate
make seed                     # 23 hand-written subjects; idempotent
uv run manage.py createsuperuser

npm install && make tw-build  # CMS styles — until this runs, /dashboard/ is unstyled
make dev                      # Django on :8000

# in a second shell
cd frontend && pnpm install
make web                      # Vite on :5173
```

Then: public site at http://localhost:5173, CMS at http://localhost:8000/dashboard/.

The database is SQLite when `POSTGRES_HOST` is empty and Postgres when it is set — no code
change either way. Vite proxies `/api` to :8000 in dev, so `VITE_API_URL` can stay empty
locally.

## Commands

All from the [Makefile](Makefile).

| Command | What it does |
|---|---|
| `make dev` | Django dev server on :8000 |
| `make web` | Frontend dev server (`pnpm run dev`) |
| `make mmg` / `make migrate` | Make / apply migrations |
| `make seed` | Load the hand-written subjects |
| `make crawl` | Real HN crawl — fetch, prefilter, judge, file drafts |
| `make crawl-dry` | Prefilter only: no API calls, nothing written |
| `make tw-build` / `make tw-run` | Build / watch `static/output.css` for the CMS |
| `make build-static` | Prod static: minified CSS, then `collectstatic` (order matters) |
| `make test` | `manage.py test` (CMS coverage in `syllabus/tests.py`) |
| `make lint` | `ruff format` + `ruff check --fix` |
| `make dock` | Full docker compose stack |
| `make upgrade` | `uv sync` + `uv lock --upgrade` |

Frontend build / typecheck: `cd frontend && pnpm run build`.

## Configuration

Everything is read from `.env` — see [.env.example](.env.example) for the full list.

- **Django** — `SECRET_KEY`, `DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CORS_ALLOWED_ORIGINS`
  (also used verbatim for `CSRF_TRUSTED_ORIGINS`)
- **Database** — `POSTGRES_DB/USER/PASSWORD/HOST/PORT`. Leave `POSTGRES_HOST` empty for SQLite.
- **Crawler** — `ANTHROPIC_API_KEY`, `SYLLABUS_CRAWLER_MODEL` (default `claude-opus-5`)
- **Auth** — `GOOGLE_OAUTH_CLIENT_ID` for the Google sign-in button
- **Payments** — `MAYAR_API_KEY`, `MAYAR_WEBHOOK_TOKEN`, `MAYAR_BASE_URL`, `PAYMENT_REDIRECT_URL`
- **URLs** — `SITE_URL`, `FRONTEND_URL` (the CMS builds its "view public page" links from this)
- **Frontend build args** — `VITE_API_URL`, `VITE_GOOGLE_CLIENT_ID`

Production guard: with `DEBUG=False` and a `SECRET_KEY` still starting `django-insecure-`,
[core/settings.py](core/settings.py) raises at import rather than booting insecurely.

## API

Base path `/api/v1/`. DRF defaults are `TokenAuthentication` + `IsAuthenticated`; the syllabus
endpoints opt out with `AllowAny`.

| Endpoint | Auth | Notes |
|---|---|---|
| `POST /auth/google/` | public | Google ID token → `{ token, user }` |
| `POST /auth/register/`, `POST /auth/login/` | public | → `{ token, user }` |
| `GET /auth/me/` | token | Rehydrate the user on page load |
| `POST /auth/logout/` | token | Deletes the token |
| `GET /syllabus/subjects/` | public | Published only. `?category=`, `?q=` |
| `GET /syllabus/subjects/<slug>/` | public | Published only |
| `POST /payments/mayar/webhook/` | `X-Callback-Token` header | Mayar callback |

Syllabus writes have no API. Content is created and published in the CMS, by design.

## Deployment

`docker compose` runs Postgres, the backend and the SPA. [Dockerfile.backend](Dockerfile.backend)
is two-stage: a Node stage builds `static/output.css`, then the Python stage runs gunicorn.
[docker/backend-entrypoint.sh](docker/backend-entrypoint.sh) waits for Postgres, then runs
`migrate` and `collectstatic` before the server starts.
[frontend/Dockerfile](frontend/Dockerfile) is two-stage the same way: Node runs `pnpm run build`,
then `nginx:alpine` serves `dist` with an SPA fallback ([frontend/nginx.conf](frontend/nginx.conf))
so a hard refresh on `/subjects/<slug>` still gets `index.html`.

```bash
make dock       # down, build, up, follow logs (uses .env.docker)
./update.sh     # git pull → build → up → migrate, for an existing box
```

Published host ports: backend **8012** (`8012:8000` — the container and gunicorn still listen on
8000), frontend **3012** (`3012:3000`). Postgres publishes nothing; the backend reaches it over
the compose network as `POSTGRES_HOST=postgres`.

`VITE_API_URL` and `VITE_GOOGLE_CLIENT_ID` are **build args**, inlined into the bundle by vite —
changing one needs `docker compose build frontend`, not a restart. `VITE_API_URL` is the URL the
*browser* calls (`http://localhost:8012`), not `http://backend:8000`. Since the SPA is served
from a different origin than the API, `DJANGO_CORS_ALLOWED_ORIGINS` must list the frontend origin
(`http://localhost:3012`) or every fetch fails CORS.

The daily crawl is a host cron job, not a container:

```cron
0 8 * * * cd /path/to/repo && /usr/bin/make crawl >> /tmp/hn-crawl.log 2>&1
```

## Notes and gotchas

- **Two Tailwind pipelines.** `static/input.css` (built by the root `npm` + `make tw-build`)
  serves the CMS; `frontend/src/styles.css` (built by Vite + `pnpm`) serves the SPA. They
  mirror each other's `@theme` tokens by hand — changing a design token is a two-file change.
- **CMS templates must live in the root `templates/`.** The Dockerfile's Tailwind stage copies
  only `static/` and `templates/`, so an app-level template directory would ship unstyled.
  Tailwind class names must also be complete literal strings in the markup — anything assembled
  from a template variable is never generated.
- **`make build-static` order is load-bearing.** In production the manifest storage turns a
  missing `output.css` into a 500, so the CSS must be built before `collectstatic`.
- **Onboarding is dormant.** `get_onboarded` in [api/v1/serializers.py](api/v1/serializers.py)
  returns `True` unconditionally, so login goes straight to `/dashboard` and `/onboarding` is
  unreachable. `CLAUDE.md` documents the four touch-points to change if you want a real one.
- **Publishing is its own POST endpoint**, not a form field, so `Subject.publish()`'s
  stamp-`published_on`-once semantics can't be bypassed.

For repo conventions — where models go, how API modules are split, how to add an app — see
[CLAUDE.md](CLAUDE.md).
