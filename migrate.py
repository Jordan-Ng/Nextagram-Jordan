import os
from dotenv import load_dotenv

os.environ['MIGRATION'] = '1'

if not os.getenv('FLASK_ENV') == 'production':
    print("Loading environment variables from .env")
    load_dotenv()

import peeweedbevolve
from models.base_model import db
from models import *

print("Running Migration")
if os.getenv('FLASK_ENV') == 'production':
    db.evolve(ignore_tables={'base_model'}, interactive=False)
else:
    db.evolve(ignore_tables={'base_model'})
print("Finish Migration")
