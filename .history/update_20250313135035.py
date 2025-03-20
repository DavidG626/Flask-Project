from flask import Flask
from extensions import provider_info_db as db

# Create a minimal Flask app just for this script
app = Flask(__name__)

# Configure the app the same way as in main.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///provider_info_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with the app
db.init_app(app)

# Import ALL models to avoid circular import issues
# Use the same import pattern as in your main.py
from models.auth_model import Auth
from models.cpt_model import CPTCode
from models.icd10_models import ICD10Code
from models.imaging_model import ImagingResult
from models.lab_model import LabResult
from models.misc_model import Misc
from models.operative_model import OperativeReport
from models.patient_medical_hx_models import Allergy, MedicalCondition, Surgery, Medication, PastMedicalHistory
from models.pr2_model import ProgressNote, ProgressNoteCPT, RequestForAuthorization, RFAItem
from models.provider_info_models import Provider
from models.wc_patient_models import Patient, Employer, ClaimsAdmin, Lawyer
from models.pr1_model import 

# Execute within the app context
with app.app_context():
    # Get all RFAs with None auth_date
    rfas = RequestForAuthorization.query.filter(RequestForAuthorization.auth_date == None).all()
    
    count = 0
    for rfa in rfas:
        # Get the associated progress note
        progress_note = ProgressNote.query.get(rfa.progress_note_id)
        if progress_note and progress_note.date_of_exam:
            # Update the RFA with the progress note's date
            rfa.auth_date = progress_note.date_of_exam
            count += 1
            print(f"Updated RFA {rfa.id} with date {progress_note.date_of_exam}")
        else:
            print(f"Could not find date for RFA {rfa.id}")
    
    # Commit all changes
    db.session.commit()
    print(f"Updated {count} RFAs")