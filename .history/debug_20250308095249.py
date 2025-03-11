# debug.py
from extensions import provider_info_db as db
from models.pr2_model import ProgressNote, ProgressNoteCPT
from models.cpt_model import CPTCode
from models.wc_patient_models import Patient

# Import your Flask app - adjust this to match your app's structure
from main import app

# Hardcode the note ID to debug
NOTE_ID = 6  # Change this to the progress note ID you want to debug

def debug_progress_note_cpt(note_id):
    print(f"\n=== Debugging Progress Note {note_id} ===\n")
    
    # Check if the progress note exists
    note = ProgressNote.query.get(note_id)
    if not note:
        print(f"Progress Note with ID {note_id} not found!")
        return
    
    print(f"Progress Note ID: {note.id}")
    print(f"Patient ID: {note.patient_id}")
    print(f"Date: {note.date_of_exam}")
    
    # Get CPT relations
    print("\n=== CPT Relations ===\n")
    cpt_relations = ProgressNoteCPT.query.filter_by(progress_note_id=note_id).all()
    print(f"Number of CPT relations: {len(cpt_relations)}")
    
    if len(cpt_relations) == 0:
        print("No CPT codes found for this progress note!")
    
    for rel in cpt_relations:
        print(f"\nRelation ID: {rel.id}, CPT ID: {rel.cpt_id}")
        
        # Check if CPT code exists
        cpt = CPTCode.query.get(rel.cpt_id)
        if cpt:
            print(f"CPT Code: {cpt.code} - {cpt.description}")
        else:
            print(f"CPT Code not found for ID {rel.cpt_id}")
    
    # Check relationship attribute
    print("\n=== Checking Relationship ===\n")
    try:
        print(f"cpt_codes_rel attribute exists: {'cpt_codes_rel' in dir(note)}")
        if hasattr(note, 'cpt_codes_rel'):
            print(f"Number of CPT codes via relationship: {len(note.cpt_codes_rel)}")
            for rel in note.cpt_codes_rel:
                print(f"Relation ID: {rel.id}")
                print(f"CPT Code via relationship: {rel.cpt_code.code if rel.cpt_code else 'None'}")
    except Exception as e:
        print(f"Error checking relationship: {str(e)}")

if __name__ == "__main__":
    # Create application context before working with the database
    with app.app_context():
        debug_progress_note_cpt(NOTE_ID)


# Progress note created with authorization request!
# Error creating progress note: Could not build url for endpoint 'progress_note_bp.view_rfa' with values ['rfa_id']. Did you mean 'pr2.view_rfa' instead?