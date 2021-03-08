import random


class Dice:

    def __int__(self):
        pass

    def roll(self, count=1, sides=6):
        results = [random.randint(1, sides) for i in range(0, count)]
        return sum(results)