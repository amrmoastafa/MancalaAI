"""
this file contains some helper functions and classes to use

"""


class State:
    """
    a class to handle state data (turn, steal, game_state)
    """

    def __init__(self, human_player_turn, steal):
        """
        initialize our class variables
        :param human_player_turn: { 1: human turn, 0: AI turn}
        :param steal: 1: Stealing mode is activated
        """
        self.steal = steal
        self.human_player_turn = human_player_turn
        self.game_state = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]


def get_actions(state: State):
    """
    get allowed actions for a the player,
    given the current state of the game
    :param state: current state of the game
    :return: allowed actions
    """

    if state.human_player_turn:
        return [i for i, v in enumerate(state.game_state[0:6]) if v > 0]
    else:
        return [i + 7 for i, v in enumerate(state.game_state[7:13]) if v > 0]


def next_state(state: State, slot_number):
    """
    given a state and a slot number (Action), get the next state
    :param state: current state of the game
    :param slot_number: action to do
    :return: new_state
    """
    # get steal value
    steal = state.steal
    import copy
    # copy the current state
    new_state = copy.deepcopy(state)
    # get the number of stones in this slot
    stones = new_state.game_state[slot_number]
    # the new number of stones in that slot will be zero
    new_state.game_state[slot_number] = 0

    # loop through the next slots and distribute them till the number of stones is 0
    while stones > 0:
        slot_number += 1
        if state.human_player_turn and slot_number == 13:
            slot_number = 0
        elif not state.human_player_turn:
            if slot_number == 14:
                slot_number = 0
            elif slot_number == 6:
                slot_number = 7
        new_state.game_state[slot_number] += 1
        stones -= 1

    # max slot_number for Human Player is 5, for AI is 12
    if not (new_state.human_player_turn and slot_number == 6) and not (
            not new_state.human_player_turn and slot_number == 13):

        # add stealing
        if steal:
            # steal for human player
            if new_state.human_player_turn and 0 <= slot_number <= 5 and new_state.game_state[slot_number] == 1:
                # position of the opposite slot
                opp_slot_pos = 13 - (slot_number + 1)
                # the score now is increased by the number of stones in that slot and the opposite one
                new_state.game_state[6] += new_state.game_state[opp_slot_pos] + new_state.game_state[slot_number]

                # the number of stones in those 2 slot will be zero
                new_state.game_state[opp_slot_pos], new_state.game_state[slot_number] = 0, 0

            # steal for AI player
            elif not new_state.human_player_turn and 7 <= slot_number <= 12 and new_state.game_state[slot_number] == 1:
                # position of the opposite slot
                opp_slot_pos = 13 - (slot_number + 1)
                # the score now is increased by the number of stones in that slot and the opposite one
                new_state.game_state[13] += new_state.game_state[opp_slot_pos] + new_state.game_state[slot_number]
                # the number of stones in those 2 slot will be zero
                new_state.game_state[opp_slot_pos], new_state.game_state[slot_number] = 0, 0

        # Reverse turn
        new_state.human_player_turn = not new_state.human_player_turn

    return new_state


def game_off(state: State):
    """
    Check if the game is finished or not, calculate the final score

    :param state: the current state of the game
    :return: true if finished, false if not
    """
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


def s_print(state: State):
    """
    print the state of the game at a given state
    :param state: state of the game
    """
    # check if the game is finished
    if not game_off(state):
        print("-----------------------------------------------")
        if state.human_player_turn:
            print("    Your turn    ")
        else:
            print("    AI turn    ")
        print("=====================")
        # AI player slots
        states = state.game_state[7:13]
        states.reverse()
        print(*states, sep=" | ")
        # AI player & human Player scores
        print("---------------------")
        print(str(state.game_state[13]) + "                   " + str(state.game_state[6]))
        print("---------------------")
        # Human Player States
        print(*state.game_state[0:6], sep=" | ")
        print("=====================\nAvailable Actions: " + str(get_actions(state)))

    # if the game is finished, print the scoreboard
    else:
        print("-----------------------------------------------")
        print("    The Game is Over    ")
        print("=====================")
        print(" Scoreboard:")
        score = state.game_state.copy()
        print("   You: " + str(score[6]) + "\n   AI: " + str(score[13]))
        print("=====================")
