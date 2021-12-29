### 练习 1：判断合法用户
# **需求**
# 1. 创建 login2.py 文件
# 2. 提示用户输入用户名和密码  15:10 上课
# 3. 获得到相关信息后，将其保存在变量中
# 4. 如果用户输的用户名为 bob，密码为 123456，
# 则输出 Login successful，否则输出 Login incorrect
username = input("username: ")
password = input("password: ")
if username == "bob" and password == "123456":
    print("Login successful")
else:
    print("Login incorrect")