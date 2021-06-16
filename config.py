import os
import json

BASE_DIR = os.path.dirname(__file__)
with open(os.path.join(BASE_DIR, 'secrets.json')) as f:
    secrets = json.loads(f.read())
GOOGLE_CLIENT_ID = secrets['google-client-id']
