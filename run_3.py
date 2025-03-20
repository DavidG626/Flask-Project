# run_3.py - Add remaining columns
from main import app, db

def add_column(table_name, column_name, column_type):
    """
    Add a new column to an existing table.
    
    Args:
        table_name (str): Name of the table to modify
        column_name (str): Name of the column to add
        column_type (str): SQL type of the column (e.g., 'VARCHAR(20)', 'INTEGER', 'DATE')
    """
    with app.app_context():
        try:
            # This command adds the new column to your table
            sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
            db.session.execute(db.text(sql))
            db.session.commit()
            print(f"✅ Column '{column_name}' added to '{table_name}' successfully!")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    # Add the exam fields that were missing
    add_column("pr1_reports", "vital_signs", "TEXT")
    add_column("pr1_reports", "general_appearance", "TEXT")
    add_column("pr1_reports", "gait", "TEXT")
    add_column("pr1_reports", "physical_exam", "TEXT")
    add_column("pr1_reports", "palpation_findings", "TEXT")
    add_column("pr1_reports", "range_of_motion", "TEXT")
    add_column("pr1_reports", "neurological_exam", "TEXT")
    add_column("pr1_reports", "diagnostic_studies", "TEXT")
    add_column("pr1_reports", "causation_analysis", "TEXT")