from repositories.settings_repository import SettingsRepository


class SettingsService:
    def __init__(self):
        self.repo = SettingsRepository()

    def get_school_name(self):
        return self.repo.get("school_name", "COMPLEXE SCOLAIRE EDUPAIE")

    def set_school_name(self, name):
        if not name or not name.strip():
            raise ValueError("Le nom de l'école ne peut pas être vide.")
        self.repo.set("school_name", name.strip())