from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo





# Patient Registration
class wc_PatientRegistrationForm(FlaskForm):
    #provider
    provider_first_name = StringField('Provider First Name')
    provider_last_name = StringField('Provider Last Name')
    #name
    patient_first_name = StringField('First Name',
    validators=[DataRequired(), Length(min=2, max=20)])

    patient_last_name = StringField('Last Name',
    validators=[DataRequired(), Length(min=2, max=20)])

    #patient address
    patient_address = StringField('Address', 
    validators=[DataRequired()])
    
    patient_city = StringField('City', 
    validators=[DataRequired()])
    
    patient_zip_code = StringField('Zip Code', 
    validators=[DataRequired()])
    
    patient_state = StringField('State', 
    validators=[DataRequired()])
    
    #DOB
    patient_dob_month = StringField('Month',
    validators=[DataRequired(), Length(min=2, max=2)])

    patient_dob_day = StringField('Day',
    validators=[DataRequired(), Length(min=2, max=2)])

    patient_dob_year = StringField('Year',
    validators=[DataRequired(), Length(min=4, max=4)])

    #DOI
    doi_month = StringField('Month',
    validators=[DataRequired(), Length(min=2, max=2)])

    doi_day = StringField('Day',
    validators=[DataRequired(), Length(min=2, max=2)])

    doi_year = StringField('Year',
    validators=[DataRequired(), Length(min=4, max=4)])

    #body parts
    body_part_1 = StringField('Body Part 1', validators=[DataRequired()])
    body_part_2 = StringField('Body Part 2')
    body_part_3 = StringField('Body Part 3')
    body_part_4 = StringField('Body Part 4')
    body_part_5 = StringField('Body Part 5')
    body_part_6 = StringField('Body Part 6')

    #claim
    claim_number = StringField('Claim #',
    validators=[DataRequired()])

    #employer
    employer = StringField('Employer',
    validators=[DataRequired()])

    employer_address = StringField('Address', 
    validators=[DataRequired()])
    
    employer_city = StringField('City', 
    validators=[DataRequired()])
    
    employer_zip_code = StringField('Zip Code', 
    validators=[DataRequired()])
    
    employer_state = StringField('State', 
    validators=[DataRequired()])

    employer_phone = StringField('Phone', 
    validators=[DataRequired()])

    employer_fax = StringField('Fax', 
    validators=[DataRequired()])

   

    #claims admin info
    admin_name = StringField('Insurance', 
    validators=[DataRequired()])
    
    adjustor = StringField('Adustor', 
    validators=[DataRequired()])

    adjustor_address = StringField('Address', 
    validators=[DataRequired()])
    
    adjustor_city = StringField('City', 
    validators=[DataRequired()])
    
    adjustor_zip_code = StringField('Zip Code', 
    validators=[DataRequired()])
    
    adjustor_state = StringField('State', 
    validators=[DataRequired()])

    adjustor_phone = StringField('Phone', 
    validators=[DataRequired()])

    adjustor_fax = StringField('Fax', 
    validators=[DataRequired()])

    adjustor_email = StringField('Email',
    validators=[DataRequired(), Email()])
    
    #esquire info
    lawyer_name = StringField('Lawyer Name')

    lawyer_address = StringField('Address')

    lawyer_city = StringField('City') 
    
    lawyer_zip_code = StringField('Zip Code') 
 
    lawyer_state = StringField('State') 
   
    lawyer_phone = StringField('Phone') 

    lawyer_fax = StringField('Fax') 
    
    lawyer_email = StringField('Lawyer Email') 
   
    #submit button
    submit = SubmitField('Submit')




    


    
    
    

    




