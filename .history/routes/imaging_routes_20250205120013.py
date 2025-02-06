from flask import Blueprint, render_template, request, redirect, url_for, flash, session  
from flask_login import login_required, current_user, logout_user
from extensions import provider_info_db as db
from models.wc_patient_models import Patient
from models.provider_info_models import Provider
from models.imaging_model import ImagingResult
from datetime import datetime
import os
import io
from werkzeug.utils import secure_filename
from security import check_session_timeout
from flask import send_file

imaging_bp = Blueprint('imaging', __name__)

""" Reference
class ImagingResult(db.Model):
    __tablename__ = 'imaging_results'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    file_name = db.Column(db.String(100))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200))
    file_data = db.Column(db.LargeBinary)  # Store the actual PDF data
    file_type = db.Column(db.String(50))   # Store the file type (e.g., 'application/pdf')
"""

# Start Imaging Results
@imaging_bp.route('/patient/<int:patient_id>/imaging')
@login_required
@check_session_timeout
def patient_imaging(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to view this patient\'s imaging.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    return render_template('imaging.html', patient=patient)


@imaging_bp.route('/upload_imaging/<int:patient_id>', methods=['GET', 'POST'])
@login_required
@check_session_timeout
def upload_imaging(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to upload imaging for this patient.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    if request.method == 'POST':
        # Check if any file was uploaded
        if 'imaging_file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['imaging_file']
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
            imaging_results = ImagingResult(
                patient_id=patient_id,
                file_name=filename,
                description=request.form.get('description'),
                file_data=file_data,
                file_type=file.content_type
            )
            
            db.session.add(imaging_results)
            db.session.commit()
            
            flash('Imaging uploaded successfully!', 'success')
            return redirect(url_for('dashboard.patient_imaging', patient_id=patient_id))
    
    return render_template('upload_imaging.html', patient=patient)


@imaging_bp.route('/view_imaging/<int:imaging_id>')
@login_required
@check_session_timeout
def view_imaging(imaging_id):

    #display a specific imaging result
    imaging_results = ImagingResult.query.get_or_404(imaging_id)
    patient = Patient.query.get(imaging_results.patient_id)

    #verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to view this imaging.', 'error')
        return redirect(url_for('dashboard.my_patients'))

    return send_file(
        io.BytesIO(imaging_results.file_data),
        mimetype=imaging_results.file_type,
        as_attachment=False,
        download_name=imaging_results.file_name
    )


@imaging_bp.route('/download_imaging/<int:imaging_id>')
@login_required
@check_session_timeout
def download_imaging(imaging_id):
   
    #download a specific imaging results
    imaging_results = ImagingResult.query.get_or_404(imaging_id)
    patient = Patient.query.get(imaging_results.patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to download this imaging.', 'error')
        return redirect(url_for('dashboard.my_patients'))

    # Send file as attachment for download
    return send_file(
        io.BytesIO(imaging_results.file_data), 
        mimetype=imaging_results.file_type,
        as_attachment=True,
        download_name=imaging_results.file_name
)
@imaging_bp.route('/delete_imaging/<int:imaging_id>', methods=['POST'])
@login_required
@check_session_timeout
def delete_imaging(imaging_id):
    # Get the imaging result
    imaging = ImagingResult.query.get_or_404(imaging_id)
    
    # Get the patient to check permissions
    patient = Patient.query.get(imaging.patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to delete this imaging.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    try:
        db.session.delete(imaging)
        db.session.commit()
        flash('Imaging deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting imaging.', 'error')
    
    return redirect(url_for('dashboard.patient_imaging', patient_id=patient.id))
