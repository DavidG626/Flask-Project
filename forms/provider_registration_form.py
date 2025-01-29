from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask import Blueprint, render_template, url_for, flash, redirect, session




# Registration
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',
    validators=[DataRequired(), Length(min=2, max=20)])

    last_name = StringField('Last Name',
    validators=[DataRequired(), Length(min=2, max=20)])

    username = StringField('username',
    validators=[DataRequired(), Length(min=2, max=20)])

    password = PasswordField('Password', 
    validators=[DataRequired(), Length(min=2, max=20)])
    
    confirm_password = PasswordField('Confirm Password', 
    validators=[DataRequired(), EqualTo('password', message= "Password Must Match")])

    email = StringField('email',
    validators=[DataRequired(), Email()])

    practice_name = StringField('Practice Name', 
    validators=[DataRequired()])

    specialty = StringField('Specialty', 
    validators=[DataRequired()])

    npi = StringField('NPI #', 
    validators=[DataRequired()])

    medical_license = StringField('Medical License', 
    validators=[DataRequired()])
    
    medical_title = SelectField('Medical Title', 
    choices=[
        ('', 'Select your title'),
        ('MD', "MD"),
        ('PA', "PA"),
        ('NP', "NP"),
        ('DO', "DO"),
        ('DC', "DC"),

    ],
    validators=[DataRequired()])

    address = StringField('Address', 
    validators=[DataRequired()])
    
    city = StringField('City', 
    validators=[DataRequired()])
    
    zip_code = StringField('Zip Code', 
    validators=[DataRequired()])
    
    state = StringField('State', 
    validators=[DataRequired()])

    phone = StringField('Phone', 
    validators=[DataRequired()])

    fax = StringField('Fax', 
    validators=[DataRequired()])
    
    contact_name = StringField('Medical Assistant', 
    validators=[DataRequired()])
    
    biller_name = StringField('Biller', 
    validators=[DataRequired()])
    
    biller_email = StringField('Biller Email', 
    validators=[DataRequired()])

    submit = SubmitField('Submit')


# Login
class LoginForm(FlaskForm):
    username = StringField('username',
    validators=[DataRequired()])
    password = PasswordField('Password', 
    validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    
    submit = SubmitField('Log In')

    


    
    
    

    



