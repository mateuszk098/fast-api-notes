from ..model.creature import Creature

_creatures: list[Creature] = [
    Creature(
        name="Bigfoot",
        country="USA",
        area="Pacific Northwest",
        description="A large, hairy, ape-like creature.",
        aka="Sasquatch",
    ),
    Creature(
        name="Loch Ness Monster",
        country="Scotland",
        area="Loch Ness",
        description="A large, aquatic creature.",
        aka="Nessie",
    ),
    Creature(
        name="Chupacabra",
        country="Puerto Rico",
        area="Central America",
        description="A blood-sucking creature.",
        aka="Goat Sucker",
    ),
    Creature(
        name="Mothman",
        country="USA",
        area="West Virginia",
        description="A large, winged creature.",
        aka="The Mothman of Point Pleasant",
    ),
    Creature(
        name="Jersey Devil",
        country="USA",
        area="New Jersey",
        description="A large, bat-winged creature.",
        aka="The Leeds Devil",
    ),
    Creature(
        name="Kraken",
        country="Norway",
        area="North Atlantic",
        description="A giant, tentacled creature.",
        aka="The Kraken",
    ),
]


def get_all() -> list[Creature]:
    return _creatures


def get_one(name: str) -> Creature | None:
    for creature in _creatures:
        if creature.name == name:
            return creature


def create(creature: Creature) -> Creature:
    return creature


def modify(creature: Creature) -> Creature:
    return creature


def replace(creature: Creature) -> Creature:
    return creature


def delete(name: str) -> None:
    pass
