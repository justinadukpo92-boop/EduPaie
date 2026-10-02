"""
EduPaie — Initialisation de la base de données SQLite.

Ce script :
  1. Supprime l'ancienne base si elle existe.
  2. Crée une nouvelle base à partir de db/schema.sql.
  3. Insère le jeu de données de test à partir de db/seed.sql.
  4. Affiche un récapitulatif (nb d'élèves, nb de paiements).

Utilisation :
    python data/init_db.py
"""

import sqlite3
import sys
from pathlib import Path


# ------------------------------------------------------------
# Chemins
# ------------------------------------------------------------
# __file__  = .../EduPaie/data/init_db.py
# BASE_DIR  = .../EduPaie
BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "db"
SCHEMA_FILE = DB_DIR / "schema.sql"
SEED_FILE = DB_DIR / "seed.sql"
DB_FILE = DB_DIR / "edupaie.db"


def executer_script_sql(curseur: sqlite3.Cursor, chemin: Path) -> None:
    """Lit un fichier .sql et exécute son contenu (plusieurs instructions)."""
    if not chemin.exists():
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")

    sql = chemin.read_text(encoding="utf-8")
    curseur.executescript(sql)


def initialiser_base() -> None:
    """Crée la base edupaie.db et la remplit avec le jeu de test."""

    # 1) Supprimer l'ancienne base si elle existe
    if DB_FILE.exists():
        DB_FILE.unlink()
        print(f"[init] Ancienne base supprimée : {DB_FILE.name}")

    # 2) Se connecter (crée le fichier automatiquement)
    connexion = sqlite3.connect(DB_FILE)
    # 3) Activer les clés étrangères
    connexion.execute("PRAGMA foreign_keys = ON;")
    curseur = connexion.cursor()

    try:
        # 4) Exécuter le schéma
        print(f"[init] Exécution de {SCHEMA_FILE.name}...")
        executer_script_sql(curseur, SCHEMA_FILE)

        # 5) Exécuter le seed
        print(f"[init] Exécution de {SEED_FILE.name}...")
        executer_script_sql(curseur, SEED_FILE)

        # 6) Commit
        connexion.commit()
        print("[init] Base créée et remplie avec succès.")

        # 7) Récapitulatif
        nb_eleves = curseur.execute("SELECT COUNT(*) FROM eleves").fetchone()[0]
        nb_paiements = curseur.execute("SELECT COUNT(*) FROM paiements").fetchone()[0]
        total_encaisse = curseur.execute(
            "SELECT COALESCE(SUM(montant), 0) FROM paiements"
        ).fetchone()[0]

        print("-" * 50)
        print(f"  Élèves en base       : {nb_eleves}")
        print(f"  Paiements enregistrés: {nb_paiements}")
        print(f"  Total encaissé       : {total_encaisse:,.0f} FCFA")
        print(f"  Fichier              : {DB_FILE}")
        print("-" * 50)

    except Exception as exc:
        connexion.rollback()
        print(f"[erreur] {exc}", file=sys.stderr)
        raise
    finally:
        connexion.close()


if __name__ == "__main__":
    initialiser_base()