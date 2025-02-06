from flask import Blueprint, render_template, request, redirect, url_for, flash, session  
from flask_login import login_required, current_user, logout_user
from extensions import provider_info_db as db
from models.provider_info_models import Provider

from models.patient_medical_hx_models import Auth
from forms.wc_patient_portal_form import wc_PatientRegistrationForm
from datetime import datetime
import os
import io
from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename
from security import check_session_timeout
from flask import send_file

"""""""