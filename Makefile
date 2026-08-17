ARCH := $(shell uname -m)

upgrade:
	uv sync
	uv lock --upgrade
	uv sync --frozen --no-install-project

audit:
	cd frontend && pnpm audit fix

lint:
	uv run ruff format .
	uv run ruff check . --fix

dev:
	uv run manage.py runserver 8000

mmg:
	uv run manage.py makemigrations

migrate:
	uv run manage.py migrate

seed:
	uv run manage.py seed_syllabus

crawl:
	uv run manage.py crawl_hn

crawl-dry:
	uv run manage.py crawl_hn --dry-run

# Manual run against the compose stack (the `cron` service does this on schedule).
# Goes through `backend`, not `cron`, so a scheduled run isn't doubled up.
crawl-docker:
	docker compose --env-file .env.docker exec -T backend uv run manage.py crawl_hn

tw-run:
	npx @tailwindcss/cli -i ./static/input.css -o ./static/output.css --watch

tw-build:
	npx @tailwindcss/cli -i ./static/input.css -o ./static/output.css

# Prod static: output.css must exist before collectstatic, or the manifest storage turns
# {% static 'output.css' %} into a 500 instead of a missing file.
build-static:
	npx @tailwindcss/cli -i ./static/input.css -o ./static/output.css --minify
	uv run manage.py collectstatic --noinput --ignore=input.css

test:
	uv run manage.py test

web:
	cd frontend && pnpm run dev

dock:
	docker compose --env-file .env.docker down
	docker compose --env-file .env.docker build
	docker compose --env-file .env.docker up -d
	docker compose --env-file .env.docker logs -f
