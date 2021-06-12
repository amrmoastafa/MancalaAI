

class AI:

    def __init__(self, depth=5):

        self.init_depth = depth

    def utility_func(self, state: State):

        utility = state.game_state[13] - state.game_state[6]
        return utility

    def minimax_alpha_beta_pruning(self, state: State):

        utility = []
        alpha = - math.inf
        beta = math.inf
        # loop over each available action and recursively consider it as root to the game tree
        # recursively build the tree of actions to the given depth
        for action in Util_file.get_actions(state):
            # get next state given the current state
            new_state = Util_file.next_state(state, action)
            if new_state.human_player_turn:
                utility.append(
                    (self.min_val(new_state, alpha, beta, self.init_depth), action))
            else:
                utility.append((self.max_val(new_state, alpha, beta, self.init_depth), action))

        if state.human_player_turn:
            final_action = min(utility)[1]
        else:
            final_action = max(utility[1])

        print("Action chosen by AI: ", final_action)
        return final_action

    def max_val(self, state: State, alpha, beta, depth=3):

        # if the game ended or the depth is 0, return utility value
        if Util_file.game_off(state) or depth == 0:
            return self.utility_func(state)
        # set min value to be - infinity
        val = - math.inf
        # loop over each available action and recursively consider it as root to the game tree
        # recursively build the tree of actions to the given depth
        for action in Util_file.get_actions(state):
            new_state = Util_file.next_state(state, action)

            if new_state.human_player_turn:
                val = max(val, self.min_val(new_state, alpha, beta, depth - 1))
            else:
                val = max(val, self.max_val(new_state, alpha, beta, depth - 1))
            # pruning
            if val >= beta:
                return val
            # reset alpha
            alpha = max(alpha, val)
        return val

    def min_val(self, state: State, alpha, beta, depth=3):

        if Util_file.game_off(state) or depth == 0:
            return self.utility_func(state)

        val = math.inf
        # loop over each available action and recursively consider it as root to the game tree
        # recursively build the tree of actions to the given depth
        for action in Util_file.get_actions(state):
            new_state = Util_file.next_state(state, action)
            if state.human_player_turn:
                val = min(val, self.max_val(new_state, alpha, beta, depth - 1))
            else:
                val = min(val, self.min_val(new_state, alpha, beta, depth - 1))

            if val <= alpha:
                return val
            beta = min(beta, val)
        return val
