"""
Modle base classes to run the game and display elements to the user
ModleGame: game logic
Modle: game display
"""
import _tkinter
import random
import string
import sys
import time
from dataclasses import dataclass
from distutils.util import strtobool
from tkinter import Tk

from colorama import Fore, Style, Back


@dataclass
class ModleGame:
    """
    Modle game logic
    """
    word_to_guess: str
    words_list: list
    guessed_words: list
    tries: int
    letters_yellow = list
    letters_green = list
    letters_grey = list
    final_output = str

    def __init__(self):
        self.pick_word()
        self.guessed_words = []
        self.tries = 6
        self.letters_yellow = []
        self.letters_green = []
        self.letters_grey = []
        self.final_output = ""

    def pick_word(self):
        """Select a random word from the list in the words.txt file"""
        with open("./words.txt", "r") as file:
            file_content = file.read()
            words = list(map(str, file_content.split()))

        self.word_to_guess = random.choice(words).upper()
        self.words_list = words

    def analyze_guess(self, guess: str):
        """
        Define which letters in the guess are correct, at correct place or not
        :param guess: user input to guess the word
        """
        # for each letter, attribute color depending on the position in the word to guess
        word_output = []
        for index, letter in enumerate(guess):
            if letter in self.word_to_guess:
                if self.word_to_guess.find(letter, index) == index:
                    word_output.append(Style.BRIGHT + Fore.GREEN + letter)
                    self.letters_green.append(letter)
                    self.final_output += "🟩"
                else:
                    # if the guess has several time the same letter and our word not
                    if guess.count(letter) > self.word_to_guess.count(letter):
                        word_output.append(Style.BRIGHT + Fore.LIGHTBLACK_EX + letter)
                        self.letters_grey.append(letter)
                        self.final_output += "⬛"
                    else:
                        word_output.append(Style.BRIGHT + Fore.YELLOW + letter)
                        self.letters_yellow.append(letter)
                        self.final_output += "🟨"
            else:
                word_output.append(Style.BRIGHT + Fore.LIGHTBLACK_EX + letter)
                self.letters_grey.append(letter)
                self.final_output += "⬛"
        self.final_output += "\n"
        self.guessed_words.append(word_output)

    def is_guess_correct_word(self, guess: str):
        """
        Check if the user word is the word to guess
        :param guess:
        :return: bool
        """
        guess = guess.upper()
        return guess == self.word_to_guess

    def remove_tries(self, number: int):
        """Remove a n number of tries"""
        self.tries -= number

    @property
    def out_of_tries(self):
        """
        Check if the user still has tries left
        :return:bool
        """
        return self.tries == 0

    def get_all_letters(self):
        """
        Get all letters from the alphabet and attribute the colors according to
        what has already been guessed
        :return: list of all letters
        """
        letters = []
        for letter in list(string.ascii_uppercase):
            if letter in self.letters_green:
                letters.append(Fore.GREEN + letter)
            elif letter in self.letters_yellow:
                letters.append(Fore.YELLOW + letter)
            elif letter in self.letters_grey:
                letters.append(Fore.LIGHTBLACK_EX + letter)
            else:
                letters.append(Fore.WHITE + letter)
        return letters

    def get_final_output(self):
        """
        Return the final output with only colors of letters in guesses
        for it to be copies in the clipboard
        :return: text
        """
        text = f"Modle {len(self.guessed_words) + 1}/6\n"
        self.final_output += "🟩" * 5
        text += self.final_output
        return text


class Modle:
    """
    Modle game display
    """

    def __init__(self):
        self.game = ModleGame()

    def display_modle(self):
        """
        Display the black square corresponding to the tries left and fill the first lines with
        the already tries words. Add the last tried word letter by letter
        """
        # Add already tried words
        for word in self.game.guessed_words[:-1]:
            print(" " * 10, *word)

        # Add lines with black square for the remaining possible guesses
        for _ in range(0, self.game.tries):
            print(" " * 10, Fore.LIGHTBLACK_EX + "■ " * 5)

        # Add last tried word
        if self.game.guessed_words:
            # Line that will be overridden by the last word
            print(" " * 10, Fore.LIGHTBLACK_EX + "■ " * 5)

            # Move cursor up to the first line still with black squares
            sys.stdout.write("\x1b[1A" * (self.game.tries + 1))

            print(" " * 10, end=" ")
            for letter in self.game.guessed_words[-1]:
                print(letter, end=" ")
                time.sleep(0.5)

            # move cursor back down to the next proposition input
            sys.stdout.write("\x1b[1B" * (self.game.tries + 1))

        self.display_all_letters()

        print("")

    def display_all_letters(self):
        """
        Display all letters with already found ones in corresponding colors
        (found, almost found, not tried, not in word)
        """
        print("")
        letters = self.game.get_all_letters()
        print(*letters)

    @staticmethod
    def delete_multiple_lines(number_of_lines: int = 1):
        """
        Delete the last line in the STDOUT.
        :param number_of_lines: how many lines to delete
        """
        for _ in range(number_of_lines):
            sys.stdout.write("\x1b[1A")  # cursor up one line
            sys.stdout.write("\x1b[2K")  # delete the last line

    def handle_guess_error(self, text_to_print: str):
        """
        Print the test and delete it + the input before
        :param text_to_print:
        """
        print(text_to_print)
        time.sleep(2)
        self.delete_multiple_lines(2)

    def clean_guess(self, guess: str):
        """
        Check if the guess can be admitted as a valid guess
        :param guess:
        :return: bool
        """
        if guess.lower() == "q":
            sys.exit()

        if guess.lower() == "godmode":
            self.handle_guess_error(self.game.word_to_guess)
            return False

        if len(guess) != 5:
            self.handle_guess_error("Ce sont des mots de 5 lettres")
            return False

        if guess.lower() not in self.game.words_list:
            self.handle_guess_error("Nous ne connaissons pas ton mot")
            return False

        return True

    def display_win(self, guess: str):
        """
        If the user found the correct word, display the letters all in green
        :param guess:
        """
        # Move cursor up to the first line still with black squares
        sys.stdout.write("\x1b[1A" * (self.game.tries + 4))

        # Display the correct word in the modle grid
        print(" " * 10, end=" ")
        for letter in guess:
            print(Style.BRIGHT + Fore.GREEN + letter, end=" ")
            time.sleep(0.5)

        # move cursor back down
        sys.stdout.write("\x1b[1B" * (self.game.tries + 4))
        self.delete_multiple_lines(1)
        print("\r     " + Back.GREEN + Fore.BLACK + "Bravo!" + Style.RESET_ALL + " 🎉")

    def analyze_guess(self, guess: str):
        """Analyse the guess and attribute the correct colors to the letters"""
        self.game.analyze_guess(guess)

    @staticmethod
    def copy_to_clipboard(txt: str):
        """Instantiate a Tk() object to clip string in argument."""
        tk_handle = Tk()
        tk_handle.withdraw()
        tk_handle.clipboard_clear()
        tk_handle.clipboard_append(txt)
        print("\nResultats copiés dans le presse-papier! \n")

    @staticmethod
    def prompt_bool(text):
        """Ask for the user to enter a yes/no input and asks until it is correct"""
        print("")
        while True:
            user_input = input(f"{text} (Y/N)")
            try:
                return strtobool(user_input)
            except ValueError:
                continue

    def try_again(self):
        """
        Ask the user if he/she wants to try again
        :return: bool
        """
        print(f"Le mot à deviner était: {Style.BRIGHT + Fore.BLUE + self.game.word_to_guess}")
        return self.prompt_bool("Try again ?")

    def share_results(self):
        """
        Ask the user to share results
        copy results to clipboard if yes
        """
        print("")
        share_results = self.prompt_bool("Partager le resultat ?")
        print("")
        if share_results:
            output = self.game.get_final_output()
            try:
                self.copy_to_clipboard(output)
            except _tkinter.TclError:
                # Some old python versions do not work correctly with TK
                print(output)

    @staticmethod
    def new_game():
        """
        Ask the user if he/she wants to start a new game
        :return: bool
        """
        return Modle.prompt_bool("Nouveau jeu ?")
