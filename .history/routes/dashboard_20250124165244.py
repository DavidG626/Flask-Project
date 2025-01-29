from flask import Blueprint, render_template, request, redirect, url_for, flash, session  
from flask_login import login_required, current_user, logout_user
from extensions import provider_info_db as db
from models.provider_info_models import Provider
from models.wc_patient_models import Patient, BodyPart, Employer, ClaimsAdmin, Lawyer
from models.patient_medical_hx_models import Allergy, PastMedicalHistory, MedicalCondition, Surgery, Medication
from forms.wc_patient_portal_form import wc_PatientRegistrationForm
from datetime import datetime
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
    try:
        print("\n=== Starting medical history update ===")
        patient = Patient.query.get_or_404(patient_id)
        print(f"Patient found: {patient.first_name} {patient.last_name}")
        
        # Verify this patient belongs to the current provider
        if (patient.provider_first_name != current_user.first_name or 
            patient.provider_last_name != current_user.last_name):
            flash('You do not have permission to edit this patient.', 'error')
            return redirect(url_for('dashboard.my_patients'))
        
        if request.method == 'POST':
            try:
                print("\nForm Data:", dict(request.form))
                
                # Create new medical history if it doesn't exist
                if not patient.medical_history:
                    print("Creating new medical history")
                    medical_history = PastMedicalHistory(patient_id=patient.id)
                    db.session.add(medical_history)
                    db.session.flush()
                else:
                    print("Using existing medical history")
                    medical_history = patient.medical_history

                # Clear existing entries
                print("Clearing existing entries")
                medical_history.allergies.clear()
                medical_history.medical_conditions.clear()
                medical_history.surgeries.clear()
                medical_history.medications.clear()

                # Add new allergies
                for i in range(1, 1):
                    allergy_name = request.form.get(f'allergy_{i}')
                    severity = request.form.get(f'allergy_severity_{i}')
                    reaction = request.form.get(f'allergy_reaction_{i}')
                    
                    if allergy_name and allergy_name.strip():
                        print(f"Adding allergy: {allergy_name}")
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

                print("Committing changes to database")
                db.session.commit()
                print("Changes committed successfully")

                flash('Medical history has been updated successfully!', 'success')
                return redirect(url_for('dashboard.patient_detail', patient_id=patient_id))
                
            except Exception as e:
                db.session.rollback()
                print(f"Error occurred: {str(e)}")
                flash('An error occurred while updating medical history.', 'error')
                return redirect(url_for('dashboard.patient_detail', patient_id=patient_id))
        
        return render_template('update_medical_hx.html', patient=patient)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        flash('An unexpected error occurred.', 'error')
        return redirect(url_for('dashboard.my_patients'))


@dashboard_bp.route("/create_patient", methods=["GET", "POST"])
@login_required
def create_patient():
    form = wc_PatientRegistrationForm()
    
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

            # Add body parts
            body_parts = [
                form.body_part_1.data,
                form.body_part_2.data,
                form.body_part_3.data,
                form.body_part_4.data,
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
            
    return render_template('create_patient.html', form=form)


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