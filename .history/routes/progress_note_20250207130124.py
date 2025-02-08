from flask import Blueprint, render_template, request, redirect, url_for, flash, session  
from flask_login import login_required, current_user, logout_user
from extensions import provider_info_db as db
from models.wc_patient_models import Patient
from models.provider_info_models import Provider
from models.imaging_model import ImagingResult
from datetime import datetime
import os
import io
from werkzeug.utils import secure_filename
from security import check_session_timeout
from flask import send_file

pr2_bp = Blueprint('pr2', __name__)

# Start Progress Note
@progress_note_bp.route('/patient/<int:patient_id>/progress_note')
@login_required
@check_session_timeout