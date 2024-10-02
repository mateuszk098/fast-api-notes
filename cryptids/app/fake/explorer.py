from ..model.explorer import Explorer

_explorers: list[Explorer] = [
    Explorer(name="John Smith", country="USA", description="A very famous explorer."),
    Explorer(name="Jane Doe", country="Canada", description="Another very famous explorer."),
    Explorer(name="Sam Spade", country="USA", description="A detective, but also an explorer."),
    Explorer(name="Gertrude Bell", country="UK", description="An early 20th century explorer."),
    Explorer(name="Ibn Battuta", country="Morocco", description="A 14th century explorer."),
    Explorer(name="Erik the Red", country="Norway", description="A Viking explorer."),
    Explorer(name="Marco Polo", country="Italy", description="An explorer of the Silk Road."),
]


def get_all() -> list[Explorer]:
    return _explorers


def get_one(name: str) -> Explorer | None:
    for explorer in _explorers:
        if explorer.name == name:
            return explorer


def create(explorer: Explorer) -> Explorer:
    return explorer


def modify(explorer: Explorer) -> Explorer:
    return explorer


def replace(explorer: Explorer) -> Explorer:
    return explorer


def delete(name: str) -> None:
    pass
