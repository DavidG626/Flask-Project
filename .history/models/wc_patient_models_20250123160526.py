from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from extensions import provider_info_db as db

class Patient(db.Model):
    __tablename__ = 'patient'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_first_name = db.Column(db.String(20), nullable=False)
    patient_last_name = db.Column(db.String(20), nullable=False)
    patient_address = db.Column(db.String(200), nullable=False)
    patient_city = db.Column(db.String(50), nullable=False)
    patient_state = db.Column(db.String(20), nullable=False)
    patient_zip_code = db.Column(db.String(10), nullable=False)
    patient_date_of_birth = db.Column(db.Date, nullable=False)
    patient_date_of_injury = db.Column(db.Date, nullable=False)
    patient_claim_number = db.Column(db.String(50), nullable=False)
    
    # Provider relationship
    provider_first_name = db.Column(db.String(20), nullable=False)
    provider_last_name = db.Column(db.String(20), nullable=False)
    
    # Relationships to other tables
    body_parts = db.relationship('BodyPart', backref='patient', cascade='all, delete-orphan')
    employer = db.relationship('Employer', backref='patient', uselist=False, cascade='all, delete-orphan')
    claims_admin = db.relationship('ClaimsAdmin', backref='patient', uselist=False, cascade='all, delete-orphan')
    lawyer = db.relationship('Lawyer', backref='patient', uselist=False, cascade='all, delete-orphan')
    medical_history = db.relationship('PastMedicalHistory', backref='patient', uselist=False, cascade='all, delete-orphan')

class BodyPart(db.Model):
    __tablename__ = 'body_parts'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    body_part_name = db.Column(db.String(50), nullable=False)

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


  
class PastMedicalHistory(db.Model):
   __tablename__ = 'past_medical_history'
   id = db.Column(db.Integer, primary_key=True)
   patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
   date = db.Column(db.Date)

   # Relationships
   allergies = db.relationship('Allergy', backref='medical_history', cascade='all, delete-orphan')
   medical_conditions = db.relationship('MedicalCondition', backref='medical_history', cascade='all, delete-orphan')
   surgeries = db.relationship('Surgery', backref='medical_history', cascade='all, delete-orphan')
   medications = db.relationship('Medication', backref='medical_history', cascade='all, delete-orphan')
   
   # Social History
   current_smoker = db.Column(db.Boolean, default=False)
   former_smoker = db.Column(db.Boolean, default=False) 
   quit_date = db.Column(db.Date)
   never_smoker = db.Column(db.Boolean, default=False)
   passive_smoker = db.Column(db.Boolean, default=False)
   vaping = db.Column(db.Boolean, default=False)
   
   # Alcohol intake
   wine_per_week = db.Column(db.Integer)
   beer_per_week = db.Column(db.Integer)
   liquor_per_week = db.Column(db.Integer)
   
   # Drug use
   marijuana = db.Column(db.Boolean, default=False)
   cocaine = db.Column(db.Boolean, default=False)
   meth = db.Column(db.Boolean, default=False)
   iv_drugs = db.Column(db.Boolean, default=False)

   created_at = db.Column(db.DateTime, default=datetime.utcnow)
   updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)