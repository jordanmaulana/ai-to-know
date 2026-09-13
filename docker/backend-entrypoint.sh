#!/bin/sh
set -e

# No postgres wait loop: compose's `depends_on: {postgres: service_healthy}` already
# gates both backend and cron, and the old loop spawned a Python interpreter once per second.

if [ "${ROLE:-web}" = "web" ]; then
  python manage.py migrate --noinput
  # input.css is the Tailwind source, not a served asset: its @import "tailwindcss" is not a
  # real URL, and the manifest storage fails the whole collect trying to resolve it.
  python manage.py collectstatic --noinput --ignore=input.css
fi

exec "$@"
