# in models/patient_medical_hx_models.py
class LabResult(db.Model):
    __tablename__ = 'lab_results'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    file_name = db.Column(db.String(100))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200))
    file_path = db.Column(db.String(200))