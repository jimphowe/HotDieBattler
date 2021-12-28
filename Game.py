import random
from collections import Counter

# GameState: {cur_player: x, cur_scores: {a: xx, b: xx}, cur_turn_score: x, cur_roll: [x, y, ..]}

# Player algos are passed their current turn score, all players scores, and their current roll,
# from which they must decide what to keep

# Update this to set up a run
# Import strategies and add them to the player mapping
import Example_Strategy

player_1 = Example_Strategy()
player_2 = Example_Strategy()

players = {1: player_1, 2: player_2}

# TODO is_hot_die(), count_points()
class Game():
    def __init__(self):
        self.players = players
        self.cur_player = 1
        self.cur_scores = {1: 0, 2:0}

    def game_over(self):
        return max([self.cur_scores.values()]) < 10000

    def roll_die(self, num_die):
        return random.sample(range(1, 6), num_die)

    def list_contained_in(self, list1, list2):
        c1, c2 = Counter(list1), Counter(list2)
        for k, n in c1.items():
            if n > c2[k]:
                return False
        return True

    def is_hot_die(self, roll):

    def is_bust(self, roll):
        if self.is_hot_die(roll):
            return False
        if 1 in roll or 5 in roll:
            return False
        for num in roll:
            if roll.count(num) > 2:
                return False
        return True

    def legal_keep(self, kept_die, cur_roll, player_num):
        if len(kept_die) > len(cur_roll):
            return False
        if len(kept_die) == 0 and self.cur_scores[player_num] < 1000:
            return False
        if not self.list_contained_in(kept_die, cur_roll):
            return False
        for num in [2,3,4,6]:
            if num in kept_die and kept_die.count(num) < 3:
                if not self.is_hot_die(kept_die):
                    return False

    def count_points(self, kept_die):

    def give_turn(self, player_num):
        turn_over = False
        player = self.players[player_num]
        die_left = 6
        cur_turn_score = 0
        cur_roll = self.roll_die(die_left)
        while not turn_over:
            kept_die, stopping = player.take_turn(cur_roll, cur_turn_score, self.cur_scores)
            if self.legal_keep(kept_die, cur_roll, player_num):
                cur_turn_score += self.count_points(kept_die)
                die_left = die_left - len(kept_die)
                if die_left == 0:
                    die_left = 6
                cur_roll = self.roll_die(die_left)
                if self.is_bust(cur_roll):
                    turn_over = True
                if stopping:
                    turn_over = True
                    self.cur_scores[player_num] += cur_turn_score
            else:
                print("Player " + str(player_num) + " returned an invalid keep!...")
                print("Die kept were " + str(kept_die) + " out of " + str(cur_roll) + ", while player had " +
                      str(self.cur_scores[player_num]) + " points.")




    def play_game(self):
        while not self.game_over():
            self.give_turn(self.cur_player)
            self.cur_player = (self.cur_player + 1) % len(self.players)
        print("Game Over!")
        print(self.cur_scores)
