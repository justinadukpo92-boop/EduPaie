from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView,
    QAbstractItemView, QTabWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from services.student_service import StudentService
from ui.student_form import StudentForm
from ui.student_detail import StudentDetail
from ui.dashboard import Dashboard
from ui.settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EduPaie — Gestion des frais scolaires")
        self.resize(1000, 650)
        self.setWindowIcon(QIcon("assets/icon.ico"))

        self.student_service = StudentService()

        # Création du système d'onglets
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # ================= Onglet 1 : Élèves =================
        self.tab_students = QWidget()
        layout_students = QVBoxLayout(self.tab_students)

        # Barre d'outils
        toolbar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher un élève (nom ou prénom)…")
        self.search_input.textChanged.connect(self.refresh)

        self.class_filter = QComboBox()
        self.class_filter.addItem("Toutes les classes", None)
        self.class_filter.currentIndexChanged.connect(self.refresh)

        btn_add = QPushButton("Ajouter un élève")
        btn_add.clicked.connect(self.add_student)

        btn_edit = QPushButton("Modifier")
        btn_edit.clicked.connect(self.edit_student)

        btn_delete = QPushButton("Supprimer")
        btn_delete.clicked.connect(self.delete_student)

        btn_detail = QPushButton("Fiche élève")
        btn_detail.clicked.connect(self.open_detail)

        btn_settings = QPushButton("Paramètres")
        btn_settings.clicked.connect(self.open_settings)

        toolbar.addWidget(self.search_input, 2)
        toolbar.addWidget(self.class_filter, 1)
        toolbar.addWidget(btn_add)
        toolbar.addWidget(btn_edit)
        toolbar.addWidget(btn_delete)
        toolbar.addWidget(btn_detail)
        toolbar.addWidget(btn_settings)

        layout_students.addLayout(toolbar)

        # Tableau des élèves
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["Nom", "Prénom", "Classe", "Année", "Total dû", "Statut"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.doubleClicked.connect(self.open_detail)
        layout_students.addWidget(self.table)

        # ================= Onglet 2 : Tableau de bord =================
        self.tab_dashboard = Dashboard()
        
        # Ajout des onglets
        self.tabs.addTab(self.tab_students, "Gestion des élèves")
        self.tabs.addTab(self.tab_dashboard, "Tableau de bord")
        
        # Mettre à jour le dashboard quand on change d'onglet
        self.tabs.currentChanged.connect(self.on_tab_changed)

        self.load_classes()
        self.refresh()

    def on_tab_changed(self, index):
        if self.tabs.widget(index) == self.tab_dashboard:
            self.tab_dashboard.load_data()

    def load_classes(self):
        current = self.class_filter.currentData()
        self.class_filter.blockSignals(True)
        self.class_filter.clear()
        self.class_filter.addItem("Toutes les classes", None)
        for c in self.student_service.classes():
            self.class_filter.addItem(c, c)
        idx = self.class_filter.findData(current)
        if idx >= 0:
            self.class_filter.setCurrentIndex(idx)
        self.class_filter.blockSignals(False)

    def refresh(self):
        search = self.search_input.text().strip()
        class_filter = self.class_filter.currentData()
        students = self.student_service.list(search=search, class_filter=class_filter)

        self.table.setRowCount(0)
        for s in students:
            info = self.student_service.get_balance(s["id"])
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(s["last_name"]))
            self.table.setItem(row, 1, QTableWidgetItem(s["first_name"]))
            self.table.setItem(row, 2, QTableWidgetItem(s["class_name"]))
            self.table.setItem(row, 3, QTableWidgetItem(s["school_year"]))
            self.table.setItem(row, 4, QTableWidgetItem(f"{s['total_fees']:,} FCFA".replace(",", " ")))
            item_status = QTableWidgetItem(info["status"])
            item_status.setData(Qt.UserRole, s["id"])
            self.table.setItem(row, 5, item_status)

    def _selected_student_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 5)
        return item.data(Qt.UserRole) if item else None

    def add_student(self):
        dialog = StudentForm(self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.student_service.create(**data)
                self.load_classes()
                self.refresh()
                QMessageBox.information(self, "Succès", "Élève ajouté.")
            except ValueError as e:
                QMessageBox.warning(self, "Erreur", str(e))

    def edit_student(self):
        sid = self._selected_student_id()
        if sid is None:
            QMessageBox.information(self, "Sélection", "Sélectionnez un élève.")
            return
        student = self.student_service.get_by_id(sid)
        dialog = StudentForm(self, student=student)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.student_service.update(sid, **data)
                self.load_classes()
                self.refresh()
                QMessageBox.information(self, "Succès", "Élève modifié.")
            except ValueError as e:
                QMessageBox.warning(self, "Erreur", str(e))

    def delete_student(self):
        sid = self._selected_student_id()
        if sid is None:
            QMessageBox.information(self, "Sélection", "Sélectionnez un élève.")
            return
        confirm = QMessageBox.question(
            self, "Confirmation",
            "Supprimer cet élève et tous ses paiements ?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            try:
                self.student_service.delete(sid)
                self.load_classes()
                self.refresh()
                QMessageBox.information(self, "Succès", "Élève supprimé.")
            except ValueError as e:
                QMessageBox.warning(self, "Erreur", str(e))

    def open_detail(self):
        sid = self._selected_student_id()
        if sid is None:
            QMessageBox.information(self, "Sélection", "Sélectionnez un élève.")
            return
        dialog = StudentDetail(self, student_id=sid)
        dialog.exec()
        self.refresh()

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()