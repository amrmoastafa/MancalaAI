from AI import AI
from Util_file import State
import Util_file
import time
import sys
import random


class Game:
    def __init__(self):
        """
        initialize our class variables
        """

        # state (human_player_turn, steal)
        self.state = State(True, 1)
        # default value for AI Depth
        self.depth = 3
        # initialize AI model
        self.ai = None
        # default value for stealing is True
        self.Is_steal = 1
        # first player to start is by default the human player
        self.turn = 1

    def set_up(self):
        """
         perform inital setup for the Game
        """
        print(" ==========================    Welcome to Mancala       ==========================")
        self.Is_steal = int(input(" ====== Enter '1' for stealing mode and '0' otherwise =======  : "))
        turn = int(input(" ====== Enter '1' to start first, Enter'0' otherwise ======  : "))
        self.turn = True if turn == 1 else False
        self.state = State(self.turn, self.Is_steal)
        print(" ====== Enter Difficulty Level ====== : ")
        self.depth = 2 + int(input(" (Easy -> 0, Medium -> 1, Hard -> 2, Very hard -> 3) :  ")) * 2
        self.ai = AI(self.depth)
        print("Setting up game...")

    def game_on(self):
        """
        the main function controlling our code, loop until the game is finished and one of the players wins:
         - take the slot number of the player and perform this action
         - perform the AI action returned by our AI algorithm

        :return: new state after each move of a player
        """
        # get initial state of the player
        Util_file.s_print(self.state)
        # loop until the game is finished and one of the players wins
        while not Util_file.game_off(self.state):
            # human_player_turn
            if self.state.human_player_turn:
                slot_number = int(input("Please enter your action : "))
                # get next state after perform this action by calling our util function (next_state)
                self.state = Util_file.next_state(self.state, slot_number)
            # AI Turn
            else:
                # alpha_beta
                # get next state after perform this action by calling our util function
                # (next_state) and the slot number is determined by our mini_max_alpha_beta algorithm
                self.state = Util_file.next_state(self.state, self.ai.minimax_alpha_beta_pruning(self.state))
            # print state after this action
            Util_file.s_print(self.state)


