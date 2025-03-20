# create_pr1_tables.py
from main import app, db

with app.app_context():
    try:
        # Import your PR1 models
        from models.pr1_model import NarrativeReport, DiagnosticImage
        
        # Create the tables
        db.create_all()
        print("✅ PR1 tables created successfully!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")