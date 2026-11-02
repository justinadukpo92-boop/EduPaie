from database.db import get_connection


class StudentRepository:
    def create(self, last_name, first_name, class_name, school_year, total_fees):
        with get_connection() as conn:
            cur = conn.execute(
                """INSERT INTO students (last_name, first_name, class_name, school_year, total_fees)
                   VALUES (?, ?, ?, ?, ?)""",
                (last_name, first_name, class_name, school_year, total_fees),
            )
            conn.commit()
            return cur.lastrowid

    def update(self, student_id, last_name, first_name, class_name, school_year, total_fees):
        with get_connection() as conn:
            conn.execute(
                """UPDATE students
                   SET last_name=?, first_name=?, class_name=?, school_year=?, total_fees=?
                   WHERE id=?""",
                (last_name, first_name, class_name, school_year, total_fees, student_id),
            )
            conn.commit()

    def delete(self, student_id):
        with get_connection() as conn:
            conn.execute("DELETE FROM students WHERE id=?", (student_id,))
            conn.commit()

    def get_by_id(self, student_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
            return dict(row) if row else None

    def get_all(self, search="", class_filter=None):
        query = "SELECT * FROM students WHERE 1=1"
        params = []
        if search:
            query += " AND (last_name LIKE ? OR first_name LIKE ?)"
            params += [f"%{search}%", f"%{search}%"]
        if class_filter:
            query += " AND class_name=?"
            params.append(class_filter)
        query += " ORDER BY last_name, first_name"
        with get_connection() as conn:
            return [dict(r) for r in conn.execute(query, params).fetchall()]

    def get_classes(self):
        with get_connection() as conn:
            rows = conn.execute("SELECT DISTINCT class_name FROM students ORDER BY class_name").fetchall()
            return [r["class_name"] for r in rows]