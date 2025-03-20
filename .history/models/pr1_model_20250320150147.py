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
    
    # Exam Fields
    vital_signs = db.Column(db.Text)
    general_appearance = db.Column(db.Text)
    gait = db.Column(db.Text)
    physical_exam = db.Column(db.Text)
    palpation_findings = db.Column(db.Text)
    range_of_motion = db.Column(db.Text)
    neurological_exam = db.Column(db.Text)
    diagnostic_studies = db.Column(db.Text)
    
    # Assessment
    subjective_complaints = db.Column(db.Text)
    objective_findings = db.Column(db.Text)
    diagnoses = db.Column(db.Text)
    causation_analysis = db.Column(db.Text)
    
    # Treatment
    treatment_to_date = db.Column(db.Text)
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
    
    # Relationships
    patient = db.relationship('Patient', backref='pr1_reports')
    
    def __repr__(self):
        return f'<PR1Report {self.id} for patient {self.patient_id}>'

class PR1CPT(db.Model):
    __tablename__ = 'pr1_cpt'
    
    id = db.Column(db.Integer, primary_key=True)
    pr1_id = db.Column(db.Integer, db.ForeignKey('pr1_reports.id'), nullable=False)
    cpt_id = db.Column(db.Integer, db.ForeignKey('cpt_codes.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Add unique constraint to prevent duplicates
    __table_args__ = (db.UniqueConstraint('pr1_id', 'cpt_id', name='unique_pr1_cpt'),)
    
    # Define relationships
    pr1_report = db.relationship('PR1Report', backref=db.backref('cpt_codes_rel', lazy=True))
    cpt_code = db.relationship('CPTCode', backref=db.backref('pr1_reports', lazy=True))

class PR1Authorization(db.Model):
    __tablename__ = 'pr1_authorization'
    
    id = db.Column(db.Integer, primary_key=True)
    pr1_id = db.Column(db.Integer, db.ForeignKey('pr1_reports.id'), nullable=False)
    
    # Request type
    is_new_request = db.Column(db.Boolean, default=True)
    is_resubmission = db.Column(db.Boolean, default=False)
    is_expedited = db.Column(db.Boolean, default=False)
    is_oral_confirmation = db.Column(db.Boolean, default=False)
    
    # Status tracking
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Authorization details
    authorization_number = db.Column(db.String(100))
    auth_date = db.Column(db.Date)
    
    # Foreign keys
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    
    # Relationships
    pr1_report = db.relationship('PR1Report', backref=db.backref('authorization_requests', lazy=True))
    patient = db.relationship('Patient', backref=db.backref('pr1_authorization_requests', lazy=True))
    
    def __repr__(self):
        return f'<PR1Authorization {self.id}>'

class PR1RFAItem(db.Model):
    __tablename__ = 'pr1_rfa_items'
    
    id = db.Column(db.Integer, primary_key=True)
    rfa_id = db.Column(db.Integer, db.ForeignKey('pr1_authorization.id'), nullable=False)
    
    # Required fields from form
    diagnosis = db.Column(db.String(200), nullable=False)
    icd_code = db.Column(db.String(20), nullable=False)
    service_requested = db.Column(db.String(255), nullable=False)
    cpt_code = db.Column(db.String(20))
    other_info = db.Column(db.Text)
    
    # Relationships
    rfa = db.relationship('PR1Authorization', backref=db.backref('items', lazy=True))
    
    def __repr__(self):
        return f'<PR1RFAItem {self.id}: {self.cpt_code}>'