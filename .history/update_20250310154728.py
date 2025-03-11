from flask import Flask
from extensions import provider_info_db as db
from models.pr2_model import RequestForAuthorization, ProgressNote

# Create a minimal Flask app just for this script
app = Flask(__name__)

# Configure the app the same way as in main.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///provider_info_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with the app
db.init_app(app)

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