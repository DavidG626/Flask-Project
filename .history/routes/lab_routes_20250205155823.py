from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file  
from flask_login import login_required, current_user
from extensions import provider_info_db as db
from models.wc_patient_models import Patient
from models.provider_info_models import Provider
from models.lab_model import LabResult
from security import check_session_timeout
from werkzeug.utils import secure_filename
import io


labs_bp = Blueprint('lab', __name__)


# Start of Lab Results
@labs_bp.route('/patient/<int:patient_id>/labs')
@login_required
@check_session_timeout
def patient_labs(patient_id):
    
    #display patient's lab results
    patient = Patient.query.get_or_404(patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to view this patient.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    return render_template('labs.html', patient=patient)



@labs_bp.route('/upload_lab/<int:patient_id>', methods=['GET', 'POST'])
@login_required
@check_session_timeout
def upload_lab(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to upload labs for this patient.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    if request.method == 'POST':
        # Check if any file was uploaded
        if 'lab_file' not in request.files:
            flash('No file provided', 'error')
            return redirect(request.url)
            
        file = request.files['lab_file']
        
        if file.filename == '':
            flash('No selected file', 'error')
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
            lab_results = LabResult(
                patient_id=patient_id,
                file_name=filename,
                description=request.form.get('description'),
                file_data=file_data,
                file_type=file.content_type
)
            
            db.session.add(lab_results)
            db.session.commit()
            
            flash('Lab result uploaded successfully', 'success')
            return redirect(url_for('dashboard.patient_labs', patient_id=patient_id))
            
    return render_template('upload_lab.html', patient=patient)


@labs_bp.route('/view_lab/<int:lab_id>')
@login_required
@check_session_timeout
def view_lab(lab_id):
   
    #display a specific lab result
    lab_result = LabResult.query.get_or_404(lab_id)
    patient = Patient.query.get(lab_result.patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to view this lab.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    return send_file(
        io.BytesIO(lab_result.file_data),
        mimetype=lab_result.file_type,
        as_attachment=False,
        download_name=lab_result.file_name
    )

    

@labs_bp.route('/download_lab/<int:lab_id>')
@login_required
@check_session_timeout
def download_lab(lab_id):
   
    #download a specific lab result
    lab_result = LabResult.query.get_or_404(lab_id)
    patient = Patient.query.get(lab_result.patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to download this lab.', 'error')
        return redirect(url_for('dashboard.my_patients'))

    # Send file as attachment for download
    return send_file(
        io.BytesIO(lab_result.file_data),  # Correct - using stored file data
        mimetype=lab_result.file_type,
        as_attachment=True,
        download_name=lab_result.file_name

)
@labs_bp.route('/delete_lab/<int:lab_id>', methods=['POST'])
@login_required
@check_session_timeout
def delete_lab(lab_id):
    # Get the lab result
    lab = LabResult.query.get_or_404(lab_id)
    
    # Get the patient to check permissions
    patient = Patient.query.get(lab.patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to delete this lab result.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    try:
        db.session.delete(lab)
        db.session.commit()
        flash('Lab result deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting lab result.', 'error')
    
    return redirect(url_for('dashboard.patient_labs', patient_id=patient.id))
