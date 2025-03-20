# create_pr1_tables.py
from main import app, db

with app.app_context():
    try:
        # Import all models from pr1_model.py
        from models.pr1_model import PR1Report, NarrativeReport, DiagnosticImage
        
        # Create tables
        db.create_all()
        print("PR1 tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {str(e)}")

if __name__ == "__main__":
    # Run the table creation
    print("Creating PR1 tables...")