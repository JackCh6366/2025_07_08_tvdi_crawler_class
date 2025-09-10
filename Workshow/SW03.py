import tkinter as tk
from tkinter import font
import datetime
import pytz

class WorldClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("世界時鐘")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")

        # 檢查是否安裝 pytz
        try:
            pytz.timezone('UTC')
        except pytz.UnknownTimeZoneError:
            messagebox.showerror("錯誤", "需要安裝 pytz 庫。請運行 'pip install pytz'")
            self.root.quit()

        # 設定時區與城市名稱
        self.clocks = {
            "台灣": "Asia/Taipei",
            "日本": "Asia/Tokyo",
            "倫敦": "Europe/London",
            "巴黎": "Europe/Paris",
            "紐約": "America/New_York",
            "溫哥華": "America/Vancouver",
            "首爾": "Asia/Seoul",
            "里斯本": "Europe/Lisbon"
        }

        # 建立一個存放時間標籤的字典
        self.time_labels = {}

        # 建立 UI
        self.create_widgets()
        
        # 開始更新時間
        self.update_clocks()

    def create_widgets(self):
        """建立時鐘介面"""
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # 設定字型
        title_font = font.Font(family="Helvetica", size=18, weight="bold")
        time_font = font.Font(family="Helvetica", size=14)

        for city, timezone_name in self.clocks.items():
            # 建立一個水平列表來顯示每個城市
            city_frame = tk.Frame(main_frame, bg="#34495e", padx=10, pady=10)
            city_frame.pack(fill=tk.X, padx=20, pady=5)
            
            # 城市名稱標籤
            city_label = tk.Label(city_frame, text=city, font=title_font, fg="#ecf0f1", bg="#34495e")
            city_label.pack(side=tk.LEFT, padx=(0, 20))

            # 時間標籤
            time_label = tk.Label(city_frame, text="", font=time_font, fg="#ecf0f1", bg="#34495e")
            time_label.pack(side=tk.LEFT, expand=True, fill=tk.X)

            # 將時間標籤存入字典中，以便後續更新
            self.time_labels[city] = time_label

    def update_clocks(self):
        """每100毫秒更新所有時鐘"""
        now_utc = datetime.datetime.now(pytz.utc)

        for city, timezone_name in self.clocks.items():
            try:
                # 取得時區物件
                tz = pytz.timezone(timezone_name)
                # 將 UTC 時間轉換為當地時間
                local_time = now_utc.astimezone(tz)
                # 格式化時間字串
                formatted_time = local_time.strftime("%Y年%m月%d日 %p %I:%M:%S.%f")[:-3]
                
                # 更新標籤文字
                self.time_labels[city].config(text=formatted_time)
            except Exception as e:
                # 處理可能的錯誤，如時區名稱錯誤
                print(f"更新 {city} 時間時發生錯誤: {e}")
                self.time_labels[city].config(text="無法顯示時間")

        # 安排在 100 毫秒後再次呼叫此函數
        self.root.after(100, self.update_clocks)


if __name__ == "__main__":
    root = tk.Tk()
    app = WorldClockApp(root)
    root.mainloop()
