# 自定义异常
def input_password():
    # 1. 提示用户输入密码
    pwd = input("password: ")
    # 2. 判断用户输入密码的长度是不是>=8
    if len(pwd) >= 8:
        return pwd
    # 3. 不足8位, 向用户抛出异常
    # 3.1 自定义异常 Exception(用户报错信息)
    ex = Exception("密码不足8位请重新输入")
    # 3.2 抛出异常，让用户看到   raise 异常
    raise ex
if __name__ == '__main__':
    try:
        pwd = input_password()
        print(pwd)
    except Exception as e:
        print(e)  # 打印报错信息
