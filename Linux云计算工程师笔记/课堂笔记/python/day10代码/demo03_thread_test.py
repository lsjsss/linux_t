#### 练习 1：扫描存活主机
# **需求：**
# 1. 通过 ping 测试主机是否可达
# 2. 如果 ping 不通，不管什么原因都认为主机不可用
# 3. 通过多线程方式实现并发扫描
import subprocess
import threading
def ping(host):
    res = subprocess.run(
        "ping -c 2 %s &> /dev/null" % host,
        shell=True
    )
    if res.returncode != 0:  # 失败
        print("%s: down" % host)
    else:  # 成功
        print("%s: up" % host)
if __name__ == '__main__':
    ips=["192.168.10.%s"%i for i in range(1, 255)]   # (1~254)
    for ip in ips:
        t = threading.Thread(target=ping,
                         args=(ip,))
        t.start()  # 干活
