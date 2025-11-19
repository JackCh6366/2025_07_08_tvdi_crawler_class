import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class FixedButtonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python 固定按鈕圖片輪播")
        self.root.geometry("900x600")
        
        # 設定視窗背景色 (當沒有圖片時顯示)
        self.root.configure(bg="#222")

        # 初始化變數
        self.image_paths = []
        self.current_index = 0

        # --- 1. 圖片顯示層 (最底層) ---
        # 讓 Label 填滿整個視窗
        self.lbl_image = tk.Label(root, text="請點擊上方按鈕選擇圖片", bg="#222", fg="#888", font=("微軟正黑體", 20))
        self.lbl_image.pack(fill=tk.BOTH, expand=True)

        # --- 2. 懸浮控制元件 (使用 place 固定位置) ---

        # [上方] 選擇檔案按鈕：固定在上方中間 (relx=0.5, rely=0.02)
        self.btn_load = tk.Button(root, text="📂 選擇圖片", command=self.load_images, 
                                  font=("Arial", 12, "bold"), bg="white", cursor="hand2")
        self.btn_load.place(relx=0.5, rely=0.03, anchor=tk.N)

        # [左側] 上一張按鈕：固定在左側垂直置中 (relx=0.02, rely=0.5)
        self.btn_prev = tk.Button(root, text="❮", command=self.prev_image, state=tk.DISABLED,
                                  font=("Arial", 20, "bold"), bg="gray", fg="white", 
                                  bd=0, activebackground="#555", activeforeground="white", cursor="hand2")
        # anchor=tk.W 代表以按鈕的左邊為錨點
        self.btn_prev.place(relx=0.02, rely=0.5, anchor=tk.W, height=60, width=40)

        # [右側] 下一張按鈕：固定在右側垂直置中 (relx=0.98, rely=0.5)
        self.btn_next = tk.Button(root, text="❯", command=self.next_image, state=tk.DISABLED,
                                  font=("Arial", 20, "bold"), bg="gray", fg="white", 
                                  bd=0, activebackground="#555", activeforeground="white", cursor="hand2")
        # anchor=tk.E 代表以按鈕的右邊為錨點
        self.btn_next.place(relx=0.98, rely=0.5, anchor=tk.E, height=60, width=40)

        # [下方] 狀態文字：固定在下方 (rely=0.95)
        self.lbl_status = tk.Label(root, text="", bg="#222", fg="white", font=("Arial", 12))
        self.lbl_status.place(relx=0.5, rely=0.95, anchor=tk.S)

        # 綁定視窗縮放事件
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

    def show_image(self):
        """顯示圖片"""
        if not self.image_paths:
            return

        image_path = self.image_paths[self.current_index]
        
        try:
            original_image = Image.open(image_path)
            
            # 取得目前視窗大小
            win_width = self.root.winfo_width()
            win_height = self.root.winfo_height()

            # 如果視窗還沒完全建立，給個預設值
            if win_width < 10: win_width = 900
            if win_height < 10: win_height = 600

            # 使用 thumbnail 自動等比例縮放 (保留一點邊距以免蓋住按鈕)
            # 這裡我們稍微扣掉一點寬高，讓圖片不要貼太滿
            display_size = (int(win_width), int(win_height))
            
            # 複製一份圖片來縮放 (Pillow 操作)
            img_copy = original_image.copy()
            img_copy.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(img_copy)

            self.lbl_image.config(image=photo, text="") 
            self.lbl_image.image = photo 
            
            # 更新下方文字
            self.lbl_status.config(text=f" {self.current_index + 1} / {len(self.image_paths)} ")

        except Exception as e:
            print(f"Error loading image: {e}")

    def next_image(self):
        if self.image_paths:
            self.current_index = (self.current_index + 1) % len(self.image_paths)
            self.show_image()

    def prev_image(self):
        if self.image_paths:
            self.current_index = (self.current_index - 1 + len(self.image_paths)) % len(self.image_paths)
            self.show_image()

    def update_ui_state(self):
        if self.image_paths:
            self.btn_prev.config(state=tk.NORMAL, bg="#444") # 啟用時變深灰
            self.btn_next.config(state=tk.NORMAL, bg="#444")

    def on_resize(self, event):
        # 只有當觸發事件的是主視窗本身時才重繪 (避免按鈕重繪觸發無限迴圈)
        if event.widget == self.root and self.image_paths:
            self.show_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = FixedButtonApp(root)
    root.mainloop()