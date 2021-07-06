export FLASK_APP=projector
export FLASK_ENV=production
flask db migrate
flask db upgrade
