from monster import Monster
from player import Person
from combat import Encounter

if __name__ == '__main__':
    m = Monster()
    m.load('../data/test_monster.json')
    p = Person()
    p.load('../data/character_1.json')

    fight = Encounter([[p], [m]])

    print('Done.')
