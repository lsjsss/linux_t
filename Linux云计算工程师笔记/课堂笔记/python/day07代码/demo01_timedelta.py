# 时间计算 timedelta
from datetime import datetime
from datetime import timedelta
now = datetime.now()  # 创建当前时间的datetime
# 时间偏移量
delta = timedelta(days=2, hours=1, minutes=15)
future = now + delta
print(future)
old = now - delta
print(old)
