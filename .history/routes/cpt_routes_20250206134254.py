# routes/cpt_routes.py
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required
from models.cpt_model import CPTCode
from extensions import provider_info_db as db

# Create a Blueprint
cpt_bp = Blueprint('cpt', __name__)

# Define routes
@cpt_bp.route('/cpt_codes')
@login_required
def cpt_codes():
    cpt_codes = CPTCode.query.filter_by(active=True).order_by(CPTCode.code).all()
    return render_template('cpt_codes.html', cpt_codes=cpt_codes)

# Add a new CPT code
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

# Delete a CPT code
@cpt_bp.route('/delete_cpt/<int:code_id>', methods=['POST'])
@login_required
def delete_cpt(code_id):
    code = CPTCode.query.get_or_404(code_id)
    try:
        db.session.delete(code)
        db.session.commit()
        flash('CPT code deleted successfully', 'success')
    except:
        db.session.rollback()
        flash('Error deleting CPT code', 'error')
    return redirect(url_for('cpt.cpt_codes'))



# Update a CPT code

@cpt_bp.route('/edit_cpt/<int:code_id>', methods=['GET', 'POST'])
@login_required
def edit_cpt(code_id):
    cpt = CPTCode.query.get_or_404(code_id)
    
    if request.method == 'POST':
        try:
            cpt.code = request.form.get('code')
            cpt.description = request.form.get('description')
            cpt.price = float(request.form.get('price')) if request.form.get('price') else None
            cpt.category = request.form.get('category')
            
            db.session.commit()
            flash('CPT code updated successfully', 'success')
            return redirect(url_for('cpt.cpt_codes'))
        except:
            db.session.rollback()
            flash('Error updating CPT code', 'error')
            return redirect(url_for('cpt.edit_cpt', code_id=code_id))
    
    return render_template('edit_cpt.html', cpt=cpt)
