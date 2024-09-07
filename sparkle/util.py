import random
import numpy as np

from multiset import FrozenMultiset
from itertools import combinations

scores = {
    FrozenMultiset((2,2,2,2)): 1000,
    FrozenMultiset((3,3,3,3)): 1000,
    FrozenMultiset((4,4,4,4)): 1000,
    FrozenMultiset((5,5,5,5)): 1000,
    FrozenMultiset((6,6,6,6)): 1000,
    FrozenMultiset((1,1,1)): 1000,
    FrozenMultiset((6,6,6)): 600,
    FrozenMultiset((5,5,5)): 500,
    FrozenMultiset((4,4,4)): 400,
    FrozenMultiset((3,3,3)): 300,
    FrozenMultiset((2,2,2)): 200,
    FrozenMultiset((1,)): 100,
    FrozenMultiset((5,)):  50,
    FrozenMultiset((1,2,3,4,5)): 1500,
    FrozenMultiset((2,3,4,5,6)): 1500,
    FrozenMultiset((1,2,3,4,5,6)): 2000,
}

def roll_dice(n=6):
    return FrozenMultiset([random.randint(1, 6) for _ in range(n)])

def roll2vect(roll):
    vect = [roll[i] for i in range(1,7)]
    return np.array(vect, dtype=float)

def dice_from_combo(combo):
    return FrozenMultiset.combine(*combo)

def legal_combo(combo, dice):
    s = FrozenMultiset.combine(*combo)
    return s <= s & dice

def combined_score(combo):
    score = 0
    for group in combo:
        score += highest_score(group)
    return score

def highest_score(dice):
    high_score = 0
    for s in scores:
        roll_vect = roll2vect(dice)
        score_vect = roll2vect(s)
        score_vect[score_vect==0] = np.nan
        if np.nanmin(roll_vect // score_vect) > 0:
            if scores[s] > high_score:
                high_score = scores[s]
    return high_score

def individual_score(dice):
    possible_scores = []
    for s in scores:
        roll_vect = np.array(roll2vect(dice))
        score_vect = np.array(roll2vect(s))
        score_vect[score_vect==0] = np.nan
        if (roll_vect // score_vect).min() > 0:
            possible_scores.append((s, scores[s]))
    return possible_scores

def scorable_dice(dice):
    possible_scores = []
    for s in scores:
        roll_vect = np.array(roll2vect(dice))
        score_vect = np.array(roll2vect(s))
        score_vect[score_vect==0] = np.nan
    #     if int(np.nanmin(roll_vect // score_vect)) > 0:
    #         possible_scores.append(s)
    # return possible_scores
        for _ in range(int(np.nanmin(roll_vect // score_vect))):
            possible_scores.append(s)
    return FrozenMultiset(possible_scores)

def scoring_options(roll):
    scorable_sets = scorable_dice(roll)
    legal_combos = []
    for r in range(1, 7):
        for combo in set(combinations(scorable_sets, r)):
            combo = FrozenMultiset(combo)
            if legal_combo(combo, roll):
                legal_combos.append(combo)
    legal_combos = sorted(legal_combos, key=combined_score, reverse=True)
    return legal_combos

def play_round(n_thresh=4, score_thresh=1000):
    n = 6
    used_dice = FrozenMultiset()
    while n > 0:
        roll = roll_dice(n)
        options = scoring_options(roll)
        if len(options) > 0:
            used_dice += options[0]
            score = combined_score(used_dice)
            roll -= FrozenMultiset.combine(*options[0])
            n = len(roll)
        else:
            return 0
        if n == 0:
            n = 6
        if n < n_thresh and combined_score(used_dice) > score_thresh:
            break
        # print(n)
    return combined_score(used_dice)

def play_game(n_thresh=4, score_thresh=1000):
    player_scores = [0]
    while sum(player_scores) < 10_000:
        player_scores.append(play_round(n_thresh, score_thresh))
    return player_scores
