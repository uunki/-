class Command:
    """Інтерфейс патерна Command."""
    name = ""
    description = ""

    def execute(self, args):
        raise NotImplementedError

class HelpCommand(Command):
    name = "help"
    description = "Показати список команд"

    def __init__(self, cli):
        self.cli = cli

    def execute(self, args):
        self.cli.renderer.show_help(self.cli.commands)

class ExitCommand(Command):
    name = "exit"
    description = "Завершити програму"

    def __init__(self, cli):
        self.cli = cli

    def execute(self, args):
        self.cli.running = False
        self.cli.renderer.info("Роботу програми завершено.")
