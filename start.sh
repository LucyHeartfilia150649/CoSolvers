#!/bin/bash
export PYTHONPATH=/app/COSOLVERS_project
python /app/COSOLVERS_project/manage.py migrate --run-syncdb || true
exec gunicorn --chdir /app/COSOLVERS_project viable_graph_project.wsgi --bind 0.0.0.0:${PORT:-8080}