import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from database.db import init_db
from ui.main_window import MainWindow
from utils.paths import get_resource_path


def main():
    init_db()
    app = QApplication(sys.argv)
    
    # Chargement du thème QSS
    style_path = get_resource_path("assets/style.qss")
    with open(style_path, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())
            
    # Chargement de l'icône
    icon_path = get_resource_path("assets/icon.ico")
    app.setWindowIcon(QIcon(icon_path))
            
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()