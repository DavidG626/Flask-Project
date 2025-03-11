# One-time script to update all existing RFAs with dates from their progress notes
from your_app import db
from models import RequestForAuthorization, ProgressNote

# Get all RFAs with None auth_date
rfas = RequestForAuthorization.query.filter(RequestForAuthorization.auth_date == None).all()

for rfa in rfas:
    # Get the associated progress note
    progress_note = ProgressNote.query.get(rfa.progress_note_id)
    if progress_note and progress_note.date_of_exam:
        # Update the RFA with the progress note's date
        rfa.auth_date = progress_note.date_of_exam
        print(f"Updated RFA {rfa.id} with date {progress_note.date_of_exam}")
    else:
        print(f"Could not find date for RFA {rfa.id}")

# Commit all changes
db.session.commit()
print(f"Updated {len(rfas)} RFAs")