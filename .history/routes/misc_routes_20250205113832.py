from flask import Blueprint, render_template, request, redirect, url_for, flash, session  
from flask_login import login_required, current_user, logout_user
from extensions import provider_info_db as db
from models.patient_medical_hx_models import Misc
from forms.wc_patient_portal_form import wc_PatientRegistrationForm
from datetime import datetime
import os
import io
from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename
from security import check_session_timeout
from flask import send_file


"""
Reference
class Misc(db.Model):
    __tablename__ = 'misc'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    file_name = db.Column(db.String(100))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200))
    file_data = db.Column(db.LargeBinary)
    file_type = db.Column(db.String(50))
"""