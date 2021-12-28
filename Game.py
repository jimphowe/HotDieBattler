import numpy as np
from collections import Counter

# GameState: {players = {a: p1, b: p2}, cur_player: x, cur_scores: {a: xx, b: xx}}

# Player algos are passed their current turn score, all players scores, and their current roll,
# from which they must decide what to keep

# Update this to set up a run
# Import strategies and add them to the player mapping
from Example_Strategy import HotDieBot as ExampleBot

player_0 = ExampleBot()
player_1 = ExampleBot()
player_2 = ExampleBot()
player_3 = ExampleBot()

players = {0: player_0, 1: player_1, 2: player_2, 3: player_3}

# TODO
class Game():
    def __init__(self):
        self.players = players
        self.cur_player = 0
        self.cur_scores = {0:0, 1:0, 2:0, 3:0}

    def game_over(self):
        return max(self.cur_scores.values()) > 10000

    def roll_die(self, num_die):
        return list(np.random.randint(1, 6, size=num_die))

    def list_contained_in(self, list1, list2):
        c1, c2 = Counter(list1), Counter(list2)
        for k, n in c1.items():
            if n > c2[k]:
                return False
        return True

    def is_hot_die(self, roll):
        if sorted(roll) == [1,2,3,4,5,6]:
            return True
        if all([n == 2 for k,n in Counter(roll).items()]) and len(roll) == 6:
            return True
        return False

    def is_bust(self, roll):
        if self.is_hot_die(roll):
            return False
        if 1 in roll or 5 in roll:
            return False
        for num in roll:
            if roll.count(num) > 2:
                return False
        return True

    def legal_keep(self, kept_die, cur_roll, player_num, cur_turn_score):
        if len(kept_die) > len(cur_roll):
            return False
        if len(kept_die) == 0 and self.cur_scores[player_num] < 1000 and cur_turn_score < 1000:
            return False
        if not self.list_contained_in(kept_die, cur_roll):
            return False
        for num in [2,3,4,6]:
            if num in kept_die and kept_die.count(num) < 3:
                if not self.is_hot_die(kept_die):
                    return False
        return True

    def count_points(self, kept_die):
        if len(kept_die) == 0:
            return 0
        if self.is_hot_die(kept_die):
            return 1500
        c = Counter(kept_die)
        for k,n in c.items():
            if n > 2:
                if k == 1:
                    return 1000*(2**(n - 3)) + self.count_points([x for x in kept_die if x != k])
                else:
                    return k*100*(2**(n - 3)) + self.count_points([x for x in kept_die if x != k])
            if k == 1:
                return 100 * n + self.count_points([x for x in kept_die if x != k])
            if k == 5:
                return 50 * n + self.count_points([x for x in kept_die if x != k])

    def give_turn(self, player_num):
        print("\nPlayer " + str(player_num) + " is playing")
        turn_over = False
        player = self.players[player_num]
        die_left = 6
        cur_turn_score = 0
        # Start the turn. Roll 6 die and hand it to the player (as long as you don't bust on 6!)
        cur_roll = self.roll_die(die_left)
        print(cur_roll)
        if self.is_bust(cur_roll):
            turn_over = True
        while not turn_over:
            kept_die, stopping = player.take_turn(cur_roll, cur_turn_score, self.cur_scores)
            stopping_str = 'stopped' if stopping else 'kept rolling'
            print("Kept: " + str(kept_die) + " and " + stopping_str)
            if self.legal_keep(kept_die, cur_roll, player_num, cur_turn_score):
                cur_turn_score += self.count_points(kept_die)
                if stopping:
                    self.cur_scores[player_num] += cur_turn_score
                    turn_over = True
                else:
                    die_left = die_left - len(kept_die)
                    if die_left == 0:
                        die_left = 6
                    cur_roll = self.roll_die(die_left)
                    print(cur_roll)
                    if self.is_bust(cur_roll):
                        print("Bust!")
                        turn_over = True
            else:
                print("Player " + str(player_num) + " returned an invalid keep!...")
                print("Die kept were " + str(kept_die) + " out of " + str(cur_roll) + ", while player had " +
                      str(self.cur_scores[player_num] + cur_turn_score) + " points, and player stopping: " + str(stopping))
                turn_over = True

    def play_game(self):
        turn_count = 0
        while not self.game_over():
            self.give_turn(self.cur_player)
            self.cur_player = (self.cur_player + 1) % len(self.players)
            print("Current Scores: " + str(self.cur_scores))
            turn_count += 1
        # Give everyone else a final turn
        for i in range(len(self.players)):
            self.give_turn(self.cur_player)
            self.cur_player = (self.cur_player + 1) % len(self.players)
            print(self.cur_scores)
            turn_count += 1
        winner = max(self.cur_scores, key=self.cur_scores.get)
        print("Game Over after " + str(turn_count // 4) + " rounds!")
        print("Player " + str(winner) + " won!")

def main():
    game = Game()
    game.play_game()

if __name__ == '__main__':
    main()