"""
Wordle Game in French : https://www.nytimes.com/games/modle/index.html
Modle
By @camille-cmd
https://github.com/Camille-cmd
"""

import argparse
import sys
import time

from colorama import init, Fore, Style

from models import Modle

# Reset style at the end of each print for colorama
init(autoreset=True)

# Initiate the parser
parser = argparse.ArgumentParser()
parser.add_argument("-god", "--godmode", help="Launch the game with godmode", action="store_true")
args = parser.parse_args()


def start_game():
    """
    Start the modle game
    """
    print(Style.BRIGHT + "Devines en 6 essais le mot")
    print("")

    # Init game
    modle = Modle()

    # Handle parameters
    if args.godmode:
        # In godmode, print the solution right away
        print(modle.game.word_to_guess)

    # Used to prevent game from re-printing last word after and error
    skip_modle = False

    while modle.game.tries > 0:

        # Display the modle grid
        if not skip_modle:
            modle.display_modle()

        skip_modle = False

        # Ask for user to give a word
        guess = input("Ta proposition : ")
        guess = guess.upper()

        # Check if the word is valid
        if not modle.clean_guess(guess):
            skip_modle = True
            continue

        # Check if the user won
        if modle.game.is_guess_correct_word(guess):
            modle.display_win(guess)
            modle.share_results()
            if modle.new_game():
                start_game()
            else:
                sys.exit()

        # Check the inputted word
        modle.analyze_guess(guess)

        # End of rounds, remove a try
        modle.game.remove_tries(1)

        time.sleep(1)

        # delete all lines for them to be re-display with the last guessed word
        modle.delete_multiple_lines(10)

    # End the game if we ran out of tries
    if modle.game.out_of_tries:
        # display one last time
        modle.display_modle()
        modle.delete_multiple_lines(1)
        if modle.try_again():
            start_game()
        else:
            sys.exit()


if __name__ == '__main__':
    print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "Bienvenue dans Modle")
    print(Style.DIM + "tape q pour quitter le jeu")
    print("")
    start_game()
