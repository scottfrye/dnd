import random
from dice import Dice


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
