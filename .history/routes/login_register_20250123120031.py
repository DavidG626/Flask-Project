from flask import Blueprint, render_template, url_for, flash, redirect, session
from forms.provider_registration_form import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from models.provider_info_models import Provider
from routes.extensions import provider_info_db as db
from flask_login import login_user
from datetime import datetime  # Add this import

import sqlite3
import os



# Create the login_register blueprint
login_register = Blueprint('login_register', __name__)

@login_register.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Hash the password
        hashed_password = generate_password_hash(form.password.data)
        
        # Check for existing username
        existing_username = Provider.query.filter_by(username=form.username.data).first()
        if existing_username:
            flash('Username already exists. Please choose a different username.', 'danger')
            return render_template('register.html', title="Register", form=form)
        
        # Check for existing email
        existing_email = Provider.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('Email already registered. Please use a different email.', 'danger')
            return render_template('register.html', title="Register", form=form)
        
        # Create new Provider instance
        new_provider = Provider(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            medical_title=form.medical_title.data,
            specialty=form.specialty.data,
            npi=form.npi.data,
            medical_license=form.medical_license.data,
            practice_name=form.practice_name.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            zip_code=form.zip_code.data,
            phone=form.phone.data,
            fax=form.fax.data,
            contact_name=form.contact_name.data,
            biller_name=form.biller_name.data,
            biller_email=form.biller_email.data,
        )
        
        try:
            db.session.add(new_provider)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login_register.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            print(f"Registration Error: {e}")
    
    return render_template('register.html', title="Register", form=form)

@login_register.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Get provider from the database based on the provided username
        provider = Provider.query.filter_by(username=form.username.data).first()

        if provider and check_password_hash(provider.password, form.password.data):
            # Successful login - store username in session and log in the user
            session['username'] = provider.username
            session['user_id'] = provider.id  # Add this
            session['last_active'] = str(datetime.now())  # Add this
            login_user(provider)  # This is needed for flask-login
            welcome_message = f"Logged in {provider.first_name} {provider.last_name}, {provider.medical_title}"
            flash(welcome_message)

            return redirect(url_for('dashboard.dashboard_view'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', title="Login", form=form)