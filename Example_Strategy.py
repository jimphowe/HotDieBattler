# Passed current turn score, all players scores, and current roll (assuming you didn't bust)

# Must contain the method take_turn, which takes in these items and returns a list representing
# the die values you would like keep

class HotDieBot():
    def __init__(self):
        self.current_score = 0

    # take_turn returns a list of dice values from the roll that we would like to keep
    def take_turn(self, roll, turn_score, all_scores):
        if self.current_score > 1000:
            return self.get_on_the_board_strat(roll, turn_score)
        else:
            return self.normal_strat(roll, turn_score)

    # Always takes 1's and 5's until 1000 points
    def get_on_the_board_strat(self, roll, turn_score):
        to_keep = []
        if turn_score >= 1000:
            return to_keep
        else:
            for value in roll:
                if value == 1 or value == 5:
                    to_keep.append(value)
        return to_keep

    # Always takes 1's and 5's until 300 points
    def normal_strat(self, roll, turn_score):
        to_keep = []
        if turn_score >= 300:
            return to_keep
        else:
            for value in roll:
                if value == 1 or value == 5:
                    to_keep.append(value)
        return to_keep



