import tkinter as tk
from tkinter import messagebox
import time

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("倒數計時器")
        self.root.geometry("300x200")
        self.root.resizable(False, False)

        self.remaining_time = 0
        self.after_id = None

        # 建立 UI 元件
        self.label = tk.Label(root, text="00:00", font=("Helvetica", 48))
        self.label.pack(pady=10)

        self.entry_frame = tk.Frame(root)
        self.entry_frame.pack(pady=5)
        
        self.entry_label = tk.Label(self.entry_frame, text="請輸入秒數:")
        self.entry_label.pack(side=tk.LEFT)
        
        self.time_entry = tk.Entry(self.entry_frame, width=10)
        self.time_entry.pack(side=tk.LEFT)

        self.start_button = tk.Button(root, text="開始", command=self.start_timer)
        self.start_button.pack(pady=5)

    def update_timer(self):
        """每秒更新一次計時器顯示"""
        if self.remaining_time > 0:
            minutes, seconds = divmod(self.remaining_time, 60)
            self.label.config(text=f"{minutes:02d}:{seconds:02d}")
            self.remaining_time -= 1
            self.after_id = self.root.after(1000, self.update_timer)
        else:
            self.label.config(text="時間到！")
            self.start_button.config(state=tk.NORMAL)
            messagebox.showinfo("計時器", "吃飯了！")

    def start_timer(self):
        """從輸入框獲取時間並開始計時"""
        try:
            self.remaining_time = int(self.time_entry.get())
            if self.remaining_time <= 0:
                messagebox.showerror("錯誤", "請輸入一個大於 0 的秒數。")
                return

            self.start_button.config(state=tk.DISABLED)
            self.update_timer()
        except ValueError:
            messagebox.showerror("錯誤", "無效的輸入。請輸入一個整數。")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
