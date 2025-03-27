from flask import Blueprint, render_template, request, redirect, url_for, flash, session  
from flask_login import login_required, current_user, logout_user
from extensions import provider_info_db as db
from models.wc_patient_models import Patient
from models.provider_info_models import Provider
from models.icd10_models import ICD10Code
from models.cpt_model import CPTCode
from models.wc_patient_models import PatientDiagnosis, ClaimsAdmin
from models.pr2_model import ProgressNote, ProgressNoteCPT, RequestForAuthorization, RFAItem
from models.pr1_model import PR1Report 
from datetime import datetime

import os
import io
from werkzeug.utils import secure_filename
from security import check_session_timeout
from flask import send_file


progress_note_bp = Blueprint('pr2', __name__)
pr1_bp = Blueprint('pr1', __name__)

# List all progress notes for a patient
@progress_note_bp.route('/patient/<int:patient_id>/progress_notes')
@login_required
@check_session_timeout
def progress_notes(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to view this patient\'s progress notes.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    # Get progress notes
    progress_notes = ProgressNote.query.filter_by(patient_id=patient_id).all()
    
    # Get PR1 reports
    pr1_reports = PR1Report.query.filter_by(patient_id=patient_id).all()
    
    return render_template('progress_notes.html', 
                          patient=patient, 
                          progress_notes=progress_notes,
                          pr1_reports=pr1_reports)

@progress_note_bp.route('/patient/<int:patient_id>/create_progress_note', methods=['GET', 'POST'])
@login_required
@check_session_timeout
def create_progress_note(patient_id):
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
   
    
    
    if request.method == 'POST':
        
        progress_note = ProgressNote(
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

            patient_id=patient_id,
            date_of_exam=datetime.strptime(request.form.get('date_of_exam'), '%Y-%m-%d').date(),
            return_to_work=datetime.strptime(request.form.get('work_status_date'), '%Y-%m-%d').date(),
            subjective_complaints=request.form.get('subjective_complaints'),
            objective_findings=request.form.get('objective_findings'),
            diagnoses=request.form.get('diagnoses'), 
            treatment_plan=request.form.get('treatment_plan'),
            #work status
            work_status=request.form.get('work_status'),
            work_restrictions=request.form.get('work_restrictions'),
            #provider info
            provider_signature=current_user.first_name + " " + current_user.last_name,
            license_number=current_user.medical_license,
            executed_at=request.form.get('executed_at'),
            provider_specialty=current_user.specialty,
            provider_phone=current_user.phone,
            
            
        )
        
        try:
            db.session.add(progress_note)
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
                            progress_note_id=progress_note.id,
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
                    progress_note_id=progress_note.id,
                    patient_id=patient_id,
                    is_new_request=bool(request.form.get('is_new_request', True)),
                    is_resubmission=bool(request.form.get('is_resubmission')),
                    is_expedited=bool(request.form.get('is_expedited')),
                    is_oral_confirmation=bool(request.form.get('is_oral_confirmation')),
                    auth_date=progress_note.date_of_exam,
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
                
                flash('Progress note created with authorization request!', 'success')
                return redirect(url_for('progress_note_bp.view_rfa', rfa_id=rfa.id))

            flash('Progress note created successfully!', 'success')
            return redirect(url_for('pr2.progress_notes', patient_id=patient_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating progress note: {str(e)}', 'error')
            return redirect(request.url)
    
    # Return template with all necessary variables
    return render_template('create_progress_note.html', 
                          patient=patient,
                          patient_diagnoses=diagnoses_details,
                          icd10_codes=icd10_codes,
                          cpt_codes=cpt_codes,
                          cpt_search_term=cpt_search_term)

@progress_note_bp.route('/rfa/<int:rfa_id>')
@login_required
@check_session_timeout
def view_rfa(rfa_id):
    rfa = RequestForAuthorization.query.get_or_404(rfa_id)
    patient = Patient.query.get(rfa.patient_id)
    progress_note = ProgressNote.query.get(rfa.progress_note_id)
    
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to view this RFA.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    return render_template('view_rfa.html', rfa=rfa, patient=patient, progress_note=progress_note)

@progress_note_bp.route('/patient/<int:patient_id>/rfas')
@login_required
@check_session_timeout
def patient_rfas(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to view this patient.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    rfas = RequestForAuthorization.query.filter_by(patient_id=patient_id).order_by(RequestForAuthorization.created_at.desc()).all()
    
    return render_template('patient_rfas.html', patient=patient, rfas=rfas)

@progress_note_bp.route('/rfa/print/<int:rfa_id>')
@login_required
@check_session_timeout
def print_rfa(rfa_id):
    rfa = RequestForAuthorization.query.get_or_404(rfa_id)
    patient = Patient.query.get(rfa.patient_id)
    progress_note = ProgressNote.query.get(rfa.progress_note_id)
    
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to print this RFA.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    return render_template('print_rfa.html', rfa=rfa, patient=patient, progress_note=progress_note)




@progress_note_bp.route('/progress_note/<int:note_id>')
@login_required
@check_session_timeout
def view_progress_note(note_id):
    progress_note = ProgressNote.query.get_or_404(note_id)
    patient = Patient.query.get(progress_note.patient_id)
    
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to view this progress note.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    # Get CPT codes associated with this progress note
    cpt_relations = ProgressNoteCPT.query.filter_by(progress_note_id=note_id).all()
    cpt_codes = []
    for rel in cpt_relations:
        cpt = CPTCode.query.get(rel.cpt_id)
        if cpt:
            cpt_codes.append(cpt)
    
    # Get RFA if one exists for this progress note
    rfa = RequestForAuthorization.query.filter_by(progress_note_id=note_id).first()
    rfa_items = []
    if rfa:
        rfa_items = RFAItem.query.filter_by(rfa_id=rfa.id).all()
    
    return render_template('view_progress_note.html', 
                          progress_note=progress_note, 
                          patient=patient,
                          cpt_codes=cpt_codes,
                          rfa=rfa,
                          rfa_items=rfa_items)



# @progress_note_bp.route('/edit_progress_note/<int:note_id>', methods=['GET', 'POST'])
# @login_required
# @check_session_timeout
# def edit_progress_note(note_id):
#     progress_note = ProgressNote.query.get_or_404(note_id)
#     patient = Patient.query.get(progress_note.patient_id)
#     icd10_codes = ICD10Code.query.order_by(ICD10Code.description).all()

#     # Verify this patient belongs to the current provider
#     if (patient.provider_first_name != current_user.first_name or 
#         patient.provider_last_name != current_user.last_name):
#         flash('You do not have permission to edit this patient.', 'error')
#         return redirect(url_for('dashboard.my_patients'))
    
#     # Get patient's existing diagnoses
#     patient_diagnoses = PatientDiagnosis.query.filter_by(patient_id=patient.id).all()
#     diagnoses_details = []
#     for diag in patient_diagnoses:
#         icd10_code = ICD10Code.query.get(diag.icd10_id)
#         if icd10_code:
#             diagnoses_details.append(icd10_code)
    
#     if request.method == 'POST':
#         try:
#             # Update progress note fields
#             progress_note.subjective_complaints = request.form.get('subjective_complaints')
#             progress_note.objective_findings = request.form.get('objective_findings')
#             progress_note.treatment_plan = request.form.get('treatment_plan')
#             progress_note.work_status = request.form.get('work_status')
#             progress_note.work_restrictions = request.form.get('work_restrictions')

#             # Update checkboxes
#             progress_note.is_periodic_report = bool(request.form.get('is_periodic_report'))
#             progress_note.is_change_in_treatment = bool(request.form.get('is_change_in_treatment'))
#             progress_note.is_release_from_care = bool(request.form.get('is_release_from_care'))
#             progress_note.is_change_in_work_status = bool(request.form.get('is_change_in_work_status'))
#             progress_note.is_need_for_referral = bool(request.form.get('is_need_for_referral'))
#             progress_note.is_response_to_request = bool(request.form.get('is_response_to_request'))
#             progress_note.is_change_in_condition = bool(request.form.get('is_change_in_condition'))
#             progress_note.is_need_for_surgery = bool(request.form.get('is_need_for_surgery'))
#             progress_note.is_request_for_authorization = bool(request.form.get('is_request_for_authorization'))

#             # Update dates
#             exam_date = request.form.get('date_of_exam')
#             if exam_date:
#                 progress_note.date_of_exam = datetime.strptime(exam_date, '%Y-%m-%d')

#             rtw_date = request.form.get('work_status_date')
#             print("Work status:", progress_note.work_status)
#             print("Work status date:", rtw_date)
#             if rtw_date:
#                 if progress_note.work_status == 'full_duty':
#                     progress_note.full_duty_date = datetime.strptime(rtw_date, '%Y-%m-%d')
#                 elif progress_note.work_status == 'modified':
#                     progress_note.modified_work_date = datetime.strptime(rtw_date, '%Y-%m-%d')
#                 elif progress_note.work_status == 'off_work':
#                     progress_note.off_work_until = datetime.strptime(rtw_date, '%Y-%m-%d')

#             # Handle diagnoses
#             selected_diagnoses = request.form.getlist('diagnoses')
#             if selected_diagnoses:
#                 PatientDiagnosis.query.filter_by(patient_id=patient.id).delete()
#                 for diagnosis_id in selected_diagnoses:
#                     if diagnosis_id:
#                         new_diagnosis = PatientDiagnosis(
#                             patient_id=patient.id,
#                             icd10_id=int(diagnosis_id)
#                         )
#                         db.session.add(new_diagnosis)
            
#             db.session.commit()
#             flash('Progress note updated successfully!', 'success')
#             return redirect(url_for('pr2.view_progress_note', note_id=note_id))

#         except Exception as e:
#             db.session.rollback()
#             print(f"Error: {str(e)}")
#             flash('Error updating progress note.', 'error')
#             return redirect(url_for('pr2.view_progress_note', note_id=note_id))
    
#     return render_template('edit_progress_note.html', 
#                          progress_note=progress_note, 
#                          patient=patient,
#                          patient_diagnoses=diagnoses_details,
#                          icd10_codes=icd10_codes)
            
    
    














@progress_note_bp.route('/delete_progress_note/<int:note_id>', methods=['POST'])
@login_required
@check_session_timeout
def delete_progress_note(note_id):
    progress_note = ProgressNote.query.get_or_404(note_id)
    patient = Patient.query.get(progress_note.patient_id)
    
    
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to delete this progress note.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    try:
        db.session.delete(progress_note)
        db.session.commit()
        flash('Progress note deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting progress note.', 'error')
    
    return redirect(url_for('pr2.progress_notes', patient_id=patient.id))