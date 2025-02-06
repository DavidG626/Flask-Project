from extensions import provider_info_db as db
from datetime import datetime

class ICD10Code(db.Model):
    __tablename__ = 'icd10_codes'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)