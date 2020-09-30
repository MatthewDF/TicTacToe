#!/usr/bin/env python3

import sys
from art import *


# A game where two players enter their names and take turns placing their game piece, an X or O, on a 3x3 grid.
# A player wins when they have three of their pieces in a row!


class Player:

    def __init__(self, name, x_or_o):
        self.name = name
        self.gamepiece = x_or_o
        # input variable that will store the grid intersection choice of the current player, I.G., 'A2' or 'C3'
        self.input = None
        # After input is broken down into its components (an a, b or c, and a 1, 2, or 3), it is stored in 'choice'
        # so that it can be accessed for grid_data
        self.choice = []


class GameData:
    # Class for organizing and storing game variables

    def __init__(self, grid_data):
        self.grid_data = grid_data

    # Every grid intersection has a starting value of '_' and should be replaced by game functions with either an X or O
    grid_data = {
        "a": {1: "_", 2: "_", 3: "_"},
        "b": {1: "_", 2: "_", 3: "_"},
        "c": {1: "_", 2: "_", 3: "_"}
    }

    def draw(draw_object):
        draw_dict = {"Intro": text2art("Tic, Tac, Toe!!"),
                     "Prompt": "Enter your grid choice (A1, B3, C2, etc): ",
                     }

        if draw_object == "Grid":
            # Blank spaces for spacing
            bsp = " "
            times = 37

            gd = GameData.grid_data
            print(times*bsp + " " + " " + "1" + " " + "2" + " " + "3" + " ")
            print(times*bsp + f"A|{gd['a'][1]}|{gd['a'][2]}|{gd['a'][3]}|")
            print(times*bsp + f"B|{gd['b'][1]}|{gd['b'][2]}|{gd['b'][3]}|")
            print(times*bsp + f"C|{gd['c'][1]}|{gd['c'][2]}|{gd['c'][3]}|")
            print("")

        elif draw_object in draw_dict:
            print(draw_dict[draw_object])

        else:
            print(draw_object)


def grid_update(current_player):
    # Collect current_player, prompt for input, process input as their 'choice', then update grid with their 'choice'

    gd = GameData.grid_data
    draw = GameData.draw
    prompt = "Prompt"
    grid = "Grid"

    # Clear choice and input from current player
    current_player.choice = []
    current_player.input = None

    # List of acceptable alpha and numeric values for grid
    # grid_values_alpha = ['a', 'b', 'c']
    # grid_values_num = [1, 2, 3]
    grid_values_accptbl = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']

    print(f"{current_player.name}, please place your {current_player.gamepiece}! ")
    draw(grid)
    draw(prompt)
    current_player.input = input()

    while True:
        if current_player.input == "ABORT":
            print("Aborting")
            sys.exit()

        elif current_player.input.upper() in grid_values_accptbl and current_player.input is not ("" or " "):
            break

        else:
            print("Incorrect input. Valid input: A1, A2, A3, B1, B2, B3, C1, C2, or C3.")
            print("Input: ")
            current_player.input = input()

    # Convert player input into a list of two values (1 alpha, 1 num) to be used for placing their piece onto the grid
    for grid_point in current_player.input:
        if grid_point.isdigit():
            current_player.choice.append(int(grid_point))
        else:
            current_player.choice.append(grid_point.lower())

    grid_key_value1 = current_player.choice[0]
    grid_key_value2 = current_player.choice[1]

    # if grid_key_value1 not in grid_values_alpha:
    #     print(f"You can't place that there! Please select another location for your {current_player.gamepiece}:")
    #     grid_update(current_player)
    # elif grid_key_value2 not in grid_values_num:
    #     print(f"You can't place that there! Please select another location for your {current_player.gamepiece}:")
    #     grid_update(current_player)

    # Both key values are valid. Assign grid key intersection for examining
    grid_key_intersection = gd[grid_key_value1][grid_key_value2]

    # Error tracking
    # print("current_player.input ", current_player.input)
    # print("current_player.choice ", current_player.choice)
    # print("grid_key_value1: ", grid_key_value1)
    # print("grid_key_value2: ", grid_key_value2)
    # print("grid_key_intersection ", grid_key_intersection)

    while True:
        if grid_key_intersection == '_':
            gd[grid_key_value1][grid_key_value2] = current_player.gamepiece
            break
        else:
            print(f"You can't place that there! Please select another location for your {current_player.gamepiece}:")
            return grid_update(current_player)


def grid_coordinates_shift_by(alpha, num, shift_by):
    # Receives an alpha, a num, and a value in which to shift by. Conducts the shift and then returns the result

    values_alpha = ['a', 'b', 'c', None]
    values_num = [1, 2, 3, None]
    values_shift = [-2, -1, 0, 1, 2]

    if alpha not in values_alpha:
        sys.exit("Error. coord_shift() called and passed an alpha value that wasn't a, b, c, or None")

    if num not in values_num:
        sys.exit("Error. coord_shift() called and passed a number value that wasn't 1, 2, 3, or None")

    if shift_by not in values_shift:
        sys.exit("Error. coord_shift() called and passed a shift value that wasn't -2, -1, 0, 1, or 2")

    if alpha is None:
        pass
    else:
        alpha = chr(ord(alpha)+shift_by)

    if num is None:
        pass
    else:
        num = num + shift_by

    if alpha is None:
        if num is not None:
            return num
        else:
            print("Error. Both alpha and num in coord_shift() are set to None. Nothing to return")
            return
    elif alpha is not None:
        if num is None:
            return alpha
        elif alpha is not None and num is not None:
            return alpha, num


def is_winner(current_player, grid_data):
    # Check to see if a victory condition has been met, and by who

    last_piece_pos = current_player.choice
    list_of_players_pieces = []
    winner = False
    empty_grid = "_"

    # Error tracking
    # print("Player: ", current_player.name)
    # print(grid_data)
    # print(last_piece_pos)

    # For the current player, make a list of grid locations where that player's pieces are
    for alpha, values in grid_data.items():
        for num in values.keys():
            if grid_data[alpha][num] == current_player.gamepiece:
                list_of_players_pieces.append((alpha, num))

    for piece_loc in list_of_players_pieces:
        origin_alpha = piece_loc[0]
        origin_num = piece_loc[1]

        for playersPiece_in_list in list_of_players_pieces:

            # Create a separate variable for each origin (alpha and num) and shift by +1, +2, -1, -2
            # By doing this we can represent the maximum value from A1 to C3. Values outside of this will fail
            # to compare.

            # +1, +2
            origin_alpha_plus1 = grid_coordinates_shift_by(origin_alpha, None, 1)
            origin_alpha_plus2 = grid_coordinates_shift_by(origin_alpha, None, 2)
            origin_num_plus1 = grid_coordinates_shift_by(None, origin_num, 1)
            origin_num_plus2 = grid_coordinates_shift_by(None, origin_num, 2)

            origin_alpha_minus1 = grid_coordinates_shift_by(origin_alpha, None, -1)
            origin_alpha_minus2 = grid_coordinates_shift_by(origin_alpha, None, -2)
            origin_num_minus1 = grid_coordinates_shift_by(None, origin_num, -1)
            origin_num_minus2 = grid_coordinates_shift_by(None, origin_num, -2)

            # In list_of_player_pieces we have each game piece that player has placed on the grid.
            # We'll take each piece on the board and shift to see if there is another piece of the same player's
            # adjacent to it.
            if (origin_alpha_plus1, origin_num) in list_of_players_pieces and winner is False:

                # Since we found a match that means that the player has two pieces next to each other. Now we'll repeat
                # our shift (in this case origin_alpha was upgraded by +1, so we'll try +2) and see if another match
                # exists. If so, victory!
                if (origin_alpha_plus2, origin_num) in list_of_players_pieces and winner is False:
                    winner = True
                    break

            if (origin_alpha, origin_num_plus1) in list_of_players_pieces and winner is False:

                if (origin_alpha, origin_num_plus2) in list_of_players_pieces and winner is False:
                    winner = True
                    break

            if (origin_alpha_plus1, origin_num_plus1) in list_of_players_pieces and winner is False:

                if (origin_alpha_plus2, origin_num_plus2) in list_of_players_pieces and winner is False:
                    winner = True
                    break

            # Now checking negative shifts to go backwards
            if (origin_alpha_minus1, origin_num) in list_of_players_pieces and winner is False:

                if (origin_alpha_minus2, origin_num) in list_of_players_pieces and winner is False:
                    winner = True
                    break

            if (origin_alpha, origin_num_minus1) in list_of_players_pieces and winner is False:

                if (origin_alpha, origin_num_minus2) in list_of_players_pieces and winner is False:
                    winner = True
                    break

            if (origin_alpha_minus1, origin_num_minus1) in list_of_players_pieces and winner is False:

                if (origin_alpha_minus2, origin_num_minus2) in list_of_players_pieces and winner is False:
                    winner = True
                    break

    # Check for draw
    list_of_blank_spaces = []
    for alpha, values in grid_data.items():
        for num in values.keys():
            if grid_data[alpha][num] == "_":
                list_of_blank_spaces.append((alpha,num))
                # print(list_of_blank_spaces)

    if not list_of_blank_spaces:
        print(f"grid_data: {grid_data}")
        print(f"List of blank spaceS: {list_of_blank_spaces}")
        print("Game over! It's a draw.")
        sys.exit()

    if winner is True:
        GameData.draw("Grid")
        print(f"Congratulations {current_player.name}, you win!")
        sys.exit()


def main():
    draw = GameData.draw
    gd = GameData.grid_data

    # Game states
    game_over = False
    player1_turn = False
    player2_turn = False
    current_player = None

    # Draw objects
    intro = "Intro"
    grid = "Grid"
    prompt = "Prompt"

    # Game initialization
    draw(intro)

    name = input("Please enter player 1's name: ")
    player1 = Player(name, "X")
    name = input("Thanks! Now please enter player 2's name: ")
    player2 = Player(name, "O")
    print(f"{player1.name} has {player1.gamepiece}'s, and {player2.name} has {player2.gamepiece}'s!")

    print(text2art("Ready? Let's begin!"))
    print(f"{player1.name} goes first.")
    player1_turn = True

    # Primary game loop
    while game_over is False:
        if player1_turn is True:
            current_player = player1
            player1_turn = False
            player2_turn = True
        elif player2_turn is True:
            current_player = player2
            player2_turn = False
            player1_turn = True
        elif player1_turn is False and player2_turn is False:
            print("Error - It is neither P1 or P2's turn")

        # Send current_player, collect user input, process their input as their choice, and if valid, update the grid
        grid_update(current_player)

        if current_player.input == "ABORT":
            break
        elif current_player.input == "TEST":
            current_player.input = ""
            current_player.choice = []
            is_winner(current_player, gd)

        is_winner(current_player, gd)


if __name__ == "__main__":
    main()