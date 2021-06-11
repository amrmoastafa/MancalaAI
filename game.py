import time
import sys
import random


class Game:
    def __init__(self):

        self.state = State(True, 1)
        self.depth = 3
        self.ai = None
        self.Is_steal = 1
        self.turn = 1

    def set_up(self):

        self.Is_steal = int(input(" ====== Enter '1' for stealing mode and '0' otherwise =======  : "))
        turn = int(input(" ====== Enter '1' to start first, Enter'0' otherwise ======  : "))
        self.turn = True if turn == 1 else False
        self.state = State(self.turn, self.Is_steal)
        print(" ====== Enter Difficulty Level ====== : ")
        self.depth = 2 + int(input(" (Easy -> 0, Medium -> 1, Hard -> 2, Very hard -> 3) :  ")) * 2
        self.ai = AI(self.depth)

    def game_on(self):

        Util_file.s_print(self.state)
        while not Util_file.game_off(self.state):
            if self.state.human_player_turn:
                slot_number = int(input("Please enter your action : "))
                self.state = Util_file.next_state(self.state, slot_number)

            else:
                self.state = Util_file.next_state(self.state, self.ai.minimax_alpha_beta_pruning(self.state))
            Util_file.s_print(self.state)


def print(state: State):

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
