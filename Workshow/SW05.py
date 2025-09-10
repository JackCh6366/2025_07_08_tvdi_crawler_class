import tkinter as tk
from tkinter import font
from tkinter import messagebox
import datetime
import pytz
import requests
import threading
from bs4 import BeautifulSoup

class WorldClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("世界時鐘")
        self.root.geometry("850x600")
        self.root.configure(bg="#2c3e50")

        # 檢查是否安裝必要的函式庫
        try:
            pytz.timezone('UTC')
            requests.get("http://www.google.com", timeout=5) # 測試 requests
            BeautifulSoup("<html></html>", "html.parser") # 測試 BeautifulSoup
        except Exception:
            messagebox.showerror("錯誤", "需要安裝必要的函式庫。請運行 'pip install requests pytz beautifulsoup4'")
            self.root.quit()
        
        # 這裡不再需要 API Key
        self.api_key = None

        # 設定時區、城市名稱、緯度和經度 (用於天氣 API)
        self.clocks = {
            "台灣": {"timezone": "Asia/Taipei", "lat": 25.0330, "lon": 121.5654},
            "日本": {"timezone": "Asia/Tokyo", "lat": 35.6895, "lon": 139.6917},
            "倫敦": {"timezone": "Europe/London", "lat": 51.5074, "lon": -0.1278},
            "巴黎": {"timezone": "Europe/Paris", "lat": 48.8566, "lon": 2.3522},
            "紐約": {"timezone": "America/New_York", "lat": 40.7128, "lon": -74.0060},
            "溫哥華": {"timezone": "America/Vancouver", "lat": 49.2827, "lon": -123.1207},
            "首爾": {"timezone": "Asia/Seoul", "lat": 37.5665, "lon": 126.9780},
            "里斯本": {"timezone": "Europe/Lisbon", "lat": 38.7223, "lon": -9.1393}
        }

        # 建立一個存放時間與天氣標籤的字典
        self.time_labels = {}
        self.weather_labels = {}

        self.create_widgets()
        
        self.update_clocks()
        self.update_weather()

    def create_widgets(self):
        """建立時鐘介面"""
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(expand=True, fill=tk.BOTH)

        title_font = font.Font(family="Helvetica", size=18, weight="bold")
        time_font = font.Font(family="Helvetica", size=14)
        weather_font = font.Font(family="Helvetica", size=12, slant="italic")

        for city, data in self.clocks.items():
            city_frame = tk.Frame(main_frame, bg="#34495e", padx=10, pady=10)
            city_frame.pack(fill=tk.X, padx=20, pady=5)
            
            city_label = tk.Label(city_frame, text=city, font=title_font, fg="#ecf0f1", bg="#34495e")
            city_label.pack(side=tk.LEFT, padx=(0, 20))

            # 時間標籤
            time_label = tk.Label(city_frame, text="", font=time_font, fg="#ecf0f1", bg="#34495e")
            time_label.pack(side=tk.LEFT, expand=True, fill=tk.X)
            self.time_labels[city] = time_label
            
            # 天氣標籤
            weather_label = tk.Label(city_frame, text="天氣資料載入中...", font=weather_font, fg="#bdc3c7", bg="#34495e")
            weather_label.pack(side=tk.RIGHT, padx=(20, 0))
            self.weather_labels[city] = weather_label

    def update_clocks(self):
        """每100毫秒更新所有時鐘"""
        now_utc = datetime.datetime.now(pytz.utc)
        
        for city, data in self.clocks.items():
            try:
                tz = pytz.timezone(data["timezone"])
                local_time = now_utc.astimezone(tz)
                formatted_time = local_time.strftime("%Y年%m月%d日 %p %I:%M:%S.%f")[:-3]
                
                self.time_labels[city].config(text=formatted_time)
            except Exception as e:
                print(f"更新 {city} 時間時發生錯誤: {e}")
                self.time_labels[city].config(text="無法顯示時間")

        self.root.after(100, self.update_clocks)

    def scrape_weather(self, city, url):
        """從網站獲取指定城市的天氣資料 (網路爬蟲)"""
        try:
            # 這裡我們使用一個範例 URL。你必須將此替換為實際的天氣網站 URL。
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 這裡我們假設溫度和天氣狀況在特定的 HTML 標籤中。
            # 這些選擇器 (.temperature, .weather-description) 必須根據你選擇的網站進行調整。
            temp_element = soup.find(class_="temperature")
            desc_element = soup.find(class_="weather-description")

            if temp_element and desc_element:
                temp = temp_element.get_text().strip()
                description = desc_element.get_text().strip()
                weather_text = f"{description}, {temp}"
                self.weather_labels[city].config(text=weather_text)
            else:
                self.weather_labels[city].config(text="無法解析天氣資料")

        except requests.exceptions.RequestException as e:
            print(f"獲取 {city} 天氣資料失敗: {e}")
            self.weather_labels[city].config(text="天氣資料載入失敗")
        except Exception as e:
            print(f"解析 {city} 天氣資料時發生錯誤: {e}")
            self.weather_labels[city].config(text="無法解析天氣資料")

    def update_weather(self):
        """每15分鐘更新一次天氣資料"""
        # 這裡我們使用一個範例 URL，你必須為每個城市找到對應的 URL
        # 並且這些 URL 的 HTML 結構必須一致，才能使用相同的解析邏輯
        weather_urls = {
            "台灣": "https://example.com/weather/taiwan",
            "日本": "https://example.com/weather/japan",
            "倫敦": "https://example.com/weather/london",
            "巴黎": "https://example.com/weather/paris",
            "紐約": "https://example.com/weather/new_york",
            "溫哥華": "https://example.com/weather/vancouver",
            "首爾": "https://example.com/weather/seoul",
            "里斯本": "https://example.com/weather/lisbon"
        }
            
        for city, url in weather_urls.items():
            # 使用線程來避免阻塞 UI 介面
            thread = threading.Thread(target=self.scrape_weather, args=(city, url))
            thread.daemon = True
            thread.start()
        
        # 安排在 15 分鐘後再次呼叫此函數 (15 * 60 * 1000 毫秒)
        self.root.after(900000, self.update_weather)


if __name__ == "__main__":
    root = tk.Tk()
    app = WorldClockApp(root)
    root.mainloop()
