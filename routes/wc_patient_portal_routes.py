from flask import Blueprint, render_template, url_for, flash, redirect, session
from forms.wc_patient_portal_form import wc_PatientRegistrationForm
from extensions import provider_info_db as db
from models.wc_patient_models import Patient, BodyPart, Employer, ClaimsAdmin, Lawyer
from datetime import datetime
from flask_login import login_required, current_user, logout_user


# Create the login_register blueprint
wc_patient_portal_bp = Blueprint('wc_patient_portal', __name__)

# Define routes patient portal
@wc_patient_portal_bp.route("/wc_patient_portal_register", methods=["GET", "POST"])
def register():
    form = wc_PatientRegistrationForm()
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
                provider_first_name=form.provider_first_name.data,
                provider_last_name=form.provider_last_name.data
            )
            db.session.add(patient)
            db.session.flush()  # Get patient ID before adding related records

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
            if form.lawyer_name.data:  # Only create lawyer record if name was provided
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
            flash(f'Account created for {form.patient_first_name.data} {form.patient_last_name.data}!', 'success')
            return redirect(url_for('wc_patient_portal.register'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error creating account. Please try again. Error: {str(e)}', 'danger')
            
    return render_template('wc_patient_portal.html', title="Register", form=form)


