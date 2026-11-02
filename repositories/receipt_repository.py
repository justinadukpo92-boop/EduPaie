from database.db import get_connection


class ReceiptRepository:
    def create(self, receipt_number, payment_id, student_id, student_full_name,
               student_class, amount, payment_date, payment_method, balance_after):
        with get_connection() as conn:
            cur = conn.execute(
                """INSERT INTO receipts
                   (receipt_number, payment_id, student_id, student_full_name,
                    student_class, amount, payment_date, payment_method, balance_after)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (receipt_number, payment_id, student_id, student_full_name,
                 student_class, amount, payment_date, payment_method, balance_after),
            )
            conn.commit()
            return cur.lastrowid

    def get_by_id(self, receipt_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM receipts WHERE id=?", (receipt_id,)).fetchone()
            return dict(row) if row else None

    def get_by_payment(self, payment_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM receipts WHERE payment_id=?", (payment_id,)).fetchone()
            return dict(row) if row else None

    def get_by_student(self, student_id):
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM receipts WHERE student_id=? ORDER BY issued_at DESC",
                (student_id,),
            ).fetchall()
            return [dict(r) for r in rows]

    def count_all(self):
        with get_connection() as conn:
            row = conn.execute("SELECT COUNT(*) AS n FROM receipts").fetchone()
            return row["n"]