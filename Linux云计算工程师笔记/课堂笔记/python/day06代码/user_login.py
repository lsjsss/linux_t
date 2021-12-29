### 练习 2：模拟用户登录信息系统
# 需求
# 1. 支持新用户注册，新用户名和密码注册到字典中
# 2. 支持老用户登陆，用户名和密码正确提示登陆成功
# 3. 主程序通过循环询问，进行何种操作，
#     根据用户的选择，执行注册或是登陆操作
user_db = {}  # {"zs": "123", "ls": "456" ...}
def register():
    username = input("username: ").strip()
    # 判断username这个key在不在字典当中
    if username != "" and username not in user_db:
        password = input("password: ")
        user_db[username] = password  # 添加用户数据
    else:
        print("用户名为空或已存在")
def login():
    username = input("username: ").strip()
    password = input("password: ")
    if (username not in user_db.keys()) or (user_db[username] != password):
        print("登陆失败")
    else:
        print("登陆成功")
def ui():
    prompt = """(0) register
(1) login
(2) exit
Please enter your choice(0/1/2): """
    cmds = {"0": register, "1": login}
    while True:
        choice = input(prompt)  # 用户的选择
        if choice not in ["0", "1", "2"]:
            print("Retry!!!")
            continue  # 让用户重新输入，执行下次循环
        if choice == "2":
            print("Bye-Bye~")
            break
        cmds[choice]()  # 注册或登录
if __name__ == '__main__':
    ui()