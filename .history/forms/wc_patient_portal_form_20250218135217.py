from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class wc_PatientRegistrationForm(FlaskForm):
    provider_first_name = StringField('Provider First Name', validators=[DataRequired()])
    provider_last_name = StringField('Provider Last Name', validators=[DataRequired()])
    patient_first_name = StringField('Patient First Name', validators=[DataRequired()])
    patient_last_name = StringField('Patient Last Name', validators=[DataRequired()])
    patient_occupation
    patient_address = StringField('Address', validators=[DataRequired()])
    patient_city = StringField('City', validators=[DataRequired()])
    patient_state = StringField('State', validators=[DataRequired()])
    patient_zip_code = StringField('ZIP Code', validators=[DataRequired()])
    
    # DOB fields
    patient_dob_month = StringField('Month', validators=[DataRequired()])
    patient_dob_day = StringField('Day', validators=[DataRequired()])
    patient_dob_year = StringField('Year', validators=[DataRequired()])
    
    # DOI fields
    doi_month = StringField('Month', validators=[DataRequired()])
    doi_day = StringField('Day', validators=[DataRequired()])
    doi_year = StringField('Year', validators=[DataRequired()])
    
    # Medical Condition fields
    medical_condition_1 = StringField('Medical Condition 1')
    medical_condition_2 = StringField('Medical Condition 2')
    medical_condition_3 = StringField('Medical Condition 3')
    medical_condition_4 = StringField('Medical Condition 4')
    medical_condition_5 = StringField('Medical Condition 5')
    medical_condition_6 = StringField('Medical Condition 6')
    
    claim_number = StringField('Claim Number', validators=[DataRequired()])
    
    # Employer fields
    employer = StringField('Employer Name', validators=[DataRequired()])
    employer_address = StringField('Employer Address', validators=[DataRequired()])
    employer_city = StringField('Employer City', validators=[DataRequired()])
    employer_state = StringField('Employer State', validators=[DataRequired()])
    employer_zip_code = StringField('Employer ZIP Code', validators=[DataRequired()])
    employer_phone = StringField('Employer Phone', validators=[DataRequired()])
    employer_fax = StringField('Employer Fax')
    
    # Claims Admin fields
    admin_name = StringField('Administrator Name', validators=[DataRequired()])
    adjustor = StringField('Adjustor Name', validators=[DataRequired()])
    adjustor_address = StringField('Adjustor Address', validators=[DataRequired()])
    adjustor_city = StringField('Adjustor City', validators=[DataRequired()])
    adjustor_state = StringField('Adjustor State', validators=[DataRequired()])
    adjustor_zip_code = StringField('Adjustor ZIP Code', validators=[DataRequired()])
    adjustor_phone = StringField('Adjustor Phone', validators=[DataRequired()])
    adjustor_fax = StringField('Adjustor Fax')
    adjustor_email = StringField('Adjustor Email')
    
    # Lawyer fields
    lawyer_name = StringField('Lawyer Name')
    lawyer_address = StringField('Lawyer Address')
    lawyer_city = StringField('Lawyer City')
    lawyer_state = StringField('Lawyer State')
    lawyer_zip_code = StringField('Lawyer ZIP Code')
    lawyer_phone = StringField('Lawyer Phone')
    lawyer_fax = StringField('Lawyer Fax')
    lawyer_email = StringField('Lawyer Email')
    
    submit = SubmitField('Register Patient')