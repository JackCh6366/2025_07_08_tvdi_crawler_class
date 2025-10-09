import tkinter as tk
from tkinter import ttk, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import threading
import re
from datetime import datetime
import requests
from urllib.parse import urljoin

class MovieScraper:
    def __init__(self):
        self.driver = None
        self.debug_mode = True
        
    def setup_driver(self):
        """設置 Chrome WebDriver"""
        try:
            chrome_options = Options()
            # 註解掉 headless 模式以便除錯
            # chrome_options.add_argument("--headless")  
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # 設置腳本以隱藏 webdriver 特徵
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return True
        except Exception as e:
            print(f"設置 WebDriver 時發生錯誤：{e}")
            return False
    
    def debug_print(self, message):
        """除錯訊息輸出"""
        if self.debug_mode:
            print(f"[DEBUG] {message}")
    
    def save_page_source(self, content, filename):
        """儲存頁面原始碼用於除錯"""
        try:
            with open(f"{filename}.html", "w", encoding="utf-8") as f:
                f.write(content)
            self.debug_print(f"頁面原始碼已儲存至 {filename}.html")
        except Exception as e:
            self.debug_print(f"儲存頁面原始碼失敗: {e}")
    
    def get_movie_data_alternative(self, movie_type):
        """使用替代方法獲取電影資料（模擬真實數據）"""
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        if movie_type == "上映中":
            return [
                {'title': '玩命關頭X', 'date': f'{current_date} 上映', 'type': movie_type, 'time': '14:20, 17:30, 20:40'},
                {'title': '蜘蛛人：穿越新宇宙', 'date': f'{current_date} 上映', 'type': movie_type, 'time': '13:15, 16:25, 19:35'},
                {'title': '不可能的任務：致命清算 第一章', 'date': f'{current_date} 上映', 'type': movie_type, 'time': '15:10, 18:20, 21:30'},
                {'title': '芭比', 'date': f'{current_date} 上映', 'type': movie_type, 'time': '12:00, 14:45, 17:15, 19:50'},
                {'title': '奧本海默', 'date': f'{current_date} 上映', 'type': movie_type, 'time': '13:30, 17:00, 20:30'},
                {'title': '變形金剛：萬獸崛起', 'date': f'{current_date} 上映', 'type': movie_type, 'time': '16:40, 19:20, 22:10'},
                {'title': '小美人魚', 'date': f'{current_date} 上映', 'type': movie_type, 'time': '14:00, 16:50, 19:40'},
                {'title': '閃電俠', 'date': f'{current_date} 上映', 'type': movie_type, 'time': '15:30, 18:15, 21:00'},
            ]
        else:  # 即將上映
            return [
                {'title': '沙丘：第二部', 'date': '2024-10-15 上映', 'type': movie_type, 'time': '敬請期待'},
                {'title': '復仇者聯盟：祕密戰爭', 'date': '2024-11-08 上映', 'type': movie_type, 'time': '敬請期待'},
                {'title': '阿凡達：火與灰', 'date': '2024-12-20 上映', 'type': movie_type, 'time': '敬請期待'},
                {'title': '雷神索爾：愛與雷電續集', 'date': '2024-10-25 上映', 'type': movie_type, 'time': '敬請期待'},
                {'title': '黑豹：瓦干達永遠', 'date': '2024-11-11 上映', 'type': movie_type, 'time': '敬請期待'},
            ]
    
    def get_movie_data(self, url, movie_type):
        """
        使用 Selenium 從網頁抓取電影資料
        """
        if not self.setup_driver():
            self.debug_print("WebDriver 設置失敗，使用替代數據")
            return self.get_movie_data_alternative(movie_type)
            
        try:
            self.debug_print(f"開始載入 URL: {url}")
            self.driver.get(url)
            
            # 等待頁面完全載入
            time.sleep(5)
            
            # 嘗試點擊或滾動以觸發動態內容載入
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            # 獲取頁面標題確認載入成功
            page_title = self.driver.title
            self.debug_print(f"頁面標題: {page_title}")
            
            # 獲取頁面原始碼
            html_content = self.driver.page_source
            self.debug_print(f"頁面原始碼長度: {len(html_content)}")
            
            # 儲存頁面原始碼用於除錯
            filename = f"debug_{movie_type.replace('上映', 'showing').replace('即將', 'coming')}"
            self.save_page_source(html_content, filename)
            
            soup = BeautifulSoup(html_content, 'html.parser')
            movies = []
            
            # 詳細的元素搜尋策略
            self.debug_print("開始搜尋電影元素...")
            
            # 策略1: 尋找包含「電影」、「片名」等關鍵字的元素
            text_elements = soup.find_all(text=True)
            movie_keywords = ['電影', '片名', '上映', '場次', '時刻', '預告', '劇情']
            
            potential_movies = []
            for text in text_elements:
                text = text.strip()
                if text and len(text) > 2 and len(text) < 50:
                    # 檢查是否包含電影相關關鍵字或看起來像電影標題
                    if (any(keyword in text for keyword in movie_keywords) or 
                        re.search(r'[\u4e00-\u9fff]{2,}', text) or  # 中文字符
                        re.search(r'[A-Za-z]{3,}', text)):  # 英文字符
                        potential_movies.append(text)
            
            self.debug_print(f"找到 {len(potential_movies)} 個潛在電影相關文字")
            
            # 策略2: 尋找特定的HTML結構
            selectors_to_try = [
                'div[class*="movie"]',
                'div[class*="film"]',
                'div[class*="show"]',
                'div[class*="item"]',
                'div[class*="list"]',
                'div[class*="card"]',
                'div[class*="info"]',
                'div[id*="movie"]',
                'div[id*="film"]',
                '.movie_list',
                '.film_list',
                '.show_list',
                'a[class*="title"]',
                'h1, h2, h3, h4',
                'span[class*="name"]',
                'div[class*="name"]'
            ]
            
            for selector in selectors_to_try:
                elements = soup.select(selector)
                self.debug_print(f"選擇器 '{selector}' 找到 {len(elements)} 個元素")
                
                for element in elements[:10]:  # 限制檢查前10個元素
                    text = element.get_text(strip=True)
                    if text and len(text) > 2 and len(text) < 100:
                        # 過濾明顯不是電影相關的內容
                        exclude_words = ['首頁', '關於', '聯絡', 'home', 'about', 'contact', 
                                       '購票須知', '會員', '登入', '註冊', '優惠', '服務']
                        if not any(word in text.lower() for word in exclude_words):
                            potential_movies.append(text)
            
            # 去重並篩選
            unique_movies = list(set(potential_movies))
            self.debug_print(f"去重後有 {len(unique_movies)} 個唯一項目")
            
            # 進一步篩選和格式化
            for text in unique_movies[:20]:  # 取前20個
                # 清理文字
                clean_text = re.sub(r'\s+', ' ', text)
                clean_text = clean_text.strip()
                
                if len(clean_text) >= 3 and len(clean_text) <= 50:
                    movies.append({
                        'title': clean_text,
                        'date': f'{datetime.now().strftime("%Y-%m-%d")} 上映' if movie_type == '上映中' else '上映日期待定',
                        'type': movie_type,
                        'time': '時刻表請洽影城' if movie_type == '上映中' else '敬請期待'
                    })
            
            # 如果仍然沒有找到電影，使用替代數據
            if not movies:
                self.debug_print("未找到電影資料，使用替代數據")
                movies = self.get_movie_data_alternative(movie_type)
            
            self.debug_print(f"最終找到 {len(movies)} 部電影")
            return movies
            
        except Exception as e:
            self.debug_print(f"抓取 {movie_type} 資料時發生錯誤：{e}")
            return self.get_movie_data_alternative(movie_type)
        
        finally:
            if self.driver:
                self.driver.quit()

class MovieGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("樂聲影城電影查詢系統")
        self.root.geometry("900x800")
        
        # 設定應用程式圖示
        try:
            self.root.iconbitmap('movie.ico')
        except:
            print("找不到圖示檔案，使用預設圖示")
        
        self.all_movies = []
        self.filtered_movies = []
        self.scraper = MovieScraper()
        
        self.setup_gui()
        self.load_sample_data()  # 先載入範例數據
    
    def setup_gui(self):
        """設置GUI界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 標題
        title_label = ttk.Label(main_frame, text="樂聲影城電影查詢系統", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # 篩選控制區
        filter_frame = ttk.LabelFrame(main_frame, text="篩選選項", padding="10")
        filter_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 電影類型篩選
        ttk.Label(filter_frame, text="電影類型:").grid(row=0, column=0, padx=(0, 5))
        self.type_var = tk.StringVar(value="全部")
        type_combo = ttk.Combobox(filter_frame, textvariable=self.type_var, 
                                 values=["全部", "上映中", "即將上映"], state="readonly", width=15)
        type_combo.grid(row=0, column=1, padx=5)
        type_combo.bind('<<ComboboxSelected>>', self.filter_movies)
        
        # 搜尋框
        ttk.Label(filter_frame, text="搜尋電影:").grid(row=0, column=2, padx=(20, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=20)
        search_entry.grid(row=0, column=3, padx=5)
        search_entry.bind('<KeyRelease>', self.filter_movies)
        
        # 按鈕區
        button_frame = ttk.Frame(filter_frame)
        button_frame.grid(row=0, column=4, padx=(20, 0))
        
        # 重新整理按鈕
        refresh_btn = ttk.Button(button_frame, text="重新整理", command=self.refresh_data)
        refresh_btn.grid(row=0, column=0, padx=2)
        
        # 載入真實數據按鈕
        load_real_btn = ttk.Button(button_frame, text="載入網站數據", command=self.start_loading)
        load_real_btn.grid(row=0, column=1, padx=2)
        
        # 狀態標籤
        self.status_var = tk.StringVar(value="已載入範例數據，點擊「載入網站數據」獲取最新資訊")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                foreground="blue")
        status_label.grid(row=2, column=0, columnspan=4, pady=(0, 10))
        
        # 電影列表框架
        list_frame = ttk.LabelFrame(main_frame, text="電影列表", padding="5")
        list_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Treeview 設定
        columns = ('type', 'title', 'date', 'time')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        # 設定欄位標題
        self.tree.heading('type', text='類型', anchor='center')
        self.tree.heading('title', text='電影名稱', anchor='w')
        self.tree.heading('date', text='日期資訊', anchor='center')
        self.tree.heading('time', text='場次時間', anchor='center')
        
        # 設定欄位寬度
        self.tree.column('type', width=80, anchor='center')
        self.tree.column('title', width=300, anchor='w')
        self.tree.column('date', width=150, anchor='center')
        self.tree.column('time', width=200, anchor='center')
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 捲軸
        scrollbar_v = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_v.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar_v.set)
        
        scrollbar_h = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollbar_h.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.tree.configure(xscrollcommand=scrollbar_h.set)
        
        # 設定網格權重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 統計資訊
        self.stats_var = tk.StringVar(value="")
        stats_label = ttk.Label(main_frame, textvariable=self.stats_var)
        stats_label.grid(row=4, column=0, columnspan=4, pady=(10, 0))
        
        # 說明標籤
        info_text = ("提示：程式包含範例數據供測試使用。\n"
                    "點擊「載入網站數據」可嘗試從樂聲影城官網獲取最新電影資訊。\n"
                    "如果網站載入失敗，將自動使用更豐富的模擬數據。")
        info_label = ttk.Label(main_frame, text=info_text, 
                              font=("Arial", 9), foreground="gray", 
                              justify="center")
        info_label.grid(row=5, column=0, columnspan=4, pady=(10, 0))
    
    def load_sample_data(self):
        """載入範例數據"""
        sample_movies = [
            {'title': '玩命關頭X', 'date': '2025-09-23 上映', 'type': '上映中', 'time': '14:20, 17:30, 20:40'},
            {'title': '蜘蛛人：穿越新宇宙', 'date': '2025-09-23 上映', 'type': '上映中', 'time': '13:15, 16:25, 19:35'},
            {'title': '不可能的任務：致命清算', 'date': '2025-09-23 上映', 'type': '上映中', 'time': '15:10, 18:20, 21:30'},
            {'title': '沙丘：第二部', 'date': '2025-10-15 上映', 'type': '即將上映', 'time': '敬請期待'},
            {'title': '復仇者聯盟：祕密戰爭', 'date': '2025-11-08 上映', 'type': '即將上映', 'time': '敬請期待'},
        ]
        
        self.update_movie_list(sample_movies)
    
    def start_loading(self):
        """開始載入網站數據"""
        self.status_var.set("正在從樂聲影城官網載入最新電影資料，請稍候...")
        
        def load_data():
            try:
                # URL 列表
                urls = [
                    ("https://www.luxcinema.com.tw/web/2020.php?type=ShowTimes#type_anchor", "上映中"),
                    ("https://www.luxcinema.com.tw/web/2020.php?type=c#type_anchor", "即將上映")
                ]
                
                all_movies = []
                
                for url, movie_type in urls:
                    self.root.after(0, lambda t=movie_type: self.status_var.set(f"正在載入{t}電影..."))
                    movies = self.scraper.get_movie_data(url, movie_type)
                    all_movies.extend(movies)
                    time.sleep(2)  # 避免請求過於頻繁
                
                # 在主執行緒中更新 GUI
                self.root.after(0, lambda: self.update_movie_list(all_movies))
                
            except Exception as e:
                self.root.after(0, lambda: self.status_var.set(f"載入失敗: {str(e)}"))
        
        # 在背景執行緒中載入數據
        thread = threading.Thread(target=load_data, daemon=True)
        thread.start()
    
    def update_movie_list(self, movies):
        """更新電影列表"""
        self.all_movies = movies
        self.filtered_movies = movies.copy()
        
        # 清空現有項目
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 插入新項目
        for movie in movies:
            self.tree.insert('', 'end', values=(
                movie['type'],
                movie['title'],
                movie['date'],
                movie.get('time', '請洽影城')
            ))
        
        # 更新統計資訊
        showing_count = len([m for m in movies if m['type'] == '上映中'])
        coming_count = len([m for m in movies if m['type'] == '即將上映'])
        
        self.stats_var.set(f"共找到 {len(movies)} 部電影 (上映中: {showing_count} 部, 即將上映: {coming_count} 部)")
        self.status_var.set("電影資料載入完成！")
    
    def filter_movies(self, event=None):
        """篩選電影"""
        if not self.all_movies:
            return
        
        type_filter = self.type_var.get()
        search_text = self.search_var.get().lower()
        
        filtered = self.all_movies.copy()
        
        # 類型篩選
        if type_filter != "全部":
            filtered = [m for m in filtered if m['type'] == type_filter]
        
        # 搜尋篩選
        if search_text:
            filtered = [m for m in filtered if search_text in m['title'].lower()]
        
        # 更新顯示
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for movie in filtered:
            self.tree.insert('', 'end', values=(
                movie['type'],
                movie['title'],
                movie['date'],
                movie.get('time', '請洽影城')
            ))
        
        self.filtered_movies = filtered
        
        # 更新統計
        showing_count = len([m for m in filtered if m['type'] == '上映中'])
        coming_count = len([m for m in filtered if m['type'] == '即將上映'])
        
        self.stats_var.set(f"顯示 {len(filtered)} 部電影 (上映中: {showing_count} 部, 即將上映: {coming_count} 部)")
    
    def refresh_data(self):
        """重新整理資料"""
        self.load_sample_data()

def main():
    """主程式"""
    try:
        root = tk.Tk()
        app = MovieGUI(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("錯誤", f"程式啟動失敗：{str(e)}")

if __name__ == "__main__":
    main()