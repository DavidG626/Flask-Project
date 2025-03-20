# models/pr1_model.py
from extensions import provider_info_db as db
from datetime import datetime

class PR1Report(db.Model):
    __tablename__ = 'pr1_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    
    # Report Type Checkboxes
    is_request_for_authorization = db.Column(db.Boolean, default=False)
    is_progress_report = db.Column(db.Boolean, default=False)
    is_response_to_request = db.Column(db.Boolean, default=False)
    is_expedited_request = db.Column(db.Boolean, default=False)
    is_change_in_work_status = db.Column(db.Boolean, default=False)
    is_change_in_patient_condition = db.Column(db.Boolean, default=False)
    is_change_in_treatment_plan = db.Column(db.Boolean, default=False)
    is_released_from_care = db.Column(db.Boolean, default=False)
    is_other = db.Column(db.Boolean, default=False)
    other_reason = db.Column(db.String(200))
    
    # Basic fields for PR1
    date_of_injury = db.Column(db.Date)
    claim_number = db.Column(db.String(100))
    employer = db.Column(db.String(100))
    
    # Administrative
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = db.relationship('Patient', backref='pr1_reports')
    
    def __repr__(self):
        return f'<PR1Report {self.id} for patient {self.patient_id}>'

class NarrativeReport(db.Model):
    __tablename__ = 'narrative_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    pr1_report_id = db.Column(db.Integer, db.ForeignKey('pr1_reports.id'))
    
    # Report Metadata
    report_date = db.Column(db.Date, default=datetime.utcnow)
    report_type = db.Column(db.String(50))  # Initial, Progress, P&S, etc.
    
    # Physical Examination
    vital_signs = db.Column(db.Text)
    general_appearance = db.Column(db.Text)
    gait = db.Column(db.Text)
    physical_exam = db.Column(db.Text)
    palpation_findings = db.Column(db.Text)
    range_of_motion = db.Column(db.Text)
    neurological_exam = db.Column(db.Text)
    
    # Diagnostic Studies
    diagnostic_studies = db.Column(db.Text)
    
    # Assessment
    diagnoses = db.Column(db.JSON)  # [{"diagnosis": "text", "icd10": "code"}]
    causation_analysis = db.Column(db.Text)
    
    # Treatment
    treatment_to_date = db.Column(db.Text)
    treatment_plan = db.Column(db.Text)
    
    # Work Status
    work_status = db.Column(db.Text)
    work_restrictions = db.Column(db.Text)
    
    # Functional Improvement
    current_functional_status = db.Column(db.Text)
    functional_goals = db.Column(db.Text)
    
    # Closing
    prognosis = db.Column(db.Text)
    mmi_status = db.Column(db.Boolean, default=False)
    anticipated_mmi_date = db.Column(db.Date)
    
    # Administrative
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('provider.id'))
    is_finalized = db.Column(db.Boolean, default=False)
    finalized_at = db.Column(db.DateTime)
    
    # Relationships
    patient = db.relationship('Patient', backref='narrative_reports')
    pr1_report = db.relationship('PR1Report', backref='narrative_reports')
    
    def __repr__(self):
        return f'<NarrativeReport {self.id} for patient {self.patient_id}>'

class DiagnosticImage(db.Model):
    __tablename__ = 'diagnostic_images'
    
    id = db.Column(db.Integer, primary_key=True)
    narrative_report_id = db.Column(db.Integer, db.ForeignKey('narrative_reports.id'))
    
    date_performed = db.Column(db.Date)
    imaging_type = db.Column(db.String(50))  # X-ray, MRI, CT, etc.
    body_part = db.Column(db.String(100))
    findings = db.Column(db.Text)
    impression = db.Column(db.Text)
    facility = db.Column(db.String(100))
    radiologist = db.Column(db.String(100))
    
    # Relationship
    narrative_report = db.relationship('NarrativeReport', backref='diagnostic_images')
    
    def __repr__(self):
        return f'<DiagnosticImage {self.id}: {self.imaging_type} of {self.body_part}>'