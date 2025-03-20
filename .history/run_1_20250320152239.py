# add_pr1_columns.py
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
    # Add all the new columns to pr1_reports
    add_column("pr1_reports", "is_periodic_report", "BOOLEAN")
    add_column("pr1_reports", "is_change_in_treatment", "BOOLEAN")
    add_column("pr1_reports", "is_release_from_care", "BOOLEAN") 
    add_column("pr1_reports", "is_change_in_work_status", "BOOLEAN")
    add_column("pr1_reports", "is_need_for_referral", "BOOLEAN")
    add_column("pr1_reports", "is_response_to_request", "BOOLEAN")
    add_column("pr1_reports", "is_change_in_condition", "BOOLEAN")
    add_column("pr1_reports", "is_need_for_surgery", "BOOLEAN")
    add_column("pr1_reports", "is_request_for_authorization", "BOOLEAN")
    add_column("pr1_reports", "other_reason", "VARCHAR(200)")
    add_column("pr1_reports", "date_of_exam", "DATE")
    add_column("pr1_reports", "subjective_complaints", "TEXT")
    add_column("pr1_reports", "objective_findings", "TEXT")
    add_column("pr1_reports", "diagnoses", "TEXT")
    add_column("pr1_reports", "treatment_plan", "TEXT")
    add_column("pr1_reports", "work_status", "VARCHAR(50)")
    add_column("pr1_reports", "off_work_until", "DATE")
    add_column("pr1_reports", "modified_work_date", "DATE")
    add_column("pr1_reports", "work_restrictions", "TEXT")
    add_column("pr1_reports", "full_duty_date", "DATE")
    add_column("pr1_reports", "prognosis", "TEXT")
    add_column("pr1_reports", "provider_signature", "VARCHAR(100)")
    add_column("pr1_reports", "license_number", "VARCHAR(50)")
    add_column("pr1_reports", "executed_at", "VARCHAR(100)")
    add_column("pr1_reports", "provider_specialty", "VARCHAR(100)")
    add_column("pr1_reports", "provider_phone", "VARCHAR(20)")