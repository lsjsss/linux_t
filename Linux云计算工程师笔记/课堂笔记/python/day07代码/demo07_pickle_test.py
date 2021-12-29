## 练习 6：记账程序
# 需求
# - 假设在记账时，有一万元钱
# - 无论是开销还是收入都要进行记账
# - 记账内容包括时间、金额,余额和说明等
# - 记账数据要求永久存储(数据落盘)
import os,pickle,time
def save(fname):  # yue=init_data[-1][-2]+100
    # [
    #   ["2021-10-22", 0, 0, 10000, "xxx"],
    #   ["2021-10-22", 20, 0, 10020, "xxx"]
    # ]
    # ["2021-10-22", 100, 0, 10120, "lianhong"]
    date = time.strftime("%Y-%m-%d")
    amount = int(input("save: "))
    with open(fname, mode="rb") as fr:
        content = pickle.load(fr)  # 取账本大列表
    yue = content[-1][-2] + amount  # 求此时的余额
    log = input("log: ")
    line = [date, amount, 0, yue, log]
    content.append(line)  # 添加新数据到账本
    # 将修改后的账本列表重新写入文件 pickle.dump(..)
    with open(fname, mode="wb") as fw:
        pickle.dump(content, fw)
def cost(fname):
    date = time.strftime("%Y-%m-%d")
    amount = int(input("cost: "))
    with open(fname, mode="rb") as fr:
        content = pickle.load(fr)  # 取账本大列表
    yue = content[-1][-2] - amount  # 求此时的余额
    log = input("log: ")
    line = [date, 0, amount, yue, log]
    content.append(line)  # 添加新数据到账本
    # 将修改后的账本列表重新写入文件 pickle.dump(..)
    with open(fname, mode="wb") as fw:
        pickle.dump(content, fw)
def query(fname):
    with open(fname, mode="rb") as fr:
        content = pickle.load(fr)  # 取出账本大列表
    for line in content:
        print("*" * 30)
        print(line)
        print("*" * 30)
def ui():
    cmds = {"0": save, "1": cost, "2": query}
    prompt = """(0) save
(1) cost
(2) query
(3) exit
Please enter your choice(0/1/2/3): """
    fname = "/tmp/account.data"  # 账本存放路径
    init_data = [  # 账本初始化数据
        ["2021-10-21", 0, 0, 10000, "init data"]
        # 时间、      收入，开销，余额，    备注
        # ["2021-10-22", 100, 0, 10100,"lianhong"]
    ]
    if not os.path.exists(fname):  # 文件不存在
        # 将初始化列表写入账本
        with open(fname, mode="wb") as fwb:
            pickle.dump(init_data, fwb)
    while True:
        choice = input(prompt).strip()#提醒用户输入
        if choice not in ["0", "1", "2", "3"]:
            print("无效选择，请重试~")
            continue
        if choice == "3":
            print("Byebye!")
            break
        cmds[choice](fname)  # 函数的调用
if __name__ == '__main__':
    ui()



