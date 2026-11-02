from repositories.receipt_repository import ReceiptRepository


class ReceiptService:
    def __init__(self):
        self.receipts = ReceiptRepository()

    def get_by_id(self, receipt_id):
        return self.receipts.get_by_id(receipt_id)

    def get_by_payment(self, payment_id):
        return self.receipts.get_by_payment(payment_id)

    def list_for_student(self, student_id):
        return self.receipts.get_by_student(student_id)