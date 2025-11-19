import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import time

class PresentationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python 展演型圖片輪播系統")
        self.root.geometry("1000x750")
        self.root.configure(bg="#1e1e1e")

        # --- 變數初始化 ---
        self.image_paths = []
        self.current_index = 0
        
        # 狀態控制
        self.is_playing = False
        self.play_job = None      
        self.timer_job = None     
        self.total_seconds = 0    
        self.is_fullscreen = False

        # 輪播邏輯變數
        self.loops_completed = 0  # 目前已完成幾輪
        self.display_mode = "IDLE" # IDLE, WELCOME, IMAGES, THANKYOU

        # --- 1. 頂部設定區 (輸入歡迎詞、致謝詞、次數) ---
        top_frame = tk.Frame(root, bg="#333", pady=10)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # 設定區排版
        tk.Label(top_frame, text="開場歡迎詞:", bg="#333", fg="white").grid(row=0, column=0, padx=5, sticky="e")
        self.entry_welcome = tk.Entry(top_frame, width=20)
        self.entry_welcome.insert(0, "Welcome to the Show")
        self.entry_welcome.grid(row=0, column=1, padx=5)

        tk.Label(top_frame, text="結束致謝詞:", bg="#333", fg="white").grid(row=0, column=2, padx=5, sticky="e")
        self.entry_thankyou = tk.Entry(top_frame, width=20)
        self.entry_thankyou.insert(0, "Thank You for Watching")
        self.entry_thankyou.grid(row=0, column=3, padx=5)

        tk.Label(top_frame, text="輪播次數:", bg="#333", fg="white").grid(row=0, column=4, padx=5, sticky="e")
        self.spin_loops = tk.Spinbox(top_frame, from_=1, to=100, width=5)
        self.spin_loops.delete(0, "end")
        self.spin_loops.insert(0, 1) # 預設 1 次
        self.spin_loops.grid(row=0, column=5, padx=5)

        # --- 2. 圖片/文字顯示層 (中間) ---
        self.display_frame = tk.Frame(root, bg="black")
        self.display_frame.pack(fill=tk.BOTH, expand=True)
        
        # 這個 Label 負責顯示 圖片 或 文字
        self.lbl_display = tk.Label(self.display_frame, text="請先載入圖片\n並設定參數", 
                                    bg="black", fg="#888", font=("微軟正黑體", 24))
        self.lbl_display.pack(fill=tk.BOTH, expand=True)

        # --- 3. 兩側切換按鈕 (懸浮) ---
        self.btn_prev = tk.Button(root, text="❮", command=self.prev_image, state=tk.DISABLED,
                                  font=("Arial", 20), bg="#444", fg="white", bd=0, cursor="hand2")
        self.btn_prev.place(relx=0.02, rely=0.5, anchor=tk.W, height=80, width=50)

        self.btn_next = tk.Button(root, text="❯", command=self.next_image, state=tk.DISABLED,
                                  font=("Arial", 20), bg="#444", fg="white", bd=0, cursor="hand2")
        self.btn_next.place(relx=0.98, rely=0.5, anchor=tk.E, height=80, width=50)

        # --- 4. 底部控制面板 ---
        self.control_frame = tk.Frame(root, bg="#2b2b2b", padx=10, pady=8)
        self.control_frame.place(relx=0.5, rely=0.96, anchor=tk.S, relwidth=0.95)

        # (A) 載入圖片按鈕 (移到這裡了)
        self.btn_load = tk.Button(self.control_frame, text="📂 載入圖片", command=self.load_images, 
                                  font=("Arial", 11), bg="#ddd", cursor="hand2")
        self.btn_load.pack(side=tk.LEFT, padx=10)

        # (B) 播放控制
        tk.Label(self.control_frame, text="間隔(秒):", bg="#2b2b2b", fg="white").pack(side=tk.LEFT)
        self.spin_interval = tk.Spinbox(self.control_frame, from_=1, to=60, width=4)
        self.spin_interval.delete(0, "end")
        self.spin_interval.insert(0, 3)
        self.spin_interval.pack(side=tk.LEFT, padx=5)

        self.btn_play = tk.Button(self.control_frame, text="▶ 開始展演", command=self.start_presentation_sequence, 
                                  state=tk.DISABLED, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), padx=10)
        self.btn_play.pack(side=tk.LEFT, padx=15)

        # (C) 資訊顯示
        self.lbl_timer = tk.Label(self.control_frame, text="時間: 00:00", bg="#2b2b2b", fg="#00ff00", font=("Consolas", 12))
        self.lbl_timer.pack(side=tk.LEFT, padx=15)

        self.lbl_loop_status = tk.Label(self.control_frame, text="輪播: 0/0", bg="#2b2b2b", fg="#ffcc00", font=("Arial", 10))
        self.lbl_loop_status.pack(side=tk.LEFT, padx=10)

        # (D) 右側功能
        self.btn_fullscreen = tk.Button(self.control_frame, text="⛶ 全螢幕", command=self.toggle_fullscreen,
                                        bg="#555", fg="white")
        self.btn_fullscreen.pack(side=tk.RIGHT, padx=10)
        
        self.lbl_status = tk.Label(self.control_frame, text="0 / 0", bg="#2b2b2b", fg="#aaa")
        self.lbl_status.pack(side=tk.RIGHT, padx=10)

        # 綁定事件
        self.root.bind("<Configure>", self.on_resize)
        self.root.bind("<Escape>", self.exit_fullscreen)

    def load_images(self):
        paths = filedialog.askopenfilenames(title="選擇圖片", filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if paths:
            self.stop_autoplay()
            self.image_paths = list(paths)
            self.current_index = 0
            self.display_mode = "IMAGES" # 預覽模式
            
            self.btn_prev.config(state=tk.NORMAL)
            self.btn_next.config(state=tk.NORMAL)
            self.btn_play.config(state=tk.NORMAL, text="▶ 開始展演", bg="#4CAF50")
            
            self.show_image()

    # --- 顯示邏輯 (區分 文字 vs 圖片) ---

    def show_text(self, text_content, font_size=40, color="white"):
        """在主畫面顯示文字"""
        self.lbl_display.config(image="", text=text_content, fg=color, font=("微軟正黑體", font_size, "bold"))
        self.lbl_display.image = None # 清除圖片參照

    def show_image(self):
        """在主畫面顯示圖片"""
        if not self.image_paths: return

        try:
            # 讀取圖片
            img_path = self.image_paths[self.current_index]
            original_image = Image.open(img_path)
            
            # 取得尺寸
            win_w = self.root.winfo_width()
            win_h = self.root.winfo_height()
            if win_w < 10: win_w, win_h = 1000, 700

            # 顯示圖片 Label 填滿 (不含邊距)
            frame_h = self.display_frame.winfo_height()
            if frame_h > 10: win_h = frame_h

            img_copy = original_image.copy()
            img_copy.thumbnail((win_w, win_h), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img_copy)

            self.lbl_display.config(image=photo, text="")
            self.lbl_display.image = photo
            
            self.lbl_status.config(text=f"{self.current_index + 1} / {len(self.image_paths)}")

        except Exception as e:
            print("Error:", e)

    # --- 展演流程控制 (核心) ---

    def start_presentation_sequence(self):
        """啟動整個展演流程"""
        if self.is_playing:
            self.stop_autoplay()
            return

        # 1. 初始化狀態
        self.is_playing = True
        self.loops_completed = 0
        self.current_index = 0
        self.total_seconds = 0
        self.btn_play.config(text="⏹ 停止", bg="#FF5722")
        
        # 更新輪播目標次數
        try:
            self.target_loops = int(self.spin_loops.get())
        except:
            self.target_loops = 1
        
        self.update_loop_status()
        self.start_timer()

        # 2. 進入全螢幕
        if not self.is_fullscreen:
            self.toggle_fullscreen()

        # 3. 顯示歡迎詞 (Phase 1)
        self.display_mode = "WELCOME"
        welcome_txt = self.entry_welcome.get()
        self.show_text(welcome_txt)
        
        # 3秒後進入圖片輪播
        self.root.after(3000, self.start_image_loop)

    def start_image_loop(self):
        """開始圖片輪播階段 (Phase 2)"""
        if not self.is_playing: return
        
        self.display_mode = "IMAGES"
        self.run_slide_logic() # 立即顯示第一張

    def run_slide_logic(self):
        """單張圖片的處理邏輯 (含淡入淡出)"""
        if not self.is_playing: return

        # 執行淡入效果 (Fade In)
        self.fade_transition(to_black=False) 
        self.show_image()

        # 計算下一張的延遲
        try:
            interval = int(self.spin_interval.get())
            if interval < 1: interval = 1
        except: interval = 2
        
        # 排程：間隔時間後，準備切下一張
        self.play_job = self.root.after(interval * 1000, self.prepare_next_slide)

    def prepare_next_slide(self):
        """準備下一張之前的檢查"""
        if not self.is_playing: return

        # 淡出 (Fade Out) -> 視覺上變暗
        self.fade_transition(to_black=True)

        # 計算索引
        self.current_index += 1
        
        # 檢查是否跑完一輪
        if self.current_index >= len(self.image_paths):
            self.current_index = 0
            self.loops_completed += 1
            self.update_loop_status()

            # 檢查是否達到總次數
            if self.loops_completed >= self.target_loops:
                self.end_presentation()
                return

        # 繼續播放下一張
        self.run_slide_logic()

    def end_presentation(self):
        """結束階段：致謝詞 (Phase 3)"""
        self.display_mode = "THANKYOU"
        thank_txt = self.entry_thankyou.get()
        self.show_text(thank_txt)
        
        # 停止計時與自動播放
        if self.timer_job: self.root.after_cancel(self.timer_job)
        
        # 3秒後退出全螢幕，但保持在致謝畫面
        self.root.after(3000, self.finish_sequence)

    def finish_sequence(self):
        """最終清理"""
        if self.is_fullscreen:
            self.exit_fullscreen()
        
        self.is_playing = False
        self.btn_play.config(text="▶ 重新展演", bg="#4CAF50")
        # 畫面停留在致謝詞，不動作

    # --- 視覺特效 ---

    def fade_transition(self, to_black=True):
        """
        模擬淡入淡出。
        由於 Tkinter 元件不支援 Alpha，這裡使用調整 '視窗透明度' 的方式模擬淡出。
        雖然會稍微看到桌面，但這是原生 Tkinter 唯一順暢的淡出方式。
        """
        step = 0.05
        delay = 10 # ms
        
        if to_black:
            # 變透明 (Fade Out)
            for i in range(10, -1, -1): # 1.0 -> 0.0
                alpha = i / 10.0
                # 限制最低透明度，避免視窗完全消失讓使用者驚慌，保留 0.1
                if alpha < 0.1: alpha = 0.1 
                self.root.attributes('-alpha', alpha)
                self.root.update()
                time.sleep(delay / 1000)
        else:
            # 變實體 (Fade In)
            for i in range(0, 11): # 0.0 -> 1.0
                alpha = i / 10.0
                self.root.attributes('-alpha', alpha)
                self.root.update()
                time.sleep(delay / 1000)
        
        # 確保最後是不透明
        self.root.attributes('-alpha', 1.0)

    # --- 輔助功能 ---

    def next_image(self):
        if self.image_paths:
            self.current_index = (self.current_index + 1) % len(self.image_paths)
            self.show_image()

    def prev_image(self):
        if self.image_paths:
            self.current_index = (self.current_index - 1 + len(self.image_paths)) % len(self.image_paths)
            self.show_image()

    def start_timer(self):
        if self.is_playing:
            self.total_seconds += 1
            mins, secs = divmod(self.total_seconds, 60)
            self.lbl_timer.config(text=f"時間: {mins:02d}:{secs:02d}")
            self.timer_job = self.root.after(1000, self.start_timer)

    def update_loop_status(self):
        self.lbl_loop_status.config(text=f"輪播: {self.loops_completed}/{self.target_loops}")

    def stop_autoplay(self):
        self.is_playing = False
        self.btn_play.config(text="▶ 開始展演", bg="#4CAF50")
        if self.play_job: self.root.after_cancel(self.play_job)
        if self.timer_job: self.root.after_cancel(self.timer_job)
        self.root.attributes('-alpha', 1.0) # 確保視窗不透明

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        self.btn_fullscreen.config(text="⛶ 視窗" if self.is_fullscreen else "⛶ 全螢幕")

    def exit_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.root.attributes("-fullscreen", False)
        self.btn_fullscreen.config(text="⛶ 全螢幕")

    def on_resize(self, event):
        if event.widget == self.root and self.image_paths and self.display_mode == "IMAGES":
            self.show_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = PresentationApp(root)
    root.mainloop()