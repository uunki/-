import random
from .commands import Command
from .models import Character, GameState
from .storage import JsonStorage

class CharacterStrategy:
    """Стратегія команд керування каталогом персонажів."""
    def __init__(self, cli):
        self.cli = cli
        self.storage = JsonStorage()

    def get_commands(self):
        return [
            ListCharacters(self), AddCharacter(self), RefreshCharacters(self)
        ]

class ListCharacters(Command):
    name = "characters"
    description = "Показати всіх персонажів"
    def __init__(self, strategy): self.s = strategy
    def execute(self, args):
        self.s.cli.renderer.show_characters(self.s.storage.load_characters())

class RefreshCharacters(Command):
    name = "refresh"
    description = "Оновити та повторно завантажити каталог"
    def __init__(self, strategy): self.s = strategy
    def execute(self, args):
        chars = self.s.storage.load_characters()
        self.s.cli.renderer.info(f"Каталог оновлено. Персонажів: {len(chars)}")
        self.s.cli.renderer.show_characters(chars)

class AddCharacter(Command):
    name = "add"
    description = "Створити персонажа через діалог"
    def __init__(self, strategy): self.s = strategy
    def execute(self, args):
        try:
            name = input("Ім'я персонажа: ").strip()
            role = input("Клас персонажа: ").strip()
            description = input("Опис: ").strip()
            health = int(input("Здоров'я (1–200): "))
            attack = int(input("Сила атаки (1–50): "))
            if not name or not role or not description:
                raise ValueError("Поля імені, класу та опису не можуть бути порожніми.")
            if not 1 <= health <= 200 or not 1 <= attack <= 50:
                raise ValueError("Здоров'я має бути 1–200, атака — 1–50.")
            chars = self.s.storage.load_characters()
            if any(c.name.lower() == name.lower() for c in chars):
                raise ValueError("Персонаж із таким ім'ям уже існує.")
            chars.append(Character(name, role, health, attack, description))
            self.s.storage.save_characters(chars)
            self.s.cli.renderer.info("Персонажа створено та збережено.")
        except ValueError as e:
            self.s.cli.renderer.error(str(e))

class GameStrategy:
    """Стратегія команд ігрового процесу."""
    def __init__(self, cli):
        self.cli = cli
        self.storage = JsonStorage()
        self.state = None

    def get_commands(self):
        return [
            StartGame(self), Attack(self), Defend(self),
            GameStatus(self), SaveGame(self), LoadGame(self)
        ]

class StartGame(Command):
    name = "start"
    description = "Почати гру та обрати персонажа"
    def __init__(self, strategy): self.s = strategy
    def execute(self, args):
        chars = self.s.storage.load_characters()
        self.s.cli.renderer.show_characters(chars)
        try:
            choice = int(input("Оберіть номер персонажа: "))
            if not 1 <= choice <= len(chars):
                raise ValueError
            c = chars[choice - 1]
            self.s.state = GameState(c.name, c.health, 60)
            self.s.cli.renderer.info(f"Гру розпочато! Проти вас ворог із 60 HP.")
            self.s.storage.save_game(self.s.state)
        except ValueError:
            self.s.cli.renderer.error("Введіть коректний номер зі списку.")

class Attack(Command):
    name = "attack"
    description = "Атакувати супротивника"
    def __init__(self, strategy): self.s = strategy
    def execute(self, args):
        state = self.s.state
        if not state or state.finished:
            self.s.cli.renderer.error("Спочатку почніть нову гру командою start.")
            return
        chars = self.s.storage.load_characters()
        character = next(c for c in chars if c.name == state.character_name)
        damage = character.attack + random.randint(0, 5)
        state.enemy_health = max(0, state.enemy_health - damage)
        self.s.cli.renderer.info(f"Ви завдали {damage} шкоди.")
        if state.enemy_health == 0:
            state.wins += 1
            state.finished = True
            self.s.cli.renderer.info("Перемога! Ворога переможено.")
        else:
            enemy_damage = random.randint(5, 12)
            state.health = max(0, state.health - enemy_damage)
            self.s.cli.renderer.info(f"Ворог відповів: -{enemy_damage} HP.")
            if state.health == 0:
                state.finished = True
                self.s.cli.renderer.info("Гру завершено. Спробуйте ще раз!")
        self.s.storage.save_game(state)

class Defend(Command):
    name = "defend"
    description = "Захиститися від наступної атаки"
    def __init__(self, strategy): self.s = strategy
    def execute(self, args):
        state = self.s.state
        if not state or state.finished:
            self.s.cli.renderer.error("Немає активної гри. Виконайте start.")
            return
        damage = random.randint(1, 4)
        state.health = max(0, state.health - damage)
        self.s.cli.renderer.info(f"Ви захистилися. Отримано лише {damage} шкоди.")
        if state.health == 0:
            state.finished = True
            self.s.cli.renderer.info("Гру завершено.")
        self.s.storage.save_game(state)

class GameStatus(Command):
    name = "status"
    description = "Показати поточний стан гри"
    def __init__(self, strategy): self.s = strategy
    def execute(self, args):
        if self.s.state:
            self.s.cli.renderer.show_status(self.s.state)
        else:
            self.s.cli.renderer.info("Активної гри немає.")

class SaveGame(Command):
    name = "save"
    description = "Зберегти стан гри"
    def __init__(self, strategy): self.s = strategy
    def execute(self, args):
        if not self.s.state:
            self.s.cli.renderer.error("Немає стану гри для збереження.")
            return
        self.s.storage.save_game(self.s.state)
        self.s.cli.renderer.info("Стан гри збережено.")

class LoadGame(Command):
    name = "load"
    description = "Завантажити останнє збереження"
    def __init__(self, strategy): self.s = strategy
    def execute(self, args):
        data = self.s.storage.load_game()
        if not data:
            self.s.cli.renderer.error("Збереження не знайдено.")
            return
        self.s.state = GameState(**data)
        self.s.cli.renderer.info("Збереження завантажено.")
        self.s.cli.renderer.show_status(self.s.state)
