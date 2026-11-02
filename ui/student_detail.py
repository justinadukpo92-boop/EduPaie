from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QHBoxLayout, QAbstractItemView, QMessageBox
)


METHOD_LABELS = {
    "especes": "Espèces",
    "cheque": "Chèque",
    "virement": "Virement",
    "mobile_money": "Mobile Money",
}


class StudentDetail(QDialog):
    def __init__(self, parent=None, student_id=None):
        super().__init__(parent)
        self.student_id = student_id
        self.setWindowTitle("Fiche élève")
        self.resize(750, 520)

        from services.student_service import StudentService
        from services.payment_service import PaymentService
        from services.receipt_service import ReceiptService

        self.student_service = StudentService()
        self.payment_service = PaymentService()
        self.receipt_service = ReceiptService()

        self.layout_ = QVBoxLayout(self)
        self.info_label = QLabel()
        self.layout_.addWidget(self.info_label)

        self.layout_.addWidget(QLabel("<h3>Historique des paiements</h3>"))

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["Date", "Montant", "Mode", "N° reçu", "Solde après"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.layout_.addWidget(self.table)

        buttons = QHBoxLayout()
        self.btn_pay = QPushButton("Enregistrer un paiement")
        self.btn_pay.clicked.connect(self.register_payment)
        btn_close = QPushButton("Fermer")
        btn_close.clicked.connect(self.accept)
        buttons.addWidget(self.btn_pay)
        buttons.addStretch()
        buttons.addWidget(btn_close)
        self.layout_.addLayout(buttons)

        self.load_data()

    def load_data(self):
        student = self.student_service.get_by_id(self.student_id)
        if not student:
            QMessageBox.warning(self, "Erreur", "Élève introuvable.")
            self.reject()
            return
        info = self.student_service.get_balance(self.student_id)

        self.info_label.setText(
            (f"<h2>{student['last_name']} {student['first_name']}</h2>"
             f"<p>Classe : <b>{student['class_name']}</b> — Année : {student['school_year']}</p>"
             f"<p>Total dû : <b>{student['total_fees']:,} FCFA</b></p>"
             f"<p>Déjà payé : <b>{info['total_paid']:,} FCFA</b></p>"
             f"<p>Solde restant : <b>{info['balance']:,} FCFA</b> — Statut : <b>{info['status']}</b></p>")
            .replace(",", " ")
        )

        self.table.setRowCount(0)
        receipts_by_payment = {
            r["payment_id"]: r for r in self.receipt_service.list_for_student(self.student_id)
        }
        for p in self.payment_service.history(self.student_id):
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(p["payment_date"]))
            self.table.setItem(row, 1, QTableWidgetItem(f"{p['amount']:,} FCFA".replace(",", " ")))
            self.table.setItem(row, 2, QTableWidgetItem(METHOD_LABELS.get(p["payment_method"], p["payment_method"])))
            r = receipts_by_payment.get(p["id"])
            self.table.setItem(row, 3, QTableWidgetItem(r["receipt_number"] if r else "—"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{r['balance_after']:,} FCFA".replace(",", " ") if r else "—"))

        # Désactiver le bouton si l'élève est soldé
        self.btn_pay.setEnabled(info["balance"] > 0)

    def register_payment(self):
        from ui.payment_dialog import PaymentDialog
        student = self.student_service.get_by_id(self.student_id)
        info = self.student_service.get_balance(self.student_id)
        dialog = PaymentDialog(self, student=student, balance=info["balance"])
        if dialog.exec() and dialog.result_data:
            self.load_data()
            data = dialog.result_data
            QMessageBox.information(
                self, "Paiement enregistré",
                f"Reçu n° {data['receipt_number']}\nSolde restant : {data['balance_after']} FCFA"
            )