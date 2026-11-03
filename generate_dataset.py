from database.db import get_db_path, init_db
from services.student_service import StudentService
from services.payment_service import PaymentService


def generate_dataset():
    # On supprime l'ancienne base pour repartir de zéro proprement
    db_path = get_db_path()
    if db_path.exists():
        db_path.unlink()

    init_db()
    student_svc = StudentService()
    payment_svc = PaymentService()

    # Format : (Nom, Prénom, Classe, Année, Total dû, Montant payé)
    students = [
        # --- SOLDÉS (Payeront tout) ---
        ("ALAO", "Marie", "6e A", "2025-2026", 150000, 150000),
        ("BENIN", "Paul", "6e A", "2025-2026", 150000, 150000),
        ("CODJIA", "Alice", "5e B", "2025-2026", 160000, 160000),
        ("DOSSOU", "Luc", "5e B", "2025-2026", 160000, 160000),
        
        # --- PARTIELS (Payeront une partie) ---
        ("EDOH", "Sarah", "4e C", "2025-2026", 180000, 100000),
        ("FAGLA", "Jean", "4e C", "2025-2026", 180000, 50000),
        ("GBAGUIDI", "Estelle", "3e D", "2025-2026", 200000, 120000),
        ("HOUNKPE", "David", "3e D", "2025-2026", 200000, 150000),
        
        # --- NON PAYÉS (Ne payeront rien) ---
        ("IDRISSOU", "Fatima", "2nde", "2025-2026", 250000, 0),
        ("JOHNSON", "Kevin", "2nde", "2025-2026", 250000, 0),
        ("KOFFI", "Emma", "1ere", "2025-2026", 300000, 0),
        ("LAWSON", "Marc", "1ere", "2025-2026", 300000, 0),
        ("MENSAH", "Chantal", "Tle", "2025-2026", 350000, 0),
        ("NOUMEDEM", "Yves", "Tle", "2025-2026", 350000, 0),
        ("OKOU", "Rita", "Tle", "2025-2026", 350000, 0),
    ]

    for nom, prenom, classe, annee, total, paye in students:
        sid = student_svc.create(nom, prenom, classe, annee, total)
        
        if paye > 0:
            if paye == total:
                # Paiement en une seule fois
                payment_svc.register(sid, paye, "2025-09-15", "especes")
            else:
                # Paiement en deux fois pour créer un historique varié
                moitie = paye // 2
                payment_svc.register(sid, moitie, "2025-09-10", "cheque")
                payment_svc.register(sid, paye - moitie, "2025-10-20", "mobile_money")

    print("Jeu de données de test généré avec succès : 15 élèves.")


if __name__ == "__main__":
    generate_dataset()