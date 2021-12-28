from collections import Counter

# Passed current turn score, all players scores, and current roll (assuming you didn't bust)

# Must contain the method take_turn, which takes in these items and returns a list representing
# the die values you would like keep, and whether you are stopping or not

class HotDieBot():
    def __init__(self):
        self.current_score = 0

    # take_turn returns a list of dice values from the roll that we would like to keep
    def take_turn(self, roll, turn_score, all_scores):
        if self.current_score < 1000:
            return self.get_on_the_board_strat(roll, turn_score)
        else:
            return self.normal_strat(roll, turn_score)

    # Always takes 1's and 5's until 1000 points
    def get_on_the_board_strat(self, roll, turn_score):
        to_keep = []
        if turn_score >= 1000:
            self.current_score += turn_score
            return [to_keep, True]
        else:
            for value in roll:
                if value == 1 or value == 5:
                    to_keep.append(value)
        roll_points = self.count_points(to_keep)
        if len(to_keep) > 0 and roll_points + turn_score < 1000:
            return [to_keep, False]
        else:
            self.current_score += roll_points + turn_score
            return [to_keep, True]

    # Always takes 1's and 5's until 300 points
    def normal_strat(self, roll, turn_score):
        to_keep = []
        if turn_score >= 300:
            self.current_score += turn_score
            return [to_keep,True]
        else:
            for value in roll:
                if value == 1 or value == 5:
                    to_keep.append(value)
        roll_points = self.count_points(to_keep)
        if len(to_keep) > 0 and roll_points + turn_score < 300:
            return [to_keep, False]
        else:
            self.current_score += roll_points + turn_score
            return [to_keep, True]

    def is_hot_die(self, roll):
        if sorted(roll) == [1,2,3,4,5,6]:
            return True
        if all([n == 2 for k,n in Counter(roll).items()]) and len(roll) == 6:
            return True
        return False

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
