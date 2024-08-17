import tkinter as tk
from tkinter import messagebox, simpledialog
import time

class NimGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Nim Game")
        self.master.geometry("1000x1000")
        self.master.configure(bg="#F8D6E5")  # Set background color to pink
        self.piles = [3, 4, 5]  # Initial number of sticks in each pile
        self.current_player = 1
        self.selected_pile = None
        self.current_mode = None

        self.create_widgets()

    def check_winner(self):
        # Check if all piles are empty
        if all(count == 0 for count in self.piles):
            if self.current_player == 1:
                return 2  # Computer wins
            else:
                return 1  # Player wins
        return -1  # Game is not over

    def make_computer_move(self):
        temp_player = self.current_player
        self.current_player = 2

        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for i in range(len(self.piles)):
            if self.piles[i] > 0:
                for sticks in range(1, self.piles[i] + 1):
                    self.piles[i] -= sticks
                    score = self.minimax(0, False, alpha, beta)
                    self.piles[i] += sticks

                    if score > best_score:
                        best_score = score
                        best_move = (i, sticks)

                    alpha = max(alpha, best_score)

        if best_move:
            pile_index, sticks = best_move
            self.piles[pile_index] -= sticks
            self.update_piles()
            self.current_player = temp_player
            self.check_game_over()
            self.switch_turn()

    def minimax(self, depth, is_maximizing, alpha, beta):
        if self.check_winner() == 1:
            return -1
        elif self.check_winner() == 2:
            return 1

        if is_maximizing:
            best_score = float('-inf')
            for i in range(len(self.piles)):
                if self.piles[i] > 0:
                    for sticks in range(1, self.piles[i] + 1):
                        self.piles[i] -= sticks
                        self.current_player = 2
                        score = self.minimax(depth + 1, False, alpha, beta)
                        self.piles[i] += sticks
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = float('inf')
            for i in range(len(self.piles)):
                if self.piles[i] > 0:
                    for sticks in range(1, self.piles[i] + 1):
                        self.piles[i] -= sticks
                        self.current_player = 1
                        score = self.minimax(depth + 1, True, alpha, beta)
                        self.piles[i] += sticks
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score

    def create_widgets(self):
        
        
        self.label_mode = tk.Label(self.master, text="Select Game Mode", font=("Arial", 60), bg="#F8D6E5")
        self.label_mode.pack(pady=100)

        self.button_player = tk.Button(self.master, text="Player vs. Computer", font=("Arial", 40),
                                       command=self.start_game_player_vs_computer, bg="#D5A6BD", fg="white")
        self.button_player.pack(pady=20)

        self.button_watch = tk.Button(self.master, text="Computer vs. Computer", font=("Arial", 40),
                                      command=self.start_game_computer_vs_computer, bg="#D5A6BD", fg="white")
        self.button_watch.pack(pady=20)

    def start_game_player_vs_computer(self):
        self.piles = [3, 4, 5]
        self.current_mode = 1
        self.label_mode.pack_forget()
        self.button_player.pack_forget()
        self.button_watch.pack_forget()

        self.label_turn = tk.Label(self.master, text="Player's Turn", font=("Arial", 40), bg="#F8D6E5")
        self.label_turn.pack(pady=20)

        self.frame_piles = tk.Frame(self.master, bg="#F8D6E5")
        self.frame_piles.pack()

        self.buttons_piles = []
        for i in range(len(self.piles)):
            sticks = "|" * self.piles[i]
            button_pile = tk.Button(self.frame_piles, text=sticks, width=self.piles[i], height=1, font=("Arial", 60),
                                    command=lambda pile=i: self.select_pile(pile), bg="#D5A6BD", fg="white")
            button_pile.pack(pady=5)
            self.buttons_piles.append(button_pile)

        self.button_restart = tk.Button(self.master, text="Restart Game", font=("Arial", 40),
                                        command=self.restart_game, bg="#D5A6BD", fg="white")
        self.button_restart.pack(pady=20)

    def start_game_computer_vs_computer(self):
        self.piles = [3, 4, 5]
        self.current_mode = 2
        self.label_mode.pack_forget()
        self.button_player.pack_forget()
        self.button_watch.pack_forget()

        self.label_turn = tk.Label(self.master, text="Computer 1's Turn", font=("Arial", 40), bg="#F8D6E5")
        self.label_turn.pack(pady=20)

        self.frame_piles = tk.Frame(self.master, bg="#F8D6E5")
        self.frame_piles.pack()

        self.buttons_piles = []
        for i in range(len(self.piles)):
            sticks = "|" * self.piles[i]
            button_pile = tk.Button(self.frame_piles, text=sticks, width=self.piles[i], height=1, font=("Arial", 60),
                                    state="disabled", bg="#D5A6BD", fg="white")
            button_pile.pack(pady=5)
            self.buttons_piles.append(button_pile)

        self.button_restart = tk.Button(self.master, text="Restart Game", font=("Arial", 40),
                                        command=self.restart_game, bg="#D5A6BD", fg="white")
        self.button_restart.pack(pady=20)

        
        self.make_computer_move()

    def select_pile(self, pile):
        if self.current_player == 1:
            self.selected_pile = pile
            sticks_to_take = simpledialog.askinteger("Take Sticks", "How many sticks do you want to take?",
                                                     minvalue=1, maxvalue=self.piles[pile])
            if sticks_to_take:
                self.piles[pile] -= sticks_to_take
                self.update_piles()
                self.check_game_over()
                self.switch_turn()

    def switch_turn(self):
        if self.current_mode == 1:
            if self.current_player == 1:
                self.current_player = 2
                self.label_turn.configure(text="Computer's Turn")
                self.selected_pile = None
                self.master.after(1000, self.make_computer_move)
            elif self.current_player == 2:
                self.current_player = 1
                self.label_turn.configure(text="Player's Turn")
        elif self.current_mode == 2:
            if self.current_player == 1:
                self.current_player = 2
                self.label_turn.configure(text="Computer 2's Turn")
                self.selected_pile = None
                self.master.after(1000, self.make_computer_move)
            elif self.current_player == 2:
                self.current_player = 1
                self.label_turn.configure(text="Computer 1's Turn")
                self.selected_pile = None
                self.master.after(1000, self.make_computer_move)

    def update_piles(self):
        for i in range(len(self.piles)):
            sticks = "|" * self.piles[i]
            self.buttons_piles[i].configure(text=sticks)

    def check_game_over(self):
        if all(count == 0 for count in self.piles):
            if self.current_player == 1:
                if self.current_mode == 1:
                    winner = "Computer"
                else:
                    winner = "Computer 2"
            else:
                if self.current_mode == 1:
                    winner = "Player"
                else:
                    winner = "Computer 1"
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self.restart_game()

    def restart_game(self):
        self.piles = [3, 4, 5]
        self.current_player = 1
        self.selected_pile = None
        self.current_mode = None
        self.update_piles()
        if self.label_turn:
            self.label_turn.pack_forget()
        if self.frame_piles:
            self.frame_piles.pack_forget()
        if self.button_restart:
            self.button_restart.pack_forget()
        self.create_widgets()


if __name__ == "__main__":
    root = tk.Tk()
    game = NimGameGUI(root)
    root.mainloop()
