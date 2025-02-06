from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from extensions import provider_info_db as db



class LabResult(db.Model):
    __tablename__ = 'lab_results'
    __table_args__ = {'extend_existing': True}  # Add this line
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    file_name = db.Column(db.String(100))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200))
    file_data = db.Column(db.LargeBinary)  # Store the actual PDF data
    file_type = db.Column(db.String(50))   # Store the file type (e.g., 'application/pdf')