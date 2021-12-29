# 1. # ] cd /linux-soft/3/pypkgs/paramiko_pkgs
# 2. pip3 install *
# 3. 进入python交互环境
#    >>> import paramiko
#    >>>
# paramiko: 实现 SSH 的相关功能，
# 例如：要对服务器进行远程管理的操作，就需要使用此模块
import paramiko
# 声明创建远程连接的客户端
ssh = paramiko.SSHClient()
# 设置远程连接的提示, 提示'yes/no', 要选择yes的操作
ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy())
ssh.connect("127.0.0.1",  # host
            username="root",   # 用户名
            password="123456")  # 密码
res = ssh.exec_command("id root;id xxx")
# print(res[0])  # 输入
print(res[1].read().decode())  # 正确输出的结果
print(res[2].read().decode())  # 错误的输出结果
