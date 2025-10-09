import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image, ImageTk

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500  # 調整高度,為按鈕留空間
ZOOM_STEP = 0.1

class ImageViewerApp:
    def __init__(self, master):
        self.master = master
        master.title("Python 圖片切換相簿 (拖曳與縮放)")
        master.geometry("850x700")  # 增加視窗高度
        
        self.image_files = []
        self.current_index = -1
        self.current_photo = None
        self.original_image = None
        self.current_image_path = None

        self.zoom_factor = 1.0
        self.img_id = None
        
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.image_position = {"x": CANVAS_WIDTH // 2, "y": CANVAS_HEIGHT // 2}

        # Canvas 不使用 expand,使用固定大小
        self.canvas = tk.Canvas(master, bg="lightgray", width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.pack(pady=10, padx=10)

        self.canvas.bind("<ButtonPress-1>", self._start_drag)
        self.canvas.bind("<B1-Motion>", self._drag)
        self.canvas.bind("<ButtonRelease-1>", self._stop_drag)

        # 按鈕區域
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        self.open_button = tk.Button(button_frame, text="開啟資料夾", command=self.open_directory, width=12)
        self.open_button.pack(side=tk.LEFT, padx=5)

        self.zoom_out_button = tk.Button(button_frame, text="縮小 (-)", command=self.zoom_out, state=tk.DISABLED, width=10)
        self.zoom_out_button.pack(side=tk.LEFT, padx=5)
        
        self.zoom_in_button = tk.Button(button_frame, text="放大 (+)", command=self.zoom_in, state=tk.DISABLED, width=10)
        self.zoom_in_button.pack(side=tk.LEFT, padx=5)
        
        self.prev_button = tk.Button(button_frame, text="上一張", command=self.show_previous_image, state=tk.DISABLED, width=10)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(button_frame, text="下一張", command=self.show_next_image, state=tk.DISABLED, width=10)
        self.next_button.pack(side=tk.LEFT, padx=5)
        
        # 狀態列
        self.status_label = tk.Label(master, text="請點擊「開啟資料夾」來載入圖片。", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)

    def _start_drag(self, event):
        if self.original_image:
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            self.drag_data["item"] = self.img_id

    def _drag(self, event):
        if self.drag_data["item"] and self.img_id:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            self.canvas.move(self.img_id, dx, dy)
            self.image_position["x"] += dx
            self.image_position["y"] += dy
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def _stop_drag(self, event):
        self.drag_data["item"] = None

    def open_directory(self):
        directory = filedialog.askdirectory(title="選擇圖片資料夾")
        if directory:
            self.image_files = []
            valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
            for filename in os.listdir(directory):
                if filename.lower().endswith(valid_extensions):
                    path = os.path.join(directory, filename)
                    self.image_files.append(path)
            self.image_files.sort()
            if self.image_files:
                self.current_index = 0
                self.current_image_path = None
                self._load_and_display_image()
            else:
                self.canvas.delete("all")
                self.status_label.config(text="資料夾中沒有找到圖片。")
                self.current_index = -1
                self.update_buttons_state()

    def _load_and_display_image(self):
        if self.image_files and 0 <= self.current_index < len(self.image_files):
            try:
                image_path = self.image_files[self.current_index]
                # 只有當圖片路徑不同時才重新載入
                if self.current_image_path != image_path:
                    self.original_image = Image.open(image_path)
                    self.current_image_path = image_path
                    self.zoom_factor = 1.0
                    # 重置圖片位置到中心
                    self.image_position["x"] = CANVAS_WIDTH // 2
                    self.image_position["y"] = CANVAS_HEIGHT // 2

                width, height = self.original_image.size
                new_width = int(width * self.zoom_factor)
                new_height = int(height * self.zoom_factor)
                resized_img = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.current_photo = ImageTk.PhotoImage(resized_img)
                self.canvas.delete("all")
                self.img_id = self.canvas.create_image(
                    self.image_position["x"], 
                    self.image_position["y"], 
                    image=self.current_photo, 
                    anchor=tk.CENTER
                )
                total = len(self.image_files)
                current = self.current_index + 1
                filename = os.path.basename(image_path)
                status_text = f"圖片 {current} / {total} - {filename} - 縮放: {int(self.zoom_factor * 100)}%"
                self.status_label.config(text=status_text)
            except Exception as e:
                self.status_label.config(text=f"載入圖片時發生錯誤: {e}")
                self.canvas.delete("all")
            self.update_buttons_state()

    def show_next_image(self):
        if self.image_files:
            self.current_index = (self.current_index + 1) % len(self.image_files)
            self.current_image_path = None
            self._load_and_display_image()

    def show_previous_image(self):
        if self.image_files:
            self.current_index = (self.current_index - 1) % len(self.image_files)
            self.current_image_path = None
            self._load_and_display_image()

    def zoom_in(self):
        if self.original_image:
            if self.zoom_factor < 5.0:
                self.zoom_factor += ZOOM_STEP
                self._load_and_display_image()
            
    def zoom_out(self):
        if self.original_image:
            if self.zoom_factor > 0.1:
                self.zoom_factor -= ZOOM_STEP
                self._load_and_display_image()

    def update_buttons_state(self):
        has_image = len(self.image_files) > 0
        is_multiple = len(self.image_files) > 1
        state = tk.NORMAL if has_image else tk.DISABLED
        self.zoom_in_button.config(state=state)
        self.zoom_out_button.config(state=state)
        switch_state = tk.NORMAL if is_multiple else tk.DISABLED
        self.prev_button.config(state=switch_state)
        self.next_button.config(state=switch_state)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.mainloop()