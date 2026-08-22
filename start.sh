#!/bin/bash
cd /app/COSOLVERS_project
python manage.py migrate --run-syncdb
exec gunicorn viable_graph_project.wsgi --bind 0.0.0.0:${PORT:-8080}
