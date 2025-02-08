from flask import Blueprint, render_template, request, redirect, url_for, flash, session  
from flask_login import login_required, current_user, logout_user
from extensions import provider_info_db as db
from models.wc_patient_models import Patient
from models.provider_info_models import Provider
from models.
from datetime import datetime
import os
import io
from werkzeug.utils import secure_filename
from security import check_session_timeout
from flask import send_file

progress_note_bp = Blueprint('pr2', __name__)

# Start Progress Note
@progress_note_bp.route('/patient/<int:patient_id>/progress_note')
@login_required
@check_session_timeout
def progress_note(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to view this patient\'s progress note.', 'error')
        return redirect(url_for('progress_note.my_patients'))
    
    return render_template('progress_note.html', patient=patient)