import sys
import os

def get_resource_path(relative_path):
    """Retourne le chemin absolu d'une ressource (icône, style, schema.sql)."""
    try:
        # PyInstaller crée un dossier temporaire _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # En développement, on utilise le dossier courant
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_app_dir():
    """Retourne le dossier où se trouve l'exécutable (pour la base de données)."""
    if getattr(sys, 'frozen', False):
        # Si on est dans un .exe, on prend le dossier de l'exe
        return os.path.dirname(sys.executable)
    # Sinon, le dossier courant
    return os.path.abspath(".")