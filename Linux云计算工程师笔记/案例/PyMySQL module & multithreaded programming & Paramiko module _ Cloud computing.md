@[TOC]( PyMySQL module & multithreaded programming & Paramiko module | Cloud computing )

---
# 1. 向表中添加数据
## 1.1 问题
1. 向employees表插入数据
2. 向salary表插入数据
3. 插入的数据需要commit到数据库中

## 1.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：PyMySQL安装**

1) 安装gcc，有些软件包是C的源码
```shell
[root@localhost ~]# yum install -y gcc
已加载插件：fastestmirror, langpacks
dvd                                                      | 3.6 kB     00:00     
Loading mirror speeds from cached hostfile
匹配 gcc-4.8.5-16.el7.x86_64 的软件包已经安装。正在检查更新。
无须任何处理
```
2)为了加速下载，可以使用国内开源镜像站点
```shell
[root@localhost ~]# mkdir ~/.pip
[root@localhost ~]# vim ~/.pip/pip.conf
[global]
index-url = http://pypi.douban.com/simple/
[install]
trusted-host=pypi.douban.com
```
3)安装pymysql
```shell
[root@localhost ~]# pip3 install pymysql
```
**步骤二：安装mariadb-server**
```shell
[root@localhost ~]# yum install –y mariadb-server
....
已安装：
        mariadb-server.x86_64 1:5.5.56-2.el7
作为依赖被安装：
        mariadb.x86_64 1:5.5.56-2.el7
        perl-DBD-MySQL. x86_64 0:4.023-5.el7
完毕！
[root@localhost ~]# systemctl start mariadb
[root@localhost ~]# systemctl enable mariadb
[root@localhost ~]# mysqladmin password tedu.cn
```
**步骤三：创建数据库**

1)创建数据库
```shell
[root@localhost ~]# mysql -uroot -ptedu.cn    
MariaDB [(none)]> CREATE DATABASE tedu DEFAULT CHARSET 'utf8';
Query OK, 1 row affected (0.00 sec)
```
2)创建部门表

部门表字段：部门ID、部门名称
```shell
MariaDB [(none)]> USE tedu;
Database changed
MariaDB [tedu]> CREATE TABLE departments(dep_id INT PRIMARY KEY, dep_name VARCHAR(20));
Query OK, 0 rows affected (0.04 sec)
```
3)创建员工表

员工表字段：员工编号、姓名、出生日期、部门ID、电话号码、email、引用外键id
```shell
MariaDB [tedu]> CREATE TABLE employees (emp_id INT PRIMARY KEY, emp_name VARCHAR(20) NOT NULL, birth_date DATE, phone CHAR(11), email VARCHAR(50), dep_id INT, FOREIGN KEY(dep_id) REFERENCES departments(dep_id));
Query OK, 0 rows affected (0.05 sec)
````
4)创建工资表

工资表字段：auto_id、员工编号、日期、基本工资、奖金、工资总和
```shell
MariaDB [tedu]> CREATE TABLE salary(auto_id INT AUTO_INCREMENT PRIMARY KEY, date DATE, emp_id INT, basic INT, awards INT, FOREIGN KEY(emp_id) REFERENCES employees(emp_id));
Query OK, 0 rows affected (0.05 sec)
```
**步骤四：向departments表插入数据**

1)新建insert_data.py文件，编写代码如下：
```shell
[root@localhost day10]# vim insert_data.py
import pymysql
1)连接数据库
conn = pymysql.connect(
    host='127.0.0.1',        #连接ip
    port=3306,            #端口号
    user='root',            #数据库用户名
    passwd='tedu.cn',        #数据库密码
    db='tedu',            #数据库名
    charset='utf8'        #设置了数据库的字符集
)
2)创建游标
cursor = conn.cursor()
3)向部门表departments中插入数据
insert1 = "INSERT INTO departments(dep_id, dep_name) VALUES(%s, %s)"
result = cursor.execute(insert1, (1, '人事部'))        # execute执行insert语句
4)将更新提交到数据库
conn.commit()    
5)关闭游标
cursor.close()
6)关闭数据库连接
conn.close()
```
2)执行insert_data.py文件：
```shell
[root@localhost day10]# python3 insert_data.py
```
3)登录mariadb查看结果：
```shell
MariaDB [tedu]>> select * from departments;
+--------+-----------+
| dep_id | dep_name  |
+--------+-----------+
|      1  |  人事部    |
+--------+-----------+
1 row in set (0.00 sec) 
```
4) 向部门表departments中插入数据还可以用如下方法：
```shell
#以上insert_data.py文件第3步可用如下代码替换：
insert1 = "INSERT INTO departments(dep_id, dep_name) VALUES(%s, %s)"
data = [(2, '运维部'), (3, '开发部')]
cursor.executemany(insert1, data)
```
mariadb查看结果如下：
```shell
MariaDB [tedu]>> select * from departments;
+--------+-----------+
| dep_id | dep_name  |
+--------+-----------+
|      1  |  人事部    |
|      2  |  运维部    |
|      3  |  开发部    |
+--------+-----------+
3 rows in set (0.01 sec)
```
**步骤五：向employees表插入数据**

1)新建insert_emp.py文件，编写代码如下：
```shell
[root@localhost day10]# vim insert_emp.py
import pymysql
1)连接数据库
conn = pymysql.connect(
    host='127.0.0.1',        #连接ip
    port=3306,            #端口号
    user='root',            #数据库用户名
    passwd='tedu.cn',        #数据库密码
    db='tedu',            #数据库名
    charset='utf8'        #设置了数据库的字符集
)
2)创建游标
cursor = conn.cursor()
3)向部门表employees中插入数据
insert1 = "INSERT INTO employees(emp_id, emp_name, birth_date,phone, email, dep_id) VALUES(%s, %s, %s, %s, %s, %s)"
result = cursor.execute(insert1, (1, '王君', '2018-9-30',\
 '15678789090', 'wj@163.com', 3))        # execute执行insert语句
4)将更新提交到数据库
conn.commit()    
5)关闭游标
cursor.close()
6)关闭数据库连接
conn.close()
```
2)执行insert_emp.py文件：
```shell
[root@localhost day10]# python3 insert_emp.py
```
3)登录mariadb查看结果：
```shell
MariaDB [tedu]>> select * from employees;
+--------+----------+------------+-------------+------------+--------+
| emp_id | emp_name | birth_date |  phone       | email      | dep_id |
+--------+----------+------------+-------------+------------+--------+
|      1  |    王君   | 2018-09-30 | 15678789090 | wj@163.com |      3 |
+--------+----------+------------+-------------+------------+--------+
 1 row in set (0.00 sec) 
```
4) 向部门表employees中插入数据还可以用如下方法：
```shell
#以上insert_emp.py文件第3步可用如下代码替换：
insert1 = "INSERT INTO employees (dep_id, dep_name) VALUES(%s, %s)"
data = [(2, '运维部'), (3, '开发部')]
cursor.executemany(insert1, data)
```
mariadb查看结果如下：
```shell
MariaDB [tedu]>> select * from departments;
+--------+----------+------------+-------------+------------+--------+
| emp_id | emp_name | birth_date |  phone       | email      | dep_id |
+--------+----------+------------+-------------+------------+--------+
|      1  |   王君    | 2018-09-30 | 15678789090 | wj@163.com |      3 |
|      2  |   李雷    | 2018-09-30 | 15678789090 | wj@163.com |      2 |
|      3  |   张美    | 2018-09-30 | 15678789090 | zm@163.com |      1 |
+--------+----------+------------+-------------+------------+--------+
3 rows in set (0.00 sec)
```
**步骤六：向salary表插入数据**

1)新建insert_sal.py文件，编写代码如下：
```shell
[root@localhost day10]# vim insert_sal.py
import pymysql
1)连接数据库
conn = pymysql.connect(
    host='127.0.0.1',        #连接ip
    port=3306,            #端口号
    user='root',            #数据库用户名
    passwd='tedu.cn',        #数据库密码
    db='tedu',            #数据库名
    charset='utf8'        #设置了数据库的字符集
)
2)创建游标
cursor = conn.cursor()
3)向部门表salary中插入数据
insert2 = "INSERT INTO salary(date, emp_id,basic, awards) VALUES(%s, %s, %s, %s)"
data = [('2018-9-30', 2, 1000, 2000), ('2018-9-30', 3, 3000, 6000),('2018-9-30', 1, 8000, 9000)]
cursor.executemany(insert2, data)
4)将更新提交到数据库
conn.commit()    
5)关闭游标
cursor.close()
6)关闭数据库连接
conn.close()
```
2)执行insert_sal.py文件：
```shell
[root@localhost day10]# python3 insert_sal.py
```
3)登录mariadb查看结果：
```shell
MariaDB [tedu]>> select * from salary;
+---------+------------+--------+-------+--------+
| auto_id | date       | emp_id | basic | awards |
+---------+------------+--------+-------+--------+
|       1 | 2018-09-30 |      2  |  1000 |   2000 |
|       2 | 2018-09-30 |      3  |  3000 |   6000 |
|       3 | 2018-09-30 |      1  |  8000 |   9000 |
+---------+------------+--------+-------+--------+
3 rows in set (0.01 sec) 
```
# 2. 扫描存活主机
## 2.1 问题
创建mtping.py脚本，实现以下功能：

1. 通过ping测试主机是否可达
2. 如果ping不通，不管什么原因都认为主机不可用
3. 通过多线程方式实现并发扫描

## 2.2 方案
subprocess.call ()方法可以调用系统命令，其返回值是系统命令退出码，也就是如果系统命令成功执行，返回0，如果没有成功执行，返回非零值。

调用Ping对象，可以调用系统的ping命令，通过退出码来判断是否ping通了该主机。如果顺序执行，每个ping操作需要消耗数秒钟，全部的254个地址需要10分钟以上。而采用多线程，可以实现对这254个地址同时执行ping操作，并发的结果就是将执行时间缩短到了10秒钟左右。

##  2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：编写脚本**
```shell
[root@localhost day09]# vim mtping.py
#!/usr/bin/env python3
import subprocess
import threading
def ping(host):
    rc = subprocess.call(
        'ping -c2 %s &> /dev/null' % host,
        shell=True
    )
    if rc:
        print('%s: down' % host)
    else:
        print('%s: up' % host)
if __name__ == '__main__':
    ips = ['172.40.58.%s' % i for i in range(1, 255)]
    for ip in ips:
        # 创建线程，ping是上面定义的函数, args是传给ping函数的参数
        t = threading.Thread(target=ping, args=(ip,))
        t.start()  # 执行ping(ip)
```
面向对象代码编写方式如下：

定义Ping类，该类可实现允许ping通任何主机功能：

1. 利用__init__方法初始化参数，当调用Ping类实例时，该方法自动调用

2. 利用__call__()方法让Ping类实例变成一个可调用对象调用，调用t.start()时， 引用subprocess模块执行shell命令ping所有主机，将执行结果返回给rc变量，此时，如果ping不通返回结果为1，如果能ping通返回结果为0

3. 如果rc变量值不为0，表示ping不通，输出down

4. 否则，表示可以ping通，输出up

利用列表推导式生成整个网段的IP地址列表[172.40.58.1,172.40.58.2....]

循环遍历整个网段列表，直接利用 Thread 类来创建线程对象，执行Ping(ip)。
```shell
[root@localhost day09]# vim mtping2.py
#!/usr/bin/env python3
import threading
import subprocess
class Ping:
    def __init__(self, host):
        self.host = host
    def __call__(self):
        rc = subprocess.call(
            'ping -c2 %s &> /dev/null' % self.host,
            shell=True
        )
        if rc:
            print('%s: down' % self.host)
        else:
            print('%s: up' % self.host)
if __name__ == '__main__':
    ips = ('172.40.58.%s' % i for i in range(1, 255))  # 创建生成器
    for ip in ips:
        # 创建线程，Ping是上面定义的函数
        t = threading.Thread(target=Ping(ip))  # 创建Ping的实例
        t.start()   #执行Ping(ip)
```
**步骤二：测试脚本执行**
```shell
[root@localhost day09]# python3 udp_time_serv.py 
172.40.58.1: up
172.40.58.69: up
172.40.58.87: up
172.40.58.90: up
172.40.58.102: up
172.40.58.101: up
172.40.58.105: up
172.40.58.106: up
172.40.58.108: up
172.40.58.110: up
172.40.58.109: up
...
...
...
...
172.40.58.241: down
172.40.58.242: down
172.40.58.243: down
172.40.58.245: down
172.40.58.246: down
172.40.58.248: down
172.40.58.247: down
172.40.58.250: down
172.40.58.249: down
172.40.58.251: down
172.40.58.252: down
172.40.58.253: down
172.40.58.254: down
```
# 3. 利用多线程实现ssh并发访问
## 3.1 问题
编写一个remote_comm.py脚本，实现以下功能：

1. 在文件中取出所有远程主机IP地址
2. 在shell命令行中接受远程服务器IP地址文件、远程服务器密码以及在远程主机上执行的命令
3. 通过多线程实现在所有的远程服务器上并发执行命令

## 3.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：安装paramiko**

paramiko 遵循SSH2协议，支持以加密和认证的方式，进行远程服务器的连接，可以实现远程文件的上传，下载或通过ssh远程执行命令。
```shell
[root@localhost ~]# pip3 install paramiko
...
...
Successfully installed bcrypt-3.1.4 paramiko-2.4.1 pyasn1-0.4.4 pynacl-1.2.1
You are using pip version 9.0.1, however version 18.0 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
```
测试是否安装成功
```shell
>>> import paramiko
>>>
```
**步骤二：编写脚本**
```shell
[root@localhost day11]# vim remote_comm.py
#!/usr/bin/env python3
import sys
import getpass
import paramiko
import threading
import os
#创建函数实现远程连接主机、服务器密码以及在远程主机上执行的命令的功能
def remote_comm(host, pwd, command):
#创建用于连接ssh服务器的实例
    ssh = paramiko.SSHClient()
#设置自动添加主机密钥
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#连接ssh服务器，添加连接的主机、用户名、密码填好
    ssh.connect(hostname=host, username='root', password=pwd)
#在ssh服务器上执行指定命令，返回3项类文件对象，分别是，输入、输出、错误
    stdin, stdout, stderr = ssh.exec_command(command)
#读取输出
    out = stdout.read()
#读取错误
    error = stderr.read()
#如果有输出
    if out:
#打印主机输出内容
        print('[%s] OUT:\n%s' % (host, out.decode('utf8')))
#如果有错误
    if error:
#打印主机错误信息
        print('[%s] ERROR:\n%s' % (host, error.decode('utf8')))
#程序结束
    ssh.close()
if __name__ == '__main__':
#设定sys.argv长度，确保remote_comm函数中参数数量
    if len(sys.argv) != 3:
        print('Usage: %s ipaddr_file "command"' % sys.argv[0])
        exit(1)
#判断命令行上输入如果不是文件，确保输入的是文件  
    if not os.path.isfile(sys.argv[1]):
        print('No such file:', sys.argv[1])
        exit(2)
#fname为存储远程主机ip的文件，用sys.argv方法，可以在执行脚本时再输入文件名，更为灵活
    fname = sys.argv[1]
#command为在远程主机上执行的命令，用sys.argv方法，可以在执行脚本时再输入相应命令，command为remote_comm函数第三个参数
    command = sys.argv[2]
#通过getpass输入远程服务器密码，pwd为remote_comm函数第二个参数
    pwd = getpass.getpass()
#打开存有远程主机ip的文件
    with open(fname) as fobj:
#将遍历文件将ip以列表形式存入ips，line.strip()可以去掉每行ip后\n
        ips = [line.strip() for line in fobj]
#循环遍历列表，获取ip地址，ip为remote_comm函数第一个参数
    for ip in ips:
#将读取到的ip地址作为remote_comm函数实际参数传递给函数，ips中有几个ip地址循环几次
#创建多线程
        t = threading.Thread(target=remote_comm, args=(ip, pwd, command))
#启用多线程
        t.start()
```
**步骤三：测试脚本执行**
```shell
#参数给少了效果如下：
[root@localhost day11]# python3 remote_comm.py server_addr.txt
Usage: remote_comm.py ipaddr_file “command”
#参数给多了效果如下：
[root@localhost day11]# python3 remote_comm.py server_addr.txt id zhangsan
Usage: remote_comm.py ipaddr_file “command”
#正常显示如下：
[root@localhost day11]# python3 remote_comm.py server_addr.txt “id zhangsan”
Password:
[192.168.4.2] OUT:
uid=1001(zhangsan) gid=1001(zhangsan) 组=1001(zhangsan)
[192.168.4.3] OUT:
uid=1001(zhangsan) gid=1001(zhangsan) 组=1001(zhangsan)
[root@localhost day11]# python3 remote_comm.py server_addr.txt “echo redhat | passwd –stdin root”
Password:
[192.168.4.3] OUT:
更改用户root的密码：
passwd：所有的身份验证令牌已经成功更新。
[192.168.4.2] OUT:
更改用户root的密码：
passwd：所有的身份验证令牌已经成功更新。
#此时密码已经变成redhat
[root@localhost day11]# python3 remote_comm.py server_addr.txt “id zhangsan”
Password:
[192.168.4.2] OUT:
uid=1001(zhangsan) gid=1001(zhangsan) 组=1001(zhangsan)
[192.168.4.3] OUT:
uid=1001(zhangsan) gid=1001(zhangsan) 组=1001(zhangsan)
```


# Exercise
## 1 安装pymysql模块的方法有哪些？
- 在线安装
```shell
pip install pymysql
```
- 访问http://pypi.python.org，下载pymysql模块后本地通过pip安装
```shell
pip3 install PyMySQL-0.8.0.tar.gz
```
- 访问http://pypi.python.org，下载pymysql模块后本地安装
```shell
tar xzf PyMySQL-0.8.0.tar.gz
cd PyMySQL
python3 setup.py install
```
## 2 通过pip在线安装模块，如何提升速度？
- pip直接安装模块时，连接到的是国外官网。如果采用国内镜像站点，可以提升效率，方法如下：
```shell
[root@localhost ~]# mkdir ~/.pip/
[root@localhost ~]# vim ~/.pip/pip.conf 
[global]
index-url=http://pypi.douban.com/simple/
[install]
trusted-host=pypi.douban.com
```
## 3 使用pymysql操作数据库的一般流程是什么？
- 先连接数据库
- 创建游标
- 通过游标对数据库进行各项操作
- 如果是增删改操作，需要确认
- 关闭到数据库的连接

## 4 通过paramiko管理远程服务器的一般流程是什么？
- 创建SSHClient实例
- 设置添加主机密钥策略
- 连接ssh服务器
- 执行指定命令
- 在shell命令行中接受用于连接远程服务器的密码以及在远程主机上执行的命令

> 如有侵权，请联系作者删除
