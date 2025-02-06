# routes/cpt_routes.py
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required
from models.cpt_model import CPTCode
from extensions import provider_info_db as db

# Create a Blueprint
cpt_bp = Blueprint('cpt', __name__)


@cpt_bp.route('/cpt_codes')
@login_required
def cpt_codes():
    cpt_codes = CPTCode.query.filter_by(active=True).order_by(CPTCode.code).all()
    return render_template('cpt_codes.html', cpt_codes=cpt_codes)

@cpt_bp.route('/add_cpt', methods=['POST'])
@login_required
def add_cpt():
    code = request.form.get('code')
    description = request.form.get('description')
    price = request.form.get('price')
    category = request.form.get('category')
    
    new_code = CPTCode(
        code=code,
        description=description,
        price=float(price) if price else None,
        category=category
    )
    
    try:
        db.session.add(new_code)
        db.session.commit()
        flash('CPT code added successfully', 'success')
    except:
        db.session.rollback()
        flash('Error adding CPT code', 'error')
    
    return redirect(url_for('cpt.cpt_codes'))