from abilities import Abilities
import json


class Person:
    abilities = Abilities()
    level = 0
    hit_points = 0
    ac = 10
    char_class = 'fighter'
    name = 'generic person'
    race = 'human'

    def load(self, path_to_file):
        with open(path_to_file) as f:
            person_dict = json.load(f)
        print(person_dict)

    def get_surprise_threshold(self):
        return



