# create_pr1_tables.py
from main import app, db

with app.app_context():
    try:
        # Import your models
        from models.pr1_model import NarrativeReport, DiagnosticImage, PR1Report
        
        # First create the PR1Report table
        if not db.engine.dialect.has_table(db.engine, 'pr1_reports'):
            PR1Report.__table__.create(db.engine)
            print("✅ PR1Report table created successfully!")
        
        # Then create the NarrativeReport table
        if not db.engine.dialect.has_table(db.engine, 'narrative_reports'):
            NarrativeReport.__table__.create(db.engine)
            print("✅ NarrativeReport table created successfully!")
        
        # Finally create the DiagnosticImage table
        if not db.engine.dialect.has_table(db.engine, 'diagnostic_images'):
            DiagnosticImage.__table__.create(db.engine)
            print("✅ DiagnosticImage table created successfully!")
            
        print("All tables created successfully!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")