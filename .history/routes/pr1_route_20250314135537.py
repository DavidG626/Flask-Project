from flask import Blueprint, render_template, request, redirect, url_for, flash, session  
from flask_login import login_required, current_user, logout_user
from extensions import provider_info_db as db
from models.wc_patient_models import Patient
from models.provider_info_models import Provider
from models.icd10_models import ICD10Code
from models.cpt_model import CPTCode
from models.wc_patient_models import PatientDiagnosis, ClaimsAdmin
from models.pr2_model import ProgressNote, ProgressNoteCPT, RequestForAuthorization, RFAItem
from datetime import datetime
import os
import io
from werkzeug.utils import secure_filename
from security import check_session_timeout
from flask import send_file

pr1_bp = Blueprint('pr1', __name__)

