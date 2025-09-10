import tkinter as tk
from tkinter import font
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import threading
import xml.etree.ElementTree as ET
import json
from datetime import datetime

class GasPriceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("油價查詢")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")

        # 檢查是否安裝必要的函式庫
        try:
            requests.get("https://www.google.com", timeout=5) # 測試 requests
            BeautifulSoup("<html></html>", "html.parser") # 測試 BeautifulSoup
        except Exception:
            messagebox.showerror("錯誤", "需要安裝必要的函式庫。請運行 'pip install requests beautifulsoup4'")
            self.root.quit()

        self.gas_prices = {}
        self.price_labels = {}
        self.time_options = []
        self.current_time_option = tk.StringVar()

        self.fetch_prices()
        self.create_widgets()

    def fetch_prices(self):
        """從中油官方API抓取油價資料"""
        # 使用官方API端點
        self.oil_url = "https://vipmbr.cpc.com.tw/CPCSTN/ListPriceWebService.asmx/getCPCMainProdListPrice_XML"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.oil_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # 先檢查回應內容是否為空
            if not response.text:
                raise ValueError("API 回應內容為空")

            # 解析XML資料
            root = ET.fromstring(response.content)
            
            # 清理並重組資料
            self.gas_prices['即時油價'] = {}
            
            # 解析XML中的油品價格
            for item in root.findall('.//Table'):
                product_name = item.find('產品名稱')
                price = item.find('參考牌價')
                
                if product_name is not None and price is not None:
                    name = product_name.text
                    price_val = price.text
                    
                    # 篩選主要油品並簡化名稱
                    if '92無鉛汽油' in name:
                        self.gas_prices['即時油價']['92無鉛'] = price_val
                    elif '95無鉛汽油' in name:
                        self.gas_prices['即時油價']['95無鉛'] = price_val  
                    elif '98無鉛汽油' in name:
                        self.gas_prices['即時油價']['98無鉛'] = price_val
                    elif '超級柴油' in name and '冬季' not in name:
                        self.gas_prices['即時油價']['柴油'] = price_val

            # 如果官方API失敗，嘗試備用方法
            if not self.gas_prices['即時油價']:
                self.fetch_prices_backup()
            
            self.time_options = ['即時油價']
            self.current_time_option.set(self.time_options[0])

        except requests.exceptions.RequestException as e:
            print(f"官方API請求失敗: {e}")
            self.fetch_prices_backup()
        except Exception as e:
            print(f"官方API解析失敗: {e}")
            self.fetch_prices_backup()

    def fetch_prices_backup(self):
        """備用方法：從中油網站抓取油價資料"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # 嘗試從中油首頁抓取價格
            response = requests.get("https://www.cpc.com.tw/", headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 手動設定目前的油價（可能需要定期更新）
            self.gas_prices['即時油價'] = {
                '92無鉛': '27.4',
                '95無鉛': '28.9', 
                '98無鉛': '30.9',
                '柴油': '26.4'
            }
            
            # 嘗試從網頁中提取實際價格
            # 這部分需要根據網站結構調整
            price_elements = soup.find_all(['div', 'span'], class_=lambda x: x and ('price' in x.lower() or 'oil' in x.lower()))
            
            for element in price_elements:
                text = element.get_text()
                if '92無鉛' in text and '元' in text:
                    import re
                    price_match = re.search(r'(\d+\.?\d*)', text)
                    if price_match:
                        self.gas_prices['即時油價']['92無鉛'] = price_match.group(1)
                        
            self.time_options = ['即時油價']
            self.current_time_option.set(self.time_options[0])
            
        except Exception as e:
            messagebox.showerror("錯誤", f"無法獲取油價資料: {e}\n將使用預設價格")
            # 提供預設價格
            self.gas_prices['即時油價'] = {
                '92無鉛': '27.4',
                '95無鉛': '28.9',
                '98無鉛': '30.9', 
                '柴油': '26.4'
            }
            self.time_options = ['即時油價 (預設)']
            self.current_time_option.set(self.time_options[0])

    def create_widgets(self):
        """建立應用程式介面"""
        main_frame = tk.Frame(self.root, bg="#2c3e50", padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)

        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        info_font = font.Font(family="Helvetica", size=16)
        price_font = font.Font(family="Helvetica", size=20, weight="bold")
        
        # 標題
        title_label = tk.Label(main_frame, text="中油油價查詢", font=title_font, fg="#ecf0f1", bg="#2c3e50")
        title_label.pack(pady=(0, 10))
        
        # 更新時間
        update_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        time_label = tk.Label(main_frame, text=f"更新時間: {update_time}", font=font.Font(family="Helvetica", size=10), fg="#95a5a6", bg="#2c3e50")
        time_label.pack(pady=(0, 20))
        
        # 重新整理按鈕
        refresh_btn = tk.Button(main_frame, text="重新整理", command=self.refresh_prices, 
                               bg="#3498db", fg="white", font=font.Font(family="Helvetica", size=12),
                               padx=20, pady=5, relief=tk.FLAT)
        refresh_btn.pack(pady=(0, 20))
        
        # 油價顯示區
        self.price_display_frame = tk.Frame(main_frame, bg="#2c3e50")
        self.price_display_frame.pack(pady=(20, 0), expand=True, fill=tk.BOTH)
        
        # 載入油價
        self.update_prices()

    def refresh_prices(self):
        """重新整理油價"""
        # 顯示載入中
        for widget in self.price_display_frame.winfo_children():
            widget.destroy()
        
        loading_label = tk.Label(self.price_display_frame, text="載入中...", 
                               font=font.Font(family="Helvetica", size=16), 
                               fg="#95a5a6", bg="#2c3e50")
        loading_label.pack(pady=50)
        
        # 在背景執行緒中重新載入資料
        def fetch_in_background():
            self.fetch_prices()
            self.root.after(0, self.update_prices)
        
        threading.Thread(target=fetch_in_background, daemon=True).start()

    def update_prices(self, *args):
        """根據選擇更新油價顯示"""
        selected_time = self.current_time_option.get()
        prices = self.gas_prices.get(selected_time, {})
        
        # 清除舊的價格顯示
        for widget in self.price_display_frame.winfo_children():
            widget.destroy()
        
        if prices:
            # 顯示油價
            for i, (name, price) in enumerate(prices.items()):
                price_frame = tk.Frame(self.price_display_frame, bg="#34495e", padx=15, pady=15)
                price_frame.pack(pady=5, padx=5, fill=tk.X)
                
                name_label = tk.Label(price_frame, text=name, 
                                    font=font.Font(family="Helvetica", size=14), 
                                    fg="#ecf0f1", bg="#34495e")
                name_label.pack(side=tk.LEFT, padx=(0, 15))
                
                price_label = tk.Label(price_frame, text=f"${price}", 
                                     font=font.Font(family="Helvetica", size=20, weight="bold"), 
                                     fg="#e74c3c", bg="#34495e")
                price_label.pack(side=tk.RIGHT)
        else:
            no_data_label = tk.Label(self.price_display_frame, text="無法載入油價資料", 
                                   font=font.Font(family="Helvetica", size=16), 
                                   fg="#95a5a6", bg="#2c3e50")
            no_data_label.pack(pady=50)


if __name__ == "__main__":
    root = tk.Tk()
    app = GasPriceApp(root)
    root.mainloop()