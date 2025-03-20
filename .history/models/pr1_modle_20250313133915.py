from extensions import provider_info_db as db
from datetime import datetime

class Pr1(db.Model):
    __tablename__ = 'pr1'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

# models/narrative_report_model.py
from extensions import provider_info_db as db
from datetime import datetime

class NarrativeReport(db.Model):
    __tablename__ = 'narrative_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    pr1_report_id = db.Column(db.Integer, db.ForeignKey('pr1_reports.id'))
    
    # Report Metadata
    report_date = db.Column(db.Date, default=datetime.utcnow)
    report_type = db.Column(db.String(50))  # Initial, Progress, P&S, etc.
    
    # Case Information
    date_of_injury = db.Column(db.Date)
    claim_number = db.Column(db.String(100))
    employer = db.Column(db.String(100))
    insurance_carrier = db.Column(db.String(100))
    adjuster = db.Column(db.String(100))
    
    # Clinical Information
    history_present_illness = db.Column(db.Text)
    past_medical_history = db.Column(db.Text)
    surgical_history = db.Column(db.Text)
    current_medications = db.Column(db.Text)
    allergies = db.Column(db.Text)
    social_history = db.Column(db.Text)
    
    # Physical Examination
    vital_signs = db.Column(db.Text)
    general_appearance = db.Column(db.Text)
    gait = db.Column(db.Text)
    spine_inspection = db.Column(db.Text)
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
    
    # Certification
    physician_name = db.Column(db.String(100))
    physician_credentials = db.Column(db.String(100))
    license_number = db.Column(db.String(50))
    npi_number = db.Column(db.String(20))
    physician_signature = db.Column(db.String(100))  # Could store signature image path
    
    # Administrative
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
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