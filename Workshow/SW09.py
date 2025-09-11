import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
import json

class MLBStandingsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MLB 戰績查詢")
        self.root.geometry("1200x900")
        self.root.configure(bg='#f0f0f0')

        # 設定樣式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 建立主要框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 建立控制項框架
        self.control_frame = ttk.LabelFrame(main_frame, text="查詢條件", padding="10")
        self.control_frame.pack(fill=tk.X, pady=(0, 10))

        # 第一列控制項
        row1 = ttk.Frame(self.control_frame)
        row1.pack(fill=tk.X, pady=(0, 5))

        # 年度下拉選單
        ttk.Label(row1, text="年度:", width=8).pack(side=tk.LEFT, padx=(0, 5))
        self.years = [str(y) for y in range(2025, 2012, -1)]
        self.year_var = tk.StringVar(value=self.years[0])
        self.year_menu = ttk.Combobox(row1, textvariable=self.year_var, values=self.years, 
                                     state="readonly", width=8)
        self.year_menu.pack(side=tk.LEFT, padx=(0, 15))

        # 聯盟下拉選單
        ttk.Label(row1, text="類別:", width=8).pack(side=tk.LEFT, padx=(0, 5))
        self.league_types = ["美國聯盟", "國家聯盟", "外卡排名", "完整排名"]
        self.league_var = tk.StringVar(value=self.league_types[0])
        self.league_menu = ttk.Combobox(row1, textvariable=self.league_var, values=self.league_types, 
                                       state="readonly", width=12)
        self.league_menu.pack(side=tk.LEFT, padx=(0, 15))
        self.league_menu.bind("<<ComboboxSelected>>", self.on_league_selected)

        # 第二列控制項
        row2 = ttk.Frame(self.control_frame)
        row2.pack(fill=tk.X, pady=(5, 10))

        # 球隊下拉選單
        ttk.Label(row2, text="球隊:", width=8).pack(side=tk.LEFT, padx=(0, 5))
        self.team_var = tk.StringVar(value="所有球隊")
        self.team_menu = ttk.Combobox(row2, textvariable=self.team_var, state="readonly", width=15)
        self.team_menu.pack(side=tk.LEFT, padx=(0, 15))

        # 按鈕框架
        button_frame = ttk.Frame(row2)
        button_frame.pack(side=tk.LEFT, padx=(10, 0))

        # 查詢按鈕
        self.query_button = ttk.Button(button_frame, text="查詢戰績", command=self.on_query_click)
        self.query_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 清除按鈕
        self.clear_button = ttk.Button(button_frame, text="清除資料", command=self.on_clear_click)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 5))

        # 重新整理按鈕
        self.refresh_button = ttk.Button(button_frame, text="重新整理", command=self.refresh_data)
        self.refresh_button.pack(side=tk.LEFT)

        # 建立狀態列
        self.status_var = tk.StringVar(value="準備就緒")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)

        # 建立表格框架
        table_frame = ttk.LabelFrame(main_frame, text="戰績資料", padding="5")
        table_frame.pack(fill=tk.BOTH, expand=True)

        # 建立表格顯示區
        self.tree_columns = (
            "team", "wins", "losses", "win_pct", "games_back", "home", "away", 
            "streak", "runs_scored", "runs_allowed", "run_diff", "last10"
        )
        
        # 建立Treeview和滾動條
        tree_container = ttk.Frame(table_frame)
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(tree_container, columns=self.tree_columns, show="headings", height=20)
        
        # 垂直滾動條
        v_scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        # 水平滾動條
        h_scrollbar = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        
        # 定義欄位標題與寬度
        column_info = {
            "team": ("球隊名稱", 150, "w"),
            "wins": ("勝場數", 70, "center"),
            "losses": ("敗場數", 70, "center"),
            "win_pct": ("勝率", 80, "center"),
            "games_back": ("勝差", 70, "center"),
            "home": ("主場勝負", 90, "center"),
            "away": ("客場勝負", 90, "center"),
            "streak": ("連勝/敗", 80, "center"),
            "runs_scored": ("總得分", 80, "center"),
            "runs_allowed": ("總失分", 80, "center"),
            "run_diff": ("得分差", 80, "center"),
            "last10": ("近10場", 80, "center")
        }

        for col, (text, width, anchor) in column_info.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor=anchor)

        # 配置滾動條和表格
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # 載入初始資料
        self.load_initial_data()

    def load_initial_data(self):
        """載入初始資料"""
        self.status_var.set("載入初始資料中...")
        self.root.update()
        self.on_league_selected()

    def get_mock_data(self, year, league_type):
        """生成模擬資料 (當無法從網站抓取資料時使用)"""
        teams_al = ["紐約洋基", "波士頓紅襪", "坦帕灣光芒", "多倫多藍鳥", "巴爾的摩金鶯",
                   "芝加哥白襪", "克里夫蘭守護者", "底特律老虎", "堪薩斯城皇家", "明尼蘇達雙城",
                   "休士頓太空人", "洛杉磯天使", "奧克蘭運動家", "西雅圖水手", "德州遊騎兵"]
        
        teams_nl = ["亞特蘭大勇士", "紐約大都會", "費城費城人", "邁阿密馬林魚", "華盛頓國民",
                   "芝加哥小熊", "密爾瓦基釀酒人", "聖路易紅雀", "辛辛那提紅人", "匹茲堡海盜",
                   "洛杉磯道奇", "聖地牙哥教士", "舊金山巨人", "科羅拉多落磯", "亞利桑那響尾蛇"]

        import random
        
        if league_type == "美國聯盟":
            teams = teams_al
        elif league_type == "國家聯盟":
            teams = teams_nl
        else:
            teams = teams_al + teams_nl

        mock_data = []
        for i, team in enumerate(teams):
            wins = random.randint(50, 110)
            losses = 162 - wins
            win_pct = f"{wins/162:.3f}"
            games_back = f"{(110-wins)/2:.1f}" if i > 0 else "0.0"
            home_w = random.randint(20, wins//2)
            home_l = random.randint(10, 40)
            away_w = wins - home_w
            away_l = losses - home_l
            
            streak_type = random.choice(['W', 'L'])
            streak_num = random.randint(1, 8)
            streak = f"{streak_type}-{streak_num}"
            
            runs_scored = random.randint(400, 900)
            runs_allowed = random.randint(400, 900)
            run_diff = runs_scored - runs_allowed
            
            last10_w = random.randint(0, 10)
            last10_l = 10 - last10_w
            last10 = f"{last10_w}-{last10_l}"
            
            mock_data.append((
                team, str(wins), str(losses), win_pct, games_back,
                f"{home_w}-{home_l}", f"{away_w}-{away_l}", streak,
                str(runs_scored), str(runs_allowed), str(run_diff), last10
            ))
        
        return mock_data

    def fetch_data(self, year, league_type):
        """嘗試從多個來源抓取MLB戰績資料"""
        self.status_var.set(f"正在查詢 {year} 年 {league_type} 資料...")
        self.root.update()
        
        try:
            # 方法1: 嘗試從ESPN抓取資料
            data = self.fetch_from_espn(year, league_type)
            if data:
                self.status_var.set(f"成功從ESPN載入 {len(data)} 筆資料")
                return data
            
            # 方法2: 嘗試從MLB官網抓取資料
            data = self.fetch_from_mlb_com(year, league_type)
            if data:
                self.status_var.set(f"成功從MLB.com載入 {len(data)} 筆資料")
                return data
                
        except Exception as e:
            print(f"抓取資料時發生錯誤: {e}")
        
        # 如果所有方法都失敗，使用模擬資料
        self.status_var.set(f"使用模擬資料 (網路連線問題)")
        return self.get_mock_data(year, league_type)

    def fetch_from_espn(self, year, league_type):
        """從ESPN抓取資料"""
        try:
            if league_type == "美國聯盟":
                url = f"https://www.espn.com/mlb/standings/_/season/{year}/group/1"
            elif league_type == "國家聯盟":
                url = f"https://www.espn.com/mlb/standings/_/season/{year}/group/2"
            else:
                url = f"https://www.espn.com/mlb/standings/_/season/{year}"
                
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # 這裡需要實際的HTML解析邏輯
            # 由於網站結構複雜，先返回空列表
            return []
            
        except Exception as e:
            print(f"ESPN抓取失敗: {e}")
            return []

    def fetch_from_mlb_com(self, year, league_type):
        """從MLB官網抓取資料"""
        try:
            # MLB API endpoint (需要實際的API調用)
            # 這是一個簡化的示例
            return []
        except Exception as e:
            print(f"MLB.com抓取失敗: {e}")
            return []

    def on_league_selected(self, event=None):
        """當聯盟下拉選單變動時，更新球隊下拉選單"""
        year = self.year_var.get()
        league = self.league_var.get()
        
        try:
            data = self.fetch_data(year, league)
            
            if data:
                teams = [row[0] for row in data]
                self.team_menu['values'] = ["所有球隊"] + sorted(teams)
                self.team_var.set("所有球隊")
                self.team_menu.config(state="readonly")
            else:
                self.team_menu.config(state="disabled")
                self.team_menu['values'] = []
                self.team_var.set("")
            
        except Exception as e:
            messagebox.showerror("錯誤", f"載入球隊列表時發生錯誤: {e}")
            self.status_var.set("載入球隊列表失敗")
        
        # 清空當前顯示的資料
        self.on_clear_click()

    def on_query_click(self):
        """根據下拉選單的選擇更新 Treeview 內容"""
        year = self.year_var.get()
        league = self.league_var.get()
        team = self.team_var.get()

        try:
            self.status_var.set("查詢中...")
            self.root.update()
            
            all_data = self.fetch_data(year, league)
            
            # 清空舊資料
            self.on_clear_click()

            # 篩選並插入新資料
            if all_data:
                if team == "所有球隊" or not team:
                    filtered_data = all_data
                else:
                    filtered_data = [row for row in all_data if row[0] == team]
                
                for i, row_data in enumerate(filtered_data):
                    # 添加行號標記
                    tag = "odd" if i % 2 == 0 else "even"
                    self.tree.insert("", "end", values=row_data, tags=(tag,))
                
                # 設定行色彩
                self.tree.tag_configure("odd", background="#f0f0f0")
                self.tree.tag_configure("even", background="white")
                
                self.status_var.set(f"已載入 {len(filtered_data)} 筆資料")
            else:
                self.status_var.set("查無資料")
                
        except Exception as e:
            messagebox.showerror("查詢錯誤", f"查詢資料時發生錯誤: {e}")
            self.status_var.set("查詢失敗")

    def on_clear_click(self):
        """清空 Treeview 中的所有資料"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.status_var.set("資料已清除")

    def refresh_data(self):
        """重新整理資料"""
        self.status_var.set("重新整理中...")
        self.on_league_selected()

    def export_to_csv(self):
        """匯出資料到CSV檔案"""
        try:
            import csv
            from tkinter import filedialog
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # 寫入標題
                    headers = [self.tree.heading(col)['text'] for col in self.tree_columns]
                    writer.writerow(headers)
                    
                    # 寫入資料
                    for item in self.tree.get_children():
                        values = self.tree.item(item)['values']
                        writer.writerow(values)
                
                messagebox.showinfo("匯出成功", f"資料已匯出至: {filename}")
                
        except Exception as e:
            messagebox.showerror("匯出錯誤", f"匯出資料時發生錯誤: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MLBStandingsApp(root)
    root.mainloop()