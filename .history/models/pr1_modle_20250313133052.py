from extensions import provider_info_db as db
from datetime import datetime

class Pr1(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

