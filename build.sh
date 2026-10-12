#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input

# Primer despliegue: crea el administrador si se definieron las variables.
if [[ -n "${DJANGO_SUPERUSER_USERNAME:-}" && -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]]; then
  python manage.py createsuperuser --no-input || true
fi

# Carga los datos iniciales solo si SEED_ON_DEPLOY=true (quítala después del primer despliegue).
if [[ "${SEED_ON_DEPLOY:-}" == "true" ]]; then
  python manage.py seed_aplideco
fi
