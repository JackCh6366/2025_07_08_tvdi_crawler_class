import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeGame:
    STYLES = {
    "經典白色": {"bg": "#ffffff", "btn_bg": "#dddddd", "fg": "black"},
    "夜間黑色": {"bg": "#1e1e1e", "btn_bg": "#444444", "fg": "white"},
    "粉嫩風":   {"bg": "#ffe6f0", "btn_bg": "#ffb3d1", "fg": "darkred"},
    "銀河藍":   {"bg": "#001f3f", "btn_bg": "#848FF1", "fg": "white"},
    "柚子橘":   {"bg": "#FFF5E1", "btn_bg": "#FFA500", "fg": "black"},
}

    def __init__(self):
        
        self.window = tk.Tk()
        self.window.title("井字遊戲進階版")
        self.style_choice = "經典白色"
        self.style = self.STYLES[self.style_choice]

        self.player1_name = ""
        self.player2_name = ""
        self.vs_ai = False
        self.current_player = "X"
        self.board = [" "] * 9
        self.buttons = [None] * 9
        self.scores = {"X": 0, "O": 0}
        self.round = 1

        self.setup_start_screen()

        self.window.mainloop()

    def setup_start_screen(self):
        
        self.setup_style_selection()
        
    def setup_style_selection(self):
        tk.Label(self.window, text="🎨 選擇風格樣式", font=("Arial", 16)).pack(pady=10)
        for name in self.STYLES.keys():
            tk.Button(self.window, text=name, font=("Arial", 12),
                      command=lambda n=name: self.set_style(n)).pack(pady=2)

    def set_style(self, style_name):
        self.style_choice = style_name
        self.style = self.STYLES[self.style_choice]
        self.window.configure(bg=self.style["bg"])
        self.setup_mode_selection()
       
    def setup_name_input(self, vs_ai):
        self.vs_ai = vs_ai
        self.clear_window()

        tk.Label(self.window, text="請輸入玩家名稱", font=("Arial", 14)).pack(pady=5)

        self.entry1 = tk.Entry(self.window, font=("Arial", 14))
        self.entry1.pack(pady=5)
        self.entry1.insert(0, "玩家一")

        if vs_ai:
            self.player2_name = "Tik Tak Tok master"
        else:
            self.entry2 = tk.Entry(self.window, font=("Arial", 14))
            self.entry2.pack(pady=5)
            self.entry2.insert(0, "玩家二")

        tk.Button(self.window, text="開始遊戲", font=("Arial", 14),
                  command=self.start_game).pack(pady=10)
   
    def setup_mode_selection(self):
        self.clear_window()

        tk.Label(self.window, text="選擇對戰模式", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.window, text="玩家 vs 玩家", font=("Arial", 14),
                  command=lambda: self.setup_name_input(vs_ai=False)).pack(pady=5)
        tk.Button(self.window, text="玩家 vs AI", font=("Arial", 14),
                  command=lambda: self.setup_name_input(vs_ai=True)).pack(pady=5)



    def start_game(self):
        self.player1_name = self.entry1.get()
        if not self.vs_ai:
            self.player2_name = self.entry2.get()

        self.current_player = "X"
        self.scores = {"X": 0, "O": 0}
        self.round = 1
        self.new_round()

    def new_round(self):
        self.board = [" "] * 9
        self.clear_window()
        self.create_board()
        self.update_status()

        restart_btn = tk.Button(self.window, text="🔁 重啟遊戲", command=self.confirm_restart)
        restart_btn.grid(row=4, column=0, columnspan=3, pady=10)

    def create_board(self):
        for i in range(9):
            btn = tk.Button(self.window, text=" ", font=('Arial', 32), width=5, height=2,bg=self.style["btn_bg"], fg=self.style["fg"],
                            command=lambda i=i: self.make_move(i))
            btn.grid(row=i//3, column=i%3)
            self.buttons[i] = btn

    def make_move(self, index):
        if self.board[index] != " ":
            return

        self.board[index] = self.current_player
        color = "#007AFF" if self.current_player == "X" else "#FF3B30"
        self.buttons[index].config(text=self.current_player, fg=color, state="disabled")
     
        if self.check_winner(self.current_player):
            self.scores[self.current_player] += 1
            self.update_status()
            self.check_game_over()
            return
        elif " " not in self.board:
            messagebox.showinfo("平手", "🤝 這局平手！")
            self.round += 1
            self.new_round()
            return

        self.current_player = "O" if self.current_player == "X" else "X"
        self.update_status()

        if self.vs_ai and self.current_player == "O":
            self.window.after(500, self.ai_move)

    def ai_move(self):
        empty_indices = [i for i, val in enumerate(self.board) if val == " "]
        if empty_indices:
            ai_choice = random.choice(empty_indices)
            self.make_move(ai_choice)

    def check_winner(self, player):
        wins = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        for cond in wins:
            if all(self.board[i] == player for i in cond):
                for i in cond:
                    self.buttons[i].config(bg="lightgreen")
                messagebox.showinfo("勝利", f"🎉 {self.get_player_name(player)} 勝利！")
                self.round += 1
                self.check_game_over()
                return True
        return False

    def check_game_over(self):
        if self.scores["X"] >= 3 or self.scores["O"] >= 3:
            winner = "X" if self.scores["X"] >= 3 else "O"
            loser = "O" if winner == "X" else "X"
            messagebox.showinfo("🏆 遊戲結束",
                                f"🎉 {self.get_player_name(winner)} 獲勝！\n"
                                f"💪 {self.get_player_name(loser)} 去伏地挺身 5 下！")
            self.setup_start_screen()
        else:
            self.window.after(1000, self.new_round)

    def update_status(self):
        status = f"{self.get_player_name('X')} (X): {self.scores['X']} | {self.get_player_name('O')} (O): {self.scores['O']} | 第 {self.round} 局"
        self.window.title(f"井字遊戲 - {status}")

    def get_player_name(self, symbol):
        return self.player1_name if symbol == "X" else self.player2_name

    def confirm_restart(self):
        if self.round <= 5:
            result = messagebox.askyesno("確認重啟", "你確定？不再挑戰一下？")
            if result:
                self.setup_start_screen()
        else:
            self.setup_start_screen()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()
            self.window.configure(bg=self.style["bg"])  # <== 背景套用
if __name__ == "__main__":
    TicTacToeGame()