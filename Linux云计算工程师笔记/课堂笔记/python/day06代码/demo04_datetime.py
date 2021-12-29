# datetime时间对象
from datetime import datetime
t = datetime.now()  # 获取当前的系统时间
print(t)  # datetime(2021, 10, 21, 17, 44, 53, 99592)
print(t.year,t.month,t.day,t.hour,t.minute,t.second)
print(t.time())
print(t.today())  # 2021-10-21 17:49:09.475893
print(t.strftime("%Y/%m/%d"))  # datetime -> str
# str -> datetime
t1 = datetime.strptime("2021/10/21", "%Y/%m/%d")
print(t1) # datetime(2021, 10, 21, 0 , 0, 0, 0)
