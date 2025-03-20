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
    Create tables for models.
    """
    with app.app_context():
        try:
            # Import your models with their actual names
            # Replace these with the actual class names from your pr1_model.py file
            from models.pr1_model import NarrativeReport, DiagnosticImage
            
            # Create tables
            for model in [NarrativeReport, DiagnosticImage]:
                model.__table__.create(db.engine, checkfirst=True)
                print(f"✅ Table '{model.__tablename__}' created successfully!")
                
            print("✅ All tables created successfully!")
        except Exception as e:
            print(f"❌ Error creating tables: {str(e)}")

if __name__ == "__main__":
    create_tables()