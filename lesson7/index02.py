#建立一個tkinter的基本樣板
#請使用物件導向的方式來建立一個簡單的GUI應用程式
import tkinter as tk
class SimpleApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x200")
        self.root.title("Simple GUI Application")
        self.create_widgets()

    def create_widgets(self):
        #建立一個標籤
        self.label = tk.Label(self.root, text="即時股票資料", font=("Arial", 16, "bold"))
        self.label.pack(pady=20)
        
        #建立一個按鈕
        
        self.button = tk.Button(self.root, text="股票查詢", command=self.on_button_click)
        self.button.pack(pady=10)

    def on_button_click(self):
        self.label.config(text="你已送出查詢!")
        self.label.config(fg="blue")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleApp(root)
    root.mainloop()