# create_tables.py
from main import app, db

def create_models():
    with app.app_context():
        try:
            # Import your models here
            from models.pr1_model import NarrativeReport, DiagnosticImage
            
            # Create the tables
            db.create_all()
            print("✅ Tables created successfully!")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    create_models()