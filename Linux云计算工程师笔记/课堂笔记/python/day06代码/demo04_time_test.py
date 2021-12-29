### 练习 1：时间类型转换
import time
t = time.time()
# - t 减去1万秒，然后转换成 **UTC 结构化** 时间
print(time.gmtime(t - 10000))
# - t 减去1万秒，然后转换成 **中国本地结构化** 时间
temp = time.localtime(t - 10000)
# - 从本地结构化时间转换为时间戳
print(time.mktime(time.localtime()))
# - 从本地结构化时间转换为时间字符串
time_str=time.strftime("%Y/%m/%d %H:%M:%S", temp)
# - 从时间字符串转换为结构化时间
st = time.strptime(time_str, "%Y/%m/%d %H:%M:%S")
print(st)
