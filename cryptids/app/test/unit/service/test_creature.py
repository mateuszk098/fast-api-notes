from app.model.creature import Creature
from app.service import creature as code

sample = Creature(
    name="Bigfoot",
    country="USA",
    area="Pacific Northwest",
    description="A large, hairy, ape-like creature.",
    aka="Sasquatch",
)


def test_create():
    response = code.create(sample)
    assert response == sample


def test_get_existing():
    response = code.get_one("Bigfoot")
    assert response == sample


def test_get_missing():
    response = code.get_one("Nessie")
    assert response is None
