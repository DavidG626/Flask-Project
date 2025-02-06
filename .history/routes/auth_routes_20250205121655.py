from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file  
from flask_login import login_required, current_user, logout_user
from extensions import provider_info_db as db
from models.wc_patient_models import Patient
from models.provider_info_models import Provider
from models.operative_model import Auth
from forms.wc_patient_portal_form import wc_PatientRegistrationForm
from datetime import datetime
import os
import io
from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename
from security import check_session_timeout
from flask import 

auth_bp = Blueprint('auths', __name__)

"""
Reference
class Auth(db.Model):
    __tablename__ = 'authorization'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    file_name = db.Column(db.String(100))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200))
    file_data = db.Column(db.LargeBinary)  # Store the actual PDF data
    file_type = db.Column(db.String(50))
"""

# Start of Auths
@auth_bp.route('/patient/<int:patient_id>/authorizations')
@login_required
@check_session_timeout
def patient_authorizations(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to view this patient\'s authorizations.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    return render_template('auths.html', patient=patient)



@auth_bp.route('/upload_auth/<int:patient_id>', methods=['GET', 'POST'])  # Changed from auth_id
@login_required
@check_session_timeout
def upload_auth(patient_id):  # Changed from auth_id
    patient = Patient.query.get_or_404(patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to upload authorization for this patient.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    if request.method == 'POST':
        # Check if any file was uploaded
        if 'authorization' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['authorization']
        
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
            
            # Create auth result record with file data
            auth_results = Auth(
                patient_id=patient_id,
                file_name=filename,
                description=request.form.get('description'),
                file_data=file_data,
                file_type=file.content_type
)
            
            db.session.add(auth_results)
            db.session.commit()
            
            flash('Authorization uploaded successfully!', 'success')
            return redirect(url_for('dashboard.patient_authorizations', patient_id=patient_id))    
    return render_template('upload_auth.html', patient=patient)  



@auth_bp.route('/download_auth/<int:auth_id>')
@login_required
@check_session_timeout
def download_auth(auth_id):
   
    #download a specific imaging results
    authorization = Auth.query.get_or_404(auth_id)
    patient = Patient.query.get(authorization.patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to download this Authorization.', 'error')
        return redirect(url_for('dashboard.my_patients'))

    # Send file as attachment for download
    return send_file(
        io.BytesIO(authorization.file_data), 
        mimetype=authorization.file_type,
        as_attachment=True,
        download_name=authorization.file_name
)
@auth_bp.route('/view_auth/<int:auth_id>')
@login_required
@check_session_timeout
def view_auth(auth_id):
    auth = Auth.query.get_or_404(auth_id)
    
    patient = Patient.query.get(auth.patient_id)
    
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to view this authorization.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    return send_file(
        io.BytesIO(auth.file_data),
        mimetype=auth.file_type,
        as_attachment=False,
        download_name=auth.file_name
    )

@auth_bp.route('/delete_auth/<int:auth_id>', methods=['POST'])
@login_required
@check_session_timeout
def delete_auth(auth_id):
    # Get the auth result
    authorization = Auth.query.get_or_404(auth_id)
    
    # Get the patient to check permissions
    patient = Patient.query.get(authorization.patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to delete this Authorization.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    try:
        db.session.delete(authorization)
        db.session.commit()
        flash('Authorization deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting authorization result.', 'error')
    
    return redirect(url_for('dashboard.patient_authorizations', patient_id=patient.id))

