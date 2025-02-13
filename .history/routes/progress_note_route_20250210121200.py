from flask import Blueprint, render_template, request, redirect, url_for, flash, session  
from flask_login import login_required, current_user, logout_user
from extensions import provider_info_db as db
from models.wc_patient_models import Patient
from models.provider_info_models import Provider
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
    
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to edit this progress note.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    if request.method == 'POST':
        # Update fields similar to create_progress_note
        try:
            # Update progress note fields
            progress_note.subjective_complaints = request.form.get('subjective_complaints')
            # ... update other fields ...
            
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