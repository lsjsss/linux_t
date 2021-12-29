# 字符串函数去左
# 去除空格: lstrip()去左 rstrip()去右 strip()去左右
str01 = "   aaa  aa    "
print(str01.lstrip())
print(str01.rstrip())
print(str01.strip())
# 切割  split()
str02 = "abc.tar.gz"
res = str02.split(".")
print(res)  # ['abc', 'tar', 'gz']
str03 = "hello world"
res1 = str03.split()  # 默认以空格方式去切
print(res1)  # ["hello", "world"]
# 将列表当中的元素组合成一个字符串  join()
str04 = "_".join(["hello", "world"])
print(str04)
#### 练习 5：创建用户
# 需求
# - 编写一个程序，实现创建用户的功能  useradd xxx
# - 提示用户输入 用户名
# - 随机生成 8位密码 (导入之前的模块文件)
# - 创建用户并设置密码
#         echo passwd | passwd --stdin user
# - 将用户相关信息 写入指定文件(mode="a")
#      格式
# info = "用户名：%s   密码：%s" % (user, passwd)
