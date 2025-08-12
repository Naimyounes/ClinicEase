from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    """Formulaire de connexion"""
    username = StringField("Nom d'utilisateur", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")


class ChangePasswordForm(FlaskForm):
    """Formulaire de changement de mot de passe"""
    current_password = PasswordField("Mot de passe actuel", validators=[DataRequired()])
    new_password = PasswordField("Nouveau mot de passe", validators=[
        DataRequired(), 
        Length(min=6, message="Le mot de passe doit contenir au moins 6 caractères")
    ])
    confirm_password = PasswordField("Confirmer le nouveau mot de passe", validators=[
        DataRequired(),
        EqualTo('new_password', message="Les mots de passe ne correspondent pas")
    ])
    submit = SubmitField("Changer le mot de passe")
