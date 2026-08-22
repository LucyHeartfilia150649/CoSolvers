@'
#!/bin/bash
set -e
cd /app/COSOLVERS_project
python manage.py migrate --run-syncdb || true
exec gunicorn viable_graph_project.wsgi --bind 0.0.0.0:${PORT:-8080}
'@ | Set-Content -Encoding utf8 start.sh