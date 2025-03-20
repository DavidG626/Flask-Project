# run_4.py - Add treatment_to_date column
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

if __name__ == "__main__":
    # Add the treatment_to_date field that was missed
    add_column("pr1_reports", "treatment_to_date", "TEXT")