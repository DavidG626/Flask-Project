from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, DateField, FieldList, FormField
from wtforms.validators import DataRequired, Optional

class AllergyForm(FlaskForm):
    allergy_name = StringField('Allergy Name', validators=[DataRequired()])

class MedicalConditionForm(FlaskForm):
    condition_name = StringField('Condition Name', validators=[DataRequired()])

class SurgeryForm(FlaskForm):
    surgery_name = StringField('Surgery Name', validators=[DataRequired()])
    surgery_date = DateField('Surgery Date', validators=[Optional()])

class MedicationForm(FlaskForm):
    medication_name = StringField('Medication Name', validators=[DataRequired()])
    dosage = StringField('Dosage', validators=[DataRequired()])
    frequency = StringField('Frequency', validators=[DataRequired()])

class PastMedicalHistoryForm(FlaskForm):
    patient_id = IntegerField('Patient ID', validators=[DataRequired()])
    date = DateField('Date', validators=[Optional()])

    allergies = FieldList(FormField(AllergyForm), min_entries=1)
    medical_conditions = FieldList(FormField(MedicalConditionForm), min_entries=1)
    surgeries = FieldList(FormField(SurgeryForm), min_entries=1)
    medications = FieldList(FormField(MedicationForm), min_entries=1)

    current_smoker = BooleanField('Current Smoker', default=False)
    former_smoker = BooleanField('Former Smoker', default=False)
    quit_date = DateField('Quit Date', validators=[Optional()])
    never_smoker = BooleanField('Never Smoker', default=False)
    passive_smoker = BooleanField('Passive Smoker', default=False)
    vaping = BooleanField('Vaping', default=False)

    wine_per_week = IntegerField('Wine per Week', validators=[Optional()])
    beer_per_week = IntegerField('Beer per Week', validators=[Optional()])
    liquor_per_week = IntegerField('Liquor per Week', validators=[Optional()])

    marijuana = BooleanField('Marijuana', default=False)
    cocaine = BooleanField('Cocaine', default=False)
    meth = BooleanField('Meth', default=False)
    iv_drugs = BooleanField('IV Drugs', default=False)