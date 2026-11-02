from datetime import date

from PySide6.QtWidgets import (
    QDialog, QFormLayout, QSpinBox, QDateEdit, QComboBox,
    QDialogButtonBox, QMessageBox, QLabel
)
from PySide6.QtCore import QDate

from services.payment_service import PaymentService, VALID_METHODS


METHOD_LABELS = {
    "especes": "Espèces",
    "cheque": "Chèque",
    "virement": "Virement",
    "mobile_money": "Mobile Money",
}


class PaymentDialog(QDialog):
    def __init__(self, parent=None, student=None, balance=0):
        super().__init__(parent)
        self.student = student
        self.balance = balance
        self.payment_service = PaymentService()
        self.result_data = None

        self.setWindowTitle("Enregistrer un paiement")
        self.setMinimumWidth(420)

        layout = QFormLayout(self)

        layout.addRow(QLabel(
            f"<b>{student['last_name']} {student['first_name']}</b> — "
            f"Classe {student['class_name']}<br>"
            f"Solde restant : <b>{balance:,} FCFA</b>".replace(",", " ")
        ))

        self.amount = QSpinBox()
        self.amount.setMaximum(100_000_000)
        self.amount.setSuffix(" FCFA")
        self.amount.setGroupSeparatorShown(True)
        self.amount.setMaximum(balance)
        self.amount.setValue(min(balance, 0))

        self.payment_date = QDateEdit()
        self.payment_date.setCalendarPopup(True)
        self.payment_date.setDisplayFormat("yyyy-MM-dd")
        self.payment_date.setDate(QDate.currentDate())

        self.method = QComboBox()
        for code in VALID_METHODS:
            self.method.addItem(METHOD_LABELS[code], code)

        layout.addRow("Montant *", self.amount)
        layout.addRow("Date *", self.payment_date)
        layout.addRow("Mode de paiement *", self.method)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._on_ok)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def _on_ok(self):
        amount = self.amount.value()
        if amount <= 0:
            QMessageBox.warning(self, "Erreur", "Le montant doit être supérieur à 0.")
            return
        if amount > self.balance:
            QMessageBox.warning(
                self, "Erreur",
                f"Le montant dépasse le solde restant ({self.balance} FCFA)."
            )
            return
        payment_date = self.payment_date.date().toString("yyyy-MM-dd")
        method = self.method.currentData()
        try:
            self.result_data = self.payment_service.register(
                self.student["id"], amount, payment_date, method
            )
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Erreur", str(e))