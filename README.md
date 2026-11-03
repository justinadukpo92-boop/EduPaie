
# EduPaie - Gestion des frais scolaires

EduPaie est une application desktop développée en Python (avec l'interface PySide6) permettant à un établissement scolaire de gérer les frais de scolarité des élèves, d'enregistrer les paiements et de générer des reçus au format PDF.

## 🚀 Fonctionnalités
- Gestion des élèves (ajout, modification, suppression, recherche).
- Enregistrement des paiements avec calcul automatique du solde.
- Génération et export de reçus uniques au format PDF.
- Tableau de bord avec statistiques (total encaissé, restant dû, impayés).

## 🛠️ Prérequis
- Python 3.10 ou supérieur.
- Windows, macOS ou Linux.

## 📦 Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/justinadukpo92-boop/EduPaie.git
cd EduPaie
```

2. Créer un environnement virtuel et l'activer :
```bash
python -m venv venv
# Sur Windows :
venv\Scripts\activate
# Sur macOS/Linux :
source venv/bin/activate
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## ▶️ Lancement

L'application crée automatiquement la base de données au premier lancement. Pour démarrer :
```bash
python main.py
```

## 🏗️ Architecture
Le projet suit une architecture en 3 couches :
- `database/` et `repositories/` : Accès aux données (SQLite).
- `services/` : Logique métier (calculs, validations).
- `ui/` : Interface graphique (PySide6).