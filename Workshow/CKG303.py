import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import time

class AdvancedImagePlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Python 高階圖片輪播")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e1e")

        # --- 變數初始化 ---
        self.image_paths = []
        self.current_index = 0
        
        # 自動播放相關
        self.is_playing = False
        self.play_job = None      # 用來儲存自動播放的排程 ID
        self.timer_job = None     # 用來儲存計時器的排程 ID
        self.total_seconds = 0    # 總播放秒數

        # 全螢幕狀態
        self.is_fullscreen = False

        # --- 1. 圖片顯示層 (底層) ---
        self.lbl_image = tk.Label(root, text="請載入圖片", bg="#1e1e1e", fg="#555", font=("微軟正黑體", 24))
        self.lbl_image.pack(fill=tk.BOTH, expand=True)

        # --- 2. 介面層 (懸浮控制項) ---

        # [頂部] 載入按鈕
        self.btn_load = tk.Button(root, text="📂 載入圖片", command=self.load_images, 
                                  font=("Arial", 11), bg="#ddd", cursor="hand2")
        self.btn_load.place(relx=0.5, rely=0.02, anchor=tk.N)

        # [兩側] 切換按鈕
        self.btn_prev = tk.Button(root, text="❮", command=self.prev_image, state=tk.DISABLED,
                                  font=("Arial", 20), bg="#444", fg="white", bd=0, cursor="hand2")
        self.btn_prev.place(relx=0.02, rely=0.5, anchor=tk.W, height=80, width=50)

        self.btn_next = tk.Button(root, text="❯", command=self.next_image, state=tk.DISABLED,
                                  font=("Arial", 20), bg="#444", fg="white", bd=0, cursor="hand2")
        self.btn_next.place(relx=0.98, rely=0.5, anchor=tk.E, height=80, width=50)

        # [底部] 綜合控制面板 (黑色半透明條)
        self.control_frame = tk.Frame(root, bg="#2b2b2b", padx=10, pady=5)
        self.control_frame.place(relx=0.5, rely=0.96, anchor=tk.S, relwidth=0.9)

        # -- 面板內容 --
        
        # 1. 總時間顯示
        self.lbl_timer = tk.Label(self.control_frame, text="時間: 00:00", bg="#2b2b2b", fg="#00ff00", font=("Consolas", 12))
        self.lbl_timer.pack(side=tk.LEFT, padx=15)

        # 2. 秒數設定
        tk.Label(self.control_frame, text="間隔(秒):", bg="#2b2b2b", fg="white").pack(side=tk.LEFT)
        self.spin_interval = tk.Spinbox(self.control_frame, from_=1, to=60, width=3, font=("Arial", 12))
        self.spin_interval.delete(0, "end")
        self.spin_interval.insert(0, 2) # 預設 2 秒
        self.spin_interval.pack(side=tk.LEFT, padx=5)

        # 3. 播放/暫停按鈕
        self.btn_play = tk.Button(self.control_frame, text="▶ 播放", command=self.toggle_autoplay, 
                                  state=tk.DISABLED, bg="#4CAF50", fg="white", width=10, font=("Arial", 10, "bold"))
        self.btn_play.pack(side=tk.LEFT, padx=15)

        # 4. 全螢幕按鈕
        self.btn_fullscreen = tk.Button(self.control_frame, text="⛶ 全螢幕", command=self.toggle_fullscreen,
                                        bg="#555", fg="white", font=("Arial", 10))
        self.btn_fullscreen.pack(side=tk.RIGHT, padx=10)

        # 5. 頁碼顯示
        self.lbl_status = tk.Label(self.control_frame, text="0 / 0", bg="#2b2b2b", fg="#aaa", font=("Arial", 10))
        self.lbl_status.pack(side=tk.RIGHT, padx=15)


        # 綁定事件
        self.root.bind("<Configure>", self.on_resize)
        self.root.bind("<Escape>", self.exit_fullscreen) # 按 ESC 退出全螢幕

    def load_images(self):
        """載入圖片並重置狀態"""
        file_types = [("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        paths = filedialog.askopenfilenames(title="選擇圖片", filetypes=file_types)

        if paths:
            # 停止目前的播放
            self.stop_autoplay()
            self.reset_timer()

            self.image_paths = list(paths)
            self.current_index = 0
            
            # 更新 UI
            self.btn_prev.config(state=tk.NORMAL)
            self.btn_next.config(state=tk.NORMAL)
            self.btn_play.config(state=tk.NORMAL, text="▶ 播放", bg="#4CAF50")
            
            self.show_image()

    def show_image(self):
        """顯示當前圖片 (核心邏輯)"""
        if not self.image_paths: return

        try:
            # 讀取圖片
            img_path = self.image_paths[self.current_index]
            original_image = Image.open(img_path)
            
            # 取得視窗大小
            win_w = self.root.winfo_width()
            win_h = self.root.winfo_height()
            if win_w < 10: win_w, win_h = 1000, 700 # 防錯

            # 縮放邏輯
            img_copy = original_image.copy()
            img_copy.thumbnail((win_w, win_h), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img_copy)

            self.lbl_image.config(image=photo, text="")
            self.lbl_image.image = photo # 防止被回收
            
            # 更新頁碼
            self.lbl_status.config(text=f"{self.current_index + 1} / {len(self.image_paths)}")

        except Exception as e:
            print("Error:", e)

    def next_image(self):
        if self.image_paths:
            self.current_index = (self.current_index + 1) % len(self.image_paths)
            self.show_image()

    def prev_image(self):
        if self.image_paths:
            self.current_index = (self.current_index - 1 + len(self.image_paths)) % len(self.image_paths)
            self.show_image()

    # --- 自動播放與計時器功能 ---

    def toggle_autoplay(self):
        """切換播放/暫停狀態"""
        if self.is_playing:
            self.stop_autoplay()
        else:
            self.start_autoplay()

    def start_autoplay(self):
        self.is_playing = True
        self.btn_play.config(text="⏸ 暫停", bg="#FF5722") # 變橘色
        
        # 啟動圖片輪播迴圈
        self.schedule_next_slide()
        
        # 啟動總計時器 (如果還沒啟動)
        if self.timer_job is None:
            self.update_total_timer()

    def stop_autoplay(self):
        self.is_playing = False
        self.btn_play.config(text="▶ 播放", bg="#4CAF50") # 變綠色
        
        # 取消圖片輪播排程
        if self.play_job:
            self.root.after_cancel(self.play_job)
            self.play_job = None
        
        # 注意：這裡我設計為「暫停時，總時間計數也暫停」。
        # 如果你想讓時間一直跑，可以把下面這段註解掉
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    def schedule_next_slide(self):
        """排程下一張圖片"""
        if self.is_playing:
            try:
                # 讀取使用者輸入的秒數
                interval = int(self.spin_interval.get())
                if interval < 1: interval = 1
            except ValueError:
                interval = 2 # 如果輸入無效，預設 2 秒
            
            # 設定定時器 (毫秒)
            self.play_job = self.root.after(interval * 1000, self.run_slide_logic)

    def run_slide_logic(self):
        """執行切換並設定下一次"""
        self.next_image()
        self.schedule_next_slide()

    # --- 總時間計數器 ---

    def update_total_timer(self):
        """每秒更新一次總時間"""
        if self.is_playing:
            self.total_seconds += 1
            
            # 格式化時間 MM:SS
            mins, secs = divmod(self.total_seconds, 60)
            time_str = f"{mins:02d}:{secs:02d}"
            self.lbl_timer.config(text=f"時間: {time_str}")
            
        # 每 1000 毫秒 (1秒) 呼叫自己一次
        self.timer_job = self.root.after(1000, self.update_total_timer)

    def reset_timer(self):
        """重置計時器"""
        self.total_seconds = 0
        self.lbl_timer.config(text="時間: 00:00")
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    # --- 全螢幕控制 ---

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        
        if self.is_fullscreen:
            self.btn_fullscreen.config(text="⛶ 視窗")
        else:
            self.btn_fullscreen.config(text="⛶ 全螢幕")

    def exit_fullscreen(self, event=None):
        """按 ESC 離開全螢幕"""
        self.is_fullscreen = False
        self.root.attributes("-fullscreen", False)
        self.btn_fullscreen.config(text="⛶ 全螢幕")

    def on_resize(self, event):
        if event.widget == self.root and self.image_paths:
            # 為了效能，可以不用每次微調都重繪，但這裡直接呼叫最流暢
            self.show_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedImagePlayer(root)
    root.mainloop()