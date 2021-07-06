export FLASK_APP=projector
export FLASK_ENV=production
flask db init || true
flask db migrate
flask db upgrade
