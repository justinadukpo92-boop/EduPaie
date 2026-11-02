from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QHBoxLayout, QAbstractItemView
)


class StudentDetail(QDialog):
    def __init__(self, parent=None, student_id=None):
        super().__init__(parent)
        self.student_id = student_id
        self.setWindowTitle("Fiche élève")
        self.resize(700, 500)

        from services.student_service import StudentService
        from services.payment_service import PaymentService
        self.student_service = StudentService()
        self.payment_service = PaymentService()

        student = self.student_service.get_by_id(student_id)
        info = self.student_service.get_balance(student_id)

        layout = QVBoxLayout(self)

        self.title = QLabel(
            f"<h2>{student['last_name']} {student['first_name']}</h2>"
            f"<p>Classe : <b>{student['class_name']}</b> — Année : {student['school_year']}</p>"
            f"<p>Total dû : <b>{student['total_fees']:,} FCFA</b></p>"
            f"<p>Déjà payé : <b>{info['total_paid']:,} FCFA</b></p>"
            f"<p>Solde restant : <b>{info['balance']:,} FCFA</b> — Statut : <b>{info['status']}</b></p>"
            .replace(",", " ")
        )
        layout.addWidget(self.title)

        layout.addWidget(QLabel("<h3>Historique des paiements</h3>"))

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["Date", "Montant", "Mode", "N° reçu", "Solde après"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.table)

        from services.receipt_service import ReceiptService
        self.receipt_service = ReceiptService()

        receipts_by_payment = {
            r["payment_id"]: r for r in self.receipt_service.list_for_student(student_id)
        }

        METHOD_LABELS = {
            "especes": "Espèces",
            "cheque": "Chèque",
            "virement": "Virement",
            "mobile_money": "Mobile Money",
        }

        history = self.payment_service.history(student_id)
        for p in history:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(p["payment_date"]))
            self.table.setItem(row, 1, QTableWidgetItem(f"{p['amount']:,} FCFA".replace(",", " ")))
            self.table.setItem(row, 2, QTableWidgetItem(METHOD_LABELS.get(p["payment_method"], p["payment_method"])))
            r = receipts_by_payment.get(p["id"])
            self.table.setItem(row, 3, QTableWidgetItem(r["receipt_number"] if r else "—"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{r['balance_after']:,} FCFA".replace(",", " ") if r else "—"))

        buttons = QHBoxLayout()
        btn_close = QPushButton("Fermer")
        btn_close.clicked.connect(self.accept)
        buttons.addStretch()
        buttons.addWidget(btn_close)
        layout.addLayout(buttons)