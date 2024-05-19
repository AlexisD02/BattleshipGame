# Battleship.py

# Description: This program is a simple Battleship game where the player clicks on cells to guess the location of the
# hidden ship.

import tkinter as tk
from tkinter import messagebox
from random import randint


class FileHandler:
    def __init__(self, file_path: [str], statistics: [dict]):
        """
        Initializes a FileHandler object with the provided file path and an empty dictionary to store statistics.
        :param file_path: a string representing the path to the file containing statistics
        """
        self.statistics = statistics
        self.file_path = file_path

    def read_statistics(self):
        """
        Reads statistics from the file and returns them as a dictionary.
        :return: a dictionary containing the statistics read from the file
        """
        try:
            # Open the file in read mode
            with open(self.file_path, 'r') as file:
                for line in file:
                    key, value = line.strip().split(': ')
                    if key == "WinRate":
                        value = float(value)  # Convert string to float
                    else:
                        value = int(value)  # Convert string to int
                    self.statistics[key] = int(value)
        except FileNotFoundError:
            print("Error: The file " + self.file_path + " was not found.")
            quit()
        except PermissionError:
            print("Error: Permission denied to read the file " + self.file_path + ".")
            quit()
        except Exception as e:
            print("An unexpected error occurred while reading the file: " + str(e))
            quit()

        return self.statistics

    def update_statistics(self):
        try:
            with open(self.file_path, 'w') as file:
                for key, value in self.statistics.items():
                    file.write(f"{key}: {value}\n")
        except Exception as e:
            print("An unexpected error occurred while updating the file:", str(e))


class BattleshipGame:
    def __init__(self, root, statistics):
        self.root = root
        self.root.title(title)

        self.statistics = statistics
        self.turns = 0

        self.result_label = tk.Label(root, text="", font=(None, 15))
        self.result_label.pack()

        self.turn_label = tk.Label(root, text="Turn: " + str(self.turns + 1), font=(None, 12))
        self.turn_label.pack()

        self.statistics["WinRate"] = (self.statistics["Wins"] / self.statistics["TotalGamesPlayed"]) * 100 \
            if self.statistics["TotalGamesPlayed"] != 0 else 0

        self.wins_label = tk.Label(root, text="Wins: " + str(self.statistics["Wins"])
                                              + "\tLosses: " + str(self.statistics["Losses"])
                                              + "\t   Win Rate: " + str(self.statistics["WinRate"]) + "%"
                                              + "\nTotal Games Played: " + str(self.statistics["TotalGamesPlayed"])
                                   , font=(None, 12))
        self.wins_label.pack()

        self.canvas = tk.Canvas(root, width=width, height=height)
        self.canvas.config(bg="light gray")
        self.canvas.pack()

        self.cells = self.create_board()
        self.ships = self.generate_ships()

        self.canvas.bind("<Button-1>", self.cell_clicked)

    @staticmethod
    def generate_ships():
        ships = []
        for _ in range(num_ships):
            while True:
                ship_row = randint(0, board_size - 1)
                ship_col = randint(0, board_size - 1)
                if (ship_row, ship_col) not in ships:
                    ships.append((ship_row, ship_col))
                    break
        return ships

    def guess(self, row: [int], col: [int]):
        if self.canvas.itemcget(self.cells[row][col][1], 'text') == "X":
            self.result_label.config(text="You guessed that one already.")
        elif (row, col) in self.ships:
            self.turns += 1
            self.turn_label.config(text="Turn: " + str(self.turns + 1))
            self.result_label.config(text="Congratulations! You sunk my battleship!")
            self.canvas.itemconfig(self.cells[row][col][1], text="X", fill="green")
            self.ships.remove((row, col))
            if not self.ships:
                statistics["Wins"] += 1
                self.show_rematch_popup()
        else:
            self.turns += 1
            self.turn_label.config(text="Turn: " + str(self.turns + 1))
            self.result_label.config(text="You missed my battleship!")
            self.canvas.itemconfig(self.cells[row][col][1], text="X", fill="black")

        if self.turns >= 10:
            statistics["Losses"] += 1
            self.result_label.config(text="Game Over! You have lost")
            self.show_rematch_popup()

    def cell_clicked(self, event):
        x, y = event.x, event.y
        for i in range(board_size):
            for j in range(board_size):
                x0, y0, x1, y1 = self.canvas.bbox(self.cells[i][j][0])
                if x0 <= x <= x1 and y0 <= y <= y1:
                    self.guess(i, j)
                    return

    def create_board(self):
        cells = [["O"] * board_size for _ in range(board_size)]
        for i in range(board_size):
            for j in range(board_size):
                x0 = j * cell_size + padding
                y0 = i * cell_size + padding
                x1 = x0 + cell_inner_size
                y1 = y0 + cell_inner_size
                rectangles = self.canvas.create_rectangle(x0, y0, x1, y1, outline="dark gray", width=1, fill="white")
                cell_text = self.canvas.create_text(x0 + cell_inner_size // 2, y0 + cell_inner_size // 2, text="O", font=(None, 25))
                cells[i][j] = (rectangles, cell_text)
        return cells

    def show_rematch_popup(self):
        statistics["TotalGamesPlayed"] += 1
        response = messagebox.askyesno("Rematch", "Do you want to play again?")
        if response:
            self.rematch()
        else:
            quit()

    def rematch(self):
        self.ships = self.generate_ships()
        for i in range(board_size):
            for j in range(board_size):
                self.canvas.itemconfig(self.cells[i][j][1], text="O", fill="black")
        self.result_label.config(text="")
        self.turns = 0
        self.turn_label.config(text="Turn: " + str(self.turns + 1))
        self.wins_label.config(text="Wins: " + str(self.statistics["Wins"])
                                    + "\tLosses: " + str(self.statistics["Losses"])
                                    + "\t   Win Rate: " + str(self.statistics["WinRate"]) + "%"
                                    + "\nTotal Games Played: " + str(self.statistics["TotalGamesPlayed"])
                               , font=(None, 12))


if __name__ == "__main__":
    filename = 'BattleshipStats.txt'
    statistics = {}

    file_handler = FileHandler(filename, statistics)
    statistics = file_handler.read_statistics()

    win = tk.Tk()

    title = "Battleship"
    board_size = 5
    num_ships = 3  # Number of battleships
    cell_size = 70
    padding = 10
    cell_inner_size = cell_size - 2 * padding
    width, height = board_size * cell_size, board_size * cell_size  # Board dimensions

    game = BattleshipGame(win, statistics)
    win.mainloop()

    file_handler.update_statistics()
