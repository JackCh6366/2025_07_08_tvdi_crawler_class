import time

def countdown(t):
    """
    這是一個簡單的倒數計時器函數。
    參數 t: 總秒數
    """
    while t:
        mins, secs = divmod(t, 60)
        timer = f'{mins:02d}:{secs:02d}'
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
    
    print('時間到！              ') # 多加空格以覆蓋上一行的時間

if __name__ == "__main__":
    try:
        # 要求使用者輸入秒數
        t = int(input("請輸入倒數計時的秒數："))
        
        # 檢查輸入是否為正數
        if t <= 0:
            print("請輸入一個大於 0 的秒數。")
        else:
            countdown(t)
    except ValueError:
        print("無效的輸入。請輸入一個整數。")