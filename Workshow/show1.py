import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("井字遊戲 Tic-Tac-Toe")
        self.current_player = "X"
        self.buttons = [None] * 9
        self.board = [" "] * 9
        self.create_board()
        self.window.mainloop()

    def create_board(self):
        for i in range(9):
            button = tk.Button(self.window, text=" ", font=('Arial', 32), width=5, height=2,
                               command=lambda i=i: self.make_move(i))
            button.grid(row=i//3, column=i%3)
            self.buttons[i] = button

    def make_move(self, index):
        if self.board[index] == " ":
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player, state="disabled")
            if self.check_winner(self.current_player):
                self.end_game(f"🎉 玩家 {self.current_player} 勝利！")
            elif " " not in self.board:
                self.end_game("🤝 平手！")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self, player):
        win_conditions = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        return any(all(self.board[i] == player for i in cond) for cond in win_conditions)

    def end_game(self, message):
        messagebox.showinfo("遊戲結束", message)
        for btn in self.buttons:
            btn.config(state="disabled")

# 啟動遊戲
TicTacToe()
