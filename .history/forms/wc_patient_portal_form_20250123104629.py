from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, BooleanField, SelectField
from wtforms.validators import Optional

class MedicalHistoryForm(FlaskForm):
    # Allergies
    allergies = [StringField(f'Allergy {i+1}') for i in range(15)]
    
    # Medical Conditions
    conditions = [StringField(f'Condition {i+1}') for i in range(15)]
    
    # Surgeries
    surgeries = [StringField(f'Surgery {i+1}') for i in range(15)]
    surgery_dates = [DateField(f'Surgery Date {i+1}', validators=[Optional()]) for i in range(15)]
    
    # Medications
    medications = [StringField(f'Medication {i+1}') for i in range(15)]
    dosages = [StringField(f'Dosage {i+1}') for i in range(15)]
    frequencies = [StringField(f'Frequency {i+1}') for i in range(15)]

    # Social History
    current_smoker = BooleanField('Current Smoker')
    former_smoker = BooleanField('Former Smoker')
    quit_date = DateField('Quit Date', validators=[Optional()])
    never_smoker = BooleanField('Never Smoker')
    passive_smoker = BooleanField('Passive Smoker')
    vaping = BooleanField('Vaping')
    
    # Alcohol
    wine_per_week = IntegerField('Wine per week', validators=[Optional()])
    beer_per_week = IntegerField('Beer per week', validators=[Optional()])
    liquor_per_week = IntegerField('Liquor per week', validators=[Optional()])