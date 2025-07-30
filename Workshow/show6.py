import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("井字遊戲 - 五局三勝")
        self.window.geometry("400x600")
        self.current_player = "X"
        self.board = ["" for _ in range(9)]
        self.player1_name = ""
        self.player2_name = ""
        self.player1_wins = 0
        self.player2_wins = 0
        self.current_round = 1
        self.is_ai_mode = False
        self.buttons = []
        self.background_styles = [
            "#F0F0F0", "#E6E6FA", "#FFFACD", "#E0FFFF", "#FFE4E1"
        ]
        self.current_style_index = 0
        self.setup_start_screen()

    def setup_start_screen(self):
        self.clear_window()
        tk.Label(self.window, text="井字遊戲 - 五局三勝", font=("Arial", 16)).pack(pady=10)
        
        tk.Label(self.window, text="玩家1姓名:").pack()
        self.player1_entry = tk.Entry(self.window)
        self.player1_entry.pack()
        
        tk.Label(self.window, text="選擇模式:").pack()
        tk.Button(self.window, text="與真人對戰", command=self.setup_two_players).pack(pady=5)
        tk.Button(self.window, text="與AI對戰", command=self.setup_ai_mode).pack(pady=5)
        
        tk.Button(self.window, text="更改背景樣式", command=self.change_background_style).pack(pady=10)

    def setup_two_players(self):
        self.is_ai_mode = False
        self.player1_name = self.player1_entry.get() or "玩家1"
        tk.Label(self.window, text="玩家2姓名:").pack()
        self.player2_entry = tk.Entry(self.window)
        self.player2_entry.pack()
        tk.Button(self.window, text="開始遊戲", command=self.start_game).pack(pady=10)

    def setup_ai_mode(self):
        self.is_ai_mode = True
        self.player1_name = self.player1_entry.get() or "玩家1"
        self.player2_name = "AI"
        self.start_game()

    def change_background_style(self):
        self.current_style_index = (self.current_style_index + 1) % len(self.background_styles)
        self.window.configure(bg=self.background_styles[self.current_style_index])

    def start_game(self):
        self.clear_window()
        self.board = ["" for _ in range(9)]
        self.current_player = "X"
        
        # 顯示當前局數和比分
        self.score_label = tk.Label(self.window, text=f"第 {self.current_round}/5 局\n{self.player1_name}: {self.player1_wins} 勝 - {self.player2_name}: {self.player2_wins} 勝", 
                                  font=("Arial", 12))
        self.score_label.pack(pady=10)
        
        # 創建遊戲盤
        game_frame = tk.Frame(self.window)
        game_frame.pack()
        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = tk.Button(game_frame, text="", font=("Arial", 20), width=5, height=2,
                                 bg=self.background_styles[self.current_style_index],
                                 command=lambda x=i*3+j: self.button_click(x))
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(button)
        
        tk.Button(self.window, text="重啟遊戲", command=self.confirm_restart).pack(pady=10)
        
        if self.is_ai_mode and self.current_player == "O":
            self.ai_move()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        self.window.configure(bg=self.background_styles[self.current_style_index])

    def button_click(self, index):
        if self.board[index] == "":
            self.board[index] = self.current_player
            color = "red" if self.current_player == "X" else "blue"
            self.buttons[index].config(text=self.current_player, fg=color)
            
            if self.check_winner():
                self.handle_round_end()
            elif "" not in self.board:
                self.handle_draw()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.is_ai_mode and self.current_player == "O":
                    self.ai_move()

    def ai_move(self):
        empty_cells = [i for i, cell in enumerate(self.board) if cell == ""]
        if empty_cells:
            move = random.choice(empty_cells)
            self.button_click(move)

    def check_winner(self):
        winning_combinations = [
            (0,1,2), (3,4,5), (6,7,8),  # 橫
            (0,3,6), (1,4,7), (2,5,8),  # 縱
            (0,4,8), (2,4,6)            # 對角
        ]
        for a, b, c in winning_combinations:
            if self.board[a] == self.board[b] == self.board[c] != "":
                return True
        return False

    def handle_round_end(self):
        winner = self.player1_name if self.current_player == "X" else self.player2_name
        loser = self.player2_name if self.current_player == "X" else self.player1_name
        
        if self.current_player == "X":
            self.player1_wins += 1
        else:
            self.player2_wins += 1
            
        messagebox.showinfo("本局結果", f"{winner} 恭喜你獲勝!\n{loser} 挑戰失敗!")
        
        if self.player1_wins >= 3 or self.player2_wins >= 3:
            self.show_final_result()
        elif self.current_round < 5:
            self.current_round += 1
            self.start_game()
        else:
            self.show_final_result()

    def handle_draw(self):
        messagebox.showinfo("本局結果", "平局!")
        if self.current_round < 5:
            self.current_round += 1
            self.start_game()
        else:
            self.show_final_result()

    def show_final_result(self):
        if self.player1_wins > self.player2_wins:
            messagebox.showinfo("最終結果", f"{self.player1_name} 恭喜你獲勝!\n{self.player2_name} 挑戰失敗!")
        elif self.player2_wins > self.player1_wins:
            messagebox.showinfo("最終結果", f"{self.player2_name} 恭喜你獲勝!\n{self.player1_name} 挑戰失敗!")
        else:
            messagebox.showinfo("最終結果", "五局比賽平局!")
        self.reset_game()

    def confirm_restart(self):
        if self.current_round < 5 and (self.player1_wins < 3 and self.player2_wins < 3):
            if messagebox.askyesno("確認", "確定要重啟遊戲嗎？"):
                self.reset_game()
        else:
            self.reset_game()

    def reset_game(self):
        self.player1_wins = 0
        self.player2_wins = 0
        self.current_round = 1
        self.setup_start_screen()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()