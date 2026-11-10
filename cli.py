import shlex
from .renderer import ConsoleRenderer
from .commands import HelpCommand, ExitCommand

class CLI:
    """Фасад командного інтерфейсу: реєстрація та запуск команд."""
    def __init__(self):
        self.renderer = ConsoleRenderer()
        self.commands = {}
        self.running = True
        self.register(HelpCommand(self))
        self.register(ExitCommand(self))

    def register(self, command):
        self.commands[command.name] = command

    def use_strategy(self, strategy):
        for command in strategy.get_commands():
            self.register(command)

    def exec_command(self, raw_string):
        try:
            parts = shlex.split(raw_string)
            if not parts:
                return
            name, args = parts[0].lower(), parts[1:]
            command = self.commands.get(name)
            if command:
                command.execute(args)
            else:
                self.renderer.error(f"Невідома команда: {name}. Введіть help.")
        except ValueError as e:
            self.renderer.error(f"Не вдалося розібрати команду: {e}")

    def run(self):
        self.renderer.title("КОНСОЛЬНА ТЕКСТОВА ГРА")
        self.renderer.info("Введіть help для перегляду команд.")
        while self.running:
            try:
                raw = input("\nГравець > ")
                self.exec_command(raw)
            except (EOFError, KeyboardInterrupt):
                self.running = False
                print()
        self.renderer.info("До зустрічі!")
