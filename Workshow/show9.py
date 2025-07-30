import tkinter as tk
from tkinter import messagebox
import random

class Plane:
    def __init__(self, color, id):
        self.color = color
        self.id = id
        self.position = -1  # -1 = 未起飛
        self.finished = False

    def fly(self):
        self.position = 0  # 起飛點

    def move(self, steps):
        if self.position != -1 and not self.finished:
            self.position += steps
            if self.position >= 56:
                self.position = 56
                self.finished = True

class Player:
    def __init__(self, color):
        self.color = color
        self.planes = [Plane(color, i) for i in range(4)]

    def has_unfinished_planes(self):
        return any(not p.finished for p in self.planes)

class Game:
    def __init__(self, root):
        self.root = root
        self.players = [Player("紅"), Player("藍")]
        self.current_player = 0

        self.label = tk.Label(root, text="歡迎來到飛行棋！")
        self.label.pack()

        self.dice_btn = tk.Button(root, text="擲骰子", command=self.roll_dice)
        self.dice_btn.pack()

    def roll_dice(self):
        dice = random.randint(1, 6)
        current = self.players[self.current_player]
        msg = f"{current.color} 玩家擲到 {dice} 點！"

        if dice == 6:
            for plane in current.planes:
                if plane.position == -1:
                    plane.fly()
                    msg += "\n有一架飛機起飛！"
                    break
        else:
            for plane in current.planes:
                if plane.position != -1 and not plane.finished:
                    plane.move(dice)
                    msg += f"\n飛機前進 {dice} 步！"
                    break

        self.label.config(text=msg)
        self.current_player = (self.current_player + 1) % len(self.players)

root = tk.Tk()
root.title("飛行棋")
game = Game(root)
root.mainloop()
