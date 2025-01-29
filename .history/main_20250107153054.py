from flask import Flask, render_template, url_for, flash, redirect, jsonify
from datetime import timedelta
import os
from extensions import provider_info_db as db
from flask_login import LoginManager  x


# routes
from routes.login_register import login_register 
from routes.dashboard import dashboard_bp
from routes.wc_patient_portal_routes import wc_patient_portal_bp

# models
from models.provider_info_models import Provider
from models.wc_patient_models import Patient

app = Flask(__name__)

# Create instance directory
if not os.path.exists('instance'):
    os.makedirs('instance')

app.config['SECRET_KEY'] = 'torito'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///provider_info_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db
db.init_app(app)

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
    app.run(debug=True, port=5005)
