from flask import Blueprint, render_template, request, redirect, url_for, flash, session  
from flask_login import login_required, current_user
from extensions import provider_info_db as db
from models.wc_patient_models import Patient
from models.provider_info_models import Provider
from models.imaging_model import OperativeReport
from datetime import datetime
import os
import io
from werkzeug.utils import secure_filename
from security import check_session_timeout
from flask import send_file

operative_bp = Blueprint('operative', __name__)

"""
Reference
class OperativeReport(db.Model):
    __tablename__ = 'operative_reports'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    file_name = db.Column(db.String(100))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200))
    file_data = db.Column(db.LargeBinary)  # Store the actual PDF data
    file_type = db.Column(db.String(50))   # Store the file type (e.g., 'application/pdf')
"""





# Start of Operative Reports
@operative_bp.route('/patient/<int:patient_id>/operative_reports')
@login_required
@check_session_timeout
def patient_operative_reports(patient_id):
   
    #display patient's operative results
    patient = Patient.query.get_or_404(patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to download this operative report.', 'error')
        return redirect(url_for('dashboard.my_patients'))

    return render_template('operative_reports.html', patient=patient)



@operative_bp.route('/upload_operative_report/<int:patient_id>', methods=['GET', 'POST'])
@login_required
@check_session_timeout
def upload_operative_report(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to upload imaging for this patient.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    if request.method == 'POST':
        # Check if any file was uploaded
        if 'operative_reports' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['operative_reports']
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
            operative_reports = OperativeReport(
                patient_id=patient_id,
                file_name=filename,
                description=request.form.get('description'),
                file_data=file_data,
                file_type=file.content_type
            )
            
            db.session.add(operative_reports)
            db.session.commit()
            
            flash('Operative Report uploaded successfully!', 'success')
            return redirect(url_for('dashboard.patient_operative_reports', patient_id=patient_id))
    
    return render_template('upload_operative.html', patient=patient)

@operative_bp.route('/view_operative_reports/<int:operative_id>')
@login_required
@check_session_timeout
def view_operative_reports(operative_id):

    #display a specific operative result
    operative_report = OperativeReport.query.get_or_404(operative_id) 
    patient = Patient.query.get(operative_report.patient_id)

    #verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to view this imaging.', 'error')
        return redirect(url_for('dashboard.my_patients'))

    return send_file(
        io.BytesIO(operative_report.file_data),
        mimetype=operative_report.file_type,
        as_attachment=False,
        download_name=operative_report.file_name
    )



@operative_bp.route('/download_operative_reports/<int:operative_id>')
@login_required
@check_session_timeout
def download_operative_report(operative_id):
    
    #download a specific operative report result
    operative_report = OperativeReport.query.get_or_404(operative_id)
    patient = Patient.query.get(operative_report.patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to download this imaging.', 'error')
        return redirect(url_for('dashboard.my_patients'))

    # Send file as attachment for download
    return send_file(
        io.BytesIO(operative_report.file_data),
        mimetype=operative_report.file_type,
        as_attachment=True,
        download_name=operative_report.file_name
    )

@operative_bp.route('/delete_operative_report/<int:report_id>', methods=['POST'])
@login_required
@check_session_timeout
def delete_operative_report(report_id):
    # Get the report
    report = OperativeReport.query.get_or_404(report_id)
    
    # Get the patient to check permissions
    patient = Patient.query.get(report.patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to delete this report.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    try:
        db.session.delete(report)
        db.session.commit()
        flash('Operative report deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting report.', 'error')
    
    return redirect(url_for('dashboard.patient_operative_reports', patient_id=patient.id))

# End of Operative Reports
