from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox
)
from services.settings_service import SettingsService


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Paramètres de l'établissement")
        self.setMinimumWidth(400)
        self.settings_service = SettingsService()

        layout = QFormLayout(self)

        self.school_name = QLineEdit()
        self.school_name.setText(self.settings_service.get_school_name())

        layout.addRow("Nom de l'école :", self.school_name)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def save(self):
        try:
            self.settings_service.set_school_name(self.school_name.text())
            QMessageBox.information(self, "Succès", "Paramètres enregistrés.")
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Erreur", str(e))