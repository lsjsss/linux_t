### 练习 4：自定义异常
# 需求
# 编写第一个函数，接收姓名和年龄
# 如果年龄不在1到150之间，产生ValueError异常
def get_info(name, age):
    if age < 1 or age > 150:
        raise ValueError("您是正常人嘛???")
    else:  # 打印用户信息
        print("name: %s, age: %s"%(name, age))
if __name__ == '__main__':
    get_info("nfx", 162)  # 自己加try处理


