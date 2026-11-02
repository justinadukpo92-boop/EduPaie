from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QSpinBox, QDialogButtonBox, QMessageBox
)


class StudentForm(QDialog):
    def __init__(self, parent=None, student=None):
        super().__init__(parent)
        self.student = student
        self.setWindowTitle("Modifier un élève" if student else "Ajouter un élève")
        self.setMinimumWidth(400)

        layout = QFormLayout(self)

        self.last_name = QLineEdit()
        self.first_name = QLineEdit()
        self.class_name = QLineEdit()
        self.school_year = QLineEdit()
        self.total_fees = QSpinBox()
        self.total_fees.setMaximum(100_000_000)
        self.total_fees.setSuffix(" FCFA")
        self.total_fees.setGroupSeparatorShown(True)

        layout.addRow("Nom *", self.last_name)
        layout.addRow("Prénom *", self.first_name)
        layout.addRow("Classe *", self.class_name)
        layout.addRow("Année scolaire *", self.school_year)
        layout.addRow("Total dû (FCFA) *", self.total_fees)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self._on_ok)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

        if student:
            self.last_name.setText(student["last_name"])
            self.first_name.setText(student["first_name"])
            self.class_name.setText(student["class_name"])
            self.school_year.setText(student["school_year"])
            self.total_fees.setValue(student["total_fees"])

    def _on_ok(self):
        if not self.last_name.text().strip():
            QMessageBox.warning(self, "Champ requis", "Le nom est obligatoire.")
            return
        if not self.first_name.text().strip():
            QMessageBox.warning(self, "Champ requis", "Le prénom est obligatoire.")
            return
        if not self.class_name.text().strip():
            QMessageBox.warning(self, "Champ requis", "La classe est obligatoire.")
            return
        if not self.school_year.text().strip():
            QMessageBox.warning(self, "Champ requis", "L'année scolaire est obligatoire.")
            return
        self.accept()

    def get_data(self):
        return {
            "last_name": self.last_name.text().strip(),
            "first_name": self.first_name.text().strip(),
            "class_name": self.class_name.text().strip(),
            "school_year": self.school_year.text().strip(),
            "total_fees": self.total_fees.value(),
        }