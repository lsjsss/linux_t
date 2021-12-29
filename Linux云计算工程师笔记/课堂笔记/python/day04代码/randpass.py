## 练习：生成随机密码
# **创建 randpass.py 脚本，要求如下：**
# 1. **编写一个能生成 8 位随机密码的函数**
#              数字(字符串)大小写字母
# 2. **使用 random 的 choice 函数随机取出字符**
# 3. **改进程序，用户可以自己决定生成多少位的密码**
import random,string
# all_chs = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
all_chs = string.ascii_letters + string.digits
def randpass(n=8):
    passwd = ""  # 用于保存最后的密码
    for i in range(n):
        ch = random.choice(all_chs) # 随机选择一个字符
        passwd += ch # 每次随机出来的字符进行拼接
    return passwd
if __name__ == "__name__":
    print(randpass(10))  # n = 10
    print(randpass())  # n = 8
