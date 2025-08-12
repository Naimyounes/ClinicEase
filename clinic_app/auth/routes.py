from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from clinic_app.auth.forms import LoginForm, ChangePasswordForm
from clinic_app.models import User
from clinic_app import db

# Création du blueprint pour l'authentification
auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Page de connexion"""
    if current_user.is_authenticated:
        if current_user.role == "doctor":
            return redirect(url_for("doctor.dashboard"))
        else:
            return redirect(url_for("secretary.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get("next")

            flash(f"Bon retour {user.username}!", "success")

            if user.role == "doctor":
                return redirect(next_page or url_for("doctor.dashboard"))
            else:
                return redirect(next_page or url_for("secretary.dashboard"))
        else:
            flash("Échec de la connexion. Veuillez vérifier le nom d'utilisateur et le mot de passe", "danger")

    return render_template("auth/login.html", title="Connexion", form=form)


@auth.route("/logout")
@login_required
def logout():
    """Déconnexion"""
    logout_user()
    flash("Vous avez été déconnecté avec succès", "info")
    return redirect(url_for("auth.login"))


@auth.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    """Changer le mot de passe"""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        # Vérification du mot de passe actuel
        if not check_password_hash(current_user.password, form.current_password.data):
            flash("Le mot de passe actuel est incorrect", "danger")
            return render_template("auth/change_password.html", title="Changer le mot de passe", form=form)
        
        # Mise à jour du mot de passe
        current_user.password = generate_password_hash(form.new_password.data)
        db.session.commit()
        
        flash("Le mot de passe a été changé avec succès", "success")
        
        # Redirection selon le type d'utilisateur
        if current_user.role == "doctor":
            return redirect(url_for("doctor.dashboard"))
        else:
            return redirect(url_for("secretary.dashboard"))
    
    return render_template("auth/change_password.html", title="Changer le mot de passe", form=form)
