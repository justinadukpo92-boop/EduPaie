from database.db import get_connection


class PaymentRepository:
    def create(self, student_id, amount, payment_date, payment_method):
        with get_connection() as conn:
            cur = conn.execute(
                """INSERT INTO payments (student_id, amount, payment_date, payment_method)
                   VALUES (?, ?, ?, ?)""",
                (student_id, amount, payment_date, payment_method),
            )
            conn.commit()
            return cur.lastrowid

    def get_by_id(self, payment_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM payments WHERE id=?", (payment_id,)).fetchone()
            return dict(row) if row else None

    def get_by_student(self, student_id):
        with get_connection() as conn:
            rows = conn.execute(
                """SELECT p.*, r.receipt_number
                   FROM payments p
                   LEFT JOIN receipts r ON r.payment_id = p.id
                   WHERE p.student_id=?
                   ORDER BY p.payment_date DESC, p.id DESC""",
                (student_id,),
            ).fetchall()
            return [dict(r) for r in rows]

    def total_paid(self, student_id):
        with get_connection() as conn:
            row = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) AS total FROM payments WHERE student_id=?",
                (student_id,),
            ).fetchone()
            return row["total"]

    def delete(self, payment_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM payments WHERE id=?", (payment_id,))
            conn.commit()

    def total_collected(self):
        with get_connection() as conn:
            row = conn.execute("SELECT COALESCE(SUM(amount), 0) AS total FROM payments").fetchone()
            return row["total"]