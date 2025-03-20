from flask import Flask, render_template, url_for, flash, redirect, jsonify
from datetime import timedelta
import os
from extensions import provider_info_db as db
from flask_login import LoginManager


# models
from models.auth_model import Auth
from models.cpt_model import CPTCode
from models.icd10_models import ICD10Code
from models.imaging_model import ImagingResult
from models.lab_model import LabResult
from models.misc_model import Misc
from models.operative_model import OperativeReport
from models.patient_medical_hx_models import Allergy, MedicalCondition, Surgery, Medication, PastMedicalHistory
from models.pr2_model import ProgressNote, ProgressNoteCPT, RequestForAuthorization, RFAItem
from models.provider_info_models import Provider
from models.wc_patient_models import Patient,  Employer, ClaimsAdmin, Lawyer
from models.pr1_model import PR1Report, NarrativeReport, DiagnosticImage

# routes
from routes.auth_routes import auth_bp
from routes.cpt_routes import cpt_bp
from routes.dashboard import dashboard_bp
from routes.icd10_routes import icd10_bp
from routes.imaging_routes import imaging_bp
from routes.lab_routes import labs_bp
from routes.login_register import login_register
from routes.misc_routes import misc_bp
from routes.operative_routes import operative_bp
from routes.progress_note_route import progress_note_bp
from routes.wc_patient_portal_routes import wc_patient_portal_bp
from routes.pr1_route import pr1_bp



# Create the Flask app
app = Flask(__name__)
                
          
# Create instance directory
if not os.path.exists('instance'):
    os.makedirs('instance')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'torito')

# Simple database configuration
if os.environ.get('DATABASE_URL'):
    # Use PostgreSQL on Render when DATABASE_URL is set
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
else:
    # Use SQLite otherwise (both locally and on Render when no DATABASE_URL)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///provider_info_db.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_register.login'  # Specify the login route
login_manager.login_message_category = 'info'      # Optional: style for login messages

@login_manager.user_loader
def load_user(user_id):
    return Provider.query.get(int(user_id))

# Set session lifetime to 30 minutes
app.permanent_session_lifetime = timedelta(minutes=30)

# register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth') 
app.register_blueprint(cpt_bp, url_prefix='/cpt')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(icd10_bp, url_prefix='/icd10')
app.register_blueprint(imaging_bp, url_prefix='/imaging') 
app.register_blueprint(labs_bp, url_prefix='/labs') 
app.register_blueprint(login_register)
app.register_blueprint(misc_bp, url_prefix='/misc')
app.register_blueprint(operative_bp, url_prefix='/operative')  
app.register_blueprint(progress_note_bp, url_prefix='/progress_note')
app.register_blueprint(wc_patient_portal_bp, url_prefix='/wc_patient_portal')
app.register_blueprint(pr1_bp, url_prefix='/pr1')


# Home route
@app.route("/")
def home():
    return render_template('home.html')

# Create the database tables
with app.app_context():
    db.create_all()

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5005))
    app.run(host='0.0.0.0', port=port, debug=True)