'''
Functions for rolling dice. Engine Hearth is not a general dice-roller
so many things can be assumed or ignored.
'''
import random

import config


# Limit d10 explosion to prevent degenerate behavior
MAX_EXPLOSIONS = 10

# d10 side sequence, ascending order
d10 = tuple(range(1, 11))


class Check:
    '''
    A roll of a pool against a target number.

    karma: roll karma
    weights: weights derived from karma
    rolls: list of raw roll results
    successes: precomputed number of successes among all rolls
    ones: precomputed number of ones among all rolls
    '''
    def __init__(self, pool_size, target_number, karma=0):
        # Record karma on the roll object for reference
        self.karma = karma
        # Convert karma to a weight sequence
        if karma != 0:
            low = max(1, 1 - karma)
            hih = max(1, 1 + karma)
            step = (hih - low) / 9  # 9 steps between 1 and 10
            self.weights = tuple((low + (i * step) for i in range(9))) + (hih,)
        else:
            self.weights = None

        # Roll and explode the pool until it's exhausted
        self.rolls = []
        current_pool_size = pool_size
        roll_count = 0
        while current_pool_size > 0 and roll_count < MAX_EXPLOSIONS:
            # Roll the current pool size
            roll = tuple(random.choices(d10, k=current_pool_size, weights=self.weights))
            self.rolls.append(roll)
            roll_count += 1
            # Set the new pool size to the number of 10s rolled
            current_pool_size = len([d for d in roll if d == 10])

        # Based on the target number, tally up the number of successes
        self.successes = len([d for roll in self.rolls for d in roll if d >= target_number])

        # Tally up the number of 1s rolled, which can be relevant to certain checks
        self.ones = len([d for roll in self.rolls for d in roll if d == 1])


ATTRIBUTES = {
    'rco': 0, 'rcom': 0, 'realitycom': 0,
    'hco': 1, 'hcom': 1, 'humancom': 1,
    'dco': 2, 'dcom': 2, 'digicon': 2,
    'mco': 3, 'mcon': 3, 'mechanicon': 3,
    'dex': 4, 'dexterity': 4,
    'mob': 5, 'mobil': 5, 'mobility': 5,
    'per': 6, 'perc': 6, 'percep': 6, 'perception': 6,
    'ref': 7, 'reflex': 7, 'reflexes': 7,
    'str': 8, 'strength': 8,
    'dur': 9, 'durab': 9, 'durability': 9,
    'buf': 10, 'buff': 10, 'buffer': 10,
    'siz': 11, 'size': 11,
    'pow': 12, 'power': 12
}


async def parse_stats(message):
    '''
    Parse a message as attribute names instead of a raw pool size.
    If the message is an attribute check, return the pool size.
    Otherwise, return None.
    '''
    # Check if the user even has stats
    with config.EnvConfig.user(message.author.id) as user:
        if 'stats' not in user:
            return None
        stats = user.get('stats')

    # Ensure that + will be split on whitespace, also normalize case
    text = message.content.lower().replace('+', ' + ')
    tokens = text.split()

    # Check for a combined pool
    if len(tokens) >= 3 and tokens[1] == '+':
        if tokens[0] in ATTRIBUTES and tokens[2] in ATTRIBUTES:
            return stats[ATTRIBUTES[tokens[0]]] + stats[ATTRIBUTES[tokens[2]]]
        else:
            return None

    # Check for a simple pool
    if len(tokens) >= 1:
        if tokens[0] in ATTRIBUTES:
            return stats[ATTRIBUTES[tokens[0]]]
        else:
            return None

    return None
