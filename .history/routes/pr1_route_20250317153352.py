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
    
    if request.method == 'POST':
        # Create new PR1Report
        pr1_report = PR1Report(
            patient_id=patient_id,
            is_request_for_authorization=request.form.get('is_request_for_authorization') == 'on',
            is_progress_report=request.form.get('is_progress_report') == 'on',
            is_response_to_request=request.form.get('is_response_to_request') == 'on',
            is_expedited_request=request.form.get('is_expedited_request') == 'on',
            is_change_in_work_status=request.form.get('is_change_in_work_status') == 'on',
            is_change_in_patient_condition=request.form.get('is_change_in_patient_condition') == 'on',
            is_change_in_treatment_plan=request.form.get('is_change_in_treatment_plan') == 'on',
            is_released_from_care=request.form.get('is_released_from_care') == 'on',
            is_other=request.form.get('is_other') == 'on',
            other_reason=request.form.get('other_reason'),
            date_of_injury=datetime.strptime(request.form.get('date_of_injury'), '%Y-%m-%d').date() if request.form.get('date_of_injury') else None,
            claim_number=request.form.get('claim_number'),
            employer=request.form.get('employer')
        )
        
        db.session.add(pr1_report)
        db.session.commit()
        
        # Create associated narrative report
        narrative_report = NarrativeReport(
            patient_id=patient_id,
            pr1_report_id=pr1_report.id,
            report_date=datetime.now().date(),
            report_type=request.form.get('report_type'),
            vital_signs=request.form.get('vital_signs'),
            general_appearance=request.form.get('general_appearance'),
            gait=request.form.get('gait'),
            physical_exam=request.form.get('physical_exam'),
            palpation_findings=request.form.get('palpation_findings'),
            range_of_motion=request.form.get('range_of_motion'),
            neurological_exam=request.form.get('neurological_exam'),
            diagnostic_studies=request.form.get('diagnostic_studies'),
            diagnoses=request.form.get('diagnoses_json'),  # You'll need to format this as JSON
            causation_analysis=request.form.get('causation_analysis'),
            treatment_to_date=request.form.get('treatment_to_date'),
            treatment_plan=request.form.get('treatment_plan'),
            work_status=request.form.get('work_status'),
            work_restrictions=request.form.get('work_restrictions'),
            current_functional_status=request.form.get('current_functional_status'),
            functional_goals=request.form.get('functional_goals'),
            prognosis=request.form.get('prognosis'),
            mmi_status=request.form.get('mmi_status') == 'on',
            anticipated_mmi_date=datetime.strptime(request.form.get('anticipated_mmi_date'), '%Y-%m-%d').date() if request.form.get('anticipated_mmi_date') else None,
            created_by=current_user.id
        )
        
        db.session.add(narrative_report)
        db.session.commit()
        
        flash('PR1 Report created successfully!', 'success')
        return redirect(url_for('pr1.view_pr1', pr1_id=pr1_report.id))
    
    # For GET request - show form
    return render_template('create_pr1.html', 
                           patient=patient, 
                           diagnoses_details=diagnoses_details,
                           icd10_codes=icd10_codes)


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