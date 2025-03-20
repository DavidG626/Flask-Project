from flask import Blueprint, render_template, request, redirect, url_for, flash, session  
from flask_login import login_required, current_user, logout_user
from extensions import provider_info_db as db
from models.wc_patient_models import Patient
from models.provider_info_models import Provider
from models.icd10_models import ICD10Code
from models.cpt_model import CPTCode
from models.wc_patient_models import PatientDiagnosis, ClaimsAdmin
from models.pr1_model import PR1Report, PR1CPT,
from datetime import datetime

import os
import io
from werkzeug.utils import secure_filename
from security import check_session_timeout
from flask import send_file

import json  # For parsing JSON data

pr1_bp = Blueprint('pr1', __name__)

# List all progress notes for a patient
@pr1_bp.route('/pr1', methods=['GET', 'POST'])
@login_required
@check_session_timeout
def pr1(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to view this patient\'s progress notes.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    # Get progress notes
    progress_notes = ProgressNote.query.filter_by(patient_id=patient_id).all()
    
    # Get PR1 reports
    pr1_reports = PR1Report.query.filter_by(patient_id=patient_id).all
    
    return render_template('pr1.html', 
                           patient=patient,
                           progress_notes=progress_notes,
                           pr1_reports=pr1_reports)



@pr1_bp.route('/patient/<int:patient_id>/create_pr1', methods=['GET', 'POST'])
@login_required
@check_session_timeout
def create_pr1(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
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
        
        pr1_report = PR1Report(
            # Form checkboxes
            is_periodic_report=bool(request.form.get('is_periodic_report')),
            is_change_in_treatment=bool(request.form.get('is_change_in_treatment')),
            is_release_from_care=bool(request.form.get('is_release_from_care')),
            is_change_in_work_status=bool(request.form.get('is_change_in_work_status')),
            is_need_for_referral=bool(request.form.get('is_need_for_referral')),
            is_response_to_request=bool(request.form.get('is_response_to_request')),
            is_change_in_condition=bool(request.form.get('is_change_in_condition')),
            is_need_for_surgery=bool(request.form.get('is_need_for_surgery')),
            is_request_for_authorization=bool(request.form.get('is_request_for_authorization')),


           
            
            # subjective
            subjective_complaints=request.form.get('subjective_complaints'),
            
            # general exam
            date_of_exam=datetime.strptime(request.form.get('date_of_exam'), '%Y-%m-%d').date(),

            vital_signs=request.form.get('vital_signs'),
            general_appearance=request.form.get('general_appearance'),
            gait=request.form.get('gait'),
            physical_exam=request.form.get('physical_exam'),
            palpation_findings=request.form.get('palpation_findings'),
            range_of_motion=request.form.get('range_of_motion'),
            neurological_exam=request.form.get('neurological_exam'),
            diagnostic_studies=request.form.get('diagnostic_studies'),
            objective_findings=request.form.get('objective_findings'),
            diagnoses=request.form.get('diagnoses'),
            causation_analysis=request.form.get('causation_analysis'),

            # Treatment to date
            treatment_to_date=request.form.get('treatment_to_date'),

            # treatment plan 
            treatment_plan=request.form.get('treatment_plan'),

            # Closing
            prognosis=request.form.get('prognosis'),

            #work status
            work_status=request.form.get('work_status'),
            off_work_until=request.form.get('off_work_until'),
            modified_work_date=request.form.get('modified_work_date'),
            full_duty_date=request.form.get('full_duty_date'),
            work_restrictions=request.form.get('work_restrictions'),
            
            #provider info
            provider_signature=current_user.first_name + " " + current_user.last_name,
            license_number=current_user.medical_license,
            executed_at=request.form.get('executed_at'),
            provider_specialty=current_user.specialty,
            provider_phone=current_user.phone,
            
            
        )
        
        try:
            db.session.add(pr1_report)
            db.session.commit()

            # Add CPT codes to the progress note
            cpt_code_ids = request.form.getlist('cpt_codes')
            has_cpt_codes = False
            selected_cpt_codes = []

            if cpt_code_ids:
                for cpt_code_id in cpt_code_ids:
                    if cpt_code_id:  # Skip empty values
                        has_cpt_codes = True
                        progress_note_cpt = ProgressNoteCPT(
                            progress_note_id=pr1_report.id,
                            cpt_id=int(cpt_code_id)
                        )
                        db.session.add(progress_note_cpt)
                        
                        # Get the CPT code for RFA
                        cpt = CPTCode.query.get(int(cpt_code_id))
                        if cpt:
                            selected_cpt_codes.append(cpt)
                            
                db.session.commit()

             # Simple data reference from PR2 to RFA
            if has_cpt_codes and 'rfa_other_info' in request.form:
                
                # Create RFA
                rfa = RequestForAuthorization(
                    progress_note_id=pr1_report.id,
                    patient_id=patient_id,
                    is_new_request=bool(request.form.get('is_new_request', True)),
                    is_resubmission=bool(request.form.get('is_resubmission')),
                    is_expedited=bool(request.form.get('is_expedited')),
                    is_oral_confirmation=bool(request.form.get('is_oral_confirmation')),
                    auth_date=pr1_report.date_of_exam,
                )
                db.session.add(rfa)
                db.session.commit()

                # Get other info
                other_info = request.form.get('rfa_other_info', '')

                # Add all CPT codes as separate items on the same RFA
                for cpt in selected_cpt_codes:
                    # Include all diagnoses with each CPT code since they're required fields
                    all_diagnoses = "; ".join([diag.description for diag in diagnoses_details]) if diagnoses_details else ""
                    all_icd_codes = "; ".join([diag.code for diag in diagnoses_details]) if diagnoses_details else ""
                    
                    rfa_item = RFAItem(
                        rfa_id=rfa.id,
                        diagnosis=all_diagnoses,
                        icd_code=all_icd_codes,
                        service_requested=cpt.description,
                        cpt_code=cpt.code,
                        other_info=other_info
                    )
                    db.session.add(rfa_item)

                db.session.commit()

                flash('PR1 Report created with RFA!', 'success')
                return redirect(url_for('progress_note_bp.view_rfa', rfa_id=rfa.id))

            flash('PR1 Report created successfully!', 'success')
            return redirect(url_for('pr2.progress_notes', patient_id=patient_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating PR1 note: {str(e)}', 'error')
            return redirect(request.url)
    
    # Return template with all necessary variables
    return render_template('create_pr1.html',                       
                    patient=patient,
                    patient_diagnoses=diagnoses_details,
                    icd10_codes=icd10_codes,
                    cpt_codes=cpt_codes,
                    cpt_search_term=cpt_search_term)

            
                
       

