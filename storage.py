import json
from pathlib import Path
from .models import Character

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CHARACTERS_FILE = DATA_DIR / "characters.json"
SAVE_FILE = DATA_DIR / "save.json"

class JsonStorage:
    """Відповідає лише за читання та запис даних у JSON."""
    def __init__(self):
        DATA_DIR.mkdir(exist_ok=True)
        if not CHARACTERS_FILE.exists():
            self.save_characters([
                Character("Аріон", "Воїн", 100, 18, "Відважний захисник королівства."),
                Character("Ліра", "Маг", 80, 25, "Мандрівна чарівниця."),
                Character("Торн", "Лучник", 90, 20, "Влучний мисливець.")
            ])

    def load_characters(self):
        with CHARACTERS_FILE.open("r", encoding="utf-8") as f:
            return [Character(**item) for item in json.load(f)]

    def save_characters(self, characters):
        with CHARACTERS_FILE.open("w", encoding="utf-8") as f:
            json.dump([c.to_dict() for c in characters], f, ensure_ascii=False, indent=2)

    def save_game(self, state):
        with SAVE_FILE.open("w", encoding="utf-8") as f:
            json.dump(state.__dict__, f, ensure_ascii=False, indent=2)

    def load_game(self):
        if not SAVE_FILE.exists():
            return None
        with SAVE_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
