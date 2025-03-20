# models/pr1_model.py
from extensions import provider_info_db as db
from datetime import datetime

class PR1Report(db.Model):
    __tablename__ = 'pr1_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    
    # Fields unique to PR1 Reports
    is_progress_report = db.Column(db.Boolean, default=False)
    is_expedited_request = db.Column(db.Boolean, default=False)
    is_change_in_patient_condition = db.Column(db.Boolean, default=False)
    is_change_in_treatment_plan = db.Column(db.Boolean, default=False)
    is_released_from_care = db.Column(db.Boolean, default=False)
    
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
    current_functional_status = db.Column(db.Text)
    functional_goals = db.Column(db.Text)
    
    # Administrative
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = db.relationship('Patient', backref='pr1_reports')
    
    def __repr__(self):
        return f'<PR1Report {self.id} for patient {self.patient_id}>'