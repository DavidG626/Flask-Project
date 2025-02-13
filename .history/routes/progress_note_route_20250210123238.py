from flask import Blueprint, render_template, request, redirect, url_for, flash, session  
from flask_login import login_required, current_user, logout_user
from extensions import provider_info_db as db
from models.wc_patient_models import Patient
from models.provider_info_models import Provider
from models.icd10_models import ICD10Code
from models.wc_patient_models import PatientDiagnosis
from models.pr2_model import ProgressNote
from datetime import datetime
import os
import io
from werkzeug.utils import secure_filename
from security import check_session_timeout
from flask import send_file


progress_note_bp = Blueprint('pr2', __name__)

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
    
    return render_template('progress_notes.html', patient=patient)




# View specific progress note
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
    
    return render_template('view_progress_note.html', progress_note=progress_note, patient=patient)

# Edit progress note
@progress_note_bp.route('/edit_progress_note/<int:note_id>', methods=['GET', 'POST'])
@login_required
@check_session_timeout
def edit_progress_note(note_id):
    progress_note = ProgressNote.query.get_or_404(note_id)
    patient = Patient.query.get(progress_note.patient_id)

    # Get patient's existing diagnoses
    patient_diagnoses = PatientDiagnosis.query.filter_by(patient_id=patient.id).all()
    diagnoses_details = []
    for diag in patient_diagnoses:
        icd10_code = ICD10Code.query.get(diag.icd10_id)
        if icd10_code:
            diagnoses_details.append(icd10_code)
    
    # Get all available ICD10 codes for dropdown
    icd10_codes = ICD10Code.query.order_by(ICD10Code.description).all()
    
    
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to edit this progress note.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    if request.method == 'POST':
        # Update fields similar to create_progress_note
        try:
            # Update progress note fields
            progress_note.subjective_complaints = request.form.get('subjective_complaints')
            progress_note.objective_findings = request.form.get('objective_findings')
            progress_note.treatment_plan = request.form.get('treatment_plan')
            progress_note.work_status = request.form.get('work_status')
            progress_note.work_restrictions = request.form.get('work_restrictions')

             # Handle diagnoses updates
            new_diagnoses = request.form.getlist('new_diagnoses')
            if new_diagnoses:
                for diagnosis_id in new_diagnoses:
                    if diagnosis_id:
                        # Check if diagnosis already exists
                        existing = PatientDiagnosis.query.filter_by(
                            patient_id=patient.id,
                            icd10_id=int(diagnosis_id)
                        ).first()
                        
                        if not existing:
                            new_diagnosis = PatientDiagnosis(
                                patient_id=patient.id,
                                icd10_id=int(diagnosis_id)
                            )
                            db.session.add(new_diagnosis)
            
            
            db.session.commit()
            flash('Progress note updated successfully!', 'success')
            return redirect(url_for('pr2.view_progress_note', note_id=note_id))
        except Exception as e:
            db.session.rollback()
            flash('Error updating progress note.', 'error')
    
    return render_template('edit_progress_note.html', progress_note=progress_note, patient=patient)


@progress_note_bp.route('/delete_progress_note/<int:note_id>', methods=['POST'])
@login_required
@check_session_timeout
def delete_progress_note(note_id):
    progress_note = ProgressNote.query.get_or_404(note_id)
    patient = Patient.query.get(progress_note.patient_id)
    
    # Verify this patient belongs to the current provider
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