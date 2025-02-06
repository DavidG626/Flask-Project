# routes/cpt_routes.py
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required
from models.cpt_model import CPTCode
from extensions import provider_info_db as db

icd10_bp = Blueprint('icd10', __name__)