#### 练习 5：创建用户  add_user
# 需求  练习: 14:33
# - 编写一个程序(函数)，实现创建用户的功能  useradd xxx
# - 提示用户输入 用户名   ---> input
# - 随机生成 8位密码 (导入之前的模块文件)
# - 创建用户并设置密码
#         echo passwd | passwd --stdin user
# - 将用户相关信息 写入指定文件(mode="a", 追加写)
#      格式
# info = "用户名：%s   密码：%s" % (user, passwd)
import subprocess, randpass
def adduser(user, passwd, fname):
    # 1.判断用户名存不存在，不存在则创建
    res=subprocess.run("id %s &> /dev/null" % user,
                   shell=True)
    if res.returncode == 0:  # 0成功，非0失败
        print("用户名已存在~")
        return  # 相当于 return None
    # 2. 创建用户以及设置密码
    subprocess.run("useradd %s"%user, shell=True)
    # echo 123456 | passwd --stdin nfx
    subprocess.run(
        "echo %s|passwd --stdin %s"%(passwd,user),
        shell=True
    )  # 15:15上课
    # 3. 用户信息写入文件
    info = "user: %s, passwd: %s\n"%(user, passwd)
    fw = open(fname, mode="a")
    fw.write(info)
    fw.close()
if __name__ == '__main__':
    passwd = randpass.randpass()
    adduser("niufx102", passwd, "/tmp/user.data")
