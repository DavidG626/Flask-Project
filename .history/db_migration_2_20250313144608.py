# db_migration.py
from main import app, db

def add_column(table_name, column_name, column_type):
    """
    Add a new column to an existing table.
    """
    with app.app_context():
        try:
            sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
            db.session.execute(db.text(sql))
            db.session.commit()
            print(f"✅ Column '{column_name}' added to '{table_name}' successfully!")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def create_tables():
    """
    Create all tables for PR1 and Narrative reports.
    """
    with app.app_context():
        try:
            # Import all models from pr1_model.py
            from models.pr1_model import PR1Report, PR1RequestForAuthorization, NarrativeReport, DiagnosticImage
            
            # Create tables
            for model in [PR1Report, PR1RequestForAuthorization, NarrativeReport, DiagnosticImage]:
                model.__table__.create(db.engine, checkfirst=True)
                print(f"✅ Table '{model.__tablename__}' created successfully!")
                
            print("✅ All tables created successfully!")
        except Exception as e:
            print(f"❌ Error creating tables: {str(e)}")

if __name__ == "__main__":
    create_tables()