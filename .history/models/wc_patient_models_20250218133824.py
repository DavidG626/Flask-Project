from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from extensions import provider_info_db as db
from .patient_medical_hx_models import PastMedicalHistory
from .icd10_models import ICD10Code

class Patient(db.Model):
   __tablename__ = 'patient'
   
   id = db.Column(db.Integer, primary_key=True)
   patient_first_name = db.Column(db.String(20), nullable=False)  
   patient_last_name = db.Column(db.String(20), nullable=False)
   patient_occupation = db.Column(db.String(20))
   patient_sex = db. Column(db.String(20), nullable=False)
   patient_address = db.Column(db.String(200), nullable=False)
   patient_city = db.Column(db.String(50), nullable=False)
   patient_state = db.Column(db.String(20), nullable=False) 
   patient_zip_code = db.Column(db.String(10), nullable=False)
   patient_date_of_birth = db.Column(db.Date, nullable=False)
   patient_date_of_injury = db.Column(db.Date, nullable=False)
   patient_claim_number = db.Column(db.String(50), nullable=False)
   diagnoses = db.relationship('ICD10Code', secondary='patient_diagnoses', 
                              backref=db.backref('patients', lazy='dynamic'))
   
   # Provider relationship
   provider_first_name = db.Column(db.String(20), nullable=False)
   provider_last_name = db.Column(db.String(20), nullable=False)
   
   # Relationships to other tables
   employer = db.relationship('Employer', backref='patient', uselist=False, cascade='all, delete-orphan')
   claims_admin = db.relationship('ClaimsAdmin', backref='patient', uselist=False, cascade='all, delete-orphan')
   lawyer = db.relationship('Lawyer', backref='patient', uselist=False, cascade='all, delete-orphan')
   medical_history = db.relationship('PastMedicalHistory', backref='patient', uselist=False, cascade='all, delete-orphan')
   lab_results = db.relationship('LabResult', backref='patient', cascade='all, delete-orphan')
   imaging_results = db.relationship('ImagingResult', backref='patient', cascade='all, delete-orphan')
   operative_reports = db.relationship('OperativeReport', backref='patient', cascade='all, delete-orphan')
   misc_results = db.relationship('Misc', backref='patient', cascade='all, delete-orphan')
   authorizations = db.relationship('Auth', backref='patient', cascade='all, delete-orphan')



class Employer(db.Model):
   __tablename__ = 'employer'
   
   id = db.Column(db.Integer, primary_key=True)
   patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
   employer_name = db.Column(db.String(100), nullable=False)
   employer_address = db.Column(db.String(200), nullable=False)
   employer_city = db.Column(db.String(50), nullable=False)
   employer_state = db.Column(db.String(20), nullable=False)
   employer_zip_code = db.Column(db.String(10), nullable=False)
   employer_phone = db.Column(db.String(20), nullable=False)
   employer_fax = db.Column(db.String(20))

class ClaimsAdmin(db.Model):
   __tablename__ = 'claims_admin'
   
   id = db.Column(db.Integer, primary_key=True)
   patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
   admin_name = db.Column(db.String(100), nullable=False)
   adjustor = db.Column(db.String(100), nullable=False)
   adjustor_address = db.Column(db.String(200), nullable=False)
   adjustor_city = db.Column(db.String(50), nullable=False)
   adjustor_state = db.Column(db.String(20), nullable=False)
   adjustor_zip_code = db.Column(db.String(10), nullable=False)
   adjustor_phone = db.Column(db.String(20), nullable=False)
   adjustor_fax = db.Column(db.String(20))
   adjustor_email = db.Column(db.String(120))

class Lawyer(db.Model):
   __tablename__ = 'lawyer'
   
   id = db.Column(db.Integer, primary_key=True)
   patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
   lawyer_name = db.Column(db.String(100))
   lawyer_address = db.Column(db.String(200))
   lawyer_city = db.Column(db.String(50))
   lawyer_state = db.Column(db.String(20))
   lawyer_zip_code = db.Column(db.String(10))
   lawyer_phone = db.Column(db.String(20))
   lawyer_fax = db.Column(db.String(20))
   lawyer_email = db.Column(db.String(120))

class PatientDiagnosis(db.Model):
    __tablename__ = 'patient_diagnoses'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    icd10_id = db.Column(db.Integer, db.ForeignKey('icd10_codes.id'), nullable=False)