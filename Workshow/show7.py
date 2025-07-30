import tkinter as tk
from tkinter import messagebox, ttk
import random

class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("井字遊戲")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        # 遊戲狀態
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_mode = None  # "human" 或 "ai"
        self.player1_name = ""
        self.player2_name = ""
        self.player1_wins = 0
        self.player2_wins = 0
        self.games_played = 0
        self.max_games = 5
        self.game_in_progress = False
        
        # 五種背景樣式配色
        self.themes = [
            {"bg": "#E8F4F8", "button": "#B8E6B8", "accent": "#4A90E2"},  # 清新藍綠
            {"bg": "#FFF0E6", "button": "#FFD4B3", "accent": "#FF8C42"},  # 溫暖橙色
            {"bg": "#F0E6FF", "button": "#D4B3FF", "accent": "#8A42FF"},  # 優雅紫色
            {"bg": "#E6FFF0", "button": "#B3FFD4", "accent": "#42FF8C"},  # 自然綠色
            {"bg": "#FFE6F0", "button": "#FFB3D4", "accent": "#FF428C"}   # 浪漫粉色
        ]
        self.current_theme = 0
        
        self.setup_main_menu()
        
    def apply_theme(self):
        theme = self.themes[self.current_theme]
        self.root.configure(bg=theme["bg"])
        
    def setup_main_menu(self):
        self.clear_window()
        self.apply_theme()
        
        # 標題
        title_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]["bg"])
        title_frame.pack(pady=30)
        
        title_label = tk.Label(title_frame, text="井字遊戲", 
                              font=("Microsoft JhengHei", 32, "bold"),
                              bg=self.themes[self.current_theme]["bg"],
                              fg=self.themes[self.current_theme]["accent"])
        title_label.pack()
        
        # 主選單框架
        menu_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]["bg"])
        menu_frame.pack(pady=20)
        
        # 遊戲模式按鈕
        tk.Button(menu_frame, text="與真人對戰", 
                 font=("Microsoft JhengHei", 16),
                 bg=self.themes[self.current_theme]["button"],
                 fg="black", width=15, height=2,
                 command=self.setup_human_vs_human).pack(pady=10)
                 
        tk.Button(menu_frame, text="與AI對戰", 
                 font=("Microsoft JhengHei", 16),
                 bg=self.themes[self.current_theme]["button"],
                 fg="black", width=15, height=2,
                 command=self.setup_human_vs_ai).pack(pady=10)
        
        # 主題切換區域
        theme_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]["bg"])
        theme_frame.pack(pady=30)
        
        tk.Label(theme_frame, text="選擇背景主題:", 
                font=("Microsoft JhengHei", 14),
                bg=self.themes[self.current_theme]["bg"]).pack()
        
        theme_buttons_frame = tk.Frame(theme_frame, bg=self.themes[self.current_theme]["bg"])
        theme_buttons_frame.pack(pady=10)
        
        theme_names = ["清新藍綠", "溫暖橙色", "優雅紫色", "自然綠色", "浪漫粉色"]
        for i, name in enumerate(theme_names):
            tk.Button(theme_buttons_frame, text=name,
                     font=("Microsoft JhengHei", 10),
                     bg=self.themes[i]["button"],
                     command=lambda x=i: self.change_theme(x),
                     width=10).pack(side=tk.LEFT, padx=5)
    
    def change_theme(self, theme_index):
        self.current_theme = theme_index
        self.setup_main_menu()
    
    def setup_human_vs_human(self):
        self.game_mode = "human"
        self.setup_name_input()
    
    def setup_human_vs_ai(self):
        self.game_mode = "ai"
        self.setup_name_input()
    
    def setup_name_input(self):
        self.clear_window()
        self.apply_theme()
        
        # 標題
        tk.Label(self.root, text="輸入玩家姓名", 
                font=("Microsoft JhengHei", 24, "bold"),
                bg=self.themes[self.current_theme]["bg"],
                fg=self.themes[self.current_theme]["accent"]).pack(pady=30)
        
        # 輸入框架
        input_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]["bg"])
        input_frame.pack(pady=20)
        
        # 玩家1姓名
        tk.Label(input_frame, text="玩家1姓名 (X):", 
                font=("Microsoft JhengHei", 14),
                bg=self.themes[self.current_theme]["bg"]).grid(row=0, column=0, padx=10, pady=10)
        
        self.player1_entry = tk.Entry(input_frame, font=("Microsoft JhengHei", 14), width=15)
        self.player1_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # 玩家2姓名 (如果是人vs人模式)
        if self.game_mode == "human":
            tk.Label(input_frame, text="玩家2姓名 (O):", 
                    font=("Microsoft JhengHei", 14),
                    bg=self.themes[self.current_theme]["bg"]).grid(row=1, column=0, padx=10, pady=10)
            
            self.player2_entry = tk.Entry(input_frame, font=("Microsoft JhengHei", 14), width=15)
            self.player2_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # 開始遊戲按鈕
        tk.Button(self.root, text="開始遊戲", 
                 font=("Microsoft JhengHei", 16),
                 bg=self.themes[self.current_theme]["button"],
                 command=self.start_game,
                 width=15, height=2).pack(pady=20)
        
        # 返回主選單按鈕
        tk.Button(self.root, text="返回主選單", 
                 font=("Microsoft JhengHei", 12),
                 bg=self.themes[self.current_theme]["button"],
                 command=self.setup_main_menu,
                 width=12).pack(pady=10)
    
    def start_game(self):
        # 獲取玩家姓名
        self.player1_name = self.player1_entry.get().strip()
        if not self.player1_name:
            messagebox.showerror("錯誤", "請輸入玩家1的姓名！")
            return
        
        if self.game_mode == "human":
            self.player2_name = self.player2_entry.get().strip()
            if not self.player2_name:
                messagebox.showerror("錯誤", "請輸入玩家2的姓名！")
                return
        else:
            self.player2_name = "AI電腦"
        
        # 重置遊戲狀態
        self.player1_wins = 0
        self.player2_wins = 0
        self.games_played = 0
        self.game_in_progress = True
        
        self.setup_game_board()
    
    def setup_game_board(self):
        self.clear_window()
        self.apply_theme()
        
        # 重置棋盤
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        
        # 標題和計分板
        info_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]["bg"])
        info_frame.pack(pady=10)
        
        tk.Label(info_frame, text=f"五局三勝制 - 第{self.games_played + 1}局", 
                font=("Microsoft JhengHei", 18, "bold"),
                bg=self.themes[self.current_theme]["bg"],
                fg=self.themes[self.current_theme]["accent"]).pack()
        
        # 計分板
        score_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]["bg"])
        score_frame.pack(pady=10)
        
        tk.Label(score_frame, text=f"{self.player1_name} (X): {self.player1_wins}勝", 
                font=("Microsoft JhengHei", 14),
                bg=self.themes[self.current_theme]["bg"],
                fg="red").grid(row=0, column=0, padx=20)
        
        tk.Label(score_frame, text=f"{self.player2_name} (O): {self.player2_wins}勝", 
                font=("Microsoft JhengHei", 14),
                bg=self.themes[self.current_theme]["bg"],
                fg="blue").grid(row=0, column=1, padx=20)
        
        # 當前玩家指示
        self.current_player_label = tk.Label(self.root, 
                                           text=f"輪到: {self.get_current_player_name()}", 
                                           font=("Microsoft JhengHei", 16),
                                           bg=self.themes[self.current_theme]["bg"],
                                           fg=self.themes[self.current_theme]["accent"])
        self.current_player_label.pack(pady=10)
        
        # 遊戲棋盤
        self.board_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]["bg"])
        self.board_frame.pack(pady=20)
        
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(self.board_frame, text="", 
                               font=("Microsoft JhengHei", 24, "bold"),
                               width=4, height=2,
                               bg="white",
                               command=lambda r=i, c=j: self.make_move(r, c))
                btn.grid(row=i, column=j, padx=2, pady=2)
                row.append(btn)
            self.buttons.append(row)
        
        # 控制按鈕
        control_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]["bg"])
        control_frame.pack(pady=20)
        
        tk.Button(control_frame, text="重新開始", 
                 font=("Microsoft JhengHei", 12),
                 bg=self.themes[self.current_theme]["button"],
                 command=self.restart_game,
                 width=12).pack(side=tk.LEFT, padx=10)
        
        tk.Button(control_frame, text="返回主選單", 
                 font=("Microsoft JhengHei", 12),
                 bg=self.themes[self.current_theme]["button"],
                 command=self.back_to_menu,
                 width=12).pack(side=tk.LEFT, padx=10)
    
    def get_current_player_name(self):
        if self.current_player == "X":
            return self.player1_name
        else:
            return self.player2_name
    
    def make_move(self, row, col):
        if self.board[row][col] != "":
            return
        
        # 玩家下棋
        self.board[row][col] = self.current_player
        self.update_button(row, col)
        
        # 檢查勝負
        if self.check_winner():
            self.handle_game_end(self.current_player)
            return
        
        if self.is_board_full():
            self.handle_game_end("tie")
            return
        
        # 切換玩家
        self.current_player = "O" if self.current_player == "X" else "X"
        self.current_player_label.config(text=f"輪到: {self.get_current_player_name()}")
        
        # AI回合
        if self.game_mode == "ai" and self.current_player == "O":
            self.root.after(500, self.ai_move)  # 延遲500ms讓AI下棋
    
    def update_button(self, row, col):
        symbol = self.board[row][col]
        color = "red" if symbol == "X" else "blue"
        self.buttons[row][col].config(text=symbol, fg=color, state="disabled")
    
    def ai_move(self):
        # 簡單的AI邏輯：優先阻擋玩家獲勝，然後尋找自己的獲勝機會，最後隨機下棋
        
        # 檢查AI是否能獲勝
        move = self.find_winning_move("O")
        if move:
            row, col = move
            self.board[row][col] = "O"
            self.update_button(row, col)
        else:
            # 檢查是否需要阻擋玩家
            move = self.find_winning_move("X")
            if move:
                row, col = move
                self.board[row][col] = "O"
                self.update_button(row, col)
            else:
                # 隨機選擇空位
                empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
                if empty_cells:
                    row, col = random.choice(empty_cells)
                    self.board[row][col] = "O"
                    self.update_button(row, col)
        
        # 檢查AI是否獲勝
        if self.check_winner():
            self.handle_game_end("O")
            return
        
        if self.is_board_full():
            self.handle_game_end("tie")
            return
        
        # 切換回玩家
        self.current_player = "X"
        self.current_player_label.config(text=f"輪到: {self.get_current_player_name()}")
    
    def find_winning_move(self, player):
        # 檢查每個空位，看是否能形成獲勝組合
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    # 暫時下棋
                    self.board[i][j] = player
                    # 檢查是否獲勝
                    if self.check_winner():
                        self.board[i][j] = ""  # 恢復
                        return (i, j)
                    self.board[i][j] = ""  # 恢復
        return None
    
    def check_winner(self):
        # 檢查行
        for row in self.board:
            if row[0] == row[1] == row[2] != "":
                return True
        
        # 檢查列
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                return True
        
        # 檢查對角線
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
        
        return False
    
    def is_board_full(self):
        for row in self.board:
            for cell in row:
                if cell == "":
                    return False
        return True
    
    def handle_game_end(self, winner):
        self.games_played += 1
        
        if winner == "X":
            self.player1_wins += 1
            messagebox.showinfo("遊戲結束", f"{self.player1_name} 獲勝！")
        elif winner == "O":
            self.player2_wins += 1
            messagebox.showinfo("遊戲結束", f"{self.player2_name} 獲勝！")
        else:
            messagebox.showinfo("遊戲結束", "平局！")
        
        # 檢查是否有玩家達到3勝
        if self.player1_wins >= 3 or self.player2_wins >= 3 or self.games_played >= 5:
            self.show_final_result()
        else:
            # 繼續下一局
            self.setup_game_board()
    
    def show_final_result(self):
        self.game_in_progress = False
        
        if self.player1_wins > self.player2_wins:
            winner_msg = f"{self.player1_name} 恭喜你獲勝！"
            loser_msg = f"{self.player2_name} 挑戰失敗"
        elif self.player2_wins > self.player1_wins:
            winner_msg = f"{self.player2_name} 恭喜你獲勝！"
            loser_msg = f"{self.player1_name} 挑戰失敗"
        else:
            winner_msg = "平局！雙方實力相當"
            loser_msg = ""
        
        result_text = f"五局挑戰結束！\n\n{winner_msg}"
        if loser_msg:
            result_text += f"\n{loser_msg}"
        
        result_text += f"\n\n最終比分：\n{self.player1_name}: {self.player1_wins}勝\n{self.player2_name}: {self.player2_wins}勝"
        
        messagebox.showinfo("挑戰結束", result_text)
        self.setup_main_menu()
    
    def restart_game(self):
        if self.game_in_progress:
            result = messagebox.askyesno("確認重新開始", 
                                       "當前挑戰尚未完成，確定要重新開始嗎？\n\n選擇 Yes 重新開始\n選擇 No 繼續挑戰")
            if not result:
                return
        
        # 重置所有遊戲狀態
        self.player1_wins = 0
        self.player2_wins = 0
        self.games_played = 0
        self.game_in_progress = True
        self.setup_game_board()
    
    def back_to_menu(self):
        if self.game_in_progress:
            result = messagebox.askyesno("確認返回", 
                                       "當前挑戰尚未完成，確定要返回主選單嗎？\n\n選擇 Yes 返回主選單\n選擇 No 繼續挑戰")
            if not result:
                return
        
        self.game_in_progress = False
        self.setup_main_menu()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()