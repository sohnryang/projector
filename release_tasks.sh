export FLASK_APP=projector
flask shell 'from projector import db;db.create_all()'
