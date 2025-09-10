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
            requests.get("https://www.google.com", timeout=5) # 測試 requests
            BeautifulSoup("<html></html>", "html.parser") # 測試 BeautifulSoup
        except Exception:
            messagebox.showerror("錯誤", "需要安裝必要的函式庫。請運行 'pip install requests pytz beautifulsoup4'")
            self.root.quit()
        
        # 這裡不再需要 API Key
        self.api_key = None

        # 設定時區與城市名稱
        self.clocks = {
            "台北": {"timezone": "Asia/Taipei"},
            "東京": {"timezone": "Asia/Tokyo"},
            "倫敦": {"timezone": "Europe/London"},
            "巴黎": {"timezone": "Europe/Paris"},
            "紐約": {"timezone": "America/New_York"},
            "溫哥華": {"timezone": "America/Vancouver"},
            "首爾": {"timezone": "Asia/Seoul"},
            "里斯本": {"timezone": "Europe/Lisbon"}
        }

        # 建立一個存放時間與天氣標籤的字典
        self.time_labels = {}
        self.weather_labels = {}
        self.is_paused = False
        self.after_id = None

        self.create_widgets()
        
        self.update_clocks()
        self.update_weather()

    def create_widgets(self):
        """建立時鐘介面"""
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # 按鈕框架
        button_frame = tk.Frame(main_frame, bg="#2c3e50")
        button_frame.pack(pady=10)

        # 重新啟動按鈕
        self.restart_button = tk.Button(button_frame, text="更新重啟", command=self.restart_updates, bg="#27ae60", fg="#ecf0f1", font=("Helvetica", 12))
        self.restart_button.pack(side=tk.LEFT, padx=5)

        # 暫停/繼續按鈕
        self.pause_button = tk.Button(button_frame, text="暫停", command=self.toggle_pause, bg="#e67e22", fg="#ecf0f1", font=("Helvetica", 12))
        self.pause_button.pack(side=tk.LEFT, padx=5)

        title_font = font.Font(family="Helvetica", size=18, weight="bold")
        time_font = font.Font(family="Helvetica", size=14)
        weather_font = font.Font(family="Helvetica", size=12, slant="italic")

        for city in self.clocks:
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
        if self.is_paused:
            return

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

        self.after_id = self.root.after(100, self.update_clocks)

    def toggle_pause(self):
        """暫停或繼續時間更新"""
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_button.config(text="繼續")
            if self.after_id:
                self.root.after_cancel(self.after_id)
        else:
            self.pause_button.config(text="暫停")
            self.update_clocks()

    def restart_updates(self):
        """重新啟動時間和天氣更新"""
        if self.is_paused:
            self.toggle_pause() # 如果是暫停狀態，先恢復
        
        self.update_weather()
        # 確保時鐘在執行
        if not self.is_paused and self.after_id is None:
             self.update_clocks()


    def scrape_weather(self, city, url, city_id=None):
        """從網站獲取指定城市的天氣資料"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            js_content = response.text

            if city_id:  # 處理台灣縣市
                import ast
                
                # 尋找 TempArray_Week 物件的起始位置
                start_str = 'var TempArray_Week = '
                start_index = js_content.find(start_str)
                
                if start_index == -1:
                    self.weather_labels[city].config(text="天氣資料格式錯誤")
                    return

                # 提取物件字串
                obj_str = js_content[start_index + len(start_str):]
                if obj_str.endswith(';'):
                    obj_str = obj_str[:-1]

                # 使用 ast.literal_eval 安全地解析
                obj_str = obj_str.replace('null', 'None')
                weather_data = ast.literal_eval(obj_str)
                
                city_weather = weather_data.get(city_id)
                if city_weather and city_weather.get('C') and city_weather['C'].get('H') and city_weather.get('Wx'):
                    temp = city_weather['C']['H'][0]
                    description = city_weather['Wx'][0][1].strip()
                    weather_text = f"{description}, {temp}°C"
                    self.weather_labels[city].config(text=weather_text)
                else:
                    self.weather_labels[city].config(text="無法取得天氣")

            else:  # 處理世界城市
                import ast
                import re

                wid = re.search(r'WID=(\d+)', url).group(1)
                js_url = f"https://www.cwa.gov.tw/Data/js/fcst/World/World_ChartData_Week_{wid}.js"
                response = requests.get(js_url, timeout=10)
                response.raise_for_status()
                js_content = response.text
                
                # 尋找 ChartData 物件的起始位置
                start_str = 'var ChartData='
                start_index = js_content.find(start_str)

                if start_index == -1:
                    self.weather_labels[city].config(text="天氣資料格式錯誤")
                    return
                
                # 提取物件字串
                obj_str = js_content[start_index + len(start_str):]
                if obj_str.endswith(';'):
                    obj_str = obj_str[:-1]

                # 使用 ast.literal_eval 安全地解析
                weather_data = ast.literal_eval(obj_str)

                if weather_data.get('MaxT_C'):
                    temp = weather_data['MaxT_C'][0]
                    description = self.get_weather_description_from_temp(temp)
                    weather_text = f"{description}, {temp}°C"
                    self.weather_labels[city].config(text=weather_text)
                else:
                    self.weather_labels[city].config(text="無法取得溫度")

        except requests.exceptions.RequestException as e:
            print(f"獲取 {city} 天氣資料失敗: {e}")
            self.weather_labels[city].config(text="天氣資料載入失敗")
        except Exception as e:
            print(f"解析 {city} 天氣資料時發生錯誤: {e}")
            self.weather_labels[city].config(text="天氣資料解析失敗")

    def get_weather_description_from_temp(self, temp):
        """根據溫度推斷天氣狀況"""
        if temp >= 30:
            return "炎熱"
        elif 20 <= temp < 30:
            return "溫暖"
        elif 10 <= temp < 20:
            return "涼爽"
        else:
            return "寒冷"

    def update_weather(self):
        """每15分鐘更新一次天氣資料"""
        weather_urls = {
            "台北": {"url": "https://www.cwa.gov.tw/Data/js/week/ChartData_Week_County_C.js", "id": "63"},
            "東京": {"url": "https://www.cwa.gov.tw/V8/C/W/world.html?TYPE=AP&WID=47662"},
            "倫敦": {"url": "https://www.cwa.gov.tw/V8/C/W/world.html?TYPE=EA&WID=3770"},
            "巴黎": {"url": "https://www.cwa.gov.tw/V8/C/W/world.html?TYPE=EA&WID=7156"},
            "紐約": {"url": "https://www.cwa.gov.tw/V8/C/W/world.html?TYPE=AM&WID=74486"},
            "溫哥華": {"url": "https://www.cwa.gov.tw/V8/C/W/world.html?TYPE=AM&WID=71892"},
            "首爾": {"url": "https://www.cwa.gov.tw/V8/C/W/world.html?TYPE=AP&WID=47108"},
            "里斯本": {"url": "https://www.cwa.gov.tw/V8/C/W/world.html?TYPE=EA&WID=8535"}
        }
            
        for city, data in weather_urls.items():
            url = data.get("url")
            city_id = data.get("id")
            if url:
                # 使用線程來避免阻塞 UI 介面
                thread = threading.Thread(target=self.scrape_weather, args=(city, url, city_id))
                thread.daemon = True
                thread.start()
        
        # 安排在 15 分鐘後再次呼叫此函數 (15 * 60 * 1000 毫秒)
        self.root.after(900000, self.update_weather)


if __name__ == "__main__":
    root = tk.Tk()
    app = WorldClockApp(root)
    root.mainloop()
