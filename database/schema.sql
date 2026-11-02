-- EduPaie - Schéma de base de données SQLite
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS students (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name       TEXT    NOT NULL,
    first_name      TEXT    NOT NULL,
    class_name      TEXT    NOT NULL,
    school_year     TEXT    NOT NULL,
    total_fees      INTEGER NOT NULL CHECK (total_fees >= 0),
    created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS payments (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id      INTEGER NOT NULL,
    amount          INTEGER NOT NULL CHECK (amount > 0),
    payment_date    TEXT    NOT NULL,
    payment_method  TEXT    NOT NULL CHECK (payment_method IN ('especes','cheque','virement','mobile_money')),
    created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS receipts (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_number      TEXT    NOT NULL UNIQUE,
    payment_id          INTEGER NOT NULL UNIQUE,
    student_id          INTEGER NOT NULL,
    student_full_name   TEXT    NOT NULL,
    student_class       TEXT    NOT NULL,
    amount              INTEGER NOT NULL,
    payment_date        TEXT    NOT NULL,
    payment_method      TEXT    NOT NULL,
    balance_after       INTEGER NOT NULL,
    issued_at           TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (payment_id) REFERENCES payments(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_students_class ON students(class_name);
CREATE INDEX IF NOT EXISTS idx_payments_student ON payments(student_id);
CREATE INDEX IF NOT EXISTS idx_payments_date ON payments(payment_date);
CREATE INDEX IF NOT EXISTS idx_receipts_student ON receipts(student_id);