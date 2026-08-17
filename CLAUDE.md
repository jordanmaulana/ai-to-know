# CLAUDE.md

Guidance for Claude Code working in this fullstack template.

## Stack

- **Backend**: Django + DRF. API in `api/` (v1 in `api/v1/`). `core/` = project config (settings/urls/wsgi) + shared abstractions only (`BaseModel`, `AppSetting`, payments, utils). **Domain models do NOT go in `core` — each context gets its own app** (see [App structure](#app-structure-where-models-go)). Token auth (`rest_framework.authtoken`). Package mgmt via `uv`.
- **Frontend**: React + Vite SPA in `frontend/`, routing by TanStack Router (file-based, `frontend/src/routes/`), state by Jotai. Package mgmt via `pnpm`.

## App structure (where models go)

**One Django app per domain context. A new model = a new (or existing) domain app, NEVER `core`.**

- Create it: `uv run manage.py startapp <name>` at repo root (top-level, sibling to `core/` and `api/`), add `"<name>"` to `INSTALLED_APPS` in `core/settings.py`, then `make mmg && make migrate`.
- Name apps by context (`accounts`, `billing`, `projects`), not by layer. Domain models subclass `BaseModel` from `core.models` for ObjectId PK + timestamps + `actor`.
- `core` is reserved for project config and cross-cutting shared code only (`BaseModel`, `AppSetting`, payments, utils). Do **not** add feature/domain models to `core/models.py`.

## API conventions (read before adding endpoints)

API modules live in `api/v1/{resource}_api.py`. Use class-based `from rest_framework.views import APIView` (one `APIView` subclass per resource), wired in `api/v1/urls.py` via `.as_view()`, serializers centralized in `api/v1/serializers.py`.

- **A `{resource}_api.py` view may only define the four standard CRUD methods: `get`, `patch`, `post`, `delete`** (retrieve/list, update, create, destroy on that resource). No other HTTP methods belong here.
- **Everything else goes to `api/v1/{resource}_extras_api.py`** — one extras file per resource, sibling to its `_api.py`, wired in the same `urls.py`, also `APIView` classes. "Everything else" = custom / RPC-style actions that aren't plain CRUD on the resource: auth flows (`login`, `register`, `logout`, `google`), webhooks, bulk / aggregate / side-effect endpoints.
- Example: `ProjectAPI(APIView)` in `projects_api.py` defines `get`/`patch`/`post`/`delete` for projects; `projects_extras_api.py` holds `POST /projects/{id}/archive/` or `POST /projects/import/`.

> Existing `auth_api.py` / `payments_api.py` use the older function-based `@api_view` style and predate this rule. `auth_api.py`'s custom endpoints (`login`/`register`/`logout`/`google`) are the canonical example of what now belongs in an `auth_extras_api.py`. Leave both as-is unless you're touching them for another reason.

## Auth + frontend flow (read before touching login/onboarding/routing)

- Endpoints: `api/v1/auth_api.py` — `POST /auth/google/`, `POST /auth/register/`, `POST /auth/login/` each return `{ token, user }`; `GET /auth/me/` rehydrates the user from the token; `POST /auth/logout/` deletes the token.
- The user shape is `UserSerializer` in `api/v1/serializers.py` → `{ id, email, onboarded }`. Frontend mirror: `AuthUser` in `frontend/src/features/auth/types.ts`.
- **Routing is centralized in `AuthGate`** (`frontend/src/features/auth/components/auth-gate.tsx`) — the single source of truth for redirects:
  - No token + not on a public path (`/`, `/login`, `/subjects/*` — see `isPublicPath`) → `/login`.
  - Token + `!onboarded` → `/onboarding` (the opt-in gate; dormant by default).
  - `onboarded` + on `/login` or `/onboarding` → `/dashboard`. Signed-in users are **not**
    bounced off `/` or `/subjects/*`, because those are the public syllabus, not a placeholder.
- **`onboarded` source of truth** = `get_onboarded` in `api/v1/serializers.py`. **It defaults to `True`** so a fresh template runs `login → dashboard` out of the box. The `/onboarding` page (`frontend/src/routes/onboarding.tsx`) is an optional placeholder and is unreachable while `onboarded` is always true.

### Enabling a real onboarding step

Previously the template trapped users in onboarding because `get_onboarded` read a non-existent `profile` model and always returned false with no way to complete it. To build a working onboarding flow, change **all four** touch-points in one pass:

1. **Model**: create an `accounts` app (`uv run manage.py startapp accounts`), add `"accounts"` to `INSTALLED_APPS` in `core/settings.py`, define `Profile(BaseModel)` (e.g. `full_name`, `OneToOne` to `User`) in `accounts/models.py`, then `make mmg && make migrate`. Do **not** put this in `core/models.py` (see [App structure](#app-structure-where-models-go)).
2. **Serializer**: `get_onboarded` in `api/v1/serializers.py` returns the real state (e.g. `bool(obj.profile.full_name)`).
3. **Endpoint**: add a PATCH/POST in `api/v1/auth_api.py` (wired in the v1 urls) that fills the profile / flips the flag.
4. **Frontend**: build the form in `frontend/src/routes/onboarding.tsx` to call that endpoint, then refetch `me()` so `AuthGate` redirects to `/dashboard`.

## The syllabus (this project's actual product)

A public list of AI capabilities. Every entry answers three questions: what it is, what you
can make with it, and what you had to do before it existed. **Editorial bar: only add
something that unlocks work which was impossible or wildly impractical before.** "Faster",
"cheaper", "a nicer version of an existing tool", model releases, benchmarks, and funding
news do not qualify.

The bar above is a paraphrase. The copy that actually runs lives in `syllabus/editorial.py` —
rendered for humans at `/dashboard/editorial/` and used verbatim as the crawler's rubric in
`crawl_hn.py`. Change it there, not here.

- **App**: `syllabus/` — `Subject` (an entry) and `CrawlCandidate` (every HN story already
  looked at, keyed by `hn_id` so nothing is judged or paid for twice).
- **Seed content**: `syllabus/seed_data.py`, loaded with `make seed` (idempotent;
  `--reset` removes them). Hand-written subjects are published immediately.
- **Crawler**: `make crawl` — pulls the Hacker News front page via the Algolia API,
  drops anything off-topic or below the points floor for free, then spends one OpenAI call
  per survivor to judge novelty against the existing subject index. Accepted stories become
  **drafts**; nothing reaches the public site until someone publishes it in the CMS.
  `make crawl-dry` runs the prefilter only — no API calls, nothing written.
- **Daily run** (host cron):
  `0 8 * * * cd /path/to/repo && /usr/bin/make crawl >> /tmp/hn-crawl.log 2>&1`
- **CMS** (superuser only, server-rendered Django templates — see below): `/dashboard/` stats,
  `/dashboard/subjects/?status=draft` the review queue for drafts, `/dashboard/queue/` every
  HN story the crawler judged, `/dashboard/editorial/` the rules. `/admin/` stays wired as the
  escape hatch.
- **Public API**: `GET /api/v1/syllabus/subjects/` and `.../<slug>/` — `AllowAny`, published
  only, supports `?category=` and `?q=`. Writes are admin-only by design.
- **Frontend**: `/` is the syllabus itself (a chronological log grouped by year),
  `/subjects/<slug>` is the detail page. Both are public — see `isPublicPath` in
  `auth-gate.tsx`. Feature code lives in `frontend/src/features/syllabus/`.

## The CMS (Django templates — editors only, never the public site)

Server-rendered pages under `/dashboard/`, gated by `SuperuserRequiredMixin` (`core/views.py`:
anonymous → `/login/?next=`, signed-in non-superuser → 403). **The public site is the React SPA
— do not server-render `/` or `/subjects/<slug>`.** Session auth here is separate from the
token auth the SPA uses.

- **Views**: `syllabus/views.py` (plain `View` subclasses + `Paginator`, matching repo style),
  routed in `syllabus/urls.py` under `app_name = "cms"`, included from `core/urls.py` at
  `dashboard/`. Query logic lives in `syllabus/selectors.py`, the form in `syllabus/forms.py`.
- **No JavaScript.** Filters, search and pagination are plain `GET` querystrings; the
  pagination partial uses Django's built-in `{% querystring %}` so filters survive page links.
  Consequence: there is no live slug-as-you-type — a blank slug is slugified server-side on
  save, matching `crawl_hn.create_draft`'s `-N` dedupe.
- **Publish/unpublish is its own POST endpoint**, not a form field, so `Subject.publish()`'s
  stamp-`published_on`-once semantics can't be bypassed. Unpublish uses
  `save(update_fields=["status", "updated_on"])` — `queryset.update()` would skip `auto_now`.
- **Templates all live in root `templates/`** (`templates/cms/*`, shared bits in
  `templates/_partials/*`) — the Dockerfile's tailwind stage copies only `static/` and
  `templates/`, so an app-level template dir would ship unstyled. Multi-line template comments
  must use `{% comment %}`: `{# … #}` only matches on one line, so a `{% include %}` inside a
  multi-line `{# #}` becomes a real tag and self-includes.
- **Styling**: `static/input.css` (Tailwind v4 `@theme`) mirrors the tokens in
  `frontend/src/styles.css` — two build pipelines, so a token change is a two-file change.
  Classes must be complete literal strings in the template; anything assembled from a variable
  is never generated. Run `make tw-build` (or `make tw-run`) before the pages render styled;
  `npm install` once at the repo root first.

## Dev commands (Makefile)

- `make dev` — Django dev server on :8000.
- `make web` — frontend dev server (`pnpm run dev`).
- `make migrate` / `make mmg` — apply / make migrations.
- `make seed` — load the hand-written syllabus subjects.
- `make crawl` / `make crawl-dry` — Hacker News crawl (real / prefilter-only).
- `make tw-build` / `make tw-run` — build / watch `static/output.css` for the CMS templates.
- `make build-static` — prod static: minified CSS then `collectstatic` (manifest storage turns
  a missing `output.css` into a 500, so the order matters).
- `make test` — `manage.py test` (CMS coverage lives in `syllabus/tests.py`).
- `make lint` — `ruff format` + `ruff check --fix`.
- `make dock` — full docker compose stack.
- Frontend build/typecheck: `cd frontend && pnpm run build`.
