# routes/cpt_routes.py
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required
from models.icd10_models import ICD10Code
from extensions import provider_info_db as db

icd10_bp = Blueprint('icd10', __name__)

@icd10_bp.route('/icd10_codes')
@login_required
def icd10_codes():
    search_query = request.args.get('search', '').strip()
    
    if search_query:
        icd10_codes = ICD10Code.query.filter(
            db.or_(
                ICD10Code.code.ilike(f'%{search_query}%'),
                ICD10Code.description.ilike(f'%{search_query}%')
            )
        ).order_by(ICD10Code.code).all()
    else:
        icd10_codes = ICD10Code.query.order_by(ICD10Code.code).all()
    
    return render_template('icd10_codes.html', icd10_codes=icd10_codes, search_query=search_query)

# Add a new ICD10 code
@icd10_bp.route('/add_icd10', methods=['POST'])
