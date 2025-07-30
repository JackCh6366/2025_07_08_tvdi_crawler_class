import tkinter as tk
from tkinter import messagebox
import random

# 初始化主畫面
root = tk.Tk()
root.title("井字遊戲：五局三勝挑戰")

# 玩家資料與設定
player1_name = ""
player2_name = ""
player1_score = 0
player2_score = 0
current_player = "X"
game_mode = "PvP"  # 可選 PvP 或 PvE
round_counter = 0

# 顏色樣式：五種背景主題
button_styles = [
    {"bg": "#f0f0f0", "font": ("Arial", 16)},         # 樸素灰
    {"bg": "#ffe6e6", "font": ("Courier", 16)},       # 淡粉紅
    {"bg": "#e6f7ff", "font": ("Helvetica", 16)},     # 天空藍
    {"bg": "#e6ffe6", "font": ("Comic Sans MS", 16)}, # 淡綠色
    {"bg": "#fffbe6", "font": ("Verdana", 16)}        # 溫柔黃
]
style_index = 0

# 儲存棋盤按鈕
buttons = []

# 建立棋盤
def create_board():
    global buttons
    buttons.clear()
    for r in range(3):
        for c in range(3):
            b = tk.Button(root, text="", width=8, height=4,
                          bg=button_styles[style_index]["bg"],
                          font=button_styles[style_index]["font"],
                          command=lambda r=r, c=c: player_move(r, c))
            b.grid(row=r+2, column=c)
            buttons.append(b)

# 換樣式背景
def switch_style():
    global style_index
    style_index = (style_index + 1) % len(button_styles)
    for btn in buttons:
        btn.config(bg=button_styles[style_index]["bg"],
                   font=button_styles[style_index]["font"])

# 玩家移動邏輯
def player_move(row, col):
    index = row * 3 + col
    if buttons[index]["text"] == "":
        color = "red" if current_player == "X" else "blue"
        buttons[index].config(text=current_player, fg=color)
        check_winner()
        switch_turn()
        if game_mode == "PvE" and current_player == "O":
            root.after(500, ai_move)

# AI 移動邏輯
def ai_move():
    available = [i for i, btn in enumerate(buttons) if btn["text"] == ""]
    if available:
        choice = random.choice(available)
        buttons[choice].config(text="O", fg="blue")
        check_winner()
        switch_turn()

# 交替玩家
def switch_turn():
    global current_player
    current_player = "O" if current_player == "X" else "X"

# 檢查勝利
def check_winner():
    global player1_score, player2_score, round_counter
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    for a, b, c in wins:
        if buttons[a]["text"] == buttons[b]["text"] == buttons[c]["text"] != "":
            winner = buttons[a]["text"]
            round_counter += 1
            if winner == "X":
                player1_score += 1
                check_game_end(player1_name, player1_score)
            else:
                player2_score += 1
                check_game_end(player2_name, player2_score)
            reset_board()
            return

    # 平手檢查
    if all(btn["text"] != "" for btn in buttons):
        round_counter += 1
        reset_board()

# 重設棋盤
def reset_board():
    for btn in buttons:
        btn.config(text="")

# 遊戲結束檢查
def check_game_end(name, score):
    if score >= 3:
        messagebox.showinfo("結果", f"{name} 恭喜你獲勝！")
        restart_prompt()

# 提示是否重啟
def restart_prompt():
    response = messagebox.askquestion("重啟遊戲", "是否重新開始挑戰？")
    if response == "yes":
        reset_game()
    else:
        pass

# 重設所有分數
def reset_game():
    global player1_score, player2_score, round_counter
    player1_score = 0
    player2_score = 0
    round_counter = 0
    reset_board()

# --- UI 控制按鈕 ---
tk.Button(root, text="切換背景", command=switch_style).grid(row=0, column=0)
tk.Button(root, text="重啟遊戲", command=restart_prompt).grid(row=0, column=1)

# 模擬玩家名稱輸入（正式應用可改為 Entry 輸入框）
player1_name = "小紅"
player2_name = "小藍"
game_mode = "PvE"  # PvP or PvE

create_board()
root.mainloop()