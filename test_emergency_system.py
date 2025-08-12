#!/usr/bin/env python3
"""
Script de test pour le système de tickets d'urgence
Teste les fonctionnalités principales du nouveau système
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clinic_app import create_app, db
from clinic_app.models import Patient, Ticket, User
from datetime import datetime

def test_emergency_system():
    """Test du système de tickets d'urgence"""
    app = create_app()
    
    with app.app_context():
        print("🧪 Test du système de tickets d'urgence")
        print("=" * 50)
        
        # 1. Vérifier qu'il y a des patients
        patient_count = Patient.query.count()
        print(f"📊 Nombre de patients dans la base: {patient_count}")
        
        if patient_count == 0:
            print("❌ Aucun patient trouvé. Création d'un patient de test...")
            test_patient = Patient(
                full_name="Patient Test Urgence",
                phone="0123456789",
                age=35,
                gender="male",
                blood_group="O+",
                address="Adresse de test"
            )
            db.session.add(test_patient)
            db.session.commit()
            print("✅ Patient de test créé")
        
        # 2. Créer des tickets de test avec différentes priorités
        patient = Patient.query.first()
        today = datetime.now().date()
        
        # Supprimer les anciens tickets de test
        Ticket.query.filter(
            db.func.date(Ticket.created_at) == today,
            Ticket.notes.like('%test%')
        ).delete()
        db.session.commit()
        
        # Obtenir le prochain numéro
        last_ticket = Ticket.query.filter(
            db.func.date(Ticket.created_at) == today
        ).order_by(Ticket.number.desc()).first()
        
        next_number = (last_ticket.number + 1) if last_ticket else 1
        
        # Créer ticket critique
        critical_ticket = Ticket(
            patient_id=patient.id,
            number=next_number,
            status="waiting",
            ticket_type="emergency",
            priority=2,
            notes="🚨 Test ticket critique - Urgence médicale",
            created_at=datetime.now()
        )
        db.session.add(critical_ticket)
        
        # Créer ticket prioritaire
        priority_ticket = Ticket(
            patient_id=patient.id,
            number=next_number + 1,
            status="waiting",
            ticket_type="reservation",
            priority=1,
            notes="⭐ Test ticket prioritaire - Rendez-vous",
            created_at=datetime.now()
        )
        db.session.add(priority_ticket)
        
        # Créer ticket normal
        regular_ticket = Ticket(
            patient_id=patient.id,
            number=next_number + 2,
            status="waiting",
            ticket_type="walk_in",
            priority=0,
            notes="📝 Test ticket normal - Sans rendez-vous",
            created_at=datetime.now()
        )
        db.session.add(regular_ticket)
        
        db.session.commit()
        
        print("✅ Tickets de test créés:")
        print(f"   🚨 Critique: N° {next_number}")
        print(f"   ⭐ Prioritaire: N° {next_number + 1}")
        print(f"   📝 Normal: N° {next_number + 2}")
        
        # 3. Vérifier les compteurs
        critical_count = Ticket.query.filter(
            db.func.date(Ticket.created_at) == today,
            Ticket.status == "waiting",
            Ticket.priority == 2
        ).count()
        
        priority_count = Ticket.query.filter(
            db.func.date(Ticket.created_at) == today,
            Ticket.status == "waiting",
            Ticket.priority == 1
        ).count()
        
        regular_count = Ticket.query.filter(
            db.func.date(Ticket.created_at) == today,
            Ticket.status == "waiting",
            Ticket.priority == 0
        ).count()
        
        print("\n📈 Statistiques actuelles:")
        print(f"   🚨 Tickets critiques: {critical_count}")
        print(f"   ⭐ Tickets prioritaires: {priority_count}")
        print(f"   📝 Tickets normaux: {regular_count}")
        print(f"   📊 Total en attente: {critical_count + priority_count + regular_count}")
        
        # 4. Vérifier l'ordre de tri
        waiting_tickets = Ticket.query.filter(
            db.func.date(Ticket.created_at) == today,
            Ticket.status == "waiting"
        ).order_by(
            Ticket.priority.desc(),
            Ticket.number.asc()
        ).all()
        
        print("\n🔄 Ordre de traitement (par priorité):")
        for i, ticket in enumerate(waiting_tickets[:5], 1):
            priority_text = {2: "🚨 CRITIQUE", 1: "⭐ PRIORITAIRE", 0: "📝 NORMAL"}
            print(f"   {i}. N° {ticket.number} - {priority_text.get(ticket.priority, 'INCONNU')}")
        
        # 5. Vérifier les médecins
        doctor_count = User.query.filter_by(role='doctor').count()
        print(f"\n👨‍⚕️ Nombre de médecins: {doctor_count}")
        
        if doctor_count == 0:
            print("⚠️  Aucun médecin trouvé. Créez un compte médecin pour tester l'interface.")
        
        print("\n🎉 Test terminé avec succès!")
        print("\n📋 Instructions pour tester:")
        print("1. Démarrez l'application: python run.py")
        print("2. Connectez-vous en tant que médecin")
        print("3. Visitez le Dashboard pour voir les tickets avec priorités")
        print("4. Allez à 'File d'attente' pour l'interface complète")
        print("5. Utilisez 'Test Urgence' pour créer plus de tickets")
        
        return True

def cleanup_test_data():
    """Nettoie les données de test"""
    app = create_app()
    
    with app.app_context():
        today = datetime.now().date()
        
        # Supprimer les tickets de test
        deleted = Ticket.query.filter(
            db.func.date(Ticket.created_at) == today,
            Ticket.notes.like('%test%')
        ).delete()
        
        db.session.commit()
        print(f"🧹 {deleted} tickets de test supprimés")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test du système de tickets d'urgence")
    parser.add_argument("--cleanup", action="store_true", help="Nettoyer les données de test")
    
    args = parser.parse_args()
    
    if args.cleanup:
        cleanup_test_data()
    else:
        test_emergency_system()