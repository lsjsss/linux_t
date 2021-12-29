import subprocess
# 不需要加 shell=True, 不能够识别系统中的环境变量
# subprocess.run(["ls"])
# subprocess.run(["ls", "/home"])  # ls /home
# subprocess.run(["echo", "$HOME"])

# 需要加 shell=True, 能够识别系统中的环境变量
# subprocess.run("echo $HOME", shell=True)
res = subprocess.run(
    "id root;id zhangsan", shell=True,
    stdout=subprocess.PIPE, # 用stdout去接收正确输出
    stderr=subprocess.PIPE  # 用stderr去接收报错信息
)
# res: CompletedProcess(args='id root;id zhangsan', returncode=1, stdout=b'uid=0(root) gid=0(root) \xe7\xbb\x84=0(root)\n', stderr=b'id: \xe2\x80\x9czhangsan\xe2\x80\x9d\xef\xbc\x9a\xe6\x97\xa0\xe6\xad\xa4\xe7\x94\xa8\xe6\x88\xb7\n')
print(res.args)  # 打印执行的命令是什么
print(res.returncode)  # 打印最后一条命令的执行结果 0成功，非0失败
print(res.stdout.decode())# 正确命令的日志
print(res.stderr.decode())# 错误命令的日志
# 字节串.decode()  ->  字符串
# CompletedProcess(
#   args='id root;id zhangsan',
#   returncode=1,
#   stdout=b'uid=0(root) gid=0(root) \xe7\xbb\x84=0(root)\n',
#   stderr=b'id: \xe2\x80\x9czhangsan\xe2\x80\x9d\xef\xbc\x9a\xe6\x97\xa0\xe6\xad\xa4\xe7\x94\xa8\xe6\x88\xb7\n')