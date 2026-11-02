from repositories.student_repository import StudentRepository
from repositories.payment_repository import PaymentRepository


class StudentService:
    def __init__(self):
        self.students = StudentRepository()
        self.payments = PaymentRepository()

    def _validate(self, last_name, first_name, class_name, school_year, total_fees):
        if not last_name or not last_name.strip():
            raise ValueError("Le nom est obligatoire.")
        if not first_name or not first_name.strip():
            raise ValueError("Le prénom est obligatoire.")
        if not class_name or not class_name.strip():
            raise ValueError("La classe est obligatoire.")
        if not school_year or not school_year.strip():
            raise ValueError("L'année scolaire est obligatoire.")
        if not isinstance(total_fees, int) or total_fees < 0:
            raise ValueError("Le montant total des frais doit être un entier positif.")

    def create(self, last_name, first_name, class_name, school_year, total_fees):
        self._validate(last_name, first_name, class_name, school_year, total_fees)
        return self.students.create(last_name.strip(), first_name.strip(),
                                    class_name.strip(), school_year.strip(), total_fees)

    def update(self, student_id, last_name, first_name, class_name, school_year, total_fees):
        self._validate(last_name, first_name, class_name, school_year, total_fees)
        student = self.students.get_by_id(student_id)
        if not student:
            raise ValueError("Élève introuvable.")
        paid = self.payments.total_paid(student_id)
        if total_fees < paid:
            raise ValueError("Le total dû ne peut pas être inférieur au montant déjà payé.")
        self.students.update(student_id, last_name.strip(), first_name.strip(),
                             class_name.strip(), school_year.strip(), total_fees)

    def delete(self, student_id):
        student = self.students.get_by_id(student_id)
        if not student:
            raise ValueError("Élève introuvable.")
        self.students.delete(student_id)

    def get_by_id(self, student_id):
        return self.students.get_by_id(student_id)

    def list(self, search="", class_filter=None):
        return self.students.get_all(search=search, class_filter=class_filter)

    def classes(self):
        return self.students.get_classes()

    def get_balance(self, student_id):
        student = self.students.get_by_id(student_id)
        if not student:
            raise ValueError("Élève introuvable.")
        paid = self.payments.total_paid(student_id)
        balance = student["total_fees"] - paid
        return {
            "total_fees": student["total_fees"],
            "total_paid": paid,
            "balance": balance,
            "status": self._status(student["total_fees"], paid),
        }

    def _status(self, total_fees, paid):
        if total_fees == 0:
            return "Soldé"
        if paid == 0:
            return "Non payé"
        if paid >= total_fees:
            return "Soldé"
        return "Partiellement payé"