# run_2.py - Create PR1 relation tables
from main import app, db  # Make sure to import app and db

def create_table(table_name, schema):
    """
    Create a new table.
    
    Args:
        table_name (str): Name of the table to create
        schema (str): SQL schema for the table
    """
    with app.app_context():
        try:
            sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})"
            db.session.execute(db.text(sql))
            db.session.commit()
            print(f"✅ Table '{table_name}' created successfully!")
        except Exception as e:
            print(f"❌ Error creating table '{table_name}': {str(e)}")

if __name__ == "__main__":
    # Create PR1 relation tables
    create_table("pr1_cpt", """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pr1_id INTEGER NOT NULL,
        cpt_id INTEGER NOT NULL,
        created_at DATETIME,
        FOREIGN KEY (pr1_id) REFERENCES pr1_reports (id),
        FOREIGN KEY (cpt_id) REFERENCES cpt_codes (id),
        UNIQUE (pr1_id, cpt_id)
    """)

    create_table("pr1_authorization", """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pr1_id INTEGER NOT NULL,
        patient_id INTEGER NOT NULL,
        is_new_request BOOLEAN DEFAULT 1,
        is_resubmission BOOLEAN DEFAULT 0,
        is_expedited BOOLEAN DEFAULT 0,
        is_oral_confirmation BOOLEAN DEFAULT 0,
        status VARCHAR(50) DEFAULT 'pending',
        created_at DATETIME,
        authorization_number VARCHAR(100),
        auth_date DATE,
        FOREIGN KEY (pr1_id) REFERENCES pr1_reports (id),
        FOREIGN KEY (patient_id) REFERENCES patient (id)
    """)

    create_table("pr1_rfa_items", """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rfa_id INTEGER NOT NULL,
        diagnosis VARCHAR(200) NOT NULL,
        icd_code VARCHAR(20) NOT NULL,
        service_requested VARCHAR(255) NOT NULL,
        cpt_code VARCHAR(20),
        other_info TEXT,
        FOREIGN KEY (rfa_id) REFERENCES pr1_authorization (id)
    """)