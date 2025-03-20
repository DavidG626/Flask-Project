# models/pr1_model.py
from extensions import provider_info_db as db
from datetime import datetime

class PR1Report(db.Model):
    __tablename__ = 'pr1_reports'
    
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
    
    # Patient Info
    date_of_exam = db.Column(db.Date)
    date_of_injury = db.Column(db.Date)
    
    # Fields for PR1-specific exam data
    vital_signs = db.Column(db.Text)
    general_appearance = db.Column(db.Text)
    gait = db.Column(db.Text)
    physical_exam = db.Column(db.Text)
    palpation_findings = db.Column(db.Text)
    range_of_motion = db.Column(db.Text)
    neurological_exam = db.Column(db.Text)
    diagnostic_studies = db.Column(db.Text)
    causation_analysis = db.Column(db.Text)
    treatment_to_date = db.Column(db.Text)
    
    # Assessment
    subjective_complaints = db.Column(db.Text)
    objective_findings = db.Column(db.Text)
    diagnoses = db.Column(db.Text)
    
    # Treatment Plan
    treatment_plan = db.Column(db.Text)
    
    # Work Status
    work_status = db.Column(db.String(50))
    off_work_until = db.Column(db.Date)
    modified_work_date = db.Column(db.Date)
    work_restrictions = db.Column(db.Text)
    full_duty_date = db.Column(db.Date)
    
    # Closing
    prognosis = db.Column(db.Text)
    
    # Provider Information
    provider_signature = db.Column(db.String(100))
    license_number = db.Column(db.String(50))
    executed_at = db.Column(db.String(100))
    provider_specialty = db.Column(db.String(100))
    provider_phone = db.Column(db.String(20))
    
    # Administrative
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = db.relationship('Patient', backref='pr1_reports')
    
    def __repr__(self):
        return f'<PR1Report {self.id} for patient {self.patient_id}>'