import tkinter as tk
from tkinter import messagebox, simpledialog
import random

# 預設五種按鈕背景色
BG_COLORS = ['#DDDDDD', '#FFF8DC', '#DFFFD6', '#FFFFC2', '#D0F0FF']

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("井字遊戲")

        self.bg_index = 0

        # 五戰三勝局數紀錄
        self.scores = [0, 0]
        self.round_games = 0  # 已玩局數 （最多5局）

        # 是否與AI對戰
        self.is_ai = False

        # 棋盤狀態 3x3 list，空為 None，O或X為字串
        self.board = [None] * 9

        self.current_player = 0  # 0: 玩家1(O)，1: 玩家2或AI(X)

        self.player_names = ["玩家1", "玩家2"]

        self.buttons = []

        self.setup_start_screen()

    def setup_start_screen(self):
        # 清除畫面
        for w in self.root.winfo_children():
            w.destroy()

        title = tk.Label(self.root, text="井字遊戲 - 請選擇模式", font=("Arial", 24))
        title.pack(pady=20)

        btn_human = tk.Button(self.root, text="真人對戰", font=("Arial", 16), width=15, command=self.setup_human)
        btn_human.pack(pady=10)

        btn_ai = tk.Button(self.root, text="與AI對戰", font=("Arial", 16), width=15, command=self.setup_ai)
        btn_ai.pack(pady=10)

    def setup_human(self):
        self.is_ai = False
        # 兩個玩家輸入姓名
        name1 = simpledialog.askstring("玩家1姓名", "請輸入玩家1的名字", parent=self.root)
        if not name1:
            name1 = "玩家1"
        name2 = simpledialog.askstring("玩家2姓名", "請輸入玩家2的名字", parent=self.root)
        if not name2:
            name2 = "玩家2"
        self.player_names = [name1, name2]
        self.start_game()

    def setup_ai(self):
        self.is_ai = True
        name1 = simpledialog.askstring("玩家姓名", "請輸入你的名字", parent=self.root)
        if not name1:
            name1 = "玩家"
        self.player_names = [name1, "電腦"]
        self.start_game()

    def start_game(self):
        # 清畫面
        for w in self.root.winfo_children():
            w.destroy()

        self.scores = [0, 0]
        self.round_games = 0
        self.current_player = 0
        self.board = [None] * 9
        self.buttons = []

        # 標題
        self.label_title = tk.Label(self.root, text=f"五戰三勝模式 {self.player_names[0]}(O)-藍色 vs {self.player_names[1]}(X)-紅色", font=("Arial", 16))
        self.label_title.pack(pady=10)

        # 顯示比分
        self.score_label = tk.Label(self.root, text=self.get_score_text(), font=("Arial", 14))
        self.score_label.pack()

        # 棋盤按鈕框架
        board_frame = tk.Frame(self.root)
        board_frame.pack(pady=10)

        for i in range(9):
            btn = tk.Button(board_frame, text="", font=("Arial", 32), width=4, height=2,
                            bg=BG_COLORS[self.bg_index],
                            command=lambda idx=i: self.on_move(idx))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)

        # 背景切換按鈕
        btn_bg = tk.Button(self.root, text="切換背景", font=("Arial", 12), command=self.switch_bg)
        btn_bg.pack(pady=5)

        # 重啟按鈕
        btn_restart = tk.Button(self.root, text="重啟遊戲", font=("Arial", 12), command=self.confirm_restart)
        btn_restart.pack(pady=5)

        # 顯示當前玩家
        self.turn_label = tk.Label(self.root, text=self.get_turn_text(), font=("Arial", 14))
        self.turn_label.pack(pady=5)

        # 若AI先手，AI自動下第一步
        if self.is_ai and self.current_player == 1:
            self.root.after(500, self.ai_move)

    def get_score_text(self):
        return f"比分：{self.player_names[0]} {self.scores[0]} : {self.scores[1]} {self.player_names[1]}"

    def get_turn_text(self):
        return f"輪到：{self.player_names[self.current_player]}（{'O' if self.current_player==0 else 'X'}）"

    def on_move(self, idx):
        if self.board[idx] is not None:
            return  # 不能選已佔位置

        sign = "O" if self.current_player == 0 else "X"
        color = "blue" if sign == "O" else "red"

        self.buttons[idx].config(text=sign, fg=color)
        self.board[idx] = sign

        # 檢查是否有勝利
        if self.check_winner(sign):
            self.scores[self.current_player] += 1
            self.round_games += 1
            self.update_score_label()

            if self.scores[self.current_player] == 3:
                # 有玩家連取三勝
                messagebox.showinfo("勝利", f"{self.player_names[self.current_player]} 恭喜你獲勝！")
                loser = 1 - self.current_player
                messagebox.showinfo("挑戰結果", f"{self.player_names[loser]} 挑戰失敗")
                self.ask_restart_or_exit(full_restart=True)
                return
            else:
                messagebox.showinfo("本局結束", f"{self.player_names[self.current_player]} 獲勝本局！")
                self.reset_board()
                return

        # 無人勝，判斷平手
        if all(self.board):
            self.round_games += 1
            messagebox.showinfo("平手", "本局平手！")
            if self.round_games >= 5:
                messagebox.showinfo("五局結束", "五局結束，未有五勝家。比賽結束。")
                self.ask_restart_or_exit(full_restart=True)
                return
            self.reset_board()
            return

        # 換人下
        self.current_player = 1 - self.current_player
        self.update_turn_label()

        # AI下棋(如果目前輪到AI)
        if self.is_ai and self.current_player == 1:
            self.root.after(500, self.ai_move)  # 延遲0.5秒更自然

    def ai_move(self):
        empty_indexes = [i for i, v in enumerate(self.board) if v is None]
        if not empty_indexes:
            return
        idx = random.choice(empty_indexes)
        self.on_move(idx)

    def update_score_label(self):
        self.score_label.config(text=self.get_score_text())

    def update_turn_label(self):
        self.turn_label.config(text=self.get_turn_text())

    def reset_board(self):
        self.board = [None] * 9
        for b in self.buttons:
            b.config(text="", fg="black", bg=BG_COLORS[self.bg_index])
        # 輪到先前贏家先手（或維持當前player）
        # 這裡維持先前先手規則不變
        # 更新顯示
        self.update_turn_label()

    def check_winner(self, sign):
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # 橫排
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # 直排
            (0, 4, 8), (2, 4, 6)              # 斜排
        ]
        for line in wins:
            if all(self.board[i] == sign for i in line):
                # 突顯勝利連線按鈕背景
                for i in line:
                    self.buttons[i].config(bg="gold")
                return True
        return False

    def switch_bg(self):
        self.bg_index = (self.bg_index + 1) % len(BG_COLORS)
        for b in self.buttons:
            if b['text'] == "":
                b.config(bg=BG_COLORS[self.bg_index])

    def confirm_restart(self):
        if self.round_games > 0 and self.round_games < 5 and max(self.scores) < 3:
            # 遊戲中途點重啟，跳出確認視窗
            if messagebox.askyesno("確認", "本輪五局尚未完成，確定要重啟嗎？"):
                self.reset_full_game()
        else:
            self.reset_full_game()

    def reset_full_game(self):
        self.scores = [0, 0]
        self.round_games = 0
        self.current_player = 0
        self.board = [None] * 9
        for b in self.buttons:
            b.config(text="", fg="black", bg=BG_COLORS[self.bg_index])
        self.update_score_label()
        self.update_turn_label()

    def ask_restart_or_exit(self, full_restart=False):
        resp = messagebox.askyesno("重新開始？", "是否要重新開始遊戲？")
        if resp:
            if full_restart:
                self.reset_full_game()
            else:
                self.reset_board()
        else:
            # 不重啟 直接結束
            self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
