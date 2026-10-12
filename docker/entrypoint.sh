#!/usr/bin/env bash
set -ex

# Install dependencies (virtualenv lives in /opt/venv, see Dockerfile)
uv sync --extra mysql

# Point Django at the db service, unless a local_settings.py already exists
if [ ! -f bang_project/local_settings.py ]; then
  cat > bang_project/local_settings.py <<PY
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bangdream',
        'USER': 'root',
        'PASSWORD': 'bangdream',
        'HOST': 'db',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
PY
fi

# Clone the static repo if it doesn't exist
if [ ! -d bang/static ]; then
  git clone https://github.com/xJakub/BanGDream-Static.git /tmp/BanGDream-Static
  mv /tmp/BanGDream-Static bang/static
fi

# Download front-end dependencies
bower install --allow-root

# Create tables, then generate the generated settings and CSS
uv run python manage.py migrate
uv run python manage.py generate_settings
uv run python manage.py generate_css

# Launch the server
while true
do
  echo "Starting server at http://localhost:8000/"
  uv run python manage.py runserver 0.0.0.0:8000 || true
  echo "Waiting 5 seconds until next start..."
  sleep 5
done
