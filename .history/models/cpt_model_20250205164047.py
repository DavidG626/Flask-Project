# models/cpt_model.py
from extensions import provider_info_db as db
from datetime import datetime

class CPTCode(db.Model):
    __tablename__ = 'cpt_codes'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float)
    category = db.Column(db.String(50))  # e.g., "Surgery", "Evaluation", etc.
    added_date = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)