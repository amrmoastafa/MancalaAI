class State:

    def __init__(self, human_player_turn, steal):
        self.steal = steal
        self.human_player_turn = human_player_turn
        self.game_state = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]


def get_actions(state: State):
    if state.human_player_turn:
        return [i for i, v in enumerate(state.game_state[0:6]) if v > 0]
    else:
        return [i + 7 for i, v in enumerate(state.game_state[7:13]) if v > 0]


def game_off(state: State):
    # if the human player slots is empty, he has lost
    if sum(state.game_state[0:6]) == 0:
        # calculate the final score (accumulate the remaining stones in the AI player slots to its score)
        state.game_state[13] += sum(state.game_state[7:13])

        return True

    # if the AI player slots is empty, the human player has won
    elif sum(state.game_state[7:13]) == 0:
        # calculate the final score (accumulate the remaining stones in the Human player slots to its score)
        state.game_state[6] += sum(state.game_state[0:6])

        return True

    else:
        return False
