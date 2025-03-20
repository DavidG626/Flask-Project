# create_tables.py
from main import app, db

def create_tables_from_module(module_name):
    """
    Create database tables from all models defined in a module.
    
    Args:
        module_name (str): Import path to the module (e.g., 'models.pr1_model')
    """
    with app.app_context():
        try:
            # Dynamic import of the module
            __import__(module_name)
            
            # Create all tables defined in the models
            db.create_all()
            print(f"✅ Tables from {module_name} created successfully!")
        except Exception as e:
            print(f"❌ Error creating tables from {module_name}: {str(e)}")

if __name__ == "__main__":
    # Specify which module contains your models
    # Just change this line whenever you have a new model file
    model_module = 'models.pr1_model'
    
    # Create the tables
    create_tables_from_module(model_module)