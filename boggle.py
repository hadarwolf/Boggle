import tkinter as tk
from tkinter import messagebox
import boggle_board_randomizer
from class_bogglemine import *
import time
from PIL import Image, ImageTk


class Boogle_board:
    """
    Class representing the Boggle board game.
    """

    def __init__(self, board, words):
        """
        Initialize the Boggle board game.
        :param board: The Boggle board.
        :param words: The word list for the game.
        """
        self.board_game = tk.Tk()
        self.start_screen(board, words)
        self.board_game.resizable(False, False)
        self.board_game.geometry("600x450")
        self.board_game.mainloop()

    def start_screen(self, board, words):
        """
        Display the start screen of the game.
        :param board: The Boggle board.
        :param words: The word list for the game.
        """
        self.start_frame = tk.Frame(self.board_game, width=50, height=50)
        self.start_frame.grid(row=5, column=5, columnspan=3)

        # Load and resize the image
        image = Image.open('open_page.jpg')  # Replace with your image file path
        image = image.resize((550, 330))  # Adjust the dimensions as needed

        # Convert the resized image to a PhotoImage object
        self.photo = ImageTk.PhotoImage(image)  # Store the PhotoImage as an attribute

        # Create a label with the image
        image_label = tk.Label(self.start_frame, image=self.photo)
        image_label.grid(row=0, column=0, padx=10, pady=10)

        start_key = tk.Button(self.start_frame, text="Start Game", command=lambda: self.start(board, words),
                              width=27, font=("Ariel", 20), background="#FB613D")
        start_key.grid(row=1, column=0, padx=10, pady=10)

    def start(self, board, words):
        """
        Start the game with the given board and word list.
        :param board: The Boggle board.
        :param words: The word list for the game.
        """
        self.start_frame.destroy()
        self.botens_game = self.create_botens(board)
        self.board_game.configure(bg="#0FA9B1")
        self.create_enter_boten("lgft")
        self.create_upper_frame("Lets Go!")
        self.words_found("")
        self.brain = Boogle(board, words)
        self.display_score(self.brain.get_score())
        self.timer_label = tk.Label(self.board_game, text="", width=10, font=("Ariel", 12))
        self.timer_label.grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.start_timer()



    def start_timer(self):
        """
        Start the timer for the game.
        """

        # Get the current time
        start_time = time.time()

        # Define the end time by adding 3 minutes (180 seconds)
        end_time = start_time + 180

        # Define a helper function for updating the timer label
        def update_timer_label():
            remaining_time = int(end_time - time.time())
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            self.timer_label.config(text="{}:{}".format(minutes, seconds))
            if time.time() < end_time:
                self.board_game.after(1000, update_timer_label)  # Schedule the next update after 1 second
            else:
                self.timer_label.config(text="Timer finished!")
                play_again = messagebox.askyesno("Game Over", "Time is up! Do you want to play again?")
                if play_again:
                    self.restart_game()
                self.board_game.quit()

        # Start updating the timer label
        update_timer_label()

    def restart_game(self):
        """
        Restart the game by creating a new instance of Boogle_board.
        """
        self.board_game.destroy()  # Destroy the existing game window

        # Restart the game by creating a new instance of Boogle_board
        board = boggle_board_randomizer.randomize_board()
        words = word_list()
        Boogle_board(board, words)

    def create_botens(self, board):
        """
        Create the buttons for each cell on the board.
        :param board: The Boggle board.
        :return: List of buttons representing the board cells.
        """
        self.left_frame = tk.Frame(self.board_game, width=120, height=200, bg="#F16623")
        self.left_frame.grid(row=1, column=0, sticky="W")
        self.button = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                bt = tk.Button(self.left_frame)
                bt.configure(text=board[i][j], command=lambda boten_name=(i, j): self.boten_cliked(boten_name),
                             width=5, font=("Ariel", 18, "bold"))
                bt.grid(row=i, column=j, padx=5, pady=5, sticky="NSEW")
                self.button.append(bt)
        return self.button

    def boten_cliked(self, cord):
        """
        Action performed when a button representing a board cell is clicked.
        :param cord: The coordinates of the clicked cell.
        """
        if self.brain.valid_step(cord):
            self.brain.update_current_path(cord)
            self.create_upper_frame(self.brain.path_to_word())
            self.display_score(self.brain.get_score())
        else:
            self.create_upper_frame("not valid step")
            self.display_score(self.brain.get_score())

    def enter(self):
        """
        Action performed when the Enter button is clicked.
        """
        if self.brain.update_word_find():
            self.display_score(self.brain.get_score())
            self.words_found(self.brain.word_find_to_print())
            self.display_score(self.brain.get_score())

        else:
            self.create_upper_frame("wrong")
            self.display_score(self.brain.get_score())

    def create_upper_frame(self, path):
        """
        Create the upper frame with an image and label.
        :param path: The current path or word.
        """
        self.upper_frame = tk.Frame(self.board_game, width=70, height=100, background="#0FA9B1")
        self.upper_frame.grid(row=0, column=0, columnspan=3, sticky="NSEW")

        # Load and resize the image
        image = Image.open('app_page.png')  # Replace with your image file path
        image = image.resize((400, 70))  # Adjust the dimensions as needed

        # Convert the resized image to a PhotoImage object
        photo = ImageTk.PhotoImage(image)  # Store the PhotoImage as an attribute

        # Create a label with the image
        image_label = tk.Label(self.upper_frame, image=photo)
        image_label.image = photo  # Store the image as an attribute to prevent garbage collection
        image_label.grid(row=0, column=0, padx=10, pady=10)

        # Add widgets or content to the upper frame
        label = tk.Label(self.upper_frame, text=path, width=15, font=("Arial", 18))
        label.grid(sticky="S")

    def create_enter_boten(self, word_found):
        """
        Create the Enter button.
        :param word_found: The word found in the current path.
        """
        self.right_frame = tk.Frame(self.board_game, width=50, height=50, bg="#F16623")
        self.right_frame.grid(row=2, column=1, columnspan=3, sticky="S")
        enter_key = tk.Button(self.right_frame, text="enter", command=self.enter, width=7, font=("Arial", 20),
                              background="#F16623")
        enter_key.grid(row=2, column=1, padx=5, pady=5)

    def words_found(self, word_found):
        """
        Display the words found in the current game.
        :param word_found: The word found in the current path.
        """
        if not hasattr(self, "word_label"):
            self.right_frame = tk.Frame(self.board_game, width=50, height=50, background="#0FA9B1",
                                        highlightthickness=2)
            self.right_frame.grid(row=1, column=1, columnspan=2, sticky="E")
            self.word_label = tk.Label(self.right_frame, text="you already found:\n" + word_found, width=16,
                                       font=("Arial", 12), background="#0FA9B1")
            self.word_label.grid(row=0, column=0, sticky="E")
        else:
            self.word_label.configure(text="You already found:\n" + word_found)

    def display_score(self, score):
        """
        Display the current score of the game.
        :param score: The current score.
        """
        self.right_frame = tk.Frame(self.board_game, width=50, height=50,
                                     highlightthickness=2,background="#0FA9B1")
        self.right_frame.grid(row=0, column=2, columnspan=2, sticky="S")
        label = tk.Label(self.right_frame, text="your score:\n" + str(score),
                         width=10, font=("Ariel", 12),background="#0FA9B1")
        label.grid(row=0, column=1, padx=5, pady=5, sticky="N")


def word_list():
    """
    Read the word list from a file.
    :return: List of words.
    """
    word_list = []
    with open("boggle_dict.txt", "r") as file:
        for i in file:
            word_list.append(i.rstrip())
    return word_list


# Start the Boggle game
Boogle_board(boggle_board_randomizer.randomize_board(), word_list())


