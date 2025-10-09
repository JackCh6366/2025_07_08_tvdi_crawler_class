import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import random
import math

# --- 介面與遊戲設定 ---
CANVAS_SIZE = 600  # 拼圖區的標準尺寸 (寬度和高度)
C_CANVAS_WIDTH = 250 # C 區畫布的固定寬度
THUMBNAIL_RATIO = 10 # 縮圖區圖片顯示比例 (原圖的 1/10)
SNAP_DISTANCE = 30 # 吸附距離 (像素)

class JigsawPuzzleGame:
    def __init__(self, master):
        self.master = master
        master.title("Python 自訂拼圖遊戲 (捲軸與新模式修正版)")
        
        self.original_image = None
        self.piece_data = [] 
        self.piece_images = [] 
        
        # --- 拖曳專用變數 ---
        self.drag_piece = None 
        self.drag_image_tk = None
        self.drag_window = None 
        self.start_canvas = None 
        
        # 設定主視窗的列和行權重
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=3) # B 區
        master.grid_columnconfigure(2, weight=1) # C 區
        master.grid_rowconfigure(1, weight=1)
        
        self.setup_control_panel()
        self.setup_game_areas()

    # --- 介面佈局設置 (新增捲軸) ---
    
    def setup_control_panel(self):
        """設置頂部的控制面板"""
        control_frame = ttk.Frame(self.master, padding="10")
        control_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
        
        ttk.Button(control_frame, text="選擇圖片", command=self.load_image).pack(side=tk.LEFT, padx=10)
        
        # 拼圖片數選擇 (新模式: 9, 16, 25)
        self.piece_var = tk.StringVar(self.master)
        self.piece_var.set("9") # 預設值
        self.piece_options = ["9", "16", "25"]
        
        ttk.Label(control_frame, text="片數:").pack(side=tk.LEFT, padx=(15, 5))
        self.piece_menu = ttk.Combobox(control_frame, textvariable=self.piece_var, values=self.piece_options, width=5, state="readonly")
        self.piece_menu.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="開始遊戲", command=self.start_game).pack(side=tk.LEFT, padx=20)

    def setup_game_areas(self):
        # A 區
        self.a_frame = ttk.Frame(self.master, borderwidth=2, relief="groove")
        self.a_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        ttk.Label(self.a_frame, text="原圖縮圖 (A 區)").pack(pady=5)
        self.thumbnail_label = ttk.Label(self.a_frame)
        self.thumbnail_label.pack(padx=10, pady=10)
        
        # --- B 區: 拼圖區 (增加捲軸) ---
        self.b_frame = ttk.Frame(self.master, borderwidth=2, relief="sunken")
        self.b_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        ttk.Label(self.b_frame, text="拼圖區 (B 區)").pack(pady=5)
        
        # 創建一個 Frame 容納 Canvas 和 Scrollbar
        b_canvas_container = ttk.Frame(self.b_frame)
        b_canvas_container.pack(fill=tk.BOTH, expand=True)
        
        # 設置垂直捲軸
        b_v_scrollbar = ttk.Scrollbar(b_canvas_container, orient=tk.VERTICAL)
        b_v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # 設置水平捲軸
        b_h_scrollbar = ttk.Scrollbar(b_canvas_container, orient=tk.HORIZONTAL)
        b_h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 創建 Canvas
        self.puzzle_canvas = tk.Canvas(
            b_canvas_container, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="#F0F0F0",
            yscrollcommand=b_v_scrollbar.set, xscrollcommand=b_h_scrollbar.set
        )
        self.puzzle_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 連結捲軸
        b_v_scrollbar.config(command=self.puzzle_canvas.yview)
        b_h_scrollbar.config(command=self.puzzle_canvas.xview)
        
        # --- C 區: 待選取打散的圖片區 (增加捲軸) ---
        self.c_frame = ttk.Frame(self.master, borderwidth=2, relief="groove")
        self.c_frame.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        ttk.Label(self.c_frame, text="待選圖片 (C 區)").pack(pady=5)
        
        c_canvas_container = ttk.Frame(self.c_frame, width=C_CANVAS_WIDTH, height=CANVAS_SIZE)
        c_canvas_container.pack(fill=tk.Y, expand=True)
        
        # 設置垂直捲軸 (C 區只需要垂直捲軸)
        c_v_scrollbar = ttk.Scrollbar(c_canvas_container, orient=tk.VERTICAL)
        c_v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 創建 Canvas
        self.c_canvas = tk.Canvas(
            c_canvas_container, width=C_CANVAS_WIDTH, height=CANVAS_SIZE, bg="#E0E0E0",
            yscrollcommand=c_v_scrollbar.set
        )
        self.c_canvas.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        
        # 連結捲軸
        c_v_scrollbar.config(command=self.c_canvas.yview)
        
        # 統一綁定滑鼠事件到 root
        self.master.bind("<ButtonPress-1>", self.on_press)
        self.master.bind("<B1-Motion>", self.on_drag)
        self.master.bind("<ButtonRelease-1>", self.on_release)


    # --- 圖片處理與遊戲邏輯 (更新片數邏輯) ---

    def load_image(self):
        # 略... (與原版相同)
        file_path = filedialog.askopenfilename(
            title="選擇圖片",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:
            try:
                img = Image.open(file_path)
                img_copy = img.copy()
                img_copy.thumbnail((CANVAS_SIZE, CANVAS_SIZE))
                self.original_image = img_copy
                
                thumb_w = img.width // THUMBNAIL_RATIO
                thumb_h = img.height // THUMBNAIL_RATIO
                thumbnail = img.copy()
                thumbnail.thumbnail((thumb_w, thumb_h))
                self.tk_thumbnail = ImageTk.PhotoImage(thumbnail)
                self.thumbnail_label.config(image=self.tk_thumbnail)
                
                messagebox.showinfo("圖片載入", "圖片載入成功！")
            except Exception as e:
                messagebox.showerror("錯誤", f"無法載入或處理圖片: {e}")

    def get_grid_size(self, total_pieces):
        """根據總片數，強制使用方形網格 (R=C)"""
        n = int(math.sqrt(total_pieces))
        if n * n == total_pieces:
            return (n, n)
        else:
            # 理論上不會發生，因為選項只有 9, 16, 25
            return (3, 3) 

    def start_game(self):
        if self.original_image is None:
            messagebox.showwarning("警告", "請先選擇一張圖片！")
            return

        self.puzzle_canvas.delete("all")
        self.c_canvas.delete("all")
        self.piece_data = []
        self.piece_images = []
        
        try:
            total_pieces = int(self.piece_var.get())
        except ValueError:
            messagebox.showerror("錯誤", "片數選擇無效。")
            return

        img_w, img_h = self.original_image.size
        # 使用新的網格計算邏輯
        self.rows, self.cols = self.get_grid_size(total_pieces)
        
        # 由於是方形模式，我們統一使用一個邊長來計算圖片大小，避免比例問題
        effective_size = min(img_w, img_h) 
        piece_w = effective_size // self.cols
        piece_h = effective_size // self.rows
        
        # --- 設置 B 區的 ScrollRegion (必須在繪製前) ---
        # 由於是方形網格，B 區的內容大小就是 CANVAS_SIZE x CANVAS_SIZE
        self.puzzle_canvas.config(scrollregion=(0, 0, CANVAS_SIZE, CANVAS_SIZE))
        
        # 繪製 B 區格線
        self.draw_grid_lines(self.rows, self.cols, self.puzzle_canvas, CANVAS_SIZE, CANVAS_SIZE)

        c_y_offset = 10 
        max_piece_h = CANVAS_SIZE // self.rows 
        
        for r in range(self.rows):
            for c in range(self.cols):
                # 裁切 (取圖片中央的正方形區域進行切割)
                x_start = (img_w - effective_size) // 2
                y_start = (img_h - effective_size) // 2
                
                left = x_start + c * piece_w
                top = y_start + r * piece_h
                right = left + piece_w
                bottom = top + piece_h
                
                piece_img = self.original_image.crop((left, top, right, bottom))
                tk_img = ImageTk.PhotoImage(piece_img)
                self.piece_images.append(tk_img) 
                
                # 正確位置 (B 區畫布上的中心座標)
                correct_x = c * (CANVAS_SIZE // self.cols) + (CANVAS_SIZE // self.cols) // 2
                correct_y = r * (CANVAS_SIZE // self.rows) + (CANVAS_SIZE // self.rows) // 2
                
                piece = {
                    "id": len(self.piece_data),
                    "image": tk_img,
                    "correct_x": correct_x, # 這是 Canvas 內容中的座標
                    "correct_y": correct_y,
                    "solved": False,
                    "canvas_id": None,
                    "width": piece_w,
                    "height": piece_h
                }
                self.piece_data.append(piece)

        # 繪製到 C 區 (打亂順序並垂直堆疊) 
        random.shuffle(self.piece_data)
        
        c_content_height = 0
        for piece in self.piece_data:
            start_x = C_CANVAS_WIDTH // 2 
            start_y = c_y_offset + piece["height"] // 2
            
            item_id = self.c_canvas.create_image(
                start_x, start_y, 
                image=piece["image"], 
                anchor=tk.CENTER,
                tags=("piece", f"id_{piece['id']}") 
            )
            piece["canvas_id"] = item_id
            
            c_y_offset += piece["height"] + 5 
            c_content_height = start_y + piece["height"] // 2 + 5

        # --- 設置 C 區的 ScrollRegion (讓捲軸起作用) ---
        self.c_canvas.config(scrollregion=(0, 0, C_CANVAS_WIDTH, c_content_height))

        messagebox.showinfo("遊戲開始", f"拼圖已打亂並置於 C 區。請將它們拖曳到 B 區格線內！")

    def draw_grid_lines(self, rows, cols, canvas, w, h):
        """繪製 B 區的格線"""
        cell_w = w // cols
        cell_h = h // rows
        
        # 繪製線條
        for i in range(1, cols):
            x = i * cell_w
            canvas.create_line(x, 0, x, h, fill="gray", dash=(4, 2), tags="grid_line")
            
        for i in range(1, rows):
            y = i * cell_h
            canvas.create_line(0, y, w, y, fill="gray", dash=(4, 2), tags="grid_line")
            
        canvas.create_rectangle(0, 0, w, h, outline="red", width=2, tags="grid_line")
        
        # 確保格線在最底層
        canvas.tag_lower("grid_line")


    # --- 修正後的跨畫布拖曳邏輯 (需考慮捲軸偏移) ---
    
    def on_press(self, event):
        """滑鼠按下時，記錄被點擊的拼圖塊並創建懸浮窗口"""
        
        canvas = event.widget
        if canvas != self.puzzle_canvas and canvas != self.c_canvas:
            return

        # 獲取捲軸偏移量 (View Offset)
        if canvas == self.puzzle_canvas:
            x_offset, y_offset = self.puzzle_canvas.canvasx(0), self.puzzle_canvas.canvasy(0)
        else:
            x_offset, y_offset = self.c_canvas.canvasx(0), self.c_canvas.canvasy(0)
            
        # 轉換事件座標為 Canvas 內容座標
        content_x = event.x + x_offset
        content_y = event.y + y_offset

        # 找出被點擊的畫布物件 (使用內容座標)
        closest_item = canvas.find_closest(content_x, content_y)
        
        if closest_item and "piece" in canvas.gettags(closest_item[0]):
            item_id = closest_item[0]
            piece = next((p for p in self.piece_data if p["canvas_id"] == item_id and not p["solved"]), None)
            
            if piece:
                self.drag_piece = piece
                self.start_canvas = canvas
                
                # 隱藏原來的拼圖塊
                canvas.itemconfig(item_id, state=tk.HIDDEN)
                
                # 創建 Toplevel 視窗
                self.drag_window = tk.Toplevel(self.master)
                self.drag_window.overrideredirect(True) 
                self.drag_window.attributes("-topmost", True) 
                
                self.drag_image_tk = piece["image"] 
                drag_label = tk.Label(self.drag_window, image=self.drag_image_tk, bg="white", borderwidth=0, highlightthickness=0)
                drag_label.pack()
                
                # 初始定位懸浮視窗 (使用滑鼠當前螢幕座標)
                w = self.drag_piece["width"] // 2
                h = self.drag_piece["height"] // 2
                self.drag_window.geometry(f'+{event.x_root - w}+{event.y_root - h}')


    def on_drag(self, event):
        """滑鼠拖曳時，移動懸浮窗口"""
        if self.drag_piece and self.drag_window:
            # 移動懸浮視窗到滑鼠當前位置
            w = self.drag_piece["width"] // 2
            h = self.drag_piece["height"] // 2
            self.drag_window.geometry(f'+{event.x_root - w}+{event.y_root - h}')


    def on_release(self, event):
        """滑鼠放開時，判斷釋放區域並處理吸附"""
        if not self.drag_piece:
            return

        # 1. 銷毀懸浮視窗
        if self.drag_window:
            self.drag_window.destroy()
            self.drag_window = None

        piece = self.drag_piece
        original_canvas = self.start_canvas
        
        # 獲取 B 區畫布在螢幕上的座標範圍
        b_x1 = self.puzzle_canvas.winfo_rootx()
        b_y1 = self.puzzle_canvas.winfo_rooty()
        b_x2 = b_x1 + self.puzzle_canvas.winfo_width()
        b_y2 = b_y1 + self.puzzle_canvas.winfo_height()
        
        # 判斷釋放點是否在 B 區畫布的*可視範圍*內
        is_dropped_on_b_zone = (b_x1 <= event.x_root <= b_x2) and (b_y1 <= event.y_root <= b_y2)
        
        if is_dropped_on_b_zone:
            # --- 釋放點在 B 區 (puzzle_canvas) ---
            
            # 將螢幕座標轉換為 B 區畫布的**內容座標** (這才是正確的定位座標)
            b_rel_x = self.puzzle_canvas.canvasx(event.x_root - b_x1)
            b_rel_y = self.puzzle_canvas.canvasy(event.y_root - b_y1)
            
            # 從原始畫布移除舊物件
            original_canvas.delete(piece["canvas_id"])
            
            # 在 B 區畫布上創建新物件
            item_id = self.puzzle_canvas.create_image(
                b_rel_x, b_rel_y, 
                image=piece["image"], 
                anchor=tk.CENTER,
                tags=("piece", f"id_{piece['id']}")
            )
            piece["canvas_id"] = item_id 
            
            # 檢查吸附邏輯 (使用內容座標進行判斷)
            dx = abs(b_rel_x - piece["correct_x"])
            dy = abs(b_rel_y - piece["correct_y"])
            
            if dx < SNAP_DISTANCE and dy < SNAP_DISTANCE:
                # 成功吸附
                self.puzzle_canvas.coords(item_id, piece["correct_x"], piece["correct_y"])
                self.puzzle_canvas.dtag(item_id, "piece")
                self.puzzle_canvas.addtag_withtag("solved", item_id)
                piece["solved"] = True
                
                # 繪製邊框
                self.puzzle_canvas.create_rectangle(
                    piece["correct_x"] - piece["width"]//2, 
                    piece["correct_y"] - piece["height"]//2,
                    piece["correct_x"] + piece["width"]//2,
                    piece["correct_y"] + piece["height"]//2,
                    outline="green", width=3, tags=("solved_border", f"id_{piece['id']}")
                )
                self.puzzle_canvas.tag_lower("solved_border", item_id) 
                
                self.check_win()
            else:
                # 未吸附成功，保持在釋放的內容座標
                self.puzzle_canvas.tag_raise(item_id)
                
        else:
            # --- 釋放點不在 B 區 ---
            # 將原始畫布上的圖片塊恢復顯示
            if original_canvas == self.c_canvas or original_canvas == self.puzzle_canvas:
                original_canvas.itemconfig(piece["canvas_id"], state=tk.NORMAL)
                 
        # 清除拖曳資料
        self.drag_piece = None
        self.start_canvas = None


    def check_win(self):
        solved_count = sum(1 for p in self.piece_data if p["solved"])
        
        if solved_count == len(self.piece_data) and len(self.piece_data) > 0:
            
            messagebox.showinfo("恭喜你挑戰成功！", "恭喜你！所有拼圖塊都已正確放置！")
            
            # 顯示完成後的完整圖片
            self.puzzle_canvas.delete("all")
            
            self.final_tk_img = ImageTk.PhotoImage(self.original_image)
            
            # 確保圖片在 Canvas 的 (0,0) 處開始繪製 (或中心)
            # 由於我們只顯示了圖片的有效方形區域，這裡將它置中
            self.puzzle_canvas.create_image(CANVAS_SIZE // 2, CANVAS_SIZE // 2, image=self.final_tk_img)


if __name__ == "__main__":
    root = tk.Tk()
    game = JigsawPuzzleGame(root)
    root.mainloop()