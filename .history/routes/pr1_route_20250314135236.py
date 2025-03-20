# routes/pr1_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models.pr1_model import PR1Report, NarrativeReport, DiagnosticImage
from models.wc_patient_models import Patient
from extensions import provider_info_db as db
from datetime import datetime