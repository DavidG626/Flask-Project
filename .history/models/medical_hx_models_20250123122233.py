from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from datetime import datetime
from extensions import provider_info_db as db

class Allergy(db.Model):
    __tablename__ = 'allergies'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    medical_history_id = db.Column(db.Integer, db.ForeignKey('past_medical_history.id'), nullable=False)
    allergy_name = db.Column(db.String(100))

class MedicalCondition(db.Model):
    __tablename__ = 'medical_conditions'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    medical_history_id = db.Column(db.Integer, db.ForeignKey('past_medical_history.id'), nullable=False)
    condition_name = db.Column(db.String(100))

class Surgery(db.Model):
    __tablename__ = 'surgeries'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    medical_history_id = db.Column(db.Integer, db.ForeignKey('past_medical_history.id'), nullable=False)
    surgery_name = db.Column(db.String(100))
    surgery_date = db.Column(db.Date, nullable=True)

class Medication(db.Model):
    __tablename__ = 'medications'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    medical_history_id = db.Column(db.Integer, db.ForeignKey('past_medical_history.id'), nullable=False)
    medication_name = db.Column(db.String(100))