## 练习 1：用列表构建栈结构
# **需求**
# - 用列表构建 **栈结构**
#   - 栈是一个 **后进先出** 的结构
#   - 编写一个程序，用列表实现栈结构
#   - 需要支持 **压栈、出栈、查询** 功能
stack = []  # 用于模拟栈结构
def push_it():  # 数据入栈
    data = input("data: ").strip()
    if data != "":  # data不为空
        stack.append(data)
    else:  # data为空
        print("入栈的元素不能为空啊兄弟~")
def pop_it():   # 数据出栈
    if stack != []:  # 栈不为空的时候
        item = stack.pop()  # 弹出尾部元素并返回
        print("弹出的元素是: %s" % item)
    else:
        print("列表为空!!!")
def view_it():  # 查看栈结构
    print(stack)
def ui():
    prompt = """(0) push it
(1) pop it
(2) view it
(3) exit
Please enter your choice(0/1/2/3): """
    cmds = {"0":push_it,"1":pop_it,"2":view_it}
    while True:
        choice = input(prompt)
        if choice not in ["0", "1", "2", "3"]:
            print("非法操作，按要求重新输入！！！")
            continue  # 让用户重新输入
        if choice == "3":
            print("Bye-Bye~")
            break
        print(cmds[choice])
        cmds[choice]()  # cmds["0"](): push_it()
        # push_it()
if __name__ == '__main__':
    ui()

        # if choice == "0":
        #     push_it()
        # elif choice == "1":
        #     pop_it()
        # else:
        #     view_it()

