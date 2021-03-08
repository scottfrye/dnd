import json


class Monster:
    def __init__(self):
        pass

    def load(self, path_to_file):
        with open(path_to_file) as f:
            person_dict = json.load(f)
        print(person_dict)

    def get_surprise_threshold(self):
        return 2
