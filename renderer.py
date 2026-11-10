class ConsoleRenderer:
    """Єдине місце для форматованого виведення в консоль."""
    def title(self, value):
        print("\n" + "=" * 54)
        print(value.center(54))
        print("=" * 54)

    def info(self, value):
        print(f"[ІНФО] {value}")

    def error(self, value):
        print(f"[ПОМИЛКА] {value}")

    def show_help(self, commands):
        self.title("ДОСТУПНІ КОМАНДИ")
        for name, command in sorted(commands.items()):
            print(f"{name:<16} — {command.description}")

    def show_characters(self, characters):
        self.title("КАТАЛОГ ПЕРСОНАЖІВ")
        for i, c in enumerate(characters, 1):
            print(f"{i}. {c.name} | {c.role} | HP: {c.health} | Атака: {c.attack}")
            print(f"   {c.description}")

    def show_status(self, state):
        self.title("СТАН ГРИ")
        print(f"Персонаж: {state.character_name}")
        print(f"Ваше здоров'я: {state.health}")
        print(f"Здоров'я ворога: {state.enemy_health}")
        print(f"Перемог: {state.wins}")
