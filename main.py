from game_cli.cli import CLI
from game_cli.strategies import CharacterStrategy, GameStrategy

def main():
    cli = CLI()
    cli.use_strategy(CharacterStrategy(cli))
    cli.use_strategy(GameStrategy(cli))
    cli.run()

if __name__ == "__main__":
    main()
