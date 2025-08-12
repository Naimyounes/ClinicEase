# Guide des Tickets d'Urgence - ClinicEase

## Vue d'ensemble
Ce guide explique comment utiliser le nouveau système de tickets d'urgence dans ClinicEase, avec des niveaux de priorité améliorés et une interface utilisateur moderne.

## Niveaux de Priorité

### 1. Tickets Critiques (Priority = 2)
- **Couleur**: Rouge (#dc3545)
- **Utilisation**: Urgences médicales, cas critiques
- **Affichage**: 
  - Animation rapide (1.5s)
  - Bordure rouge épaisse (5px)
  - Badge "CRITIQUE" avec icône d'exclamation
  - Effet de brillance et pulsation
  - Son d'alerte aigu (800Hz)

### 2. Tickets Prioritaires (Priority = 1)
- **Couleur**: Jaune/Orange (#ffc107)
- **Utilisation**: Patients avec rendez-vous, cas prioritaires
- **Affichage**:
  - Animation modérée (2s)
  - Bordure jaune (4px)
  - Badge "PRIORITÉ" avec icône étoile
  - Effet de scintillement
  - Son d'alerte moyen (600Hz)

### 3. Tickets Réguliers (Priority = 0)
- **Couleur**: Bleu (#007bff)
- **Utilisation**: Patients sans rendez-vous, cas normaux
- **Affichage**:
  - Pas d'animation spéciale
  - Bordure standard
  - Affichage normal

## Fonctionnalités Implémentées

### Dashboard Médecin
- ✅ Affichage différencié des tickets selon la priorité
- ✅ Tri automatique par priorité puis par numéro
- ✅ Badges et icônes distinctifs
- ✅ Animations CSS avancées
- ✅ Bouton de test pour créer des tickets d'urgence

### Page File d'Attente (waiting_queue_status)
- ✅ Interface moderne et responsive
- ✅ Traduction complète en français
- ✅ Séparation en 3 colonnes : Critiques, Prioritaires, Réguliers
- ✅ Statistiques en temps réel
- ✅ Calcul automatique du temps d'attente
- ✅ Boutons d'action rapide pour appeler les patients
- ✅ Mise à jour automatique de la date et heure

### Améliorations Visuelles
- ✅ CSS séparé pour les tickets d'urgence
- ✅ Animations fluides et non intrusives
- ✅ Design responsive pour mobile
- ✅ Effets de hover et focus
- ✅ Indicateurs visuels (points de statut, overlays)

### JavaScript Interactif
- ✅ Gestionnaire de tickets d'urgence
- ✅ Notifications du navigateur
- ✅ Sons d'alerte différenciés
- ✅ Vérification périodique des nouveaux tickets
- ✅ Calcul automatique des temps d'attente
- ✅ Effets visuels interactifs

## Comment Utiliser

### 1. Créer un Ticket Critique
```python
# Dans le code Python
ticket = Ticket(
    patient_id=patient.id,
    number=next_number,
    status="waiting",
    ticket_type="emergency",
    priority=2,  # Critique
    notes="Urgence médicale"
)
```

### 2. Créer un Ticket Prioritaire
```python
# Dans le code Python
ticket = Ticket(
    patient_id=patient.id,
    number=next_number,
    status="waiting",
    ticket_type="reservation",
    priority=1,  # Prioritaire
    notes="Rendez-vous confirmé"
)
```

### 3. Tester le Système
1. Connectez-vous en tant que médecin
2. Allez au Dashboard
3. Cliquez sur "Test Urgence" pour créer des tickets de test
4. Observez les différents affichages selon la priorité
5. Visitez la "File d'attente" pour voir l'interface complète

## API Endpoints

### GET /doctor/api/emergency-tickets-count
Retourne le nombre de tickets d'urgence en attente:
```json
{
    "critical": 2,
    "priority": 5,
    "total": 7
}
```

## Fichiers Modifiés

### Templates
- `doctor/dashboard.html` - Dashboard médecin amélioré
- `doctor/waiting_queue_status.html` - Interface moderne de file d'attente
- `layout.html` - Ajout des CSS et JS

### CSS
- `static/css/emergency-tickets.css` - Styles principaux
- `static/css/emergency-enhancements.css` - Améliorations supplémentaires

### JavaScript
- `static/js/emergency-tickets.js` - Gestionnaire interactif

### Python
- `doctor/routes.py` - Routes et API endpoints

## Responsive Design

### Desktop (>768px)
- 3 colonnes pour les différents types de tickets
- Statistiques sur 6 colonnes
- Animations complètes

### Tablet (768px-992px)
- 2 colonnes adaptatives
- Statistiques sur 4 colonnes
- Animations réduites

### Mobile (<768px)
- 1 colonne empilée
- Statistiques sur 2 colonnes
- Animations minimales
- Boutons pleine largeur

## Personnalisation

### Modifier les Couleurs
Éditez `emergency-tickets.css`:
```css
/* Couleur critique */
.critical-item-highlight {
    border-left: 5px solid #your-color !important;
}

/* Couleur prioritaire */
.emergency-item-dashboard {
    border-left: 4px solid #your-color !important;
}
```

### Modifier les Animations
Éditez les keyframes dans `emergency-tickets.css`:
```css
@keyframes critical-glow {
    0% { /* État initial */ }
    100% { /* État final */ }
}
```

### Modifier les Sons
Éditez `emergency-tickets.js`:
```javascript
// Fréquences des sons d'alerte
const frequency = type === 'critical' ? 800 : 600;
const duration = type === 'critical' ? 0.3 : 0.2;
```

## Dépannage

### Les animations ne fonctionnent pas
1. Vérifiez que les CSS sont bien chargés
2. Contrôlez la console pour les erreurs
3. Assurez-vous que les classes CSS sont appliquées

### Les sons ne marchent pas
1. Vérifiez les permissions du navigateur
2. L'utilisateur doit interagir avec la page d'abord
3. Certains navigateurs bloquent l'audio automatique

### Les notifications ne s'affichent pas
1. Accordez les permissions de notification
2. Vérifiez que l'API endpoint fonctionne
3. Contrôlez la console JavaScript

## Support
Pour toute question ou problème, consultez les logs de l'application ou contactez l'équipe de développement.