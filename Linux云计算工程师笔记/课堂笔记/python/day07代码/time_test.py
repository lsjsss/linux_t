## 练习 2：取出指定时间段的文本
# 需求
# 1. 有一日志文件，按时间先后顺序记录日志
# 2. 给定 时间范围[9~12点]，取出该范围内的日志
# 3. 自定义日志文件 /tmp/myweb.log
# /tmp/myweb.log
# [root@localhost day01]# vim /tmp/myweb.log
# 2030-01-02 08:01:43 aaaaaaaaaaaaaaaaa
# 2030-01-02 08:34:23 bbbbbbbbbbbbbbbbbbbb
# 2030-01-02 09:23:12 ccccccccccccccccccccc
# 2030-01-02 10:56:13 dddddddddddddddddddd
# 2030-01-02 11:38:19 eeeeeeeeeeeeeeee
# 2030-01-02 12:02:28 ffffffffffffffff
from datetime import datetime
# 1. 将9点和12点转换成datetime类型的数据
t9 = datetime.strptime("2030-01-02 09:00:00",
                  "%Y-%m-%d %H:%M:%S")
t12 = datetime.strptime("2030-01-02 12:00:00",
                  "%Y-%m-%d %H:%M:%S")
# 2. 通过切片获取日志文件时间字符串并转换成datetime
fr = open("/tmp/myweb.log", mode="r")
for line in fr.readlines():  # 10:10上课
    t = datetime.strptime(line[:19],
                      "%Y-%m-%d %H:%M:%S")
    if t > t12:  # 时间类型之间可以比较大小
        break
    if t >= t9:
        print(line, end="")
fr.close()
