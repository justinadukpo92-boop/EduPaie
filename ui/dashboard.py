from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QAbstractItemView, QWidget
)
from PySide6.QtCore import Qt

from services.dashboard_service import DashboardService
from services.student_service import StudentService


class Dashboard(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tableau de bord")
        self.resize(900, 600)

        self.dashboard_service = DashboardService()
        self.student_service = StudentService()

        layout = QVBoxLayout(self)

        # Cartes de statistiques
        stats_layout = QHBoxLayout()
        
        self.card_students = self._create_card("Total Élèves", "0")
        self.card_collected = self._create_card("Total Encaissé", "0 FCFA")
        self.card_remaining = self._create_card("Restant dû", "0 FCFA")
        self.card_unpaid = self._create_card("Élèves non soldés", "0")

        stats_layout.addWidget(self.card_students)
        stats_layout.addWidget(self.card_collected)
        stats_layout.addWidget(self.card_remaining)
        stats_layout.addWidget(self.card_unpaid)

        layout.addLayout(stats_layout)

        # Tableau des élèves non soldés
        layout.addWidget(QLabel("<h3>Élèves avec un solde restant</h3>"))
        
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["Nom", "Prénom", "Classe", "Total dû", "Solde restant"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.table)

        buttons = QHBoxLayout()
        btn_close = QPushButton("Fermer")
        btn_close.clicked.connect(self.accept)
        buttons.addStretch()
        buttons.addWidget(btn_close)
        layout.addLayout(buttons)

        self.load_data()

    def _create_card(self, title, value):
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border-radius: 8px;
                padding: 10px;
            }
            QLabel {
                color: #ffffff;
            }
        """)
        card_layout = QVBoxLayout(widget)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-size: 12px; color: #aaaaaa;")
        
        lbl_value = QLabel(value)
        lbl_value.setStyleSheet("font-size: 20px; font-weight: bold;")
        lbl_value.setAlignment(Qt.AlignCenter)
        widget.value_label = lbl_value

        card_layout.addWidget(lbl_title)
        card_layout.addWidget(lbl_value)
        return widget

    def load_data(self):
        stats = self.dashboard_service.get_stats()

        # Mise à jour des cartes
        self.card_students.value_label.setText(str(stats["total_students"]))
        self.card_collected.value_label.setText(f"{stats['total_collected']:,} FCFA".replace(",", " "))
        self.card_remaining.value_label.setText(f"{stats['total_remaining']:,} FCFA".replace(",", " "))
        self.card_unpaid.value_label.setText(str(stats["unpaid_count"]))

        # Mise à jour du tableau
        self.table.setRowCount(0)
        students = self.student_service.list()
        
        for s in students:
            info = self.student_service.get_balance(s["id"])
            if info["balance"] > 0:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(s["last_name"]))
                self.table.setItem(row, 1, QTableWidgetItem(s["first_name"]))
                self.table.setItem(row, 2, QTableWidgetItem(s["class_name"]))
                self.table.setItem(row, 3, QTableWidgetItem(f"{s['total_fees']:,} FCFA".replace(",", " ")))
                self.table.setItem(row, 4, QTableWidgetItem(f"{info['balance']:,} FCFA".replace(",", " ")))