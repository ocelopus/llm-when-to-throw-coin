import random
import numpy as np
from typing import Any

class HorseRaceGame:
    def __init__(self, players: dict[int, Any], horses_per_player=5, horse_power: dict[int, dict[int, float]] = None):
        self.players = players
        self.horses_per_player = horses_per_player
        self.history: dict[int, dict[int, int]] = [[] for i in range(len(players))] # Do not use [[]] * len(players) because this will duplicate the pointer!!! 
        self.step_num = 0
        self.total_rewards = np.zeros(shape=(len(players),), dtype=float)
        self.terminated = False
        if horse_power is not None:
            self.horse_power = horse_power
        else: 
            self.horse_power = np.zeros(shape=(len(players), self.horses_per_player)) + np.arange(self.horses_per_player)

    def get_choice_invalidity(self, choices: dict[int, int]) -> dict[int, int]:
        choices = np.array(choices)
        out_of_range = np.logical_or((choices < 0), (choices >= self.horses_per_player))
        repeated = [choice in self.history[player] for player, choice in enumerate(choices)]
        repeated = np.array(repeated)
        return np.logical_or(repeated, out_of_range)

    def log_history(self, choices):
        [(self.history[player]).append(choice) for player, choice in enumerate(choices)]    

    def step(self, choices: dict[int, int]):
        """
            assume choices to be valid.
        """
        assert self.terminated == False, "Error: Game has ended"
        assert self.get_choice_invalidity(choices).any() == False, "Error: Invalid Choice"

        self.log_history(choices)

        strength = [self.horse_power[player, choice] for player, choice in enumerate(choices)]
        strength = np.array(strength)

        largest = np.max(strength)
        wins = (strength == largest)
        reward = np.array(wins, dtype=float)
        reward /= reward.sum()
        self.total_rewards += reward

        ranks = np.argsort(strength)
        self.step_num += 1
        
        self.terminated = self.step_num == self.horses_per_player

        return {
            "choices": choices, 
            "strength": strength,
            "wins": wins,
            "largest": largest, 
            "ranks": ranks
                
                }, reward, self.terminated, False, None

    def get_total_rewards(self) -> np.ndarray:
        assert self.terminated, "Error: Game has not ended"
        return self.total_rewards
        