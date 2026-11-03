import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from database.db import init_db
from ui.main_window import MainWindow


def main():
    init_db()
    app = QApplication(sys.argv)
    
    # 1. Chargement du thème QSS
    base_dir = os.path.dirname(os.path.abspath(__file__))
    style_path = os.path.join(base_dir, "assets", "style.qss")
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
            
    # 2. Chargement de l'icône
    icon_path = os.path.join(base_dir, "assets", "icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
            
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()