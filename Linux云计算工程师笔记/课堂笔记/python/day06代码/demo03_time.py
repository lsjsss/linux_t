# time
# 1. time.sleep(t): 表示程序暂停几秒后再执行
import time
def nfg():
    print("sheng...")
    time.sleep(5)  # 程序暂停五秒
    print("wuwuwu~~~")
# 2. time.time(): 返回当前系统时间戳.一般用于计算
print(time.time())
# 3. time.gmtime([secs]):将一个时间戳转换为UTC时区的结构化时间
#   secs默认值: time.time()
print(time.gmtime())
# 4. time.localtime([secs]):将一个时间戳转换为当前时区的结构化时间
#   secs默认值: time.time()
now = time.localtime()
print(now[3:5])
print(now.tm_mon)
# 5. time.mktime(t) 结构化时间 -> 时间戳
print(time.mktime(time.localtime()))
# 6. time.ctime([secs])把一个时间戳转化为本地时间的格式化字符串
#   secs默认值: time.time()
print(time.ctime())
# 7. time.asctime([t]): 结构化时间 -> 字符串
print(time.asctime(time.localtime()))
# 8. time.strftime(format[, t]) 结构化时间 -> 字符串
print(time.strftime("%Y/%m/%d %H:%M:%S"))
# 2021-10-21 16:30:34
# 9. time.strptime(string[, format])
#    字符串 -> 结构化时间
temp = time.strptime("2021-10-21 16:30:34",
              "%Y-%m-%d %H:%M:%S")
print(temp)
print(temp.tm_year)
# for i in temp:
#     print(i)
