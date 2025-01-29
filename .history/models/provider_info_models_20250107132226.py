from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from extensions import provider_info_db as db






#Provider info database
class Provider(db.Model):
    
    # Provider Information
    id = db.Column(db.Integer, primary_key=True)  
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    
    # Password
    password = db.Column(db.String(60), nullable=False)  # Use hashing later
    
    # Professional Information
    medical_title = db.Column(db.String(10), nullable=False)
    specialty = db.Column(db.String(50), nullable=False)
    npi = db.Column(db.String(20), unique=True, nullable=False)
    medical_license = db.Column(db.String(30), unique=True, nullable=False)
    practice_name = db.Column(db.String(100), nullable=False)
    
    # Contact Information
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    fax = db.Column(db.String(20), nullable=False)
    
    # Staff Information
    contact_name = db.Column(db.String(50), nullable=False)  # Medical Assistant
    biller_name = db.Column(db.String(50), nullable=False)
    biller_email = db.Column(db.String(120), nullable=False)
    
    # Profile Picture
    #image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    
   
    def __repr__(self):
        return f"Provider('{self.first_name}', '{self.last_name}', '{self.medical_title}')"