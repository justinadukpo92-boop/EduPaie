import sqlite3
from pathlib import Path
from utils.paths import get_resource_path, get_app_dir


def get_db_path() -> Path:
    # La base de données sera TOUJOURS à côté de l'exécutable (pour qu'elle sauvegarde les données)
    return Path(get_app_dir()) / "school.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    # Le schema.sql est embarqué DANS l'exécutable (ressource)
    schema_file = get_resource_path("database/schema.sql")
    with open(schema_file, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    with get_connection() as conn:
        conn.executescript(schema_sql)
        conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('school_name', 'COMPLEXE SCOLAIRE EDUPAIE')")
        conn.commit()