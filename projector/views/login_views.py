from flask import Blueprint, render_template

bp = Blueprint('login', __name__, url_prefix='/login')
google_client_id = ''

def set_client_id(state):
    global google_client_id
    google_client_id = state.app.config['GOOGLE_CLIENT_ID']
bp.record(set_client_id)

@bp.route('/')
def login():
    return render_template('login.html', client_id=google_client_id)
