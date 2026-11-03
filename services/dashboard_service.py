from repositories.student_repository import StudentRepository
from repositories.payment_repository import PaymentRepository


class DashboardService:
    def __init__(self):
        self.students = StudentRepository()
        self.payments = PaymentRepository()

    def get_stats(self):
        all_students = self.students.get_all()
        total_students = len(all_students)
        total_collected = self.payments.total_collected()
        
        total_due = sum(s["total_fees"] for s in all_students)
        total_remaining = total_due - total_collected
        
        unpaid_count = 0
        for s in all_students:
            paid = self.payments.total_paid(s["id"])
            if paid < s["total_fees"]:
                unpaid_count += 1

        return {
            "total_students": total_students,
            "total_collected": total_collected,
            "total_remaining": total_remaining,
            "unpaid_count": unpaid_count
        }