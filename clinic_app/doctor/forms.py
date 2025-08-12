from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, SelectField, FloatField, FieldList, FormField, DateTimeLocalField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from clinic_app.models import Patient, Ticket, Visit, Prescription, DoctorSettings, Appointment


class VisitForm(FlaskForm):
    symptoms = TextAreaField("Symptômes", validators=[DataRequired(), Length(min=5, max=500)])
    diagnosis = TextAreaField("Diagnostic", validators=[DataRequired(), Length(min=5, max=500)])
    treatment = TextAreaField("Traitement", validators=[DataRequired(), Length(min=5, max=500)])
    notes = TextAreaField("Notes", validators=[Optional(), Length(max=500)])
    status = SelectField("État", choices=[
        ("stable", "Stable"),
        ("suivi", "Suivi"),
        ("urgent", "Urgent"),
        ("en_attente", "En attente")
    ], validators=[DataRequired()])
    price = FloatField("Prix de la consultation", validators=[DataRequired(), NumberRange(min=0)])
    payment_status = SelectField("État du paiement", choices=[
        ("non_payé", "Non payé"),
        ("payé", "Payé"),
        ("partiellement_payé", "Partiellement payé")
    ], validators=[DataRequired()])
    follow_up_date = DateTimeLocalField('Date de suivi', validators=[Optional()], format='%Y-%m-%dT%H:%M')
    follow_up_notes = TextAreaField("Notes du rendez-vous", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Enregistrer la consultation")


class MedicationEntryForm(FlaskForm):
    medication_id = SelectField('Médicament', coerce=int, validators=[DataRequired()])
    quantity = StringField('Quantité/Durée', validators=[Optional(), Length(max=50)])
    instructions = StringField('Instructions', validators=[DataRequired(), Length(min=2, max=200)])


class PrescriptionForm(FlaskForm):
    predefined_prescription = SelectField('Choisir une ordonnance prédéfinie', coerce=int, choices=[(0, 'Choisir une ordonnance prédéfinie')], validators=[Optional()])
    medications = FieldList(FormField(MedicationEntryForm), min_entries=1)
    submit = SubmitField('Créer une ordonnance')


class DoctorSettingsForm(FlaskForm):
    default_visit_price = FloatField("Prix de consultation par défaut", validators=[DataRequired(), NumberRange(min=0)])
    
    # Paramètres du nom du médecin et de la clinique
    doctor_name_arabic = StringField("Nom du médecin en arabe", validators=[Optional(), Length(max=100)])
    doctor_name_latin = StringField("Nom du médecin en latin", validators=[Optional(), Length(max=100)])
    clinic_name = StringField("Nom de la clinique en arabe", validators=[Optional(), Length(max=100)])
    clinic_name_latin = StringField("Nom de la clinique en latin", validators=[Optional(), Length(max=100)])
    doctor_specialty = StringField("Spécialité du médecin en arabe", validators=[Optional(), Length(max=100)])
    doctor_specialty_latin = StringField("Spécialité du médecin en latin", validators=[Optional(), Length(max=100)])
    
    # Logo de la clinique
    clinic_logo = FileField("Logo de la clinique", validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Seuls les fichiers image sont autorisés (JPG, PNG, GIF)')
    ])
    
    submit = SubmitField("Enregistrer les paramètres")


class MedicationForm(FlaskForm):
    name = StringField('Nom du médicament', validators=[DataRequired(), Length(min=2, max=100)])
    dosage = StringField('Dosage', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Ajouter un médicament')


class PredefinedPrescriptionForm(FlaskForm):
    name = StringField('Nom de l\'ordonnance prédéfinie', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Ajouter une ordonnance prédéfinie')


class AppointmentForm(FlaskForm):
    appointment_date = DateTimeLocalField('Date et heure du rendez-vous', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    notes = TextAreaField('Notes sur le rendez-vous', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Réserver le rendez-vous')
