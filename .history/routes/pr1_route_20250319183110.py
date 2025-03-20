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
    
    
    return render_template('pr1.html', 
                           patient=patient
                           progress_notes=progress_notes,
                           pr1_reports=pr1_reports)



@pr1_bp.route('/patient/<int:patient_id>/create_pr1', methods=['GET', 'POST'])
@login_required
@check_session_timeout
def create_pr1(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    # Get today's date
    today_date = datetime.now().strftime('%Y-%m-%d')
    
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
        flash('You do not have permission to create reports for this patient.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    if request.method == 'POST':
        # Create new PR1Report
        pr1_report = PR1Report(
            patient_id=patient_id,
            
            # Report Type Checkboxes
            is_request_for_authorization=bool(request.form.get('is_request_for_authorization')),
            is_progress_report=bool(request.form.get('is_progress_report')),
            is_response_to_request=bool(request.form.get('is_response_to_request')),
            is_expedited_request=bool(request.form.get('is_expedited_request')),
            is_change_in_work_status=bool(request.form.get('is_change_in_work_status')),
            is_change_in_patient_condition=bool(request.form.get('is_change_in_patient_condition')),
            is_change_in_treatment_plan=bool(request.form.get('is_change_in_treatment_plan')),
            is_released_from_care=bool(request.form.get('is_released_from_care')),
            is_other=bool(request.form.get('is_other')),
            other_reason=request.form.get('other_reason'),
            
            # Basic fields
            date_of_injury=datetime.strptime(request.form.get('date_of_injury'), '%Y-%m-%d').date() if request.form.get('date_of_injury') else None,
            claim_number=request.form.get('claim_number'),
            employer=request.form.get('employer')
        )
        
        try:
            db.session.add(pr1_report)
            db.session.commit()
            
            # Create associated narrative report
            narrative_report = NarrativeReport(
                patient_id=patient_id,
                pr1_report_id=pr1_report.id,
                report_date=datetime.strptime(request.form.get('report_date'), '%Y-%m-%d').date() if request.form.get('report_date') else datetime.now().date(),
                report_type=request.form.get('report_type'),
                
                # Physical Examination
                vital_signs=request.form.get('vital_signs'),
                general_appearance=request.form.get('general_appearance'),
                gait=request.form.get('gait'),
                physical_exam=request.form.get('physical_exam'),
                palpation_findings=request.form.get('palpation_findings'),
                range_of_motion=request.form.get('range_of_motion'),
                neurological_exam=request.form.get('neurological_exam'),
                
                # Diagnostic Studies
                diagnostic_studies=request.form.get('diagnostic_studies'),
                
                # Assessment
                diagnoses=request.form.get('diagnoses_json'),
                causation_analysis=request.form.get('causation_analysis'),
                
                # Treatment
                treatment_to_date=request.form.get('treatment_to_date'),
                treatment_plan=request.form.get('treatment_plan'),
                
                # Work Status
                work_status=request.form.get('work_status'),
                work_restrictions=request.form.get('work_restrictions'),
                
                # Functional Improvement
                current_functional_status=request.form.get('current_functional_status'),
                functional_goals=request.form.get('functional_goals'),
                
                # Closing
                prognosis=request.form.get('prognosis'),
                mmi_status=request.form.get('mmi_status') == 'on',
                anticipated_mmi_date=datetime.strptime(request.form.get('anticipated_mmi_date'), '%Y-%m-%d').date() if request.form.get('anticipated_mmi_date') else None,
                
                # Administrative
                created_by=current_user.id
            )
            
            db.session.add(narrative_report)
            db.session.commit()
            
            flash('PR1 Report created successfully!', 'success')
            return redirect(url_for('pr2.progress_notes', patient_id=patient_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating PR1 report: {str(e)}', 'error')
            return redirect(request.url)
    
    # For GET request
    return render_template('create_pr1.html', 
                           patient=patient, 
                           diagnoses_details=diagnoses_details,
                           icd10_codes=icd10_codes,
                           cpt_codes=cpt_codes,
                           cpt_search_term=cpt_search_term,
                           today_date=today_date)
                
       

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
    provider = current_user
    
    # Just use the template name without the folder path
    return render_template('view_pr1.html', 
                          pr1_report=pr1_report, 
                          patient=patient,
                          narrative_report=narrative_report,
                          diagnostic_images=diagnostic_images,
                          diagnoses=diagnoses,
                          provider=provider)