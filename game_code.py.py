from tkinter import * # From tkinter import all
import numpy as np

# Initialising the basic parameters at the start itself

board_size = 600
symbol_size = (board_size / 3 - board_size / 8) / 3  # size of X and O
symbol_thickness = 30 # Thickness of cross and circle
symbol_X_color = '#EE4035' # red
symbol_O_color = '#3CB371' # green
Black_color = '#000000'
# Green_color = '#7BC043'


class Tic_Tac_Toe():
    """
    The main class for the game
    """
    def __init__(self):
        self.window_pannel = Tk()  # window panel on which the game will be played
        self.window_pannel.title('Tic Tac Toe - Sushant And Alok')  
        self.canvas = Canvas(self.window_pannel, width=board_size, height=board_size)
        self.canvas.pack()

        self.window_pannel.bind('<Button-1>', self.click) # Takes input in the form of a click

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))

        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.Total_X_score = 0
        self.O_score = 0
        self.tie_score = 0

    def mainloop(self):
        """
        The main loop due to which the 2 players are able to play one after other
        """
        self.window_pannel.mainloop()

    def initialize_board(self):
        """
        Initialising the lines and structure of the board
        """
        for i in range(2):
            self.canvas.create_line((i + 1) * board_size / 3, 0, (i + 1) * board_size / 3, board_size)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * board_size / 3, board_size, (i + 1) * board_size / 3)

    def play_again(self):
        """
        Code for the feature which will switch the person who starts the game once the game gets over and again starts the game
        """
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts   
        self.player_X_turns = self.player_X_starts        
        self.board_status = np.zeros(shape=(3, 3))


    def draw_O(self, logical_position):
        """
        A function to draw the O symbol
        """
        logical_position = np.array(logical_position)

        grid_position = self.convert_logical_to_grid_position(logical_position)

        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=symbol_O_color)  

    def draw_X(self, logical_position):
        """
        A function to draw the X symbol
        """
        grid_position = self.convert_logical_to_grid_position(logical_position)

        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness, fill=symbol_X_color)

        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size, grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness, fill=symbol_X_color)

    def display_gameover(self):
        """
        The game displays 'gameover' when either Player1 wins or Player2 wins or the game has tied.
        """
        if self.X_wins:
            self.Total_X_score += 1 #
            text = 'Player1 (X) is the Winner!'  # the player x wins according to the criteria of winning
            color = symbol_X_color

        elif self.O_wins:
            self.O_score += 1
            text = 'Player2 (O) is the Winner!'  # the player y wins according to the criteria of winning
            color = symbol_O_color

        else:
            self.tie_score += 1
            text = 'Game Tied!'  # The game gets tied when neither of the player wins
            color = 'gray'

        self.canvas.delete("all")  # deletes all the symbols and resets the whole game

        self.canvas.create_text(board_size / 2, board_size / 3, font="cmr 30 bold", fill=color, text=text)

        score_text = 'Scores \n'

        self.canvas.create_text(board_size / 2, 5 * board_size / 8, font="cmr 20 bold", fill=Black_color ,text=score_text)

        score_text = 'Player 1 (X) : ' + str(self.Total_X_score) + '\n'
        score_text += 'Player 2 (O): ' + str(self.O_score) + '\n'
        score_text += 'Tie : ' + str(self.tie_score)

        self.canvas.create_text(board_size / 2, 3 * board_size / 4, font="cmr 20 bold", fill=Black_color, text=score_text)
        self.reset_board = True

        score_text = 'Play again \n'
        self.canvas.create_text(board_size / 2, 15 * board_size / 16, font="cmr 10 bold", fill="gray", text=score_text)

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (board_size / 3) * logical_position + board_size / 6

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (board_size / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        """
        A function to check whether the grid is occupied
        """
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True

    def is_winner(self, player):
        """
        A player is a winner if any of the diagonal or any of the row is X or O.
        """

        player = -1 if player == 'X' else 1

        # Three in a row
        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True

        # Diagonals
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True

        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True

        return False

    def is_tie(self):
        r, c = np.where(self.board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True

        return tie

    def is_gameover(self):
        # Either someone wins or all grid occupied
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')

        if not self.O_wins:
            self.tie = self.is_tie()

        gameover = self.X_wins or self.O_wins or self.tie

        if self.X_wins:
            print('X is winner')
        if self.O_wins:
            print('O is winner')
        if self.tie:
            print('Game tied')

        return gameover


    def click(self, event):
        """
        A function to carry out the action of clicking
        """
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            if self.player_X_turns:
                if not self.is_grid_occupied(logical_position):
                    self.draw_X(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                    self.player_X_turns = not self.player_X_turns
            else:
                if not self.is_grid_occupied(logical_position):
                    self.draw_O(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    self.player_X_turns = not self.player_X_turns

    
            if self.is_gameover():  # Check if game is concluded
                self.display_gameover()

        else:  
            self.canvas.delete("all")  # Play Again
            self.play_again()
            self.reset_board = False


game_instance = Tic_Tac_Toe()
game_instance.mainloop()
