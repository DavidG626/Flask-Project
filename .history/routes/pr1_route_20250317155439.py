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



@pr1_bp.route('/patient/<int:patient_id>/create_pr1', methods=['GET', 'POST'])
@login_required
@check_session_timeout
def create_pr1(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    cpt_codes = CPTCode.query.order_by(CPTCode.code).all()
    
    # Get patient's existing diagnoses
    patient_diagnoses = PatientDiagnosis.query.filter_by(patient_id=patient_id).all()
    diagnoses_details = []
    for diag in patient_diagnoses:
        icd10_code = ICD10Code.query.get(diag.icd10_id)
        if icd10_code:
            diagnoses_details.append(icd10_code)

    # Get ICD-10 codes ordered by description
    icd10_codes = ICD10Code.query.order_by(ICD10Code.description).all()

     # Get CPT codes for dropdown based on search term
    cpt_search_term = request.args.get('cpt_search', '')
    if cpt_search_term:
        cpt_codes = CPTCode.query.filter(
            (CPTCode.code.ilike(f'%{cpt_search_term}%')) |
            (CPTCode.description.ilike(f'%{cpt_search_term}%'))
        ).order_by(CPTCode.description).limit(50).all()
    else:
        # Without a search term, just get a few codes or none
        cpt_codes = CPTCode.query.order_by(CPTCode.code).limit(20).all()

    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to create progress notes for this patient.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    if request.method == 'POST':
        # Create new PR1Report
        pr1_report = PR1Report(
            patient_id=patient_id,
            date_of_exam=datetime.strptime(request.form.get('date_of_exam'), '%Y-%m-%d').date(),
            return_to_work=datetime.strptime(request.form.get('work_status_date'), '%Y-%m-%d').date(),
            subjective_complaints=request.form.get('subjective_complaints'),
            objective_findings=request.form.get('objective_findings'),
            diagnoses=request.form.get('diagnoses'), 
            treatment_plan=request.form.get('treatment_plan'),
            work_status=request.form.get('work_status'),
            work_restrictions=request.form.get('work_restrictions'),
            provider_signature=current_user.first_name + " " + current_user.last_name,
            license_number=current_user.medical_license,
            executed_at=request.form.get('executed_at'),
            provider_specialty=current_user.specialty,
            provider_phone=current_user.phone,
    
        
 
                
       

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