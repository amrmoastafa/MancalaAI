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