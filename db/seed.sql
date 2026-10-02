-- ============================================================
-- EduPaie — Jeu de données de test (seed)
-- 15 élèves + historique de paiements variés
-- À exécuter APRÈS schema.sql
-- ============================================================

PRAGMA foreign_keys = ON;

-- Nettoyage (permet de relancer le seed sans doublons)
DELETE FROM paiements;
DELETE FROM eleves;
DELETE FROM sqlite_sequence WHERE name IN ('eleves', 'paiements');

-- ------------------------------------------------------------
-- 15 ÉLÈVES
-- ------------------------------------------------------------
INSERT INTO eleves (id, nom, prenom, sexe, classe, annee_scolaire, montant_total_du, actif) VALUES
( 1, 'ADUKPO',    'Justin',     'M', '6ème A', '2025-2026', 150000, 1),
( 2, 'DIALLO',    'Aïcha',      'F', '5ème B', '2025-2026', 120000, 1),
( 3, 'KOFFI',     'Yao',        'M', '4ème A', '2025-2026', 180000, 1),
( 4, 'TRAORÉ',    'Fatou',      'F', '3ème B', '2025-2026', 200000, 1),
( 5, 'MENSAH',    'Kofi',       'M', '6ème A', '2025-2026', 150000, 1),
( 6, 'KOUAME',    'Akissi',     'F', '5ème B', '2025-2026', 120000, 1),
( 7, 'BAKAYOKO',  'Ibrahim',    'M', '4ème A', '2025-2026', 180000, 1),
( 8, 'N''GUESSAN','Adjoua',     'F', '6ème A', '2025-2026', 150000, 1),
( 9, 'OUATTARA',  'Moussa',     'M', '3ème B', '2025-2026', 200000, 1),
(10, 'YAO',       'Akoua',      'F', '5ème B', '2025-2026', 120000, 1),
(11, 'KONE',      'Souleymane', 'M', '4ème A', '2025-2026', 180000, 1),
(12, 'KOUADIO',   'Aya',        'F', '6ème A', '2025-2026', 150000, 1),
(13, 'SANOGO',    'Aminata',    'F', '3ème B', '2025-2026', 200000, 1),
(14, 'GBAGBO',    'Serge',      'M', '5ème B', '2025-2026', 120000, 1),
(15, 'ZADI',      'Grégoire',   'M', '4ème A', '2025-2026', 180000, 1);

-- ------------------------------------------------------------
-- 14 PAIEMENTS
-- Répartition : soldés (5), partiels (6), non payés (4)
-- Modes : Espèces, Chèque, Virement, Mobile Money
-- ------------------------------------------------------------
INSERT INTO paiements (eleve_id, montant, date_paiement, mode_paiement, numero_recu, solde_apres) VALUES
-- ADUKPO Justin (1) — 150 000 dû — SOLDÉ en 2 versements
( 1, 100000, '2026-09-15', 'Espèces',      'REC-2026-0001',  50000),
( 1,  50000, '2026-09-20', 'Mobile Money', 'REC-2026-0002',      0),

-- DIALLO Aïcha (2) — 120 000 dû — PARTIEL (60 000)
( 2,  60000, '2026-09-18', 'Virement',     'REC-2026-0003',  60000),

-- MENSAH Kofi (5) — 150 000 dû — PARTIEL (75 000)
( 5,  75000, '2026-09-19', 'Espèces',      'REC-2026-0004',  75000),

-- TRAORÉ Fatou (4) — 200 000 dû — SOLDÉ en 1 versement
( 4, 200000, '2026-09-16', 'Chèque',       'REC-2026-0005',      0),

-- KOUAME Akissi (6) — 120 000 dû — SOLDÉ en 2 versements
( 6,  60000, '2026-09-17', 'Espèces',      'REC-2026-0006',  60000),
( 6,  60000, '2026-09-25', 'Virement',     'REC-2026-0007',      0),

-- BAKAYOKO Ibrahim (7) — 180 000 dû — PARTIEL (90 000)
( 7,  90000, '2026-09-22', 'Mobile Money', 'REC-2026-0008',  90000),

-- YAO Akoua (10) — 120 000 dû — SOLDÉ en 1 versement
(10, 120000, '2026-09-20', 'Espèces',      'REC-2026-0009',      0),

-- OUATTARA Moussa (9) — 200 000 dû — PARTIEL (100 000)
( 9, 100000, '2026-09-23', 'Chèque',       'REC-2026-0010', 100000),

-- KOUADIO Aya (12) — 150 000 dû — PARTIEL (50 000)
(12,  50000, '2026-09-24', 'Espèces',      'REC-2026-0011', 100000),

-- SANOGO Aminata (13) — 200 000 dû — SOLDÉ en 2 versements
(13, 100000, '2026-09-21', 'Virement',     'REC-2026-0012', 100000),
(13, 100000, '2026-09-28', 'Mobile Money', 'REC-2026-0013',      0),

-- GBAGBO Serge (14) — 120 000 dû — PARTIEL (40 000)
(14,  40000, '2026-09-26', 'Espèces',      'REC-2026-0014',  80000);

-- ------------------------------------------------------------
-- Récapitulatif (à titre indicatif)
-- Élèves SOLDÉS      : 1, 4, 6, 10, 13          (5)
-- Élèves PARTIELS    : 2, 5, 7, 9, 12, 14       (6)
-- Élèves NON PAYÉS   : 3, 8, 11, 15             (4)
-- Total élèves       : 15
-- Total paiements    : 14
-- ------------------------------------------------------------