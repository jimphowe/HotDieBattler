from collections import Counter

# Passed current turn score, all players scores, and current roll (assuming you didn't bust)

# Must contain the method take_turn, which takes in these items and returns a list representing
# the die values you would like keep, and whether you are stopping or not

class HotDieBot():
    def __init__(self):
        self.current_score = 0

    # take_turn returns a list of dice values from the roll that we would like to keep
    def take_turn(self, roll, turn_score, all_scores):
        on_board = self.current_score + turn_score > 1000
        return self.full_strat(roll, turn_score, on_board)

    def full_strat(self, roll, turn_score, on_board):
        take_able = self.all_take_able(roll)
        take_able_points = self.count_points(take_able)
        # For 1,2,3 die, always go around the corner if we can
        # If not, take whatever points there are and continue only if not at 1000pts
        if len(roll) in [1,2,3]:
            if self.can_take_all(roll):
                # Around the corner wooooo
                return [roll,False]
            elif on_board:
                self.current_score += turn_score + take_able_points
                return [take_able,True]
            else:
                if turn_score + take_able_points < 1000:
                    return [take_able,False]
                else:
                    self.current_score += turn_score + take_able_points
                    return [take_able,True]
        # For 4 die, always go around the corner if we can
        # If not, if taking everything would put us at 250+, do that
        # Otherwise, take a single 1 or 5 and roll the other 3
        elif len(roll) == 4:
            if self.can_take_all(roll):
                return [roll,False]
            elif on_board:
                if turn_score + take_able_points > 200:
                    return [take_able,True]
                else:
                    if 1 in roll:
                        return [[1],False]
                    else:
                        return [[5],False]
            else:
                if turn_score + take_able_points < 1000:
                    return [take_able,False]
                else:
                    self.current_score += turn_score + take_able_points
                    return [take_able, True]
        # For 4 die, always go around the corner if we can
        # If not, if taking everything would put us at 350+, do that
        # Otherwise, take a single 1 or 5 and roll the other 4
        elif len(roll) == 5:
            if self.can_take_all(roll):
                return [roll,False]
            elif on_board:
                self.current_score += turn_score + take_able_points
                return [take_able,True]
            else:
                if turn_score + take_able_points < 1000:
                    return [take_able, False]
                else:
                    self.current_score += turn_score + take_able_points
                    return [take_able, True]
        elif len(roll) == 6:
            if self.can_take_all(roll):
                return [roll, False]
            elif on_board:
                self.current_score += turn_score + take_able_points
                return [take_able, True]
            else:
                if turn_score + take_able_points < 1000:
                    return [take_able, False]
                else:
                    self.current_score += turn_score + take_able_points
                    return [take_able, True]

    def all_take_able(self,roll):
        take_able = []
        if self.can_take_all(roll):
            return roll
        c = Counter(roll)
        for k, n in c.items():
            if n > 2:
                roll = [num for num in roll if num != k]
                for i in range(n):
                    take_able.append(k)
        for val in roll:
            if val == 1 or val == 5:
                take_able.append(val)
        return take_able

    def can_take_all(self, roll):
        if self.is_hot_die(roll):
            return True
        c = Counter(roll)
        for k, n in c.items():
            if n > 2:
                roll = [num for num in roll if num != k]
        if len(roll) == 0:
            return True
        if self.all_one_or_five(roll):
            return True
        return False



    def all_one_or_five(self, roll):
        return all(elem in [1,5] for elem in roll)

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
