import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import random
import math

# --- 設定 ---
# 遊戲視窗寬高，用於標準化圖片顯示大小
GAME_WIDTH = 600
GAME_HEIGHT = 600

class JigsawPuzzleGame:
    def __init__(self, master):
        self.master = master
        master.title("Python 自訂拼圖遊戲")
        
        self.original_image = None
        self.puzzle_pieces = []
        self.piece_images = []
        self.current_piece_count = 0
        self.cols = 0
        self.rows = 0
        
        # 拖曳相關變數
        self.drag_data = {"item": None, "x": 0, "y": 0, "original_pos": (0, 0)}

        # --- 設定主畫面佈局 ---
        
        # 1. 控制面板 (Control Panel)
        self.control_frame = ttk.Frame(master, padding="10")
        self.control_frame.pack(side=tk.TOP, fill=tk.X)
        
        ttk.Button(self.control_frame, text="選擇圖片", command=self.load_image).pack(side=tk.LEFT, padx=5)
        
        # 拼圖片數選擇
        self.piece_var = tk.StringVar(master)
        self.piece_var.set("12") # 預設值
        self.piece_options = ["12", "20", "50"]
        
        ttk.Label(self.control_frame, text="片數:").pack(side=tk.LEFT, padx=(15, 5))
        self.piece_menu = ttk.Combobox(self.control_frame, textvariable=self.piece_var, values=self.piece_options, width=5)
        self.piece_menu.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.control_frame, text="開始遊戲", command=self.start_game).pack(side=tk.LEFT, padx=5)

        # 2. 遊戲畫布 (Canvas)
        self.canvas = tk.Canvas(master, width=GAME_WIDTH, height=GAME_HEIGHT, bg="white", highlightthickness=1, highlightbackground="gray")
        self.canvas.pack(padx=10, pady=10)
        
        # 綁定滑鼠事件
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        ttk.Label(master, text="請先點擊「選擇圖片」並「開始遊戲」").pack(pady=5)
    
    # --- 圖片處理與遊戲邏輯 ---

    def load_image(self):
        """開啟檔案對話框，讓使用者選擇圖片"""
        file_path = filedialog.askopenfilename(
            title="選擇圖片",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:
            try:
                # 使用 Pillow 載入圖片
                img = Image.open(file_path)
                # 將圖片調整為標準遊戲大小並保持比例
                img.thumbnail((GAME_WIDTH, GAME_HEIGHT))
                self.original_image = img
                messagebox.showinfo("圖片載入", f"圖片載入成功: {file_path}")
            except Exception as e:
                messagebox.showerror("錯誤", f"無法載入圖片: {e}")

    def get_grid_size(self, total_pieces):
        """
        根據總片數，盡量找出接近正方形的行(rows)和列(cols)
        
        例如: 
        12片: 3x4 或 4x3
        20片: 4x5 或 5x4
        50片: 5x10 或 10x5 (取決於圖片比例，這裡用近似正方形)
        """
        if total_pieces == 12:
            return (3, 4) # 3行 x 4列 或 4行 x 3列
        elif total_pieces == 20:
            return (4, 5) # 4行 x 5列 或 5行 x 4列
        elif total_pieces == 50:
            return (5, 10) # 5行 x 10列 或 10行 x 5列
        else:
            # 默認使用接近正方形的網格
            n = int(math.sqrt(total_pieces))
            while total_pieces % n != 0:
                n -= 1
            return (n, total_pieces // n)


    def start_game(self):
        """初始化遊戲，切割圖片並打亂拼圖塊"""
        if not self.original_image:
            messagebox.showwarning("警告", "請先選擇一張圖片！")
            return

        # 清空畫布
        self.canvas.delete("all")
        self.puzzle_pieces = []
        self.piece_images = []
        
        # 獲取片數和網格大小
        try:
            self.current_piece_count = int(self.piece_var.get())
        except:
            messagebox.showerror("錯誤", "片數選擇無效。")
            return

        # 根據圖片比例決定網格方向
        width_ratio = self.original_image.width / self.original_image.height
        r, c = self.get_grid_size(self.current_piece_count)
        
        if width_ratio > 1: # 橫向圖片，列數應多於行數
            self.rows, self.cols = min(r, c), max(r, c)
        else: # 縱向或正方形圖片，行數和列數相反或相等
            self.rows, self.cols = max(r, c), min(r, c)
            
        
        img_w, img_h = self.original_image.size
        piece_w = img_w // self.cols
        piece_h = img_h // self.rows
        
        # 1. 切割圖片並儲存資訊
        original_positions = []
        piece_id = 0
        for r in range(self.rows):
            for c in range(self.cols):
                # 切割範圍 (left, top, right, bottom)
                left = c * piece_w
                top = r * piece_h
                right = left + piece_w
                bottom = top + piece_h
                
                # 裁切圖片塊
                piece_img = self.original_image.crop((left, top, right, bottom))
                tk_img = ImageTk.PhotoImage(piece_img)
                self.piece_images.append(tk_img) # 必須保留參考，否則會被垃圾回收
                
                # 儲存資訊 (ID, 圖片物件, 正確位置-像素, 正確網格位置)
                original_pos_x = c * (GAME_WIDTH // self.cols) + (GAME_WIDTH // self.cols) // 2
                original_pos_y = r * (GAME_HEIGHT // self.rows) + (GAME_HEIGHT // self.rows) // 2
                
                self.puzzle_pieces.append({
                    "id": piece_id,
                    "image": tk_img,
                    "correct_x": original_pos_x,
                    "correct_y": original_pos_y,
                    "correct_row": r,
                    "correct_col": c
                })
                original_positions.append((original_pos_x, original_pos_y))
                piece_id += 1

        # 2. 打亂位置
        random.shuffle(original_positions)
        
        # 3. 繪製拼圖塊到畫布上
        for i, piece in enumerate(self.puzzle_pieces):
            # 隨機位置是從 'original_positions' 列表中取出的
            start_x, start_y = original_positions[i]
            
            # 在畫布上創建圖片物件
            item_id = self.canvas.create_image(
                start_x, start_y, 
                image=piece["image"], 
                anchor=tk.CENTER,
                tags=("piece", f"id_{piece['id']}") # 設定標籤方便識別
            )
            
            # 將畫布上的物件ID存回 piece 資訊中
            piece["canvas_id"] = item_id

        # 提示
        messagebox.showinfo("遊戲開始", f"已切割成 {self.rows} 行 x {self.cols} 列，共 {self.current_piece_count} 片。請開始拖曳！")

    # --- 滑鼠事件處理 (拖曳邏輯) ---
    
    def on_press(self, event):
        """滑鼠按下時，記錄被點擊的拼圖塊及其起始位置"""
        # 找到點擊位置下方的畫布物件
        closest_item = self.canvas.find_closest(event.x, event.y)
        
        # 檢查是否為拼圖塊 (piece tag)
        if closest_item and "piece" in self.canvas.gettags(closest_item[0]):
            self.drag_data["item"] = closest_item[0]
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            
            # 將被拖曳的拼圖塊移到最上層
            self.canvas.tag_raise(self.drag_data["item"])
            
            # 記錄拼圖塊的原始中心位置，用於判斷是否回到原位
            current_coords = self.canvas.coords(self.drag_data["item"])
            if current_coords:
                 self.drag_data["original_pos"] = (current_coords[0], current_coords[1])


    def on_drag(self, event):
        """滑鼠拖曳時，移動拼圖塊"""
        if self.drag_data["item"]:
            # 計算位移量
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            
            # 移動畫布上的物件
            self.canvas.move(self.drag_data["item"], dx, dy)
            
            # 更新起始位置
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def on_release(self, event):
        """滑鼠放開時，判斷拼圖塊是否放對位置"""
        if self.drag_data["item"]:
            item_id = self.drag_data["item"]
            current_x, current_y = self.canvas.coords(item_id)
            
            # 找出對應的拼圖塊資訊
            piece = next((p for p in self.puzzle_pieces if p["canvas_id"] == item_id), None)

            if piece:
                # 判斷是否 "接近" 正確位置 (使用吸附邏輯)
                SNAP_DISTANCE = 30 # 距離閾值 (像素)
                
                dx = abs(current_x - piece["correct_x"])
                dy = abs(current_y - piece["correct_y"])
                
                if dx < SNAP_DISTANCE and dy < SNAP_DISTANCE:
                    # 吸附到正確位置
                    self.canvas.coords(item_id, piece["correct_x"], piece["correct_y"])
                    # 將此拼圖塊標記為已完成 (例如，變更標籤或顏色，這裡我們直接用標籤)
                    self.canvas.dtag(item_id, "piece") # 移除 "piece" 標籤，使其無法再被拖曳
                    self.canvas.addtag_withtag("solved", item_id)
                    
                    # 檢查遊戲是否完成
                    self.check_win()
                else:
                    # 如果不是傳統拼圖，這裡可以加入檢查與其他拼圖塊是否相鄰的邏輯
                    pass # 這裡的基礎範例只是簡單的 grid-based 拼圖
            
            # 清除拖曳資料
            self.drag_data = {"item": None, "x": 0, "y": 0, "original_pos": (0, 0)}

    def check_win(self):
        """檢查所有拼圖塊是否都已拼好"""
        # 如果已完成的拼圖塊數量等於總片數，則勝利
        solved_count = len(self.canvas.find_withtag("solved"))
        if solved_count == self.current_piece_count and self.current_piece_count > 0:
            messagebox.showinfo("恭喜", "拼圖完成！你太棒了！")
            
            # 顯示完成後的完整圖片 (可選)
            self.canvas.delete("all")
            # 重新標準化圖片大小以適應畫布
            final_img = self.original_image.copy()
            final_img.thumbnail((GAME_WIDTH, GAME_HEIGHT))
            self.final_tk_img = ImageTk.PhotoImage(final_img)
            self.canvas.create_image(GAME_WIDTH//2, GAME_HEIGHT//2, image=self.final_tk_img)


if __name__ == "__main__":
    root = tk.Tk()
    game = JigsawPuzzleGame(root)
    root.mainloop()