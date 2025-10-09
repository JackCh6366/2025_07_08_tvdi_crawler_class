import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image, ImageTk

# 圖片顯示的固定大小
MAX_WIDTH = 800
MAX_HEIGHT = 600

class ImageViewerApp:
    def __init__(self, master):
        self.master = master
        master.title("Python 圖片切換相簿")
        master.geometry("900x700") # 設定初始視窗大小
        
        # 狀態變數
        self.image_files = [] # 儲存圖片檔案路徑的列表
        self.current_index = -1 # 目前顯示圖片在列表中的索引
        self.current_photo = None # 儲存 Tkinter PhotoImage 物件，防止被垃圾回收

        # 1. 建立圖片顯示區域
        self.image_label = tk.Label(master, bg="lightgray")
        self.image_label.pack(pady=10, padx=10, fill="both", expand=True)

        # 2. 建立按鈕框架
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        # 3. 建立按鈕
        self.open_button = tk.Button(button_frame, text="開啟資料夾", command=self.open_directory)
        self.open_button.pack(side=tk.LEFT, padx=10)

        self.prev_button = tk.Button(button_frame, text="上一張", command=self.show_previous_image, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(button_frame, text="下一張", command=self.show_next_image, state=tk.DISABLED)
        self.next_button.pack(side=tk.LEFT, padx=10)
        
        # 4. 建立狀態標籤
        self.status_label = tk.Label(master, text="請點擊「開啟資料夾」來載入圖片。", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)

    # --- 核心功能函式 ---

    def open_directory(self):
        """開啟檔案對話框，讓使用者選擇一個資料夾。"""
        # 選擇資料夾
        directory = filedialog.askdirectory(title="選擇圖片資料夾")
        
        if directory:
            self.image_files = []
            valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
            
            # 遍歷資料夾中的所有檔案，篩選出圖片
            for filename in os.listdir(directory):
                if filename.lower().endswith(valid_extensions):
                    path = os.path.join(directory, filename)
                    self.image_files.append(path)
            
            # 排序檔案，讓切換順序更自然
            self.image_files.sort()
            
            if self.image_files:
                self.current_index = 0
                self.show_image()
            else:
                self.image_label.config(image='')
                self.status_label.config(text="資料夾中沒有找到圖片。")
                self.current_index = -1
                self.update_buttons_state()

    def show_image(self):
        """顯示目前索引指向的圖片。"""
        if self.image_files and 0 <= self.current_index < len(self.image_files):
            try:
                # 獲取圖片路徑
                image_path = self.image_files[self.current_index]
                
                # 1. 使用 PIL 開啟圖片
                img = Image.open(image_path)
                
                # 2. 計算縮放比例並調整圖片大小
                width, height = img.size
                
                # 保持長寬比進行縮放
                ratio_w = MAX_WIDTH / width
                ratio_h = MAX_HEIGHT / height
                
                ratio = min(ratio_w, ratio_h)
                
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                
                # 縮放圖片
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # 3. 轉換為 Tkinter 可用的格式
                self.current_photo = ImageTk.PhotoImage(resized_img)
                
                # 4. 在 Label 中顯示圖片
                self.image_label.config(image=self.current_photo)
                
                # 5. 更新狀態列
                total = len(self.image_files)
                current = self.current_index + 1
                self.status_label.config(text=f"圖片 {current} / {total} - 檔名: {os.path.basename(image_path)}")
                
            except Exception as e:
                self.status_label.config(text=f"載入圖片時發生錯誤: {e}")
                self.image_label.config(image='')
            
            # 6. 更新按鈕狀態
            self.update_buttons_state()

    def show_next_image(self):
        """切換到下一張圖片。"""
        if self.image_files:
            # 使用模數運算 (Modulo) 實現循環切換
            self.current_index = (self.current_index + 1) % len(self.image_files)
            self.show_image()

    def show_previous_image(self):
        """切換到上一張圖片。"""
        if self.image_files:
            # 使用模數運算 (Modulo) 實現循環切換
            self.current_index = (self.current_index - 1) % len(self.image_files)
            self.show_image()

    def update_buttons_state(self):
        """根據圖片數量更新按鈕是否可用。"""
        if len(self.image_files) > 1:
            self.prev_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.NORMAL)
        else:
            # 只有 0 或 1 張圖片時，切換按鈕禁用
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)


# 執行主程式
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.mainloop()