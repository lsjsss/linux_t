## 练习 1：调用 ping 命令
# 需求   ping -c 2 xxxx &> /dev/null
# - 调用 ping 命令
#   - 编写 ping 函数
#   - 用于测试远程主机的联通性
#   - ping 通显示：x.x.x.x:up
#   - ping 不通显示：x.x.x.x:down
import subprocess
def ping(host):
    res = subprocess.run(
        "ping -c 2 " + host + " &> /dev/null",
        shell=True
    )  # ping -c 2 127.0.0.1 &>/dev/null
    if res.returncode == 0:  # 表示指令执行成功
        print(host + ": up")
    else:
        print(host + ": down")
if __name__ == '__main__':
    ping("www.baidu.com")