# game_state = {other_scores : [1, 2, 3], on_the_board : False, roll : {score_taken: 100, last_roll: [3,5,2]} }

class HotDieBot():
    def __init__(self):
        self.current_score = 0

    # The game_state will contain a 'last_roll' list
    # take_turn returns a list of indexes from last_roll that you would like to re-roll
    def take_turn(self, game_state):
        if game_state.on_the_board:
            return self.get_on_the_board_strat(game_state)
        else:
            return self.normal_strat(game_state)

    # Always takes 1's and 5's until 1000 points
    def get_on_the_board_strat(self, game_state):
        to_re_roll = []
        if game_state.score_taken >= 1000:
            return to_re_roll
        else:
            for i,value in enumerate(game_state.last_roll):
                if value != 1 and value != 5:
                    to_re_roll.append(i)
        return to_re_roll

    # Always takes 1's and 5's until 300 points
    def normal_strat(self, game_state):
        to_re_roll = []
        if game_state.score_taken >= 300:
            return to_re_roll
        else:
            for i, value in enumerate(game_state.last_roll):
                if value != 1 and value != 5:
                    to_re_roll.append(i)
        return to_re_roll



