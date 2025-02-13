from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file, abort
from flask_login import login_required, current_user, logout_user
from extensions import provider_info_db as db
from models.provider_info_models import Provider
from models.wc_patient_models import Patient, BodyPart, Employer, ClaimsAdmin, Lawyer, PatientDiagnosis
from models.patient_medical_hx_models import Allergy, PastMedicalHistory, MedicalCondition, Surgery, Medication
from models.icd10_models import ICD10Code
from forms.wc_patient_portal_form import wc_PatientRegistrationForm
from datetime import datetime
import os
import io
from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename
from security import check_session_timeout



dashboard_bp = Blueprint('dashboard', __name__)




@dashboard_bp.route('/')
@login_required
@check_session_timeout
def dashboard_view():
    """
    Main dashboard view
    """
    return render_template('dashboard.html', 
                         show_info=False,
                         provider=current_user,
                         show_patients=False)

@dashboard_bp.route('/my_patients')
@login_required
@check_session_timeout
def my_patients():
    """
    Display list of provider's patients
    """
    search_query = request.args.get('search', '').strip()
    
    if search_query:
        patients = Patient.query.filter(
            db.or_(
                Patient.patient_first_name.ilike(f'%{search_query}%'),
                Patient.patient_last_name.ilike(f'%{search_query}%'),
                Patient.patient_claim_number.ilike(f'%{search_query}%')
            ),
            Patient.provider_first_name == current_user.first_name,
            Patient.provider_last_name == current_user.last_name
        ).all()
    else:
        patients = Patient.query.filter_by(
            provider_first_name=current_user.first_name,
            provider_last_name=current_user.last_name
        ).all()
    
    return render_template('dashboard.html', 
                         show_info=False,
                         provider=current_user,
                         patients=patients,
                         search_query=search_query,
                         show_patients=True)

@dashboard_bp.route('/patient/<int:patient_id>')
@login_required
@check_session_timeout
def patient_detail(patient_id):
    """
    Display detailed patient information
    """
    patient = Patient.query.get_or_404(patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to view this patient.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    return render_template('patient_info.html',
                         patient=patient,
                         provider=current_user)




@dashboard_bp.route('/my_info')
@login_required
@check_session_timeout
def my_info():
    """
    Display provider's information
    """
    return render_template('dashboard.html',
                         show_info=True,
                         provider=current_user)

@dashboard_bp.route('/update_info', methods=['GET', 'POST'])
@login_required
@check_session_timeout
def update_info():
    """
    Update provider's information
    """
    if request.method == 'POST':
        try:
            current_user.first_name = request.form.get('first_name')
            current_user.last_name = request.form.get('last_name')
            current_user.medical_title = request.form.get('medical_title')
            current_user.specialty = request.form.get('specialty')
            current_user.npi = request.form.get('npi')
            current_user.medical_license = request.form.get('medical_license')
            current_user.practice_name = request.form.get('practice_name')
            current_user.address = request.form.get('address')
            current_user.city = request.form.get('city')
            current_user.state = request.form.get('state')
            current_user.zip_code = request.form.get('zip_code')
            current_user.phone = request.form.get('phone')
            current_user.fax = request.form.get('fax')
            current_user.contact_name = request.form.get('contact_name')
            current_user.biller_name = request.form.get('biller_name')
            current_user.biller_email = request.form.get('biller_email')
            
            db.session.commit()
            flash('Your information has been updated successfully!', 'success')
            return redirect(url_for('dashboard.my_info'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your information.', 'error')
            return redirect(url_for('dashboard.my_info'))
    
    return render_template('update_info.html', provider=current_user)

@dashboard_bp.route('/patient/<int:patient_id>/medical_history')
@login_required
@check_session_timeout
def patient_medical_history(patient_id):
    """
    Display patient's medical history
    """
    patient = Patient.query.get_or_404(patient_id)

    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to view this patient.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    return render_template('medical_history.html',
                         patient=patient,
                         provider=current_user)
                       

@dashboard_bp.route('/update_medical_history/<int:patient_id>', methods=['GET', 'POST'])
@login_required
@check_session_timeout
def update_medical_history(patient_id):
    """
    Update patient's medical history
    """
    patient = Patient.query.get_or_404(patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to edit this patient.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    if request.method == 'POST':
        try:
            # FIRST: Create medical history if it doesn't exist and commit right away
            if not patient.medical_history:
                medical_history = PastMedicalHistory(patient_id=patient.id)
                db.session.add(medical_history)
                db.session.commit()  # Add this commit to save the medical history first
            else:
                medical_history = patient.medical_history

            # Now we know we have a medical history, keep rest of your code the same...
            # Clear existing entries
            medical_history.allergies.clear()
            medical_history.medical_conditions.clear()
            medical_history.surgeries.clear()
            medical_history.medications.clear()

        # Rest of your code stays exactly the same...

            # Add new allergies
            for i in range(1, 16):
                allergy_name = request.form.get(f'allergy_{i}')
                severity = request.form.get(f'allergy_severity_{i}')
                reaction = request.form.get(f'allergy_reaction_{i}')
                
                if allergy_name and allergy_name.strip():
                    allergy = Allergy(
                        medical_history_id=medical_history.id,
                        allergy_name=allergy_name.strip(),
                        allergy_severity=severity.strip() if severity else None,
                        reaction=reaction.strip() if reaction else None
                    )
                    db.session.add(allergy)

            # Add new medical conditions
            for i in range(1, 11):
                condition_name = request.form.get(f'condition_{i}')
                if condition_name and condition_name.strip():
                    condition = MedicalCondition(
                        medical_history_id=medical_history.id,
                        condition_name=condition_name.strip()
                    )
                    db.session.add(condition)

            # Add new surgeries
            for i in range(1, 11):
                surgery_name = request.form.get(f'surgery_{i}')
                surgery_date = request.form.get(f'surgery_date_{i}')
                if surgery_name and surgery_name.strip():
                    surgery = Surgery(
                        medical_history_id=medical_history.id,
                        surgery_name=surgery_name.strip(),
                        surgery_date=datetime.strptime(surgery_date, '%Y-%m-%d') if surgery_date else None
                    )
                    db.session.add(surgery)

            # Add new medications
            for i in range(1, 11):
                med_name = request.form.get(f'medication_{i}')
                dosage = request.form.get(f'dosage_{i}')
                frequency = request.form.get(f'frequency_{i}')
                if med_name and med_name.strip():
                    medication = Medication(
                        medical_history_id=medical_history.id,
                        medication_name=med_name.strip(),
                        dosage=dosage.strip() if dosage else None,
                        frequency=frequency.strip() if frequency else None
                    )
                    db.session.add(medication)

            # Update smoking history
            medical_history.current_smoker = 'current_smoker' in request.form
            medical_history.former_smoker = 'former_smoker' in request.form
            medical_history.never_smoker = 'never_smoker' in request.form
            medical_history.passive_smoker = 'passive_smoker' in request.form
            medical_history.vaping = 'vaping' in request.form
            
            # Update quit date if former smoker
            quit_date = request.form.get('quit_date')
            if quit_date:
                medical_history.quit_date = datetime.strptime(quit_date, '%Y-%m-%d')

            # Update alcohol intake
            medical_history.wine_per_week = request.form.get('wine_per_week', type=int)
            medical_history.beer_per_week = request.form.get('beer_per_week', type=int)
            medical_history.liquor_per_week = request.form.get('liquor_per_week', type=int)

            # Update substance use
            medical_history.marijuana = 'marijuana' in request.form
            medical_history.cocaine = 'cocaine' in request.form
            medical_history.meth = 'meth' in request.form
            medical_history.iv_drugs = 'iv_drugs' in request.form

            db.session.commit()
            flash('Medical history has been updated successfully!', 'success')
            return redirect(url_for('dashboard.patient_medical_history', patient_id=patient_id))  # Change this line
        
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating medical history.', 'error')
            return redirect(url_for('dashboard.patient_medical_history', patient_id=patient_id))  # Change this line too
    return render_template('update_medical_hx.html', patient=patient)


@dashboard_bp.route("/create_patient", methods=["GET", "POST"])
@login_required
def create_patient():
    form = wc_PatientRegistrationForm()

     # Get ICD-10 codes ordered by description
    icd10_codes = ICD10Code.query.order_by(ICD10Code.description).all()
    
    # Pre-fill provider info
    form.provider_first_name.data = current_user.first_name
    form.provider_last_name.data = current_user.last_name
    
    if form.validate_on_submit():
        try:
            # Create new patient
            patient = Patient(
                patient_first_name=form.patient_first_name.data,
                patient_last_name=form.patient_last_name.data,
                patient_address=form.patient_address.data,
                patient_city=form.patient_city.data,
                patient_state=form.patient_state.data,
                patient_zip_code=form.patient_zip_code.data,
                patient_date_of_birth=datetime(
                    year=int(form.patient_dob_year.data),
                    month=int(form.patient_dob_month.data),
                    day=int(form.patient_dob_day.data)
                ),
                patient_date_of_injury=datetime(
                    year=int(form.doi_year.data),
                    month=int(form.doi_month.data),
                    day=int(form.doi_day.data)
                ),
                patient_claim_number=form.claim_number.data,
                provider_first_name=current_user.first_name,
                provider_last_name=current_user.last_name
            )
            db.session.add(patient)
            db.session.flush()

            # Add diagnoses from form
            selected_diagnoses = request.form.getlist('diagnoses')  # Get multiple selections
            for diagnosis_id in selected_diagnoses:
                if diagnosis_id:
                    diagnosis = PatientDiagnosis(
                        patient_id=patient.id,
                        icd10_id=int(diagnosis_id)
                    )
                    db.session.add(diagnosis)

            # Add body parts
            medical_condition = [
                form.medical_condition_1.data,
                form.edical_condition_2.data,
                form.bedical_condition_3.data,
                form._4.data,
                form.body_part_5.data,
                form.body_part_6.data
            ]
            for part in body_parts:
                if part:  # Only add if body part was entered
                    body_part = BodyPart(
                        patient_id=patient.id,
                        body_part_name=part
                    )
                    db.session.add(body_part)

            # Add employer information
            employer = Employer(
                patient_id=patient.id,
                employer_name=form.employer.data,
                employer_address=form.employer_address.data,
                employer_city=form.employer_city.data,
                employer_state=form.employer_state.data,
                employer_zip_code=form.employer_zip_code.data,
                employer_phone=form.employer_phone.data,
                employer_fax=form.employer_fax.data
            )
            db.session.add(employer)

            # Add claims administrator
            claims_admin = ClaimsAdmin(
                patient_id=patient.id,
                admin_name=form.admin_name.data,
                adjustor=form.adjustor.data,
                adjustor_address=form.adjustor_address.data,
                adjustor_city=form.adjustor_city.data,
                adjustor_state=form.adjustor_state.data,
                adjustor_zip_code=form.adjustor_zip_code.data,
                adjustor_phone=form.adjustor_phone.data,
                adjustor_fax=form.adjustor_fax.data,
                adjustor_email=form.adjustor_email.data
            )
            db.session.add(claims_admin)

            # Add lawyer if provided
            if form.lawyer_name.data:
                lawyer = Lawyer(
                    patient_id=patient.id,
                    lawyer_name=form.lawyer_name.data,
                    lawyer_address=form.lawyer_address.data,
                    lawyer_city=form.lawyer_city.data,
                    lawyer_state=form.lawyer_state.data,
                    lawyer_zip_code=form.lawyer_zip_code.data,
                    lawyer_phone=form.lawyer_phone.data,
                    lawyer_fax=form.lawyer_fax.data,
                    lawyer_email=form.lawyer_email.data
                )
                db.session.add(lawyer)

            

            db.session.commit()
            flash(f'Patient {form.patient_first_name.data} {form.patient_last_name.data} has been created successfully!', 'success')
            return redirect(url_for('dashboard.my_patients'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating patient. Please try again. Error: {str(e)}', 'danger')
            
    return render_template('create_patient.html', form=form, icd10_codes=icd10_codes)


@dashboard_bp.route('/update_patient/<int:patient_id>', methods=['GET', 'POST'])
@login_required
@check_session_timeout
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    # Verify this patient belongs to the current provider
    if (patient.provider_first_name != current_user.first_name or 
        patient.provider_last_name != current_user.last_name):
        flash('You do not have permission to edit this patient.', 'error')
        return redirect(url_for('dashboard.my_patients'))
    
    # Get patient's existing diagnoses
    patient_diagnoses = PatientDiagnosis.query.filter_by(patient_id=patient.id).all()
    diagnoses_details = []
    for diag in patient_diagnoses:
        icd10_code = ICD10Code.query.get(diag.icd10_id)
        if icd10_code:
            diagnoses_details.append(icd10_code)

    # Get ICD10 codes for dropdown
    search_term = request.args.get('search', '')
    if search_term:
        icd10_codes = ICD10Code.query.filter(
            (ICD10Code.code.ilike(f'%{search_term}%')) |
            (ICD10Code.description.ilike(f'%{search_term}%'))
        ).limit(10).all()
    else:
        icd10_codes = ICD10Code.query.order_by(ICD10Code.code).limit(50).all()

    
    if request.method == 'POST':
        try:
            # Update patient info
            patient.patient_first_name = request.form.get('patient_first_name')
            patient.patient_last_name = request.form.get('patient_last_name')
            patient.patient_address = request.form.get('patient_address')
            patient.patient_city = request.form.get('patient_city')
            patient.patient_state = request.form.get('patient_state')
            patient.patient_zip_code = request.form.get('patient_zip_code')
            patient.patient_claim_number = request.form.get('patient_claim_number')
            
            # Update DOB if provided
            dob_year = request.form.get('dob_year')
            dob_month = request.form.get('dob_month')
            dob_day = request.form.get('dob_day')
            if all([dob_year, dob_month, dob_day]):
                patient.patient_date_of_birth = datetime(
                    year=int(dob_year),
                    month=int(dob_month),
                    day=int(dob_day)
                )
            
            # Update DOI if provided
            doi_year = request.form.get('doi_year')
            doi_month = request.form.get('doi_month')
            doi_day = request.form.get('doi_day')
            if all([doi_year, doi_month, doi_day]):
                patient.patient_date_of_injury = datetime(
                    year=int(doi_year),
                    month=int(doi_month),
                    day=int(doi_day)
                )

            # Update body parts
            # First, remove existing body parts
            for body_part in patient.body_parts:
                db.session.delete(body_part)

            # First, remove existing diagnoses
            for diagnosis in patient.diagnoses:
                db.session.delete(diagnosis)

            # Add new diagnoses from form
            selected_diagnoses = request.form.getlist('diagnoses')  # Get multiple selections
            for diagnosis_id in selected_diagnoses:
                if diagnosis_id:
                    new_diagnosis = PatientDiagnosis(
                        patient_id=patient.id,
                        icd10_id=int(diagnosis_id)
                    )
                    db.session.add(new_diagnosis)
            
            # Add new body parts
            for i in range(1, 7):
                body_part_name = request.form.get(f'body_part_{i}')
                if body_part_name and body_part_name.strip():
                    new_body_part = BodyPart(
                        patient_id=patient.id,
                        body_part_name=body_part_name.strip()
                    )
                    db.session.add(new_body_part)

            # Update employer info
            if patient.employer:
                patient.employer.employer_name = request.form.get('employer')
                patient.employer.employer_address = request.form.get('employer_address')
                patient.employer.employer_city = request.form.get('employer_city')
                patient.employer.employer_state = request.form.get('employer_state')
                patient.employer.employer_zip_code = request.form.get('employer_zip_code')
                patient.employer.employer_phone = request.form.get('employer_phone')
                patient.employer.employer_fax = request.form.get('employer_fax')

            # Update claims admin info
            if patient.claims_admin:
                patient.claims_admin.admin_name = request.form.get('admin_name')
                patient.claims_admin.adjustor = request.form.get('adjustor')
                patient.claims_admin.adjustor_address = request.form.get('adjustor_address')
                patient.claims_admin.adjustor_city = request.form.get('adjustor_city')
                patient.claims_admin.adjustor_state = request.form.get('adjustor_state')
                patient.claims_admin.adjustor_zip_code = request.form.get('adjustor_zip_code')
                patient.claims_admin.adjustor_phone = request.form.get('adjustor_phone')
                patient.claims_admin.adjustor_fax = request.form.get('adjustor_fax')
                patient.claims_admin.adjustor_email = request.form.get('adjustor_email')

            
            # Update lawyer info
            if request.form.get('lawyer_name'):
                if patient.lawyer:
                    patient.lawyer.lawyer_name = request.form.get('lawyer_name')
                    patient.lawyer.lawyer_address = request.form.get('lawyer_address')
                    patient.lawyer.lawyer_city = request.form.get('lawyer_city')
                    patient.lawyer.lawyer_state = request.form.get('lawyer_state')
                    patient.lawyer.lawyer_zip_code = request.form.get('lawyer_zip_code')
                    patient.lawyer.lawyer_phone = request.form.get('lawyer_phone')
                    patient.lawyer.lawyer_fax = request.form.get('lawyer_fax')
                    patient.lawyer.lawyer_email = request.form.get('lawyer_email')
                else:
                    new_lawyer = Lawyer(
                        patient_id=patient.id,
                        lawyer_name=request.form.get('lawyer_name'),
                        lawyer_address=request.form.get('lawyer_address'),
                        lawyer_city=request.form.get('lawyer_city'),
                        lawyer_state=request.form.get('lawyer_state'),
                        lawyer_zip_code=request.form.get('lawyer_zip_code'),
                        lawyer_phone=request.form.get('lawyer_phone'),
                        lawyer_fax=request.form.get('lawyer_fax'),
                        lawyer_email=request.form.get('lawyer_email')
                    )
                    db.session.add(new_lawyer)
            elif patient.lawyer:  # Add just this section
                db.session.delete(patient.lawyer)

            db.session.commit()
            flash('Patient information has been updated successfully!', 'success')
            return redirect(url_for('dashboard.patient_detail', patient_id=patient_id))
        
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating patient information.', 'error')
            return redirect(url_for('dashboard.patient_detail', patient_id=patient_id))
    
    return render_template('update_patient.html', patient=patient, icd10_codes=ICD10Code.query.order_by(ICD10Code.description).all())

   


@dashboard_bp.route('/logout')
@login_required
def logout():
    """
    Logout route
    """
    session.clear()
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login_register.login'))

# Future routes to implement based on sidebar:
# @dashboard_bp.route('/office_schedule')
# @dashboard_bp.route('/or_schedule')
# @dashboard_bp.route('/billing')
# @dashboard_bp.route('/cpt')
# @dashboard_bp.route('/icd10')