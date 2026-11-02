import os
import sqlite3
from pathlib import Path


def get_db_path() -> Path:
    """Retourne le chemin de la base .db, à côté de l'exécutable ou du projet."""
    base_dir = Path(__file__).resolve().parent.parent
    return base_dir / "school.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    """Crée les tables si elles n'existent pas, à partir de schema.sql."""
    schema_file = Path(__file__).resolve().parent / "schema.sql"
    with open(schema_file, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    with get_connection() as conn:
        conn.executescript(schema_sql)
        conn.commit()