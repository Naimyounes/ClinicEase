/**
 * JavaScript pour la gestion des tickets d'urgence
 * Améliore l'expérience utilisateur avec des effets visuels et sonores
 */

class EmergencyTicketManager {
    constructor() {
        this.init();
        this.setupEventListeners();
        this.startPeriodicUpdates();
    }

    init() {
        console.log('Emergency Ticket Manager initialized');
        this.applyEmergencyStyles();
        this.setupNotifications();
    }

    /**
     * Applique les styles d'urgence aux tickets existants
     */
    applyEmergencyStyles() {
        // Appliquer les styles aux tickets critiques
        const criticalTickets = document.querySelectorAll('[data-priority="2"]');
        criticalTickets.forEach(ticket => {
            ticket.classList.add('ticket-critical');
            this.addCriticalIndicators(ticket);
        });

        // Appliquer les styles aux tickets prioritaires
        const priorityTickets = document.querySelectorAll('[data-priority="1"]');
        priorityTickets.forEach(ticket => {
            ticket.classList.add('ticket-priority');
            this.addPriorityIndicators(ticket);
        });

        // Appliquer les styles aux tickets réguliers
        const regularTickets = document.querySelectorAll('[data-priority="0"]');
        regularTickets.forEach(ticket => {
            ticket.classList.add('ticket-regular');
        });
    }

    /**
     * Ajoute des indicateurs visuels pour les tickets critiques
     */
    addCriticalIndicators(ticket) {
        // Ajouter un badge critique si pas déjà présent
        if (!ticket.querySelector('.badge-critical')) {
            const badge = document.createElement('span');
            badge.className = 'badge badge-critical ms-2';
            badge.innerHTML = '<i class="fas fa-exclamation-circle me-1"></i>CRITIQUE';
            
            const patientName = ticket.querySelector('h6, .patient-name');
            if (patientName) {
                patientName.appendChild(badge);
            }
        }

        // Ajouter une icône critique
        const icon = ticket.querySelector('.fa-user, .fa-clock');
        if (icon) {
            icon.classList.add('icon-critical');
        }

        // Ajouter un indicateur de statut
        ticket.classList.add('status-critical');
    }

    /**
     * Ajoute des indicateurs visuels pour les tickets prioritaires
     */
    addPriorityIndicators(ticket) {
        // Ajouter un badge prioritaire si pas déjà présent
        if (!ticket.querySelector('.badge-priority')) {
            const badge = document.createElement('span');
            badge.className = 'badge badge-priority ms-2';
            badge.innerHTML = '<i class="fas fa-star me-1"></i>PRIORITÉ';
            
            const patientName = ticket.querySelector('h6, .patient-name');
            if (patientName) {
                patientName.appendChild(badge);
            }
        }

        // Ajouter une icône prioritaire
        const icon = ticket.querySelector('.fa-user, .fa-clock');
        if (icon) {
            icon.classList.add('icon-priority');
        }

        // Ajouter un indicateur de statut
        ticket.classList.add('status-priority');
    }

    /**
     * Configure les écouteurs d'événements
     */
    setupEventListeners() {
        // Écouteur pour les boutons d'appel d'urgence
        document.addEventListener('click', (e) => {
            if (e.target.closest('.btn-call-critical')) {
                this.handleCriticalCall(e);
            } else if (e.target.closest('.btn-call-priority')) {
                this.handlePriorityCall(e);
            }
        });

        // Écouteur pour les tickets d'urgence (hover effects)
        document.addEventListener('mouseenter', (e) => {
            const ticket = e.target.closest('.ticket-critical, .ticket-priority');
            if (ticket) {
                this.highlightTicket(ticket);
            }
        }, true);

        document.addEventListener('mouseleave', (e) => {
            const ticket = e.target.closest('.ticket-critical, .ticket-priority');
            if (ticket) {
                this.unhighlightTicket(ticket);
            }
        }, true);
    }

    /**
     * Gère l'appel d'un patient critique
     */
    handleCriticalCall(event) {
        const button = event.target.closest('.btn-call-critical');
        
        // Animation du bouton
        button.style.transform = 'scale(0.95)';
        setTimeout(() => {
            button.style.transform = 'scale(1)';
        }, 150);

        // Notification visuelle
        this.showNotification('Patient critique appelé!', 'critical');
        
        // Son d'alerte (si supporté)
        this.playAlertSound('critical');
    }

    /**
     * Gère l'appel d'un patient prioritaire
     */
    handlePriorityCall(event) {
        const button = event.target.closest('.btn-call-priority');
        
        // Animation du bouton
        button.style.transform = 'scale(0.95)';
        setTimeout(() => {
            button.style.transform = 'scale(1)';
        }, 150);

        // Notification visuelle
        this.showNotification('Patient prioritaire appelé!', 'priority');
        
        // Son d'alerte (si supporté)
        this.playAlertSound('priority');
    }

    /**
     * Met en surbrillance un ticket
     */
    highlightTicket(ticket) {
        ticket.style.transform = 'translateY(-3px)';
        ticket.style.zIndex = '10';
    }

    /**
     * Retire la surbrillance d'un ticket
     */
    unhighlightTicket(ticket) {
        ticket.style.transform = 'translateY(0)';
        ticket.style.zIndex = 'auto';
    }

    /**
     * Affiche une notification
     */
    showNotification(message, type) {
        // Créer l'élément de notification
        const notification = document.createElement('div');
        notification.className = `alert alert-dismissible fade show notification-${type}`;
        notification.style.position = 'fixed';
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.zIndex = '9999';
        notification.style.minWidth = '300px';
        
        notification.innerHTML = `
            <strong><i class="fas fa-${type === 'critical' ? 'exclamation-circle' : 'star'} me-2"></i>${message}</strong>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Ajouter au DOM
        document.body.appendChild(notification);

        // Supprimer automatiquement après 3 secondes
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 3000);
    }

    /**
     * Joue un son d'alerte
     */
    playAlertSound(type) {
        try {
            // Créer un contexte audio
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            
            // Fréquences différentes selon le type
            const frequency = type === 'critical' ? 800 : 600;
            const duration = type === 'critical' ? 0.3 : 0.2;
            
            // Créer l'oscillateur
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime);
            oscillator.type = 'sine';
            
            gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + duration);
        } catch (error) {
            console.log('Audio not supported or blocked');
        }
    }

    /**
     * Configure les notifications du navigateur
     */
    setupNotifications() {
        // Demander la permission pour les notifications
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
    }

    /**
     * Envoie une notification du navigateur
     */
    sendBrowserNotification(title, message, type) {
        if ('Notification' in window && Notification.permission === 'granted') {
            const notification = new Notification(title, {
                body: message,
                icon: type === 'critical' ? '/static/images/critical-icon.png' : '/static/images/priority-icon.png',
                badge: '/static/images/clinic-badge.png',
                tag: `emergency-${type}`,
                requireInteraction: type === 'critical'
            });

            // Fermer automatiquement après 5 secondes (sauf pour critique)
            if (type !== 'critical') {
                setTimeout(() => notification.close(), 5000);
            }
        }
    }

    /**
     * Démarre les mises à jour périodiques
     */
    startPeriodicUpdates() {
        // Vérifier les nouveaux tickets d'urgence toutes les 10 secondes
        setInterval(() => {
            this.checkForNewEmergencyTickets();
        }, 10000);

        // Mettre à jour les styles toutes les 30 secondes
        setInterval(() => {
            this.applyEmergencyStyles();
        }, 30000);
    }

    /**
     * Vérifie s'il y a de nouveaux tickets d'urgence
     */
    async checkForNewEmergencyTickets() {
        try {
            const response = await fetch('/api/emergency-tickets-count');
            const data = await response.json();
            
            if (data.critical > this.lastCriticalCount) {
                this.sendBrowserNotification(
                    'PATIENT CRITIQUE!',
                    `${data.critical} patient(s) critique(s) en attente`,
                    'critical'
                );
                this.showNotification(`${data.critical} patient(s) critique(s) en attente!`, 'critical');
            }
            
            if (data.priority > this.lastPriorityCount) {
                this.sendBrowserNotification(
                    'Patients prioritaires',
                    `${data.priority} patient(s) prioritaire(s) en attente`,
                    'priority'
                );
            }
            
            this.lastCriticalCount = data.critical;
            this.lastPriorityCount = data.priority;
        } catch (error) {
            console.log('Could not check for emergency tickets:', error);
        }
    }

    /**
     * Met à jour les compteurs en temps réel
     */
    updateCounters() {
        const criticalCount = document.querySelectorAll('[data-priority="2"]').length;
        const priorityCount = document.querySelectorAll('[data-priority="1"]').length;
        
        // Mettre à jour les badges de comptage
        const criticalBadge = document.querySelector('.critical-count');
        const priorityBadge = document.querySelector('.priority-count');
        
        if (criticalBadge) {
            criticalBadge.textContent = criticalCount;
            criticalBadge.style.display = criticalCount > 0 ? 'inline' : 'none';
        }
        
        if (priorityBadge) {
            priorityBadge.textContent = priorityCount;
            priorityBadge.style.display = priorityCount > 0 ? 'inline' : 'none';
        }
    }
}

// Initialiser le gestionnaire quand le DOM est prêt
document.addEventListener('DOMContentLoaded', () => {
    window.emergencyManager = new EmergencyTicketManager();
});

// Fonctions utilitaires globales
window.EmergencyUtils = {
    /**
     * Marque un ticket comme critique
     */
    markAsCritical: function(ticketElement) {
        ticketElement.setAttribute('data-priority', '2');
        ticketElement.classList.add('ticket-critical');
        window.emergencyManager.addCriticalIndicators(ticketElement);
    },

    /**
     * Marque un ticket comme prioritaire
     */
    markAsPriority: function(ticketElement) {
        ticketElement.setAttribute('data-priority', '1');
        ticketElement.classList.add('ticket-priority');
        window.emergencyManager.addPriorityIndicators(ticketElement);
    },

    /**
     * Calcule le temps d'attente
     */
    calculateWaitingTime: function(createdAt) {
        const now = new Date();
        const created = new Date(createdAt);
        const diffMs = now - created;
        const diffMins = Math.floor(diffMs / 60000);
        
        if (diffMins < 60) {
            return `${diffMins} min`;
        } else {
            const hours = Math.floor(diffMins / 60);
            const minutes = diffMins % 60;
            return `${hours}h ${minutes}min`;
        }
    },

    /**
     * Formate l'heure d'arrivée
     */
    formatArrivalTime: function(dateTime) {
        const date = new Date(dateTime);
        return date.toLocaleTimeString('fr-FR', {
            hour: '2-digit',
            minute: '2-digit'
        });
    }
};