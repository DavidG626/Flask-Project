from flask import Blueprint, render_template, request, redirect, url_for, flash, session  
from flask_login import login_required, current_user, logout_user
from extensions import provider_info_db as db
from models.wc_patient_models import Patient
from models.provider_info_models import Provider
from models.icd10_models import ICD10Code
from models.cpt_model import CPTCode
from models.wc_patient_models import PatientDiagnosis, ClaimsAdmin
from models.pr2_model import ProgressNote, ProgressNoteCPT, RequestForAuthorization, RFAItem
from datetime import datetime
import os
import io
from werkzeug.utils import secure_filename
from security import check_session_timeout
from flask import send_file

from models.pr1_model import PR1Report, NarrativeReport, DiagnosticImage
import json  # For parsing JSON data

pr1_bp = Blueprint('pr1', __name__)

@pr1_bp.route('/pr1', methods=['GET', 'POST'])
@login_required
def pr1(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to view this patient\'s progress notes.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    return render_template('pr1.html', patient=patient)




                
       

@pr1_bp.route('/pr1/<int:pr1_id>')
@login_required
@check_session_timeout
def view_pr1(pr1_id):
    # Get the PR1 report
    pr1_report = PR1Report.query.get_or_404(pr1_id)
    patient = Patient.query.get(pr1_report.patient_id)
    
    # Check permission
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to view this PR1 report.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    # Get the associated narrative report
    narrative_report = NarrativeReport.query.filter_by(pr1_report_id=pr1_id).first()
    
    # Get diagnostic images if any exist
    diagnostic_images = []
    if narrative_report:
        diagnostic_images = DiagnosticImage.query.filter_by(narrative_report_id=narrative_report.id).all()
    
    # Parse diagnoses JSON if it exists
    diagnoses = []
    if narrative_report and narrative_report.diagnoses:
        try:
            diagnoses = json.loads(narrative_report.diagnoses)
        except:
            # Handle potential JSON parsing error
            pass
    
    return render_template('pr1/view_pr1.html', 
                          pr1_report=pr1_report, 
                          patient=patient,
                          narrative_report=narrative_report,
                          diagnostic_images=diagnostic_images,
                          diagnoses=diagnoses)