from flask import Blueprint, render_template, request, redirect, url_for, flash, session  
from flask_login import login_required, current_user, logout_user
from extensions import provider_info_db as db
from models.wc_patient_models import Patient
from models.misc_model import Misc
from forms.wc_patient_portal_form import wc_PatientRegistrationForm
from datetime import datetime
import os
import io
from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename
from security import check_session_timeout
from flask import send_file


"""
Reference
class Misc(db.Model):
    __tablename__ = 'misc'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    file_name = db.Column(db.String(100))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200))
    file_data = db.Column(db.LargeBinary)
    file_type = db.Column(db.String(50))
"""

# Start Misc
@misc_bp.route('/patient/<int:patient_id>/misc')
@login_required
@check_session_timeout
def patient_misc(patient_id):  # Changed to match template url_for
    patient = Patient.query.get_or_404(patient_id)
    
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to view this patient.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    return render_template('misc.html', patient=patient)


@misc_bp.route('/upload_misc/<int:patient_id>', methods=['GET', 'POST'])
@login_required
@check_session_timeout
def upload_misc(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to upload misc for this patient.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    if request.method == 'POST':
        # Check if any file was uploaded
        if 'misc_file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['misc_file']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        # If no file was selected
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file:
            # Read the file data
            file_data = file.read()
            filename = secure_filename(file.filename)
            
            # Create imaging result record with file data
            misc_results = Misc(
                patient_id=patient_id,
                file_name=filename,
                description=request.form.get('description'),
                file_data=file_data,
                file_type=file.content_type
            )
            
            db.session.add(misc_results)
            db.session.commit()
            
            flash('Misc uploaded successfully!', 'success')
            return redirect(url_for('dashboard.patient_misc', patient_id=patient_id))
    
    return render_template('upload_misc.html', patient=patient)

@misc_bp.route('/view_misc/<int:misc_id>')
@login_required
@check_session_timeout
def view_misc(misc_id):
    misc = Misc.query.get_or_404(misc_id)
    
    patient = Patient.query.get(misc.patient_id)
    
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to view this misc.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    return send_file(
        io.BytesIO(misc.file_data),
        mimetype=misc.file_type,
        as_attachment=False,
        download_name=misc.file_name
    )

@misc_bp.route('/download_misc/<int:misc_id>')
@login_required
@check_session_timeout
def download_misc(misc_id):
    misc = Misc.query.get_or_404(misc_id)
    patient = Patient.query.get(misc.patient_id)
    
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to download this misc.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    return send_file(
        io.BytesIO(misc.file_data),
        mimetype=misc.file_type,
        as_attachment=True,
        download_name=misc.file_name
    )

@misc_bp.route('/delete_misc/<int:misc_id>', methods=['POST'])
@login_required
@check_session_timeout
def delete_misc(misc_id):
    # Get the misc result
    misc = Misc.query.get_or_404(misc_id)
    
    # Get the patient to check permissions
    patient = Patient.query.get(misc.patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to delete this misc.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    try:
        db.session.delete(misc)
        db.session.commit()
        flash('Misc deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting misc.', 'error')
    
    return redirect(url_for('dashboard.patient_misc', patient_id=patient.id))

