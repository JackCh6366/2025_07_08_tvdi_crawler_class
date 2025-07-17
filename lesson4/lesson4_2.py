import time
from tracemalloc import start

def task(id,deley):
    print(f"開始任務{id}")
    time.sleep(deley)
    print(f"任務{id}完成")

start= time.time()
task(1,1)
task(2,2)
print(f"總共花費時間{time.time()-start}秒")