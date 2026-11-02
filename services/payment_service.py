from datetime import datetime

from repositories.payment_repository import PaymentRepository
from repositories.student_repository import StudentRepository
from repositories.receipt_repository import ReceiptRepository


VALID_METHODS = ("especes", "cheque", "virement", "mobile_money")


class PaymentService:
    def __init__(self):
        self.payments = PaymentRepository()
        self.students = StudentRepository()
        self.receipts = ReceiptRepository()

    def _validate(self, student_id, amount, payment_date, payment_method):
        student = self.students.get_by_id(student_id)
        if not student:
            raise ValueError("Élève introuvable.")
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Le montant doit être un entier strictement positif.")
        try:
            datetime.strptime(payment_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La date doit être au format AAAA-MM-JJ.")
        if payment_method not in VALID_METHODS:
            raise ValueError("Mode de paiement invalide.")
        paid = self.payments.total_paid(student_id)
        balance = student["total_fees"] - paid
               if amount > balance:
            raise ValueError(
                f"Le montant dépasse le solde restant ({balance} FCFA)."
            )
        return student, balance

    def register(self, student_id, amount, payment_date, payment_method):
        student, balance_before = self._validate(
            student_id, amount, payment_date, payment_method
        )
        payment_id = self.payments.create(
            student_id, amount, payment_date, payment_method
        )
        balance_after = balance_before - amount

        receipt_number = self._next_receipt_number()
        full_name = f"{student['last_name']} {student['first_name']}"
        self.receipts.create(
            receipt_number=receipt_number,
            payment_id=payment_id,
            student_id=student_id,
            student_full_name=full_name,
            student_class=student["class_name"],
            amount=amount,
            payment_date=payment_date,
            payment_method=payment_method,
            balance_after=balance_after,
        )
        return {
            "payment_id": payment_id,
            "receipt_number": receipt_number,
            "balance_after": balance_after,
        }

    def _next_receipt_number(self):
        year = datetime.now().year
        count = self.receipts.count_all() + 1
        return f"REC-{year}-{count:06d}"

    def history(self, student_id):
        return self.payments.get_by_student(student_id)