from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from extensions import provider_info_db as db

class Patient(db.Model):
    __tablename__ = 'patient'
    
   ', uselist=False, cascade='all, delete-orphan')

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

#pmh
class PastMedicalHistory(db.Model):
    __tablename__ = 'past_medical_history'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.Date)
    
    # Medical Conditions (Boolean fields)
    allergies = db.Column(db.Boolean, default=False)
    anemia = db.Column(db.Boolean, default=False)
    anxiety = db.Column(db.Boolean, default=False)
    arthritis = db.Column(db.Boolean, default=False)
    asthma = db.Column(db.Boolean, default=False)
    blood_transfusion = db.Column(db.Boolean, default=False)
    cancer = db.Column(db.Boolean, default=False)
    congestive_heart_failure = db.Column(db.Boolean, default=False)
    nerve_muscle_disease = db.Column(db.Boolean, default=False)
    lung_disease = db.Column(db.Boolean, default=False)
    meningitis = db.Column(db.Boolean, default=False)
    depression = db.Column(db.Boolean, default=False)
    hiv_aids = db.Column(db.Boolean, default=False)
    kidney_disease = db.Column(db.Boolean, default=False)
    diabetes = db.Column(db.Boolean, default=False)
    clotting_disorder = db.Column(db.Boolean, default=False)
    high_blood_pressure = db.Column(db.Boolean, default=False)
    acid_reflux = db.Column(db.Boolean, default=False)
    glaucoma = db.Column(db.Boolean, default=False)
    gout = db.Column(db.Boolean, default=False)
    heart_attack = db.Column(db.Boolean, default=False)
    high_cholesterol = db.Column(db.Boolean, default=False)
    osteoporosis = db.Column(db.Boolean, default=False)
    seizures = db.Column(db.Boolean, default=False)
    sickle_cell = db.Column(db.Boolean, default=False)
    stroke = db.Column(db.Boolean, default=False)
    substance_abuse = db.Column(db.Boolean, default=False)
    thyroid_disease = db.Column(db.Boolean, default=False)
    tuberculosis = db.Column(db.Boolean, default=False)
    ulcers = db.Column(db.Boolean, default=False)
    anesthetic_complications = db.Column(db.Boolean, default=False)
    cataracts = db.Column(db.Boolean, default=False)
    other_medical = db.Column(db.String(200))  # For "Other" field
    no_medical_history = db.Column(db.Boolean, default=False)  # For "No medical history to report"

    # Surgical History (Boolean fields)
    appendix = db.Column(db.Boolean, default=False)
    brain_surgery = db.Column(db.Boolean, default=False)
    breast_surgery = db.Column(db.Boolean, default=False)
    heart_bypass = db.Column(db.Boolean, default=False)
    gall_bladder = db.Column(db.Boolean, default=False)
    colon_surgery = db.Column(db.Boolean, default=False)
    fracture_surgery = db.Column(db.Boolean, default=False)
    hernia_repair = db.Column(db.Boolean, default=False)
    c_section = db.Column(db.Boolean, default=False)
    eye_surgery = db.Column(db.Boolean, default=False)
    hysterectomy = db.Column(db.Boolean, default=False)
    joint_replacement = db.Column(db.Boolean, default=False)
    small_intestine = db.Column(db.Boolean, default=False)
    spine_surgery = db.Column(db.Boolean, default=False)
    tubes_tied = db.Column(db.Boolean, default=False)
    valve_replacement = db.Column(db.Boolean, default=False)
    cosmetic_surgery = db.Column(db.Boolean, default=False)
    orthopedic_surgery = db.Column(db.String(200))  # For specific ortho surgery
    other_surgery = db.Column(db.String(200))  # For "Other" surgery
    never_had_surgery = db.Column(db.Boolean, default=False)

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
    
    # Relationship with Patient
    patient = db.relationship('Patient', backref='medical_history', uselist=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)