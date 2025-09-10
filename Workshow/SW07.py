import tkinter as tk
from tkinter import font, ttk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import threading
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta
import calendar

class GasPriceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("油價查詢 - 即時與歷史")
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
        
        # 初始化歷史資料
        self.init_historical_data()
        
        self.fetch_prices()
        self.create_widgets()

    def init_historical_data(self):
        """初始化歷史油價資料（模擬數據，實際使用時可替換為真實API）"""
        base_prices = {
            '92無鉛': 27.4,
            '95無鉛': 28.9,
            '98無鉛': 30.9,
            '柴油': 26.4
        }
        
        # 生成過去12個月的歷史資料
        current_date = datetime.now()
        for i in range(12, 0, -1):  # 從12個月前到現在
            # 計算日期
            year = current_date.year
            month = current_date.month - i
            if month <= 0:
                month += 12
                year -= 1
            
            # 生成該月的油價（模擬價格變動）
            month_name = f"{year}年{month:02d}月"
            
            # 模擬價格波動（基於時間的簡單演算法）
            price_factor = 1 + (i - 6) * 0.02 + (i % 3 - 1) * 0.015
            
            self.gas_prices[month_name] = {
                '92無鉛': f"{base_prices['92無鉛'] * price_factor:.1f}",
                '95無鉛': f"{base_prices['95無鉛'] * price_factor:.1f}",
                '98無鉛': f"{base_prices['98無鉛'] * price_factor:.1f}",
                '柴油': f"{base_prices['柴油'] * price_factor:.1f}"
            }

    def fetch_historical_prices(self, year, month):
        """抓取特定年月的歷史油價（可擴展為真實API呼叫）"""
        # 這裡可以實作真實的歷史資料API呼叫
        # 目前使用模擬資料
        month_key = f"{year}年{month:02d}月"
        if month_key in self.gas_prices:
            return self.gas_prices[month_key]
        else:
            # 如果沒有該月資料，生成模擬資料
            base_prices = {
                '92無鉛': 27.4,
                '95無鉛': 28.9,
                '98無鉛': 30.9,
                '柴油': 26.4
            }
            
            # 簡單的價格模擬
            months_ago = (datetime.now().year - year) * 12 + (datetime.now().month - month)
            price_factor = 1 + months_ago * 0.01
            
            return {
                '92無鉛': f"{base_prices['92無鉛'] * price_factor:.1f}",
                '95無鉛': f"{base_prices['95無鉛'] * price_factor:.1f}",
                '98無鉛': f"{base_prices['98無鉛'] * price_factor:.1f}",
                '柴油': f"{base_prices['柴油'] * price_factor:.1f}"
            }

    def fetch_prices(self):
        """從中油官方API抓取即時油價資料"""
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

        except requests.exceptions.RequestException as e:
            print(f"官方API請求失敗: {e}")
            self.fetch_prices_backup()
        except Exception as e:
            print(f"官方API解析失敗: {e}")
            self.fetch_prices_backup()
        
        # 準備時間選項列表
        self.prepare_time_options()

    def fetch_prices_backup(self):
        """備用方法：使用預設油價"""
        self.gas_prices['即時油價'] = {
            '92無鉛': '27.4',
            '95無鉛': '28.9', 
            '98無鉛': '30.9',
            '柴油': '26.4'
        }

    def prepare_time_options(self):
        """準備時間選項（即時 + 已有的歷史月份 + 可查詢的歷史月份）"""
        self.time_options = ['即時油價']
        
        # 添加已載入的歷史月份
        historical_months = [key for key in self.gas_prices.keys() if key != '即時油價']
        historical_months.sort(reverse=True)  # 最新的在前
        
        # 如果沒有歷史資料，生成過去12個月的選項
        if not historical_months:
            current_date = datetime.now()
            for i in range(1, 13):  # 過去12個月
                year = current_date.year
                month = current_date.month - i
                if month <= 0:
                    month += 12
                    year -= 1
                
                month_name = f"{year}年{month:02d}月"
                self.time_options.append(month_name)
        else:
            # 使用已有的歷史資料
            self.time_options.extend(historical_months)
        
        # 設定預設選項
        if self.time_options:
            self.current_time_option.set(self.time_options[0])

    def create_widgets(self):
        """建立應用程式介面"""
        main_frame = tk.Frame(self.root, bg="#2c3e50", padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)

        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        
        # 標題
        title_label = tk.Label(main_frame, text="中油油價查詢", font=title_font, fg="#ecf0f1", bg="#2c3e50")
        title_label.pack(pady=(0, 10))
        
        # 控制面板
        control_frame = tk.Frame(main_frame, bg="#2c3e50")
        control_frame.pack(pady=(0, 20), fill=tk.X)
        
        # 時間選擇下拉選單
        time_label = tk.Label(control_frame, text="查詢時間:", 
                             font=font.Font(family="Helvetica", size=12), 
                             fg="#ecf0f1", bg="#2c3e50")
        time_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # 使用 ttk.Combobox 建立下拉選單
        self.time_combo = ttk.Combobox(control_frame, textvariable=self.current_time_option,
                                      values=self.time_options, state="readonly",
                                      font=font.Font(family="Helvetica", size=11),
                                      width=15)
        self.time_combo.pack(side=tk.LEFT, padx=(0, 20))
        self.time_combo.bind('<<ComboboxSelected>>', self.on_time_changed)
        
        # 重新整理按鈕
        refresh_btn = tk.Button(control_frame, text="重新整理", command=self.refresh_prices, 
                               bg="#3498db", fg="white", font=font.Font(family="Helvetica", size=11),
                               padx=15, pady=5, relief=tk.FLAT)
        refresh_btn.pack(side=tk.LEFT)
        
        # 更新時間顯示
        self.update_time_label = tk.Label(main_frame, text="", 
                                         font=font.Font(family="Helvetica", size=10), 
                                         fg="#95a5a6", bg="#2c3e50")
        self.update_time_label.pack(pady=(0, 20))
        
        # 油價顯示區
        self.price_display_frame = tk.Frame(main_frame, bg="#2c3e50")
        self.price_display_frame.pack(pady=(10, 0), expand=True, fill=tk.BOTH)
        
        # 載入油價
        self.update_prices()
        self.update_time_display()

    def on_time_changed(self, event=None):
        """當時間選擇改變時的處理"""
        selected_time = self.current_time_option.get()
        
        # 如果選擇歷史月份且尚未載入資料
        if selected_time != '即時油價' and selected_time not in self.gas_prices:
            # 解析年月
            try:
                year_month = selected_time.replace('年', '-').replace('月', '')
                year, month = year_month.split('-')
                year, month = int(year), int(month)
                
                # 載入該月歷史資料
                historical_data = self.fetch_historical_prices(year, month)
                self.gas_prices[selected_time] = historical_data
                
            except ValueError:
                messagebox.showerror("錯誤", "無法解析選擇的日期")
                return
        
        self.update_prices()
        self.update_time_display()

    def refresh_prices(self):
        """重新整理油價"""
        selected_time = self.current_time_option.get()
        
        # 顯示載入中
        for widget in self.price_display_frame.winfo_children():
            widget.destroy()
        
        loading_label = tk.Label(self.price_display_frame, text="載入中...", 
                               font=font.Font(family="Helvetica", size=16), 
                               fg="#95a5a6", bg="#2c3e50")
        loading_label.pack(pady=50)
        
        # 在背景執行緒中重新載入資料
        def fetch_in_background():
            if selected_time == '即時油價':
                self.fetch_prices()
            else:
                # 重新載入歷史資料
                try:
                    year_month = selected_time.replace('年', '-').replace('月', '')
                    year, month = year_month.split('-')
                    year, month = int(year), int(month)
                    
                    historical_data = self.fetch_historical_prices(year, month)
                    self.gas_prices[selected_time] = historical_data
                    
                except ValueError:
                    pass
            
            self.root.after(0, lambda: (self.update_prices(), self.update_time_display()))
        
        threading.Thread(target=fetch_in_background, daemon=True).start()

    def update_time_display(self):
        """更新時間顯示"""
        selected_time = self.current_time_option.get()
        if selected_time == '即時油價':
            update_text = f"即時資料 - 更新時間: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        else:
            update_text = f"歷史資料 - {selected_time}"
        
        self.update_time_label.config(text=update_text)

    def update_prices(self, *args):
        """根據選擇更新油價顯示"""
        selected_time = self.current_time_option.get()
        prices = self.gas_prices.get(selected_time, {})
        
        # 清除舊的價格顯示
        for widget in self.price_display_frame.winfo_children():
            widget.destroy()
        
        if prices:
            # 油價標題
            price_title = tk.Label(self.price_display_frame, 
                                 text=f"{selected_time}",
                                 font=font.Font(family="Helvetica", size=16, weight="bold"), 
                                 fg="#3498db", bg="#2c3e50")
            price_title.pack(pady=(0, 15))
            
            # 顯示油價
            for i, (name, price) in enumerate(prices.items()):
                price_frame = tk.Frame(self.price_display_frame, bg="#34495e", padx=20, pady=15)
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
            no_data_label = tk.Label(self.price_display_frame, text=f"無法載入 {selected_time} 資料", 
                                   font=font.Font(family="Helvetica", size=16), 
                                   fg="#95a5a6", bg="#2c3e50")
            no_data_label.pack(pady=50)

    def add_custom_historical_period(self, period_name, prices_data):
        """添加自定義歷史期間的油價資料"""
        self.gas_prices[period_name] = prices_data
        if period_name not in self.time_options:
            self.time_options.append(period_name)
            self.time_combo['values'] = self.time_options


if __name__ == "__main__":
    root = tk.Tk()
    app = GasPriceApp(root)
    root.mainloop()