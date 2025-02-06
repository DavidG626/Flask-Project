from flask import Flask, render_template, url_for, flash, redirect, jsonify
from datetime import timedelta
import os
from extensions import provider_info_db as db
from flask_login import LoginManager




# models
from models.auth_model import Auth
from models.imaging_model import ImagingResult
from models.lab_model import LabResult
from models.misc_model import Misc
from models.operative_model import OperativeReport
from models.provider_info_models import Provider
from models.patient_medical_hx_models import Allergy, MedicalCondition, Surgery, Medication, PastMedicalHistory
from models.wc_patient_models import Patient, BodyPart, Employer, ClaimsAdmin, Lawyer



# routes
from routes.login_register import login_register 
from routes.dashboard import dashboard_bp
from routes.wc_patient_portal_routes import wc_patient_portal_bp
from routes.auth_routes import auth_bp
from routes.imaging_routes import imaging_bp
from routes.lab_route import lab_bp
from routes.misc_routes import misc_bp
from routes.operative_routes import operative_bp






app = Flask(__name__)

# Create instance directory
if not os.path.exists('instance'):
    os.makedirs('instance')

app.config['SECRET_KEY'] = 'torito'
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

app.permanent_session_lifetime = timedelta(minutes=30)

app.register_blueprint(login_register)
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(wc_patient_portal_bp, url_prefix='/wc_patient_portal')

@app.route("/")
def home():
    return render_template('home.html')

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5004)