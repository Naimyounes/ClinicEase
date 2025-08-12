# ClinicEase - Système de Gestion de Cliniques Médicales

## 🏥 À propos

ClinicEase est un système complet de gestion de cliniques médicales développé avec Flask et Python. Il offre une solution intégrée pour la gestion des patients, des rendez-vous, des consultations, des ordonnances et de la comptabilité.

## ✨ Fonctionnalités principales

### 👨‍⚕️ Interface Médecin
- **Tableau de bord intelligent** avec statistiques en temps réel
- **Gestion des patients** avec historique médical complet
- **Consultations** avec enregistrement des symptômes et diagnostics
- **Ordonnances électroniques** avec génération PDF
- **Gestion des médicaments** et ordonnances prédéfinies
- **Calendrier des rendez-vous** et planification
- **Rapports financiers** et statistiques

### 👩‍💼 Interface Secrétaire
- **Gestion des patients** - inscription et mise à jour
- **Liste d'attente intelligente** avec système de priorité
- **Gestion des rendez-vous** avec notifications
- **Suivi des paiements** et comptabilité
- **Écran d'attente** pour les patients
- **Recherche avancée** des patients

### 🎯 Fonctionnalités générales
- **Interface multilingue** (Français)
- **Système d'authentification** sécurisé
- **Responsive design** pour tous les appareils
- **Notifications en temps réel**
- **Sauvegarde automatique** des données
- **Rapports PDF** personnalisables

## 🚀 Installation

### Prérequis
- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation rapide

1. **Cloner le projet**
```bash
git clone https://github.com/votre-repo/ClinicEase.git
cd ClinicEase
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Lancer l'application**
```bash
python run.py
```

4. **Accéder à l'application**
- Application principale: http://localhost:5000
- Écran d'attente: http://localhost:5000/waiting-room

### Installation Windows (Script automatique)
```bash
setup_and_run.bat
```

## 👥 Comptes par défaut

### Compte Médecin
- **Nom d'utilisateur**: `doctor`
- **Mot de passe**: `doctor123`

### Compte Secrétaire
- **Nom d'utilisateur**: `secretary`
- **Mot de passe**: `secretary123`

## 🛠️ Technologies utilisées

### Backend
- **Flask 2.2.5** - Framework web Python
- **SQLAlchemy** - ORM pour base de données
- **Flask-Login** - Gestion des sessions
- **Flask-WTF** - Gestion des formulaires
- **SQLite** - Base de données

### Frontend
- **Bootstrap 5** - Framework CSS
- **Font Awesome** - Icônes
- **Roboto Font** - Typographie
- **JavaScript/jQuery** - Interactivité

### Génération PDF
- **ReportLab** - Génération de PDF
- **Arabic Reshaper** - Support des langues RTL
- **Python-BIDI** - Algorithme bidirectionnel

## 📁 Structure du projet

```
ClinicEase/
├── clinic_app/
│   ├── auth/                 # Authentification
│   ├── doctor/              # Interface médecin
│   ├── secretary/           # Interface secrétaire
│   ├── main/                # Pages principales
│   ├── static/              # Fichiers statiques
│   ├── templates/           # Templates HTML
│   └── models.py            # Modèles de données
├── instance/                # Base de données
├── requirements.txt         # Dépendances
├── run.py                  # Point d'entrée
└── README_FR.md            # Documentation
```

## 🗄️ Modèles de données

### Utilisateurs
- Médecins et secrétaires avec rôles distincts
- Authentification sécurisée

### Patients
- Informations personnelles complètes
- Historique médical
- Groupe sanguin et allergies

### Consultations
- Symptômes et diagnostics
- Traitements prescrits
- Suivi des paiements

### Rendez-vous
- Planification avancée
- Notifications automatiques
- Gestion des statuts

### Ordonnances
- Médicaments avec posologie
- Génération PDF automatique
- Modèles prédéfinis

## 💰 Gestion financière

- **Suivi des paiements** en temps réel
- **Rapports financiers** détaillés
- **Statistiques de revenus** par période
- **Gestion des impayés**
- **Devise**: Dinar Algérien (DA)

## 📱 Interface responsive

L'application s'adapte automatiquement à tous les types d'écrans :
- **Desktop** - Interface complète
- **Tablette** - Navigation optimisée
- **Mobile** - Interface tactile

## 🔒 Sécurité

- **Authentification** par session
- **Protection CSRF** sur tous les formulaires
- **Validation** des données côté serveur
- **Hashage** sécurisé des mots de passe
- **Contrôle d'accès** basé sur les rôles

## 📊 Tableaux de bord

### Médecin
- Patients en attente
- Consultations du jour
- Revenus quotidiens
- Rendez-vous à venir
- Statistiques mensuelles

### Secrétaire
- Liste d'attente en temps réel
- Nouveaux patients
- Paiements en attente
- Rendez-vous du jour
- Notifications importantes

## 🎨 Personnalisation

### Thèmes
- Interface moderne et épurée
- Couleurs professionnelles
- Animations fluides
- Mode sombre (à venir)

### Paramètres médecin
- Prix de consultation par défaut
- Informations de la clinique
- Signature électronique
- Modèles d'ordonnances

## 📈 Rapports et statistiques

- **Rapports quotidiens** automatiques
- **Statistiques de fréquentation**
- **Analyse des revenus**
- **Suivi des patients**
- **Export PDF** des rapports

## 🌐 Déploiement

### Développement
```bash
python run.py
```

### Production (avec Gunicorn)
```bash
gunicorn run:app
```

### Déploiement sur Render
Le projet inclut un fichier `render.yaml` pour déploiement automatique.

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

Pour toute question ou support :
- **Email**: support@clinicease.com
- **Documentation**: [Wiki du projet](https://github.com/votre-repo/ClinicEase/wiki)
- **Issues**: [GitHub Issues](https://github.com/votre-repo/ClinicEase/issues)

## 🎯 Roadmap

### Version 2.0 (À venir)
- [ ] Application mobile
- [ ] Télémédecine
- [ ] IA pour diagnostic
- [ ] Intégration laboratoires
- [ ] API REST complète
- [ ] Multi-cliniques
- [ ] Sauvegarde cloud

### Version 1.5 (En cours)
- [x] Interface française complète
- [x] Amélioration UX/UI
- [x] Optimisation performances
- [ ] Mode hors ligne
- [ ] Notifications push

## 🏆 Remerciements

Merci à tous les contributeurs et utilisateurs qui ont rendu ce projet possible !

---

**ClinicEase** - Simplifiez la gestion de votre clinique médicale 🏥

*Développé avec ❤️ pour les professionnels de santé*