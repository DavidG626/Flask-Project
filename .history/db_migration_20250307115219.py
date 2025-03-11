# db_migration.py


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
    # Example usage - uncomment and modify as needed
    add_column("patient", "patient_phone", "VARCHAR(20)")

    # "patient"
    
    # For future changes, you can add more columns like this:
    # add_column("patient", "patient_email", "VARCHAR(100)")
    # add_column("provider", "provider_specialty", "VARCHAR(50)")