from dataclasses import dataclass, asdict

@dataclass
class Character:
    name: str
    role: str
    health: int
    attack: int
    description: str

    def to_dict(self):
        return asdict(self)

@dataclass
class GameState:
    character_name: str
    health: int
    enemy_health: int
    wins: int = 0
    finished: bool = False
