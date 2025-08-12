from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, SelectField, DateTimeLocalField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional
from datetime import date


class PatientForm(FlaskForm):
    """نموذج تسجيل مريض جديد أو تحديث بيانات المريض (النسخة العربية)"""
    full_name = StringField("الاسم الكامل", validators=[DataRequired(), Length(min=3, max=100)])
    phone = StringField("رقم الهاتف", validators=[DataRequired(), Length(min=8, max=20)])
    birth_date = DateField("تاريخ الميلاد", format='%Y-%m-%d', validators=[Optional()], default=date.today)
    gender = SelectField(
        "الجنس", 
        choices=[
            ("", "اختر الجنس"),
            ("male", "ذكر"),
            ("female", "أنثى"),
            ("other", "غير محدد")
        ],
        validators=[Optional()]
    )
    blood_group = SelectField(
        "فصيلة الدم",
        choices=[
            ("", "اختر فصيلة الدم"),
            ("A+", "A+"),
            ("A-", "A-"),
            ("B+", "B+"),
            ("B-", "B-"),
            ("AB+", "AB+"),
            ("AB-", "AB-"),
            ("O+", "O+"),
            ("O-", "O-")
        ],
        validators=[Optional()]
    )
    address = StringField("العنوان", validators=[Optional(), Length(max=200)])
    submit = SubmitField("حفظ")


class PatientFormFrench(FlaskForm):
    """Formulaire d'enregistrement d'un nouveau patient ou de mise à jour des données patient (Version française)"""
    full_name = StringField("Nom complet", validators=[DataRequired(), Length(min=3, max=100)])
    phone = StringField("Numéro de téléphone", validators=[DataRequired(), Length(min=8, max=20)])
    birth_date = DateField("Date de naissance", format='%Y-%m-%d', validators=[Optional()], default=date.today)
    gender = SelectField(
        "Sexe", 
        choices=[
            ("", "Choisir le sexe"),
            ("male", "Homme"),
            ("female", "Femme")
        ],
        validators=[Optional()]
    )
    blood_group = SelectField(
        "Groupe sanguin",
        choices=[
            ("", "Choisir le groupe sanguin"),
            ("A+", "A+"),
            ("A-", "A-"),
            ("B+", "B+"),
            ("B-", "B-"),
            ("AB+", "AB+"),
            ("AB-", "AB-"),
            ("O+", "O+"),
            ("O-", "O-")
        ],
        validators=[Optional()]
    )
    address = StringField("Adresse", validators=[Optional(), Length(max=200)])
    submit = SubmitField("Enregistrer")


class SecretaryAppointmentForm(FlaskForm):
    """Formulaire de réservation de rendez-vous par la secrétaire"""
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    doctor_id = SelectField('Médecin', coerce=int, validators=[DataRequired()])
    appointment_date = DateTimeLocalField('Date et heure du rendez-vous', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    notes = TextAreaField('Notes sur le rendez-vous', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Réserver le rendez-vous')


class PaymentUpdateForm(FlaskForm):
    """Formulaire de mise à jour du statut de paiement"""
    payment_status = SelectField("Statut de paiement", choices=[
        ("payé", "Payé"),
        ("non_payé", "Non payé"),
        ("partiellement_payé", "Partiellement payé")
    ], validators=[DataRequired()])
    submit = SubmitField("Mettre à jour le statut")