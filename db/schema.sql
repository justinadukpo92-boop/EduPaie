-- ============================================================
-- EduPaie — Script de création de la base de données
-- SGBD : SQLite 3
-- ============================================================

-- Activer les clés étrangères (obligatoire à chaque connexion SQLite)
PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
-- Table : eleves
-- Stocke les informations d'un élève et le montant total
-- des frais de scolarité qu'il doit pour l'année scolaire.
--
-- Suppression douce : la colonne "actif" permet de masquer
-- un élève sans supprimer son historique de paiements.
--   actif = 1  -> élève visible
--   actif = 0  -> élève supprimé (masqué mais conservé)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS eleves (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    nom               TEXT    NOT NULL,
    prenom            TEXT    NOT NULL,
    sexe              TEXT    NOT NULL CHECK (sexe IN ('M', 'F')),
    classe            TEXT    NOT NULL,
    annee_scolaire    TEXT    NOT NULL,
    montant_total_du  REAL    NOT NULL CHECK (montant_total_du >= 0),
    actif             INTEGER NOT NULL DEFAULT 1 CHECK (actif IN (0, 1)),
    created_at        TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index pour accélérer les recherches/filtres
CREATE INDEX IF NOT EXISTS idx_eleves_classe ON eleves(classe);
CREATE INDEX IF NOT EXISTS idx_eleves_annee  ON eleves(annee_scolaire);
CREATE INDEX IF NOT EXISTS idx_eleves_actif  ON eleves(actif);

-- ------------------------------------------------------------
-- Table : paiements
-- Enregistre chaque versement effectué par un élève.
-- Le numéro de reçu est unique (contrainte d'intégrité).
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS paiements (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    eleve_id        INTEGER NOT NULL,
    montant         REAL    NOT NULL CHECK (montant > 0),
    date_paiement   TEXT    NOT NULL,
    mode_paiement   TEXT    NOT NULL CHECK (mode_paiement IN ('Espèces', 'Chèque', 'Virement', 'Mobile Money')),
    numero_recu     TEXT    NOT NULL UNIQUE,
    solde_apres     REAL    NOT NULL CHECK (solde_apres >= 0),
    created_at      TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (eleve_id) REFERENCES eleves(id) ON DELETE CASCADE
);

-- Index pour accélérer l'historique d'un élève et les stats par date
CREATE INDEX IF NOT EXISTS idx_paiements_eleve ON paiements(eleve_id);
CREATE INDEX IF NOT EXISTS idx_paiements_date  ON paiements(date_paiement);