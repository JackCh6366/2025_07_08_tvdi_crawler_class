import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageCarouselApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python 圖片輪播展示器")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # 初始化變數
        self.image_paths = []  # 儲存圖片路徑
        self.current_index = 0 # 當前圖片索引

        # --- 介面佈局 ---

        # 1. 頂部控制區
        top_frame = tk.Frame(root, pady=10)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        self.btn_load = tk.Button(top_frame, text="📂 選擇圖片 (可多選)", command=self.load_images, font=("Arial", 12), bg="#e1e1e1")
        self.btn_load.pack()

        # 2. 圖片顯示區
        self.image_frame = tk.Frame(root, bg="#333") # 深色背景讓圖片更明顯
        self.image_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        self.lbl_image = tk.Label(self.image_frame, text="請點擊上方按鈕選擇圖片", bg="#333", fg="white", font=("Arial", 16))
        self.lbl_image.pack(expand=True)

        # 3. 底部導航區
        bottom_frame = tk.Frame(root, pady=20)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.btn_prev = tk.Button(bottom_frame, text="❮ 上一張", command=self.prev_image, state=tk.DISABLED, font=("Arial", 12), width=10)
        self.btn_prev.pack(side=tk.LEFT, padx=50)

        self.lbl_status = tk.Label(bottom_frame, text="0 / 0", font=("Arial", 12))
        self.lbl_status.pack(side=tk.LEFT, expand=True)

        self.btn_next = tk.Button(bottom_frame, text="下一張 ❯", command=self.next_image, state=tk.DISABLED, font=("Arial", 12), width=10)
        self.btn_next.pack(side=tk.RIGHT, padx=50)

        # 綁定視窗大小改變事件，以便重新調整圖片大小
        self.root.bind("<Configure>", self.on_resize)

    def load_images(self):
        """開啟檔案選取視窗"""
        file_types = [("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        paths = filedialog.askopenfilenames(title="選擇圖片", filetypes=file_types)

        if paths:
            self.image_paths = list(paths)
            self.current_index = 0
            self.update_ui_state()
            self.show_image()
        elif not self.image_paths:
            # 如果沒選且原本也沒圖片
            pass

    def show_image(self):
        """讀取並顯示當前索引的圖片"""
        if not self.image_paths:
            return

        image_path = self.image_paths[self.current_index]
        
        try:
            # 使用 Pillow 開啟圖片
            original_image = Image.open(image_path)
            
            # 取得目前顯示區域的大小
            frame_width = self.image_frame.winfo_width()
            frame_height = self.image_frame.winfo_height()

            # 避免視窗剛啟動時大小為 1 的情況
            if frame_width < 10 or frame_height < 10:
                frame_width = 800
                frame_height = 500

            # 計算縮放比例 (保持長寬比)
            original_image.thumbnail((frame_width, frame_height), Image.Resampling.LANCZOS)
            
            # 轉換為 Tkinter 可用的格式
            photo = ImageTk.PhotoImage(original_image)

            # 更新 Label
            self.lbl_image.config(image=photo, text="") # 清除文字
            self.lbl_image.image = photo # 重要！必須保留 reference 避免被記憶體回收
            
            # 更新狀態文字
            self.lbl_status.config(text=f"第 {self.current_index + 1} 張 / 共 {len(self.image_paths)} 張")

        except Exception as e:
            messagebox.showerror("錯誤", f"無法開啟圖片：\n{e}")

    def next_image(self):
        """切換到下一張"""
        if self.image_paths:
            self.current_index += 1
            # 循環播放邏輯：如果是最後一張，就回到第一張
            if self.current_index >= len(self.image_paths):
                self.current_index = 0
            self.show_image()

    def prev_image(self):
        """切換到上一張"""
        if self.image_paths:
            self.current_index -= 1
            # 循環播放邏輯：如果是第一張，就跳到最後一張
            if self.current_index < 0:
                self.current_index = len(self.image_paths) - 1
            self.show_image()

    def update_ui_state(self):
        """啟用按鈕"""
        if self.image_paths:
            self.btn_prev.config(state=tk.NORMAL)
            self.btn_next.config(state=tk.NORMAL)

    def on_resize(self, event):
        """當視窗大小改變時重新繪製圖片 (簡單防抖動處理)"""
        # 這裡做一個簡單的檢查，確保是主視窗在變動，且圖片已載入
        if event.widget == self.root and self.image_paths:
            # 為了效能，通常可以加個 Timer 延遲，但這裡直接呼叫即可滿足基本需求
            # 注意：頻繁 resize 可能會稍微閃爍
            self.show_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCarouselApp(root)
    root.mainloop()