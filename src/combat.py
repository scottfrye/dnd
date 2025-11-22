import random
from dataclasses import make_dataclass
import pandas as pd


class Encounter():
    combatants = list()
    side_1 = dict()
    side_2 = dict()

    def __init__(self, side_list):
        # make sure a list was passed in
        if not isinstance(side_list, list):
            raise ValueError('inputs must be a lists of members of each side')

        if len(side_list) > 2:
            raise ValueError('Only 2 sides are allowed')

        # make sure it is a list of lists
        inputs_valid = all([isinstance(s, list) for s in side_list])

        if not inputs_valid:
            raise ValueError('inputs must be a lists of members of each side')

        # for each side, add all the members to the combatants list with their side identifier
        side_number = 0
        for side in side_list:
            side_number += 1
            for c in side:
                self.combatants.append({'combatant': c, 'side': side_number})

        # determine surprise by side and distance by side

        # get the minumum suprise of all the entities on the side.
        first_surprise_threshold = min([e['combatant'].get_surprise_threshold() for e in self.combatants if
                                        e['side'] == 1])
        second_surpise_threshold = min([e['combatant'].get_surprise_threshold() for e in self.combatants if
                                        e['side'] == 2])

        roll_side1 = random.randint(1, 6)
        roll_side2 = random.randint(1, 6)  # TODO: some monsters have 1 in 8, might need to convert to %

        surprised_side1 = True if roll_side1 < first_surprise_threshold else False
        surprised_side2 = True if roll_side2 < second_surpise_threshold else False

        if surprised_side1:
            self.side_2['extra_segments'] = roll_side2 - roll_side1

        if surprised_side2:
            self.side_1['extra_segments'] = roll_side1 - roll_side2

    def start_fight(self):
        # Determine surprise
        # determine distance
        pass

    def take_turn(self):
        """
            determine initiative
            determine action for 1st
                Retreat
                Parley
                Wait action
                Discharge Missiles or magical device
                Charge/Close to striking
                strike to kill or subdue
                Grapple or Hold

            Other Team
        """

        pass

    def attack(self, attacker_class='Monster', attacker_level=1, defendor_armor_type=10, defender_armor_class=10):
        cleric_table = make_dataclass("cleric", [("ac", int), "level", int])

        return True


if __name__ == '__main__':
    def combat_range(start, end, first):
        twenty_run = 6
        value_list = []
        twenty_count = 1
        current_value = first
        for i in range(start, end, -1):
            value_list.append(current_value)
            if (current_value == 20) & (twenty_count < twenty_run):
                twenty_count += 1
            else:
                current_value += 1

        return value_list


    level_1_3 = combat_range(start=10, end=-11, first=10)
    level_4_6 = combat_range(start=10, end=-11, first=8)
    level_7_9 = combat_range(start=10, end=-11, first=6)
    level_10_12 = combat_range(start=10, end=-11, first=4)
    level_13_15 = combat_range(start=10, end=-11, first=2)
    level_16_18 = combat_range(start=10, end=-11, first=0)
    level_19plus = combat_range(start=10, end=-11, first=-1)
    # columns = range(10, -10, -1)
    # df = pd.DataFrame({1: level_1_3})
    # df.columns = list(columns)

    df_all = pd.DataFrame({1: level_1_3,
                           2: level_1_3,
                           3: level_1_3,
                           4: level_4_6,
                           5: level_4_6,
                           6: level_4_6,
                           7: level_7_9,
                           8: level_7_9,
                           9: level_7_9,
                           10: level_10_12,
                           11: level_10_12,
                           12: level_10_12,
                           13: level_13_15,
                           14: level_13_15,
                           15: level_13_15,
                           16: level_16_18,
                           17: level_16_18,
                           18: level_16_18,
                           19: level_19plus}

                          )

    print("Done.")
