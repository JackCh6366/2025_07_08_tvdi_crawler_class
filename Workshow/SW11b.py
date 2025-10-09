def show_data_source_dialog(self):
        """顯示資料來源選擇對話框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("選擇資料來源")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 置中顯示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (250 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        tk.Label(dialog, text="選擇資料來源", font=('Arial', 16, 'bold')).pack(pady=20)
        
        tk.Label(dialog, text="請選擇要使用的球員資料來源:", font=('Arial', 12)).pack(pady=10)
        
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def use_real_data():
            dialog.destroy()
            self.load_real_data_with_progress()
        
        def use_sample_data():
            dialog.destroy()
            self.load_sample_data()
        
        tk.Button(button_frame, text="🌐 載入真實MLB資料\n(需要網路連線，較慢)", 
                 font=('Arial', 11), bg='#4CAF50', fg='white', relief='flat',
                 width=20, height=3, command=use_real_data).pack(side='left', padx=10)
        
        tk.Button(button_frame, text="📋 使用示例資料\n(快速載入)", 
                 font=('Arial', 11), bg='#FF9800', fg='white', relief='flat',
                 width=20, height=3, command=use_sample_data).pack(side='right', padx=10)
        
        tk.Label(dialog, text="註: 真實資料載入可能需要1-2分鐘", 
                font=('Arial', 9), fg='gray').pack(pady=10)
    
        def load_real_data_with_progress(self):
          """帶進度顯示的真實資料載入"""
        # 建立進度對話框
        progress_dialog = tk.Toplevel(self.root)
        progress_dialog.title("載入MLB資料")
        progress_dialog.geometry("500x150")
        progress_dialog.resizable(False, False)
        progress_dialog.transient(self.root)
        progress_dialog.grab_set()
        
        # 置中顯示
        progress_dialog.update_idletasks()
        x = (progress_dialog.w#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MLB球員數據查詢系統 - tkinter GUI版本
只使用Python內建模組，無需額外安裝套件
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
from datetime import datetime
import threading

class MLBPlayerDatabase:
    def __init__(self):
        self.players_data = self.load_sample_data()
    
    def load_sample_data(self):
        """載入示例球員數據"""
        return [
            {
                'id': 1,
                'name': 'Mike Trout',
                'team': 'Los Angeles Angels',
                'position': 'OF',
                'jersey': '27',
                'age': 33,
                'batting_avg': 0.283,
                'home_runs': 40,
                'rbi': 104,
                'ops': 0.972,
                'stolen_bases': 25,
                'era': None,
                'wins': None,
                'strikeouts_pitched': None,
                'whip': None,
                'salary': 43_000_000
            },
            {
                'id': 2,
                'name': 'Aaron Judge',
                'team': 'New York Yankees',
                'position': 'OF',
                'jersey': '99',
                'age': 32,
                'batting_avg': 0.311,
                'home_runs': 58,
                'rbi': 144,
                'ops': 1.111,
                'stolen_bases': 6,
                'era': None,
                'wins': None,
                'strikeouts_pitched': None,
                'whip': None,
                'salary': 40_000_000
            },
            {
                'id': 3,
                'name': 'Gerrit Cole',
                'team': 'New York Yankees',
                'position': 'P',
                'jersey': '45',
                'age': 34,
                'batting_avg': None,
                'home_runs': None,
                'rbi': None,
                'ops': None,
                'stolen_bases': None,
                'era': 2.63,
                'wins': 15,
                'strikeouts_pitched': 222,
                'whip': 1.12,
                'salary': 36_000_000
            },
            {
                'id': 4,
                'name': 'Fernando Tatis Jr.',
                'team': 'San Diego Padres',
                'position': 'SS',
                'jersey': '23',
                'age': 26,
                'batting_avg': 0.276,
                'home_runs': 42,
                'rbi': 97,
                'ops': 0.895,
                'stolen_bases': 36,
                'era': None,
                'wins': None,
                'strikeouts_pitched': None,
                'whip': None,
                'salary': 34_000_000
            },
            {
                'id': 5,
                'name': 'Shohei Ohtani',
                'team': 'Los Angeles Dodgers',
                'position': 'DH/P',
                'jersey': '17',
                'age': 30,
                'batting_avg': 0.304,
                'home_runs': 54,
                'rbi': 130,
                'ops': 1.036,
                'stolen_bases': 59,
                'era': 3.18,
                'wins': 10,
                'strikeouts_pitched': 167,
                'whip': 1.05,
                'salary': 70_000_000
            },
            {
                'id': 6,
                'name': 'Vladimir Guerrero Jr.',
                'team': 'Toronto Blue Jays',
                'position': '1B',
                'jersey': '27',
                'age': 25,
                'batting_avg': 0.287,
                'home_runs': 31,
                'rbi': 95,
                'ops': 0.842,
                'stolen_bases': 2,
                'era': None,
                'wins': None,
                'strikeouts_pitched': None,
                'whip': None,
                'salary': 19_900_000
            },
            {
                'id': 7,
                'name': 'Jacob deGrom',
                'team': 'Texas Rangers',
                'position': 'P',
                'jersey': '48',
                'age': 36,
                'batting_avg': None,
                'home_runs': None,
                'rbi': None,
                'ops': None,
                'stolen_bases': None,
                'era': 2.67,
                'wins': 11,
                'strikeouts_pitched': 174,
                'whip': 0.95,
                'salary': 37_000_000
            },
            {
                'id': 8,
                'name': 'José Altuve',
                'team': 'Houston Astros',
                'position': '2B',
                'jersey': '27',
                'age': 34,
                'batting_avg': 0.295,
                'home_runs': 13,
                'rbi': 69,
                'ops': 0.794,
                'stolen_bases': 18,
                'era': None,
                'wins': None,
                'strikeouts_pitched': None,
                'whip': None,
                'salary': 29_000_000
            },
            {
                'id': 9,
                'name': 'Max Scherzer',
                'team': 'Texas Rangers',
                'position': 'P',
                'jersey': '31',
                'age': 40,
                'batting_avg': None,
                'home_runs': None,
                'rbi': None,
                'ops': None,
                'stolen_bases': None,
                'era': 3.95,
                'wins': 8,
                'strikeouts_pitched': 132,
                'whip': 1.28,
                'salary': 43_333_333
            },
            {
                'id': 10,
                'name': 'Ronald Acuña Jr.',
                'team': 'Atlanta Braves',
                'position': 'OF',
                'jersey': '13',
                'age': 26,
                'batting_avg': 0.337,
                'home_runs': 41,
                'rbi': 106,
                'ops': 1.012,
                'stolen_bases': 73,
                'era': None,
                'wins': None,
                'strikeouts_pitched': None,
                'whip': None,
                'salary': 17_000_000
            },
            # 新增更多球員數據
            {
                'id': 11,
                'name': 'Mookie Betts',
                'team': 'Los Angeles Dodgers',
                'position': 'OF',
                'jersey': '50',
                'age': 31,
                'batting_avg': 0.289,
                'home_runs': 39,
                'rbi': 107,
                'ops': 0.892,
                'stolen_bases': 16,
                'era': None,
                'wins': None,
                'strikeouts_pitched': None,
                'whip': None,
                'salary': 30_000_000
            },
            {
                'id': 12,
                'name': 'Francisco Lindor',
                'team': 'New York Mets',
                'position': 'SS',
                'jersey': '12',
                'age': 30,
                'batting_avg': 0.254,
                'home_runs': 33,
                'rbi': 98,
                'ops': 0.781,
                'stolen_bases': 29,
                'era': None,
                'wins': None,
                'strikeouts_pitched': None,
                'whip': None,
                'salary': 34_100_000
            },
            {
                'id': 13,
                'name': 'Corbin Burnes',
                'team': 'Milwaukee Brewers',
                'position': 'P',
                'jersey': '39',
                'age': 29,
                'batting_avg': None,
                'home_runs': None,
                'rbi': None,
                'ops': None,
                'stolen_bases': None,
                'era': 2.93,
                'wins': 10,
                'strikeouts_pitched': 200,
                'whip': 1.15,
                'salary': 10_010_000
            },
            {
                'id': 14,
                'name': 'Juan Soto',
                'team': 'New York Yankees',
                'position': 'OF',
                'jersey': '22',
                'age': 25,
                'batting_avg': 0.288,
                'home_runs': 41,
                'rbi': 109,
                'ops': 0.989,
                'stolen_bases': 7,
                'era': None,
                'wins': None,
                'strikeouts_pitched': None,
                'whip': None,
                'salary': 31_000_000
            },
            {
                'id': 15,
                'name': 'Freddie Freeman',
                'team': 'Los Angeles Dodgers',
                'position': '1B',
                'jersey': '5',
                'age': 35,
                'batting_avg': 0.331,
                'home_runs': 22,
                'rbi': 89,
                'ops': 0.903,
                'stolen_bases': 13,
                'era': None,
                'wins': None,
                'strikeouts_pitched': None,
                'whip': None,
                'salary': 27_000_000
            },
            {
                'id': 16,
                'name': 'Shane Bieber',
                'team': 'Cleveland Guardians',
                'position': 'P',
                'jersey': '57',
                'age': 29,
                'batting_avg': None,
                'home_runs': None,
                'rbi': None,
                'ops': None,
                'stolen_bases': None,
                'era': 2.41,
                'wins': 8,
                'strikeouts_pitched': 153,
                'whip': 0.98,
                'salary': 13_100_000
            },
            {
                'id': 17,
                'name': 'Pete Alonso',
                'team': 'New York Mets',
                'position': '1B',
                'jersey': '20',
                'age': 29,
                'batting_avg': 0.240,
                'home_runs': 46,
                'rbi': 118,
                'ops': 0.788,
                'stolen_bases': 3,
                'era': None,
                'wins': None,
                'strikeouts_pitched': None,
                'whip': None,
                'salary': 20_500_000
            },
            {
                'id': 18,
                'name': 'Kyle Schwarber',
                'team': 'Philadelphia Phillies',
                'position': 'OF/DH',
                'jersey': '12',
                'age': 31,
                'batting_avg': 0.197,
                'home_runs': 38,
                'rbi': 104,
                'ops': 0.765,
                'stolen_bases': 5,
                'era': None,
                'wins': None,
                'strikeouts_pitched': None,
                'whip': None,
                'salary': 20_000_000
            },
            {
                'id': 19,
                'name': 'Sandy Alcantara',
                'team': 'Miami Marlins',
                'position': 'P',
                'jersey': '22',
                'age': 29,
                'batting_avg': None,
                'home_runs': None,
                'rbi': None,
                'ops': None,
                'stolen_bases': None,
                'era': 4.14,
                'wins': 14,
                'strikeouts_pitched': 201,
                'whip': 1.31,
                'salary': 13_000_000
            },
            {
                'id': 20,
                'name': 'Bo Bichette',
                'team': 'Toronto Blue Jays',
                'position': 'SS',
                'jersey': '11',
                'age': 26,
                'batting_avg': 0.298,
                'home_runs': 20,
                'rbi': 73,
                'ops': 0.811,
                'stolen_bases': 25,
                'era': None,
                'wins': None,
                'strikeouts_pitched': None,
                'whip': None,
                'salary': 7_125_000
            }
        ]

class MLBPlayerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("⚾ 2025 MLB 球員數據查詢系統")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # 初始化數據庫
        self.db = MLBPlayerDatabase()
        self.current_players = self.db.players_data.copy()
        self.selected_player = None
        
        # 設定樣式
        self.setup_styles()
        
        # 建立主介面
        self.create_widgets()
        
        # 初始化顯示所有球員
        self.update_player_list()
    
    def setup_styles(self):
        """設定ttk樣式"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 自訂樣式
        self.style.configure('Title.TLabel', font=('Arial', 20, 'bold'), foreground='#2E4057')
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'), foreground='#2E4057')
        self.style.configure('Info.TLabel', font=('Arial', 10), foreground='#666666')
        self.style.configure('Custom.TButton', font=('Arial', 10, 'bold'))
    
    def create_widgets(self):
        """建立主要界面元件"""
        # 主標題
        title_frame = tk.Frame(self.root, bg='#2E4057', height=80)
        title_frame.pack(fill='x', pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="⚾ 2025 MLB 球員數據查詢系統", 
                              font=('Arial', 24, 'bold'), fg='white', bg='#2E4057')
        title_label.pack(expand=True)
        
        # 主容器
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=10)
        
        # 左側面板 - 搜尋和篩選
        left_panel = tk.Frame(main_container, bg='white', relief='raised', bd=1)
        left_panel.pack(side='left', fill='y', padx=(0, 10), pady=5)
        left_panel.configure(width=350)
        left_panel.pack_propagate(False)
        
        self.create_search_panel(left_panel)
        
        # 右側面板 - 結果顯示
        right_panel = tk.Frame(main_container, bg='white', relief='raised', bd=1)
        right_panel.pack(side='right', fill='both', expand=True, padx=(0, 0), pady=5)
        
        self.create_results_panel(right_panel)
        
        # 狀態列
        self.create_status_bar()
    
    def create_search_panel(self, parent):
        """建立搜尋面板"""
        # 搜尋標題
        search_title = tk.Label(parent, text="🔍 搜尋篩選", font=('Arial', 16, 'bold'), 
                               bg='white', fg='#2E4057')
        search_title.pack(pady=10)
        
        # 球員姓名搜尋
        name_frame = tk.Frame(parent, bg='white')
        name_frame.pack(fill='x', padx=15, pady=5)
        
        tk.Label(name_frame, text="球員姓名:", font=('Arial', 10, 'bold'), 
                bg='white').pack(anchor='w')
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(name_frame, textvariable=self.name_var, 
                                  font=('Arial', 10), width=30)
        self.name_entry.pack(fill='x', pady=2)
        self.name_entry.bind('<KeyRelease>', self.on_search_change)
        
        # 球隊篩選
        team_frame = tk.Frame(parent, bg='white')
        team_frame.pack(fill='x', padx=15, pady=5)
        
        tk.Label(team_frame, text="選擇球隊:", font=('Arial', 10, 'bold'), 
                bg='white').pack(anchor='w')
        self.team_var = tk.StringVar()
        teams = ['全部'] + sorted(list(set(p['team'] for p in self.db.players_data)))
        self.team_combo = ttk.Combobox(team_frame, textvariable=self.team_var, 
                                      values=teams, state='readonly', font=('Arial', 10))
        self.team_combo.set('全部')
        self.team_combo.pack(fill='x', pady=2)
        self.team_combo.bind('<<ComboboxSelected>>', self.on_search_change)
        
        # 位置篩選
        position_frame = tk.Frame(parent, bg='white')
        position_frame.pack(fill='x', padx=15, pady=5)
        
        tk.Label(position_frame, text="守備位置:", font=('Arial', 10, 'bold'), 
                bg='white').pack(anchor='w')
        self.position_var = tk.StringVar()
        positions = ['全部', 'P', 'C', '1B', '2B', '3B', 'SS', 'OF', 'DH']
        self.position_combo = ttk.Combobox(position_frame, textvariable=self.position_var, 
                                         values=positions, state='readonly', font=('Arial', 10))
        self.position_combo.set('全部')
        self.position_combo.pack(fill='x', pady=2)
        self.position_combo.bind('<<ComboboxSelected>>', self.on_search_change)
        
        # 年薪範圍
        salary_frame = tk.Frame(parent, bg='white')
        salary_frame.pack(fill='x', padx=15, pady=5)
        
        tk.Label(salary_frame, text="年薪範圍:", font=('Arial', 10, 'bold'), 
                bg='white').pack(anchor='w')
        self.salary_var = tk.StringVar()
        salary_ranges = ['全部', '< 2000萬', '2000萬-3000萬', '3000萬-4000萬', '> 4000萬']
        self.salary_combo = ttk.Combobox(salary_frame, textvariable=self.salary_var, 
                                       values=salary_ranges, state='readonly', font=('Arial', 10))
        self.salary_combo.set('全部')
        self.salary_combo.pack(fill='x', pady=2)
        self.salary_combo.bind('<<ComboboxSelected>>', self.on_search_change)
        
        # 搜尋按鈕
        btn_frame = tk.Frame(parent, bg='white')
        btn_frame.pack(fill='x', padx=15, pady=20)
        
        search_btn = tk.Button(btn_frame, text="🔍 搜尋球員", font=('Arial', 11, 'bold'),
                              bg='#4CAF50', fg='white', relief='flat', pady=8,
                              command=self.search_players)
        search_btn.pack(fill='x', pady=2)
        
        clear_btn = tk.Button(btn_frame, text="🔄 清除篩選", font=('Arial', 10),
                             bg='#FF9800', fg='white', relief='flat', pady=6,
                             command=self.clear_filters)
        clear_btn.pack(fill='x', pady=2)
        
        # 統計資訊
        stats_frame = tk.LabelFrame(parent, text="📊 統計資訊", font=('Arial', 12, 'bold'),
                                   bg='white', fg='#2E4057', padx=10, pady=5)
        stats_frame.pack(fill='x', padx=15, pady=10)
        
        self.stats_label = tk.Label(stats_frame, text="", font=('Arial', 10),
                                   bg='white', fg='#666666', justify='left')
        self.stats_label.pack(anchor='w')
        
        # 快速篩選按鈕
        quick_frame = tk.LabelFrame(parent, text="⚡ 快速篩選", font=('Arial', 12, 'bold'),
                                   bg='white', fg='#2E4057', padx=5, pady=5)
        quick_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Button(quick_frame, text="🏏 所有打者", font=('Arial', 9),
                 bg='#2196F3', fg='white', relief='flat', pady=4,
                 command=self.show_batters).pack(fill='x', pady=1)
        
        tk.Button(quick_frame, text="⚾ 所有投手", font=('Arial', 9),
                 bg='#9C27B0', fg='white', relief='flat', pady=4,
                 command=self.show_pitchers).pack(fill='x', pady=1)
        
        tk.Button(quick_frame, text="💰 高薪球員", font=('Arial', 9),
                 bg='#FF5722', fg='white', relief='flat', pady=4,
                 command=self.show_high_salary).pack(fill='x', pady=1)
    
    def create_results_panel(self, parent):
        """建立結果顯示面板"""
        # 建立筆記本(分頁)控制項
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 球員列表分頁
        self.create_player_list_tab()
        
        # 球員詳細資訊分頁
        self.create_player_detail_tab()
        
        # 統計排行分頁
        self.create_statistics_tab()
    
    def create_player_list_tab(self):
        """建立球員列表分頁"""
        list_frame = ttk.Frame(self.notebook)
        self.notebook.add(list_frame, text="📋 球員列表")
        
        # 工具列
        toolbar = tk.Frame(list_frame, bg='#f8f9fa', height=40)
        toolbar.pack(fill='x', pady=(0, 5))
        toolbar.pack_propagate(False)
        
        # 結果計數
        self.result_label = tk.Label(toolbar, text="", font=('Arial', 10, 'bold'),
                                    bg='#f8f9fa', fg='#2E4057')
        self.result_label.pack(side='left', padx=10, pady=8)
        
        # 匯出按鈕
        export_btn = tk.Button(toolbar, text="💾 匯出 CSV", font=('Arial', 9),
                              bg='#17a2b8', fg='white', relief='flat',
                              command=self.export_csv)
        export_btn.pack(side='right', padx=10, pady=5)
        
        # 建立Treeview
        columns = ('name', 'team', 'position', 'age', 'salary')
        self.player_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # 設定標題
        self.player_tree.heading('name', text='球員姓名')
        self.player_tree.heading('team', text='球隊')
        self.player_tree.heading('position', text='位置')
        self.player_tree.heading('age', text='年齡')
        self.player_tree.heading('salary', text='年薪(百萬)')
        
        # 設定欄寬
        self.player_tree.column('name', width=150, anchor='w')
        self.player_tree.column('team', width=200, anchor='w')
        self.player_tree.column('position', width=80, anchor='center')
        self.player_tree.column('age', width=60, anchor='center')
        self.player_tree.column('salary', width=100, anchor='e')
        
        # 綁定選擇事件
        self.player_tree.bind('<<TreeviewSelect>>', self.on_player_select)
        self.player_tree.bind('<Double-1>', self.on_double_click)
        
        # 滾動條
        tree_scroll = ttk.Scrollbar(list_frame, orient='vertical', command=self.player_tree.yview)
        self.player_tree.configure(yscrollcommand=tree_scroll.set)
        
        # 包裝樹視圖和滾動條
        tree_frame = tk.Frame(list_frame)
        tree_frame.pack(fill='both', expand=True)
        
        self.player_tree.pack(side='left', fill='both', expand=True)
        tree_scroll.pack(side='right', fill='y')
    
    def create_player_detail_tab(self):
        """建立球員詳細資訊分頁"""
        detail_frame = ttk.Frame(self.notebook)
        self.notebook.add(detail_frame, text="👤 球員詳情")
        
        # 建立滾動區域
        canvas = tk.Canvas(detail_frame, bg='white')
        scrollbar = ttk.Scrollbar(detail_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 球員詳細資訊容器
        self.detail_container = scrollable_frame
        
        # 初始提示
        self.no_selection_label = tk.Label(self.detail_container, 
                                          text="請從球員列表中選擇一位球員查看詳細資訊", 
                                          font=('Arial', 14), fg='#666666')
        self.no_selection_label.pack(expand=True, pady=50)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_statistics_tab(self):
        """建立統計排行分頁"""
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="📊 統計排行")
        
        # 建立子分頁
        stats_notebook = ttk.Notebook(stats_frame)
        stats_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 打擊排行
        self.create_batting_stats(stats_notebook)
        
        # 投球排行
        self.create_pitching_stats(stats_notebook)
        
        # 年薪排行
        self.create_salary_stats(stats_notebook)
    
    def create_batting_stats(self, parent):
        """建立打擊統計"""
        batting_frame = ttk.Frame(parent)
        parent.add(batting_frame, text="🏏 打擊排行")
        
        # 取得打者數據
        batters = [p for p in self.db.players_data if p['batting_avg'] is not None]
        
        # 全壘打王
        hr_frame = tk.LabelFrame(batting_frame, text="🏆 全壘打王", font=('Arial', 12, 'bold'),
                                fg='#2E4057', padx=10, pady=5)
        hr_frame.pack(fill='x', padx=10, pady=5)
        
        hr_leaders = sorted(batters, key=lambda x: x['home_runs'], reverse=True)[:5]
        for i, player in enumerate(hr_leaders, 1):
            text = f"{i}. {player['name']} - {player['team']} ({player['home_runs']} 支)"
            tk.Label(hr_frame, text=text, font=('Arial', 10), anchor='w').pack(fill='x')
        
        # 打擊率王
        avg_frame = tk.LabelFrame(batting_frame, text="🏆 打擊率王", font=('Arial', 12, 'bold'),
                                 fg='#2E4057', padx=10, pady=5)
        avg_frame.pack(fill='x', padx=10, pady=5)
        
        avg_leaders = sorted(batters, key=lambda x: x['batting_avg'], reverse=True)[:5]
        for i, player in enumerate(avg_leaders, 1):
            text = f"{i}. {player['name']} - {player['team']} ({player['batting_avg']:.3f})"
            tk.Label(avg_frame, text=text, font=('Arial', 10), anchor='w').pack(fill='x')
        
        # 打點王
        rbi_frame = tk.LabelFrame(batting_frame, text="🏆 打點王", font=('Arial', 12, 'bold'),
                                 fg='#2E4057', padx=10, pady=5)
        rbi_frame.pack(fill='x', padx=10, pady=5)
        
        rbi_leaders = sorted(batters, key=lambda x: x['rbi'], reverse=True)[:5]
        for i, player in enumerate(rbi_leaders, 1):
            text = f"{i}. {player['name']} - {player['team']} ({player['rbi']} 分)"
            tk.Label(rbi_frame, text=text, font=('Arial', 10), anchor='w').pack(fill='x')
    
    def create_pitching_stats(self, parent):
        """建立投球統計"""
        pitching_frame = ttk.Frame(parent)
        parent.add(pitching_frame, text="⚾ 投手排行")
        
        # 取得投手數據
        pitchers = [p for p in self.db.players_data if p['era'] is not None]
        
        # 防禦率王
        era_frame = tk.LabelFrame(pitching_frame, text="🏆 防禦率王", font=('Arial', 12, 'bold'),
                                 fg='#2E4057', padx=10, pady=5)
        era_frame.pack(fill='x', padx=10, pady=5)
        
        era_leaders = sorted(pitchers, key=lambda x: x['era'])[:5]
        for i, player in enumerate(era_leaders, 1):
            text = f"{i}. {player['name']} - {player['team']} ({player['era']:.2f})"
            tk.Label(era_frame, text=text, font=('Arial', 10), anchor='w').pack(fill='x')
        
        # 勝投王
        wins_frame = tk.LabelFrame(pitching_frame, text="🏆 勝投王", font=('Arial', 12, 'bold'),
                                  fg='#2E4057', padx=10, pady=5)
        wins_frame.pack(fill='x', padx=10, pady=5)
        
        win_leaders = sorted(pitchers, key=lambda x: x['wins'], reverse=True)[:5]
        for i, player in enumerate(win_leaders, 1):
            text = f"{i}. {player['name']} - {player['team']} ({player['wins']} 勝)"
            tk.Label(wins_frame, text=text, font=('Arial', 10), anchor='w').pack(fill='x')
        
        # 三振王
        k_frame = tk.LabelFrame(pitching_frame, text="🏆 三振王", font=('Arial', 12, 'bold'),
                               fg='#2E4057', padx=10, pady=5)
        k_frame.pack(fill='x', padx=10, pady=5)
        
        k_leaders = sorted(pitchers, key=lambda x: x['strikeouts_pitched'], reverse=True)[:5]
        for i, player in enumerate(k_leaders, 1):
            text = f"{i}. {player['name']} - {player['team']} ({player['strikeouts_pitched']} 次)"
            tk.Label(k_frame, text=text, font=('Arial', 10), anchor='w').pack(fill='x')
    
    def create_salary_stats(self, parent):
        """建立年薪統計"""
        salary_frame = ttk.Frame(parent)
        parent.add(salary_frame, text="💰 年薪排行")
        
        # 年薪排行榜
        salary_rank_frame = tk.LabelFrame(salary_frame, text="💰 年薪排行榜", 
                                         font=('Arial', 12, 'bold'), fg='#2E4057', 
                                         padx=10, pady=5)
        salary_rank_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        salary_leaders = sorted(self.db.players_data, key=lambda x: x['salary'], reverse=True)
        for i, player in enumerate(salary_leaders, 1):
            salary_mil = player['salary'] / 1_000_000
            text = f"{i:2d}. {player['name']:<20} - {player['team']:<25} (${salary_mil:>6.1f}M)"
            label = tk.Label(salary_rank_frame, text=text, font=('Courier', 10), anchor='w')
            label.pack(fill='x')
            
            # 高亮前三名
            if i <= 3:
                colors = ['#FFD700', '#C0C0C0', '#CD7F32']  # 金、銀、銅
                label.configure(bg=colors[i-1], fg='black')
        
        # 統計摘要
        summary_frame = tk.LabelFrame(salary_frame, text="📈 薪資統計", 
                                     font=('Arial', 12, 'bold'), fg='#2E4057', 
                                     padx=10, pady=5)
        summary_frame.pack(fill='x', padx=10, pady=5)
        
        total_salary = sum(p['salary'] for p in self.db.players_data) / 1_000_000
        avg_salary = total_salary / len(self.db.players_data)
        max_salary = max(p['salary'] for p in self.db.players_data) / 1_000_000
        min_salary = min(p['salary'] for p in self.db.players_data) / 1_000_000
        
        tk.Label(summary_frame, text=f"總薪資: ${total_salary:.1f}M", 
                font=('Arial', 11), anchor='w').pack(fill='x')
        tk.Label(summary_frame, text=f"平均薪資: ${avg_salary:.1f}M", 
                font=('Arial', 11), anchor='w').pack(fill='x')
        tk.Label(summary_frame, text=f"最高薪資: ${max_salary:.1f}M", 
                font=('Arial', 11), anchor='w').pack(fill='x')
        tk.Label(summary_frame, text=f"最低薪資: ${min_salary:.1f}M", 
                font=('Arial', 11), anchor='w').pack(fill='x')
    
    def create_status_bar(self):
        """建立狀態列"""
        self.status_frame = tk.Frame(self.root, bg='#34495e', height=25)
        self.status_frame.pack(fill='x', side='bottom')
        self.status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar()
        self.status_var.set("準備就緒")
        self.status_label = tk.Label(self.status_frame, textvariable=self.status_var, 
                                    bg='#34495e', fg='white', font=('Arial', 9))
        self.status_label.pack(side='left', padx=10, pady=2)
        
        # 時間顯示
        self.update_time()
    
    def update_time(self):
        """更新時間顯示"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time_label = tk.Label(self.status_frame, text=current_time, 
                             bg='#34495e', fg='white', font=('Arial', 9))
        time_label.pack(side='right', padx=10, pady=2)
        
        # 每秒更新時間
        self.root.after(1000, self.update_time)
    
    def on_search_change(self, event=None):
        """搜尋條件改變時的處理"""
        self.search_players()
    
    def search_players(self):
        """執行球員搜尋"""
        self.status_var.set("搜尋中...")
        
        # 取得搜尋條件
        name = self.name_var.get().strip().lower()
        team = self.team_var.get()
        position = self.position_var.get()
        salary_range = self.salary_var.get()
        
        # 篩選球員
        filtered_players = []
        for player in self.db.players_data:
            # 姓名篩選
            if name and name not in player['name'].lower():
                continue
            
            # 球隊篩選
            if team != '全部' and player['team'] != team:
                continue
            
            # 位置篩選
            if position != '全部' and position not in player['position']:
                continue
            
            # 年薪篩選
            if salary_range != '全部':
                salary = player['salary']
                if salary_range == '< 2000萬' and salary >= 20_000_000:
                    continue
                elif salary_range == '2000萬-3000萬' and not (20_000_000 <= salary < 30_000_000):
                    continue
                elif salary_range == '3000萬-4000萬' and not (30_000_000 <= salary < 40_000_000):
                    continue
                elif salary_range == '> 4000萬' and salary < 40_000_000:
                    continue
            
            filtered_players.append(player)
        
        self.current_players = filtered_players
        self.update_player_list()
        self.update_statistics()
    
    def clear_filters(self):
        """清除所有篩選條件"""
        self.name_var.set("")
        self.team_var.set("全部")
        self.position_var.set("全部")
        self.salary_var.set("全部")
        self.current_players = self.db.players_data.copy()
        self.update_player_list()
        self.update_statistics()
        self.status_var.set("已清除所有篩選條件")
    
    def show_batters(self):
        """顯示所有打者"""
        self.current_players = [p for p in self.db.players_data if p['batting_avg'] is not None]
        self.update_player_list()
        self.update_statistics()
        self.status_var.set("顯示所有打者")
    
    def show_pitchers(self):
        """顯示所有投手"""
        self.current_players = [p for p in self.db.players_data if p['era'] is not None]
        self.update_player_list()
        self.update_statistics()
        self.status_var.set("顯示所有投手")
    
    def show_high_salary(self):
        """顯示高薪球員(>3000萬)"""
        self.current_players = [p for p in self.db.players_data if p['salary'] > 30_000_000]
        self.update_player_list()
        self.update_statistics()
        self.status_var.set("顯示高薪球員")
    
    def update_player_list(self):
        """更新球員列表顯示"""
        # 清除現有項目
        for item in self.player_tree.get_children():
            self.player_tree.delete(item)
        
        # 添加球員到列表
        for player in self.current_players:
            salary_mil = player['salary'] / 1_000_000
            self.player_tree.insert('', 'end', values=(
                player['name'],
                player['team'],
                player['position'],
                player['age'],
                f"${salary_mil:.1f}M"
            ))
        
        # 更新結果計數
        self.result_label.config(text=f"找到 {len(self.current_players)} 位球員")
        self.status_var.set(f"顯示 {len(self.current_players)} 位球員")
    
    def update_statistics(self):
        """更新統計資訊"""
        if not self.current_players:
            self.stats_label.config(text="無數據")
            return
        
        total_players = len(self.current_players)
        batters = len([p for p in self.current_players if p['batting_avg'] is not None])
        pitchers = len([p for p in self.current_players if p['era'] is not None])
        avg_age = sum(p['age'] for p in self.current_players) / total_players
        avg_salary = sum(p['salary'] for p in self.current_players) / total_players / 1_000_000
        
        stats_text = f"""總球員數: {total_players}
打者: {batters} 位
投手: {pitchers} 位
平均年齡: {avg_age:.1f} 歲
平均年薪: ${avg_salary:.1f}M"""
        
        self.stats_label.config(text=stats_text)
    
    def on_player_select(self, event):
        """處理球員選擇事件"""
        selection = self.player_tree.selection()
        if selection:
            item = selection[0]
            player_name = self.player_tree.item(item, 'values')[0]
            
            # 找到對應的球員數據
            for player in self.current_players:
                if player['name'] == player_name:
                    self.selected_player = player
                    self.show_player_detail()
                    break
    
    def on_double_click(self, event):
        """雙擊事件 - 切換到詳情頁面"""
        if self.selected_player:
            self.notebook.select(1)  # 切換到詳情分頁
    
    def show_player_detail(self):
        """顯示選中球員的詳細資訊"""
        if not self.selected_player:
            return
        
        # 清除現有內容
        for widget in self.detail_container.winfo_children():
            widget.destroy()
        
        player = self.selected_player
        
        # 球員頭像區域 (模擬)
        header_frame = tk.Frame(self.detail_container, bg='#2E4057', height=100)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # 球員基本資訊
        player_name = tk.Label(header_frame, text=player['name'], 
                              font=('Arial', 24, 'bold'), fg='white', bg='#2E4057')
        player_name.pack(pady=10)
        
        team_info = tk.Label(header_frame, text=f"{player['team']} | #{player['jersey']} | {player['position']}", 
                            font=('Arial', 14), fg='#ecf0f1', bg='#2E4057')
        team_info.pack()
        
        # 基本資訊卡片
        basic_frame = tk.LabelFrame(self.detail_container, text="📋 基本資訊", 
                                   font=('Arial', 14, 'bold'), fg='#2E4057', 
                                   padx=20, pady=10)
        basic_frame.pack(fill='x', padx=20, pady=10)
        
        basic_info = tk.Frame(basic_frame)
        basic_info.pack(fill='x')
        
        # 左側基本資訊
        left_basic = tk.Frame(basic_info)
        left_basic.pack(side='left', fill='both', expand=True)
        
        tk.Label(left_basic, text=f"年齡: {player.get('age', 'N/A')} 歲", 
                font=('Arial', 12), anchor='w').pack(fill='x', pady=2)
        tk.Label(left_basic, text=f"守備位置: {player['position']}", 
                font=('Arial', 12), anchor='w').pack(fill='x', pady=2)
        if player.get('height'):
            tk.Label(left_basic, text=f"身高體重: {player['height']} / {player.get('weight', 'N/A')}lbs", 
                    font=('Arial', 12), anchor='w').pack(fill='x', pady=2)
        
        # 右側基本資訊
        right_basic = tk.Frame(basic_info)
        right_basic.pack(side='right', fill='both', expand=True)
        
        tk.Label(right_basic, text=f"球衣號碼: #{player.get('jersey', 'N/A')}", 
                font=('Arial', 12), anchor='w').pack(fill='x', pady=2)
        if player.get('bats') and player.get('throws'):
            tk.Label(right_basic, text=f"打擊/投球: {player['bats']}/{player['throws']}", 
                    font=('Arial', 12), anchor='w').pack(fill='x', pady=2)
        
        if player.get('salary'):
            salary_mil = player['salary'] / 1_000_000
            tk.Label(right_basic, text=f"年薪: ${salary_mil:.1f}M", 
                    font=('Arial', 12, 'bold'), fg='#27ae60', anchor='w').pack(fill='x', pady=2)
        else:
            tk.Label(right_basic, text="年薪: 資料未提供", 
                    font=('Arial', 12), fg='#7f8c8d', anchor='w').pack(fill='x', pady=2)
        
        # 打擊數據卡片
        if player['batting_avg'] is not None:
            batting_frame = tk.LabelFrame(self.detail_container, text="🏏 打擊數據", 
                                         font=('Arial', 14, 'bold'), fg='#2E4057', 
                                         padx=20, pady=10)
            batting_frame.pack(fill='x', padx=20, pady=10)
            
            batting_info = tk.Frame(batting_frame)
            batting_info.pack(fill='x')
            
            # 打擊數據 - 左側
            left_batting = tk.Frame(batting_info)
            left_batting.pack(side='left', fill='both', expand=True)
            
            tk.Label(left_batting, text=f"打擊率: {player['batting_avg']:.3f}", 
                    font=('Arial', 12, 'bold'), fg='#e74c3c', anchor='w').pack(fill='x', pady=2)
            tk.Label(left_batting, text=f"全壘打: {player['home_runs']} 支", 
                    font=('Arial', 12), anchor='w').pack(fill='x', pady=2)
            tk.Label(left_batting, text=f"打點: {player['rbi']} 分", 
                    font=('Arial', 12), anchor='w').pack(fill='x', pady=2)
            
            # 打擊數據 - 右側
            right_batting = tk.Frame(batting_info)
            right_batting.pack(side='right', fill='both', expand=True)
            
            tk.Label(right_batting, text=f"OPS: {player['ops']:.3f}", 
                    font=('Arial', 12, 'bold'), fg='#8e44ad', anchor='w').pack(fill='x', pady=2)
            tk.Label(right_batting, text=f"盜壘: {player['stolen_bases']} 次", 
                    font=('Arial', 12), anchor='w').pack(fill='x', pady=2)
            
            # 打擊等級評估
            self.add_batting_rating(batting_frame, player)
        
        # 投球數據卡片
        if player['era'] is not None:
            pitching_frame = tk.LabelFrame(self.detail_container, text="⚾ 投球數據", 
                                          font=('Arial', 14, 'bold'), fg='#2E4057', 
                                          padx=20, pady=10)
            pitching_frame.pack(fill='x', padx=20, pady=10)
            
            pitching_info = tk.Frame(pitching_frame)
            pitching_info.pack(fill='x')
            
            # 投球數據 - 左側
            left_pitching = tk.Frame(pitching_info)
            left_pitching.pack(side='left', fill='both', expand=True)
            
            tk.Label(left_pitching, text=f"防禦率: {player['era']:.2f}", 
                    font=('Arial', 12, 'bold'), fg='#e74c3c', anchor='w').pack(fill='x', pady=2)
            tk.Label(left_pitching, text=f"勝場: {player['wins']} 勝", 
                    font=('Arial', 12), anchor='w').pack(fill='x', pady=2)
            
            # 投球數據 - 右側
            right_pitching = tk.Frame(pitching_info)
            right_pitching.pack(side='right', fill='both', expand=True)
            
            tk.Label(right_pitching, text=f"三振: {player['strikeouts_pitched']} 次", 
                    font=('Arial', 12), anchor='w').pack(fill='x', pady=2)
            tk.Label(right_pitching, text=f"WHIP: {player['whip']:.2f}", 
                    font=('Arial', 12, 'bold'), fg='#8e44ad', anchor='w').pack(fill='x', pady=2)
            
            # 投球等級評估
            self.add_pitching_rating(pitching_frame, player)
        
        # 操作按鈕
        button_frame = tk.Frame(self.detail_container)
        button_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Button(button_frame, text="📊 詳細統計", font=('Arial', 11, 'bold'),
                 bg='#3498db', fg='white', relief='flat', pady=8,
                 command=self.show_detailed_stats).pack(side='left', padx=5, fill='x', expand=True)
        
        tk.Button(button_frame, text="📈 表現趨勢", font=('Arial', 11, 'bold'),
                 bg='#9b59b6', fg='white', relief='flat', pady=8,
                 command=self.show_performance_trend).pack(side='left', padx=5, fill='x', expand=True)
    
    def add_batting_rating(self, parent, player):
        """添加打擊評級"""
        rating_frame = tk.Frame(parent)
        rating_frame.pack(fill='x', pady=(10, 0))
        
        tk.Label(rating_frame, text="🏆 打擊評級:", font=('Arial', 11, 'bold')).pack(side='left')
        
        # 簡單的評級系統
        avg = player['batting_avg']
        hr = player['home_runs']
        ops = player['ops']
        
        if avg >= 0.300 and hr >= 30 and ops >= 0.900:
            rating = "⭐⭐⭐⭐⭐ MVP級別"
            color = '#f39c12'
        elif avg >= 0.280 and hr >= 25 and ops >= 0.850:
            rating = "⭐⭐⭐⭐ 明星級別"
            color = '#e74c3c'
        elif avg >= 0.250 and hr >= 20:
            rating = "⭐⭐⭐ 優秀"
            color = '#27ae60'
        elif avg >= 0.230:
            rating = "⭐⭐ 良好"
            color = '#3498db'
        else:
            rating = "⭐ 普通"
            color = '#95a5a6'
        
        tk.Label(rating_frame, text=rating, font=('Arial', 11, 'bold'), 
                fg=color).pack(side='left', padx=10)
    
    def add_pitching_rating(self, parent, player):
        """添加投球評級"""
        rating_frame = tk.Frame(parent)
        rating_frame.pack(fill='x', pady=(10, 0))
        
        tk.Label(rating_frame, text="🏆 投球評級:", font=('Arial', 11, 'bold')).pack(side='left')
        
        # 簡單的評級系統
        era = player['era']
        wins = player['wins']
        k = player['strikeouts_pitched']
        
        if era <= 2.50 and wins >= 12 and k >= 180:
            rating = "⭐⭐⭐⭐⭐ 賽揚獎級別"
            color = '#f39c12'
        elif era <= 3.00 and wins >= 10 and k >= 150:
            rating = "⭐⭐⭐⭐ 明星級別"
            color = '#e74c3c'
        elif era <= 3.50 and wins >= 8:
            rating = "⭐⭐⭐ 優秀"
            color = '#27ae60'
        elif era <= 4.00:
            rating = "⭐⭐ 良好"
            color = '#3498db'
        else:
            rating = "⭐ 普通"
            color = '#95a5a6'
        
        tk.Label(rating_frame, text=rating, font=('Arial', 11, 'bold'), 
                fg=color).pack(side='left', padx=10)
    
    def show_detailed_stats(self):
        """顯示詳細統計 (模擬)"""
        if not self.selected_player:
            return
        
        messagebox.showinfo("詳細統計", 
                           f"{self.selected_player['name']} 的詳細統計功能正在開發中...")
    
    def show_performance_trend(self):
        """顯示表現趨勢 (模擬)"""
        if not self.selected_player:
            return
        
        messagebox.showinfo("表現趨勢", 
                           f"{self.selected_player['name']} 的表現趨勢分析功能正在開發中...")
    
    def export_csv(self):
        """匯出CSV檔案"""
        if not self.current_players:
            messagebox.showwarning("警告", "沒有數據可以匯出！")
            return
        
        # 選擇儲存位置
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="儲存CSV檔案",
            initialname=f"mlb_players_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    fieldnames = ['姓名', '球隊', '位置', '球衣號碼', '年齡', '年薪', 
                                 '打擊率', '全壘打', '打點', 'OPS', '盜壘', 
                                 '防禦率', '勝場', '三振', 'WHIP']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for player in self.current_players:
                        writer.writerow({
                            '姓名': player['name'],
                            '球隊': player['team'],
                            '位置': player['position'],
                            '球衣號碼': player['jersey'],
                            '年齡': player['age'],
                            '年薪': player['salary'],
                            '打擊率': player['batting_avg'] if player['batting_avg'] is not None else '',
                            '全壘打': player['home_runs'] if player['home_runs'] is not None else '',
                            '打點': player['rbi'] if player['rbi'] is not None else '',
                            'OPS': player['ops'] if player['ops'] is not None else '',
                            '盜壘': player['stolen_bases'] if player['stolen_bases'] is not None else '',
                            '防禦率': player['era'] if player['era'] is not None else '',
                            '勝場': player['wins'] if player['wins'] is not None else '',
                            '三振': player['strikeouts_pitched'] if player['strikeouts_pitched'] is not None else '',
                            'WHIP': player['whip'] if player['whip'] is not None else ''
                        })
                
                messagebox.showinfo("成功", f"已成功匯出 {len(self.current_players)} 筆記錄到 {filename}")
                self.status_var.set(f"已匯出 {len(self.current_players)} 筆記錄")
                
            except Exception as e:
                messagebox.showerror("錯誤", f"匯出失敗: {str(e)}")

def main():
    """主程式進入點"""
    root = tk.Tk()
    
    # 設定應用程式圖示和屬性
    try:
        root.iconbitmap('baseball.ico')  # 如果有圖示檔案的話
    except:
        pass
    
    # 建立應用程式
    app = MLBPlayerGUI(root)
    
    # 啟動主迴圈
    root.mainloop()

if __name__ == "__main__":
    main()