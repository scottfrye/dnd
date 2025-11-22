import random
import string
from dataclasses import dataclass, field


def generate_id() -> string:
    return "".join(random.choices(string.ascii_uppercase, k=12))


@dataclass
class Person:
    name: str
    location: str
    room: str
    race: str
    name: str
    level: int
    hp: int
    attacks: str
    xp: int
    age: int
    active: bool = True
    inventory: list = field(default_factory=list)
    not_on_inventory: list = field(default_factory=list)
    # id: str = field(init=False, default_factory=generate_id)
    spells: dict = field(default_factory=dict)


if __name__ == '__main__':
    person = Person("John", 25)
    print(person)
    print('Done.')
