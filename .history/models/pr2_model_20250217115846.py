# models/progress_note_model.py
from extensions import provider_info_db as db
from datetime import datetime

class ProgressNote(db.Model):
    __tablename__ = 'progress_notes'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    
    # Report Type Checkboxes
    is_periodic_report = db.Column(db.Boolean, default=False)
    is_change_in_treatment = db.Column(db.Boolean, default=False)
    is_release_from_care = db.Column(db.Boolean, default=False)
    is_change_in_work_status = db.Column(db.Boolean, default=False)
    is_need_for_referral = db.Column(db.Boolean, default=False)
    is_response_to_request = db.Column(db.Boolean, default=False)
    is_change_in_condition = db.Column(db.Boolean, default=False)
    is_need_for_surgery = db.Column(db.Boolean, default=False)
    is_request_for_authorization = db.Column(db.Boolean, default=False)
    other_reason = db.Column(db.String(200))
    
    # Patient Info (might be redundant with patient relationship, but matches form)
    date_of_exam = db.Column(db.Date)
    date_of_injury = db.Column(db.Date)
    return
    
    # Medical Information
    subjective_complaints = db.Column(db.Text)
    objective_findings = db.Column(db.Text)
    
    # Diagnoses (up to 12 as per form)
    diagnoses = db.Column(db.JSON)  # Store as {"1": {"description": "...", "icd10": "..."}, "2": {...}}
    
    # Treatment Plan
    treatment_plan = db.Column(db.Text)
    treatment_changes = db.Column(db.Text)
    
    # Work Status
    work_status = db.Column(db.String(50))  # 'off_work', 'modified', 'full_duty'
    off_work_until = db.Column(db.Date)
    modified_work_date = db.Column(db.Date)
    work_restrictions = db.Column(db.Text)
    full_duty_date = db.Column(db.Date)
    
    # Provider Information
    provider_signature = db.Column(db.String(100))  # Could store signature image path
    license_number = db.Column(db.String(50))
    executed_at = db.Column(db.String(100))
    executed_date = db.Column(db.Date)
    provider_specialty = db.Column(db.String(100))
    provider_phone = db.Column(db.String(20))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = db.relationship('Patient', backref='progress_notes')