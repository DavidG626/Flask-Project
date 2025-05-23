from extensions import provider_info_db as db
from datetime import datetime

class Allergy(db.Model):
   __tablename__ = 'allergies'
   id = db.Column(db.Integer, primary_key=True)
   medical_history_id = db.Column(db.Integer, db.ForeignKey('past_medical_history.id'), nullable=False)
   allergy_name = db.Column(db.String(100))

class MedicalCondition(db.Model):
   __tablename__ = 'medical_conditions'
   id = db.Column(db.Integer, primary_key=True)
   medical_history_id = db.Column(db.Integer, db.ForeignKey('past_medical_history.id'), nullable=False)
   condition_name = db.Column(db.String(100))

class Surgery(db.Model):
   __tablename__ = 'surgeries'
   id = db.Column(db.Integer, primary_key=True)
   medical_history_id = db.Column(db.Integer, db.ForeignKey('past_medical_history.id'), nullable=False)
   surgery_name = db.Column(db.String(100))
   surgery_date = db.Column(db.Date, nullable=True)

class Medication(db.Model):
   __tablename__ = 'medications'
   id = db.Column(db.Integer, primary_key=True)
   medical_history_id = db.Column(db.Integer, db.ForeignKey('past_medical_history.id'), nullable=False)
   medication_name = db.Column(db.String(100))
   dosage = db.Column(db.String(50))
   frequency = db.Column(db.String(50))

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

   # Timestamps
   created_at = db.Column(db.DateTime, default=datetime.utcnow)
   updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)