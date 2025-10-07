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

def roll_dice(n: int = 6) -> FrozenMultiset:
    """
    Roll n dice and return as a FrozenMultiset.
    
    Args:
        n (int, optional): Number of dice to roll. Defaults to 6.
    
    Returns:
        FrozenMultiset: Multiset containing the rolled dice values (1-6)
    """
    return FrozenMultiset([random.randint(1, 6) for _ in range(n)])

def roll2vect(roll: FrozenMultiset) -> np.ndarray:
    """
    Convert a dice roll to a count vector.
    
    Args:
        roll (FrozenMultiset): Multiset of dice values
    
    Returns:
        np.ndarray: Vector of length 6 with counts for each die value (1-6)
    """
    vect = [roll[i] for i in range(1,7)]
    return np.array(vect, dtype=float)

def dice_from_combo(combo: tuple) -> FrozenMultiset:
    """
    Combine dice from a combination into a single multiset.
    
    Args:
        combo (tuple): Tuple of dice combinations
    
    Returns:
        FrozenMultiset: Combined multiset of all dice in the combination
    """
    return FrozenMultiset.combine(*combo)

def legal_combo(combo: tuple, dice: FrozenMultiset) -> bool:
    """
    Check if a combination of dice is legal (can be formed from available dice).
    
    Args:
        combo (tuple): Combination of dice to check
        dice (FrozenMultiset): Available dice
    
    Returns:
        bool: True if the combination can be formed from available dice
    """
    s = FrozenMultiset.combine(*combo)
    return s <= s & dice

def combined_score(combo: tuple) -> int:
    """
    Calculate the total score for a combination of dice groups.
    
    Args:
        combo (tuple): Combination of dice groups
    
    Returns:
        int: Total score from all groups in the combination
    """
    score = 0
    for group in combo:
        score += highest_score(group)
    return score

def highest_score(dice: FrozenMultiset) -> int:
    """
    Find the highest possible score for a set of dice.
    
    Args:
        dice (FrozenMultiset): Set of dice to score
    
    Returns:
        int: Highest possible score for the dice
    
    Algorithm:
        - Check each scoring pattern against the dice
        - Use vector division to check if pattern can be formed
        - Return the highest scoring pattern that can be formed
    """
    high_score = 0
    for s in scores:
        roll_vect = roll2vect(dice)
        score_vect = roll2vect(s)
        score_vect[score_vect==0] = np.nan
        if np.nanmin(roll_vect // score_vect) > 0:
            if scores[s] > high_score:
                high_score = scores[s]
    return high_score

def individual_score(dice: FrozenMultiset) -> list[tuple]:
    """
    Find all possible scoring patterns for a set of dice.
    
    Args:
        dice (FrozenMultiset): Set of dice to analyze
    
    Returns:
        list[tuple]: List of (pattern, score) tuples for all possible scores
    
    Returns all scoring patterns that can be formed from the dice,
    not just the highest scoring one.
    """
    possible_scores = []
    for s in scores:
        roll_vect = np.array(roll2vect(dice))
        score_vect = np.array(roll2vect(s))
        score_vect[score_vect==0] = np.nan
        if (roll_vect // score_vect).min() > 0:
            possible_scores.append((s, scores[s]))
    return possible_scores

def scorable_dice(dice: FrozenMultiset) -> FrozenMultiset:
    """
    Find all scoring patterns that can be formed from dice, with multiplicity.
    
    Args:
        dice (FrozenMultiset): Set of dice to analyze
    
    Returns:
        FrozenMultiset: Multiset of all scoring patterns that can be formed
    
    For each scoring pattern, includes it multiple times if it can be formed
    multiple times from the available dice.
    """
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

def scoring_options(roll: FrozenMultiset) -> list[FrozenMultiset]:
    """
    Find all legal scoring combinations for a dice roll, sorted by score.
    
    Args:
        roll (FrozenMultiset): Dice roll to find scoring options for
    
    Returns:
        list[FrozenMultiset]: List of legal scoring combinations, sorted by score (highest first)
    
    Algorithm:
        1. Find all scorable patterns from the dice
        2. Generate all possible combinations of patterns
        3. Filter to only legal combinations
        4. Sort by combined score in descending order
    """
    scorable_sets = scorable_dice(roll)
    legal_combos = []
    for r in range(1, 7):
        for combo in set(combinations(scorable_sets, r)):
            combo = FrozenMultiset(combo)
            if legal_combo(combo, roll):
                legal_combos.append(combo)
    legal_combos = sorted(legal_combos, key=combined_score, reverse=True)
    return legal_combos

def play_round(n_thresh: int = 4, score_thresh: int = 1000) -> int:
    """
    Simulate a single round of the dice game.
    
    Args:
        n_thresh (int, optional): Minimum dice threshold for early stopping. Defaults to 4.
        score_thresh (int, optional): Score threshold for early stopping. Defaults to 1000.
    
    Returns:
        int: Final score for the round (0 if bust)
    
    Game flow:
        1. Start with 6 dice
        2. Roll dice and find best scoring option
        3. If no options, bust (return 0)
        4. Remove scored dice, continue with remaining
        5. If all dice used, get 6 new dice
        6. Stop if dice count < n_thresh and score > score_thresh
    """
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

def play_game(n_thresh: int = 4, score_thresh: int = 1000) -> list[int]:
    """
    Simulate a complete game with multiple rounds until 10,000 points.
    
    Args:
        n_thresh (int, optional): Minimum dice threshold for early stopping. Defaults to 4.
        score_thresh (int, optional): Score threshold for early stopping. Defaults to 1000.
    
    Returns:
        list[int]: List of scores for each round played
    
    Game continues until total score reaches 10,000 points.
    Each round uses the same thresholds for early stopping.
    """
    player_scores = [0]
    while sum(player_scores) < 10_000:
        player_scores.append(play_round(n_thresh, score_thresh))
    return player_scores
