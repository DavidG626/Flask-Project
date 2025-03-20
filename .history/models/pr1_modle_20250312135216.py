from extensions import provider_info_db as db
from datetime import datetime

class Pr1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pate