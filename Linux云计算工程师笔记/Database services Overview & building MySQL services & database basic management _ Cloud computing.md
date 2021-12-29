@[TOC]( Database services Overview & building MySQL services & database basic management & MySQL data types | Cloud computing )

---
# 1. 构建MySQL服务器
## 1.1 问题
要求如下：
- 在IP地址192.168.4.50主机和192.168.4.51的主机上部署mysql服务
- 192.168.4.50主机设置数据库管理员root本机登录密码为123qqq...A
- 192.168.4.51主机设置数据库管理员root本机登录密码为NSD123...a

## 1.2 方案
克隆2台新虚拟机（红帽7操作系统）：
在eth0网卡配置ip地址
主机名称:host50、host51
拷贝软件mysql-5.7.17.tar 到新克隆的虚拟机里
关闭防火墙（如果有的话）
关闭SELinux（如果有的话）
配置yum源（本地源或网络源都可以）

## 1.3 步骤
实现此案例需要按照如下步骤进行(以主机host50为例演示)。

**步骤一：准备工作**

1）如果之前有mariadb，则需要先卸载，并删除对应的配置与数据：
```shell
[root@host50 ~]# systemctl  stop mariadb
```
2）删除/etc/my.cnf配置文件
此配置文件由RHEL自带的mariadb-libs库提供：
```shell
[root@host50 ~]# rm -rf /etc/my.cnf
```
3）删除数据
```shell
 [root@host50 ~]# rm -rf /var/lib/mysql/*
```
4）卸载软件包
```shell
 [root@host50 ~]# rpm -e --nodeps mariadb-server  mariadb 
警告：/var/log/mariadb/mariadb.log 已另存为/var/log/mariadb/mariadb.log.rpmsave
```
**步骤二：安装mysql软件包**
1）解压mysql-5.7.17.tar 软件包
```shell
[root@host50 ~]# tar -xvf mysql-5.7.17.tar               //解压mysql整合包
./mysql-community-client-5.7.17-1.el7.x86_64.rpm
./mysql-community-common-5.7.17-1.el7.x86_64.rpm
./mysql-community-devel-5.7.17-1.el7.x86_64.rpm
./mysql-community-embedded-5.7.17-1.el7.x86_64.rpm
./mysql-community-embedded-compat-5.7.17-1.el7.x86_64.rpm
./mysql-community-embedded-devel-5.7.17-1.el7.x86_64.rpm
./mysql-community-libs-5.7.17-1.el7.x86_64.rpm
./mysql-community-libs-compat-5.7.17-1.el7.x86_64.rpm
./mysql-community-minimal-debuginfo-5.7.17-1.el7.x86_64.rpm
./mysql-community-server-5.7.17-1.el7.x86_64.rpm
./mysql-community-test-5.7.17-1.el7.x86_64.rpm
```
2）安装MySQL软件包
```shell
[root@host50 ~]# yum  -y   install    mysql-community-*.rpm   //yum安装自动解决依赖
./mysql-community-client-5.7.17-1.el7.x86_64.rpm
./mysql-community-common-5.7.17-1.el7.x86_64.rpm
./mysql-community-devel-5.7.17-1.el7.x86_64.rpm
./mysql-community-embedded-5.7.17-1.el7.x86_64.rpm
./mysql-community-embedded-compat-5.7.17-1.el7.x86_64.rpm
./mysql-community-embedded-devel-5.7.17-1.el7.x86_64.rpm
./mysql-community-libs-5.7.17-1.el7.x86_64.rpm
./mysql-community-libs-compat-5.7.17-1.el7.x86_64.rpm
./mysql-community-minimal-debuginfo-5.7.17-1.el7.x86_64.rpm
./mysql-community-server-5.7.17-1.el7.x86_64.rpm
./mysql-community-test-5.7.17-1.el7.x86_64.rpm
```
3）启动MySQL数据库服务并设置开机自启
提示：第一次启动，需要初始化数据，会比较慢
```shell
[root@host50 ~]# systemctl start mysqld                  //启动mysql服务
[root@host50 ~]# systemctl enable mysqld                 //设置开机自启
[root@host50 ~]# systemctl status mysqld                 //查看mysql服务状态
● mysqld.service - MySQL Server
   Loaded: loaded (/usr/lib/systemd/system/mysqld.service; enabled; vendor preset: disabled)
   Active: active (running) since 二 2018-08-28 10:03:24 CST; 8min ago
     Docs: man:mysqld(8)
           http://dev.mysql.com/doc/refman/en/using-systemd.html
 Main PID: 4284 (mysqld)
   CGroup: /system.slice/mysqld.service
           └─4284 /usr/sbin/mysqld --daemonize --pid-file=/var/r...
8月 28 10:02:56 localhost.localdomain systemd[1]: Starting MySQ...
8月 28 10:03:24 localhost.localdomain systemd[1]: Started MySQL...
Hint: Some lines were ellipsized, use -l to show in full.
[root@host50 ~]# ps -C  mysqld   //查看进程
  PID TTY          TIME CMD
20161 ?        00:00:00 mysqld
[root@host50 ~]# 
[root@host50 ~]# ss -utnlp  | grep 3306  //查看端口
tcp    LISTEN     0      80       :::3306                 :::*                   users:(("mysqld",pid=20161,fd=22))
[root@host50 ~]# 
```
**步骤三：连接MySQL服务器，修改密码**
1）查看初始密码
```shell
[root@host50 ~]#grep -i  'password' /var/log/mysqld.log
2017-04-01T18:10:42.948679Z 1 [Note] A temporary password is generated for root@localhost: mtoa>Av<p6Yk        //随机生成的管理密码为mtoa>Av<p6Yk
```
2）使用初始密码连接mysql服务
```shell
[root@host50 ~]# mysql -u root -p'mtoa>Av<p6Yk' //初始密码登录，
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 11
Server version: 5.7.17
Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql>                                     //登录成功后，进入SQL操作环境
```
3）重置数据库管理员root本机登录密码
```shell
mysql> show databases;  
ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement  //提示必须修改密码
mysql> alter user  root@”localhost” identified by "123qqq...A";  //修改登陆密码必须要满足密码策略的要求
Query OK, 0 rows affected (0.00 sec)
mysql> exit //断开连接
[root@host50 ~]#
```
4）使用修改的密码登录
```shell
[root@host50 ~]# mysql -uroot –p123qqq...A   //使用修改后的密码登录
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 15
Server version: 5.7.17 MySQL Community Server (GPL)
Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
mysql> show  databases; //查看数据库（看到默认的4个库）
+--------------------+
| Database            |
+--------------------+
| information_schema |
| mysql                |
| performance_schema  |
| sys                |
+--------------------+
4 rows in set (0.00 sec)
mysql> exit   //断开连接
```
# 2. 密码管理
## 2.1 问题
在192.168.4.50主机做如下练习：
- 修改密码策略
- 破解线下服务器root密码
- 破解线上服务器root密码
- 修改服务器root密码
![在这里插入图片描述](https://img-blog.csdnimg.cn/9f365bc9947446f8bbabda5248338b56.png)
## 2.2 步骤
**步骤一：修改密码策略**

命令行修改临时有效
```shell
[root@host50 ~]# mysql -uroot -p123qqq...A          //管理员root登录
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 16
Server version: 5.7.17 MySQL Community Server (GPL)
Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
                                 
mysql> show variables  like "validate_password_%"; //查看与密码相关的全局变量 
+--------------------------------------+--------+
| Variable_name                        | Value  |
+--------------------------------------+--------+
| validate_password_check_user_name    | OFF    |
| validate_password_dictionary_file    |        |
| validate_password_length             | 8      |    //默认密码长度
| validate_password_mixed_case_count   | 1      |
| validate_password_number_count       | 1      |
| validate_password_policy             | MEDIUM |   //默认密码策略
| validate_password_special_char_count | 1      |
+--------------------------------------+--------+
7 rows in set (0.00 sec)
mysql> set global validate_password_length = 6;  //修改密码最小长度
Query OK, 0 rows affected (0.00 sec)
mysql> set global validate_password_policy = 0 ;  //修改密码策略等级为0
Query OK, 0 rows affected (0.00 sec)
mysql> alter user  root@"localhost" identified by "123456";  //修改root密码
Query OK, 0 rows affected (0.03 sec)
mysql> exit; 断开连接
[root@host50 ~]# mysql -uroot -p123456  //新密码登录
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 28
Server version: 5.7.17-log MySQL Community Server (GPL)
Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql> 
```
永久配置，修改配置文件
```shell
[root@host50 ~]# vim /etc/my.cnf
[mysqld]
validate_password_length = 6   //密码最小长度
validate_password_policy = 0   //密码等级
:wq
[root@host50 ~]# systemctl  restart mysqld   //重启服务
[root@host50 ~]# mysql -uroot -p123456  //登录
mysql> show variables like "validate_password_length";  //只查看密码长度
+--------------------------+-------+
| Variable_name            | Value |
+--------------------------+-------+
| validate_password_length | 6     |
+--------------------------+-------+
1 row in set (0.00 sec)
mysql>  show variables like "validate_password_policy"; //只查看密码策略
+--------------------------+-------+
| Variable_name            | Value |
+--------------------------+-------+
| validate_password_policy | LOW   |
+--------------------------+-------+
1 row in set (0.00 sec)
mysql> 
```
**步骤2：破解线下服务器root密码**
1）修改运行参数并重启服务
如果修改了密码策略必须恢复为默认的默默策略，不然服务无法跳过授权表启动
```shell
[root@host50 ~]# vim /etc/my.cnf
[mysqld]
skip-grant-tables  #逃过授权表
#validate_password_length = 6   //注释掉
#validate_password_policy = 0   //注释掉
:wq
[root@host50 ~]# systemctl  restart mysqld    //重启服务
```
2）无密码登录
```shell
[root@host50 ~]# mysql    //无密码登录
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 5
Server version: 5.7.17-log MySQL Community Server (GPL)
Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql> update mysql.user set  authentication_string=password("123qqq...A")
    -> where user="root" and host="localhost";  //修改root用户本机登录密码(要符合默认的密码策略)
Query OK, 1 row affected, 1 warning (0.05 sec)
Rows matched: 1  Changed: 1  Warnings: 1
mysql> flush privileges;  //让修改生效
Query OK, 0 rows affected (0.02 sec)
mysql> exit  //断开连接
Bye
[root@host50 ~]#   
```
3）修改配置文件并重启服务
```shell
[root@host50 ~]#  vim  /etc/my.cnf
[mysqld]
#skip-grant-tables   //注释
validate_password_length = 6  //删除注释
validate_password_policy = 0  //删除注释
:wq
[root@host50 ~]# systemctl  restart mysqld
```
4）修改后的密码登录
```shell
[root@host50 ~]# mysql -uroot -p123qqq...A   //登录
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 5
Server version: 5.7.17-log MySQL Community Server (GPL)
Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql> 
```
**步骤三：破解线上服务器root密码（线上服务器的服务是不允许随便重启的）**
1）拷贝管理员能正常登录的数据库服务器的MySQL库覆盖本机的mysql库
把host51主机的mysql库拷贝给host50主机
```shell
[root@host50 ~]# scp -r root@192.168.4.51:/var/lib/mysql/mysql /var/lib/mysql/
root@192.168.4.51's password:  输入登录51主机的密码
```
2)重新加载数据
```shell
[root@host50 ~]# which  pstree  || yum -y install psmisc   安装pstree命令软件
/usr/bin/pstree
[root@host50 ~]# 
[root@host50 ~]# pstree -p | grep   mysqld  | head  -1   查看父进程pid号
           |-mysqld(20261)-+-{mysqld}(20262)
[root@host50 ~]# 
[root@host50 ~]# 
[root@host50 ~]# kill  -SIGHUP 20261    发送信号给进程
[root@host50 ~]#
```
3)使用和host51主机一样的密码连接服务
```shell
[root@host50 ~]# mysql -uroot -pNSD123...a    密码登录
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 5.7.17 MySQL Community Server (GPL)
Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql> 
```
**步骤四：修改root密码**
1）修改密码
需要指定旧密码，新密码才能修改
```shell
[root@host50 ~]# mysqladmin  -uroot -pNSD123...a  password "123qqq...A"
mysqladmin: [Warning] Using a password on the command line interface can be insecure.
Warning: Since password will be sent to server in plain text, use ssl connection to ensure password safety.
 或
[root@host50 ~]# mysqladmin  -uroot  -p   password 
Enter password: 旧密码
New password: 新密码
Confirm new password: 再输入一遍新密码
Warning: Since password will be sent to server in plain text, use ssl connection to ensure password safety.
[root@host50 ~]# 
```
2）使用修改后的密码登录
```shell
[root@host50 ~]# mysql -uroot -p123qqq...A
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 15
Server version: 5.7.17 MySQL Community Server (GPL)
Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql>
```
# 3. 安装图形软件
## 3.1 问题：具体要求如下：
1. 在IP地址192.168.4.50主机安装phpmyadmin软件
2. 客户端通过访问phpmyadmin软件管理数据库

## 3.2 步骤
**步骤一：在IP地址192.168.4.50主机安装phpmyadmin软件。**

1）在 192.168.4.50主机部署LAP环境
```shell
[root@host50 ~]# yum -y install httpd  php  php-mysql  安装软件
[root@host50 ~]# rpm -q  httpd  php  php-mysql  查看是否安装成功
httpd-2.4.6-80.el7.centos.x86_64
php-5.4.16-45.el7.x86_64
php-mysql-5.4.16-45.el7.x86_64
[root@host50 ~]# 
[root@host50 ~]# systemctl start httpd  启动服务
[root@host50 ~]# systemctl enable httpd 开机运行
Created symlink from /etc/systemd/system/multi-user.target.wants/httpd.service to /usr/lib/systemd/system/httpd.service.
[root@host50 ~]#
```
2）安装phpmyadmin软件

事先把phpMyAdmin-2.11.11-all-languages.tar.gz软件从真机拷贝到50主机的/root目录下
```shell
[root@host50 ~]# tar -zxvf  phpMyAdmin-2.11.11-all-languages.tar.gz  解压软件
[root@host50 ~]# ls  查看解压后的名字
Desktop                           phpMyAdmin-2.11.11-all-languages.tar.gz
phpMyAdmin-2.11.11-all-languages
[root@host50 ~]# 
[root@host50 ~]# mv phpMyAdmin-2.11.11-all-languages /var/www/html/phpmyadmin  移动并改名
```
3) 修改配置文件
```shell
[root@host50 ~]# cd /var/www/html/phpmyadmin/   进入安装目录
[root@host50 phpmyadmin]# 
[root@host50 phpmyadmin]# cp config.sample.inc.php config.inc.php 拷贝模板文件，生成主配置文件config.inc.php  
[root@host50 phpmyadmin]# vim +17 config.inc.php 只需要修改第17行
$cfg['blowfish_secret'] = 'plj123';  随便添点字符就可以
:wq
```
**步骤二：客户端通过访问phpmyadmin软件管理数据库。**

1. 打开真机浏览器，地址栏输入网址 http://192.168.4.50/phpmyadmin

登录用户名 root
密码 管理员本机登录密码

如图-1、图-2所示

![在这里插入图片描述](https://img-blog.csdnimg.cn/2afb8655bd244c06ad999b6513d9b191.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_16,color_FFFFFF,t_70,g_se,x_16)
图-1

![在这里插入图片描述](https://img-blog.csdnimg.cn/f316c2f8678d4d32ae28d7aa70c03279.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-2

# 4 查询条件
## 4.1 问题：具体要求如下：
- 练习别名、拼接、去重
- 练习数值比较的使用
- 练习字符比较的使用
- 练习范围匹配的使用
- 练习模糊匹配的使用
- 练习正则匹配的使用
- 练习逻辑比较的使用

## 5.2 步骤
环境准备（host50主机做如下操作）
```shell
使用备份文件创建数据
[root@host50 ~]# ls   查看备份文件
Desktop    tarena.sql
[root@host50 ~]# 
[root@host50 ~]# 
[root@host50 ~]# mysql -uroot -p123qqq...A  < tarena.sql  使用备份文件创建数据
mysql: [Warning] Using a password on the command line interface can be insecure.
[root@host50 ~]# 
[root@host50 ~]# mysql -uroot -p123qqq...A  管理员登录
mysql> use tarena; 进入tarena库
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A
Database changed
mysql> show tables;  查看表
+------------------+
| Tables_in_tarena |
+------------------+
| departments      |
| employees        |
| salary           |
| user             |
+------------------+
4 rows in set (0.00 sec)
mysql> 
```
练习使用的user表说明如图-1所示

![在这里插入图片描述](https://img-blog.csdnimg.cn/85844dabfe064f0db864f9d4637825d2.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-1

**步骤一：练习别名、拼接、去重**
```sql
//别名
mysql> select name as 姓名 , homedir  家目录 from  tarena.user;
+-----------------+--------------------+
| 姓名            | 家目录             |
+-----------------+--------------------+
| root            | /root              |
| bin             | /bin               |
| daemon          | /sbin              |
| adm             | /var/adm           |
| lp              | /var/spool/lpd     |
//拼接
mysql> select concat(name, "-" , uid ) from tarena.user;
+--------------------------+
| concat(name, "-" , uid ) |
+--------------------------+
| root-0                   |
| bin-1                    |
| daemon-2                 |
| adm-3                    |
| lp-4                     |
| sync-5                   |
//去重
mysql> select distinct gid from tarena.user;
+-------+
| gid   |
+-------+
|     0 |
|     1 |
|     2 |
|     4 |
|     7 |
|    12 |
|   100 |
|    50 |
```
**步骤二、练习数值比较的使用**

符号两边要是数值或是数值类型的字段
```sql
//查看uid号和号相等的用户名、UID号、gid号
mysql> select name ,uid,gid from tarena.user where uid = gid ;
+-----------------+-------+-------+
| name            | uid   | gid   |
+-----------------+-------+-------+
| root            |     0 |     0 |
| bin             |     1 |     1 |
| daemon          |     2 |     2 |
| nobody          |    99 |    99 |
| systemd-network |   192 |   192 |
| dbus            |    81 |    81 |
//查看uid号不等与gid号的用户名、UID号、gid号
mysql> select name ,uid,gid from tarena.user where uid != gid ;
+----------+------+------+
| name     | uid  | gid  |
+----------+------+------+
| adm      |    3 |    4 |
| lp       |    4 |    7 |
| sync     |    5 |    0 |
| shutdown |    6 |    0 |
| halt     |    7 |    0 |
| mail     |    8 |   12 |
//查看表记录的前5行
mysql> select  * from  tarena.user where  id <= 5;  
+----+--------+----------+------+------+---------+----------------+---------------+
| id | name   | password | uid  | gid  | comment | homedir        | shell         |
+----+--------+----------+------+------+---------+----------------+---------------+
|  1 | root   | x        |    0 |    0 | root    | /root          | /bin/bash     |
|  2 | bin    | x        |    1 |    1 | bin     | /bin           | /sbin/nologin |
|  3 | daemon | x        |    2 |    2 | daemon  | /sbin          | /sbin/nologin |
|  4 | adm    | x        |    3 |    4 | adm     | /var/adm       | /sbin/nologin |
|  5 | lp     | x        |    4 |    7 | lp      | /var/spool/lpd | /sbin/nologin |
+----+--------+----------+------+------+---------+----------------+---------------+
5 rows in set (0.01 sec)
mysql> 
```
**步骤三、练习字符比较的使用**
```sql
//查找名字叫apache的用户
mysql> select name from tarena.user where name="apache"; 
+--------+
| name   |
+--------+
| apache |
+--------+
1 row in set (0.00 sec)
//查看shell是/bin/bash的用户
mysql> select name , shell from tarena.user 
where shell = "/bin/bash" ;
+------+-----------+
| name | shell     |
+------+-----------+
| root | /bin/bash |
| plj  | /bin/bash |
+------+-----------+
2 rows in set (0.00 sec)
//查看shell不是/bin/bash的用户
mysql> select name , shell from tarena.user where shell != "/bin/bash" ;
+-----------------+----------------+
| name            | shell          |
+-----------------+----------------+
| bin             | /sbin/nologin  |
| daemon          | /sbin/nologin  |
| adm             | /sbin/nologin  |
| lp              | /sbin/nologin  |
//查找uid字段没有数据的记录
mysql> select name , uid from tarena.user where uid is null ; 
+------+------+
| name | uid  |
+------+------+
| bob  | NULL |
+------+------+
1 row in set (0.00 sec)
mysql> 
//查看uid字段不是空的记录
mysql> select name , uid from tarena.user where uid is not  null ; 
+-----------------+-------+
| name            | uid   |
+-----------------+-------+
| root            |     0 |
| bin             |     1 |
| daemon          |     2 |
| adm             |     3 |
| lp              |     4 |
| sync            |     5 |
| shutdown        |     6 |
//没有数据
mysql> select name , comment from tarena.user where comment is null;
 +------+---------+
| name | comment |
+------+---------+
| bob  | NULL    |
+------+---------+
1 row in set (0.00 sec)
//零个字符
mysql> select name , comment from tarena.user where comment="" ; 
+---------+---------+
| name    | comment |
+---------+---------+
| postfix |         |
| chrony  |         |
| plj     |         |
+---------+---------+
3 rows in set (0.00 sec)
mysql> 
```
**步骤四、练习范围匹配的使用**
```sql
//查看uid号是1或3或5或7的记录
mysql> select name,uid,shell from tarena.user where uid in  (1,3,5,7); 
+------+------+---------------+
| name | uid  | shell         |
+------+------+---------------+
| bin  |    1 | /sbin/nologin |
| adm  |    3 | /sbin/nologin |
| sync |    5 | /bin/sync     |
| halt |    7 | /sbin/halt    |
+------+------+---------------+
4 rows in set (0.01 sec)
mysql> 
//查看shell不是/bin/bash 或 /sbin/nologin的用户
mysql> select name,uid,shell from tarena.user where shell not in  ("/bin/bash","/sbin/nologin"); 
+----------+------+----------------+
| name     | uid  | shell          |
+----------+------+----------------+
| sync     |    5 | /bin/sync      |
| shutdown |    6 | /sbin/shutdown |
| halt     |    7 | /sbin/halt     |
| mysql    |   27 | /bin/false     |
+----------+------+----------------+
4 rows in set (0.00 sec)
mysql> 
//查看uid 在10到30之间的记录，包括10和30本身
mysql> select name , uid , gid  from tarena.user where uid between 10 and 30 ;
+----------+------+------+
| name     | uid  | gid  |
+----------+------+------+
| operator |   11 |    0 |
| games    |   12 |  100 |
| ftp      |   14 |   50 |
| rpcuser  |   29 |   29 |
| mysql    |   27 |   27 |
+----------+------+------+
5 rows in set (0.00 sec)
mysql> 
```
**步骤五、练习模糊匹配的使用**
```sql
//查看名字是3个字符的
mysql> select name from tarena.user where name like "___";
+------+
| name |
+------+
| bin  |
| adm  |
| ftp  |
| rpc  |
| plj  |
| bob  |
+------+
6 rows in set (0.00 sec)
mysql>
//查看名字至少是4个字符的 
mysql> select name from tarena.user where name like "__%__"; 
+-----------------+
| name            |
+-----------------+
| root            |
| daemon          |
| sync            |
| shutdown        |
| halt            |
| mail            |
| operator        |
| games           |
| nobody          |
| systemd-network |
| dbus            |
| polkitd         |
| sshd            |
| postfix         |
| chrony          |
| rpcuser         |
//查看名字里有字母a的
mysql> select name from tarena.user where name like "%a%"; 
+----------+
| name     |
+----------+
| daemon   |
| adm      |
| halt     |
| mail     |
| operator |
| games    |
| haproxy  |
| apache   |
+----------+
8 rows in set (0.00 sec)
mysql> 
```
**步骤六、练习正则匹配的使用**
```sql
//查看名字必须是r开头且是t结尾的名字
mysql> select name from tarena.user where name regexp "^r.*t$"; 
+------+
| name |
+------+
| root |
+------+
1 row in set (0.00 sec)
mysql> 
//查看名字是字母r 开头或字母t结尾的名字
mysql> select name from tarena.user where name regexp "^r|t$"; 
+---------+
| name    |
+---------+
| root    |
| halt    |
| rpc     |
| rpcuser |
+---------+
4 rows in set (0.00 sec)
mysql> 
//查看名字里有数字的
mysql> select name from tarena.user where name regexp "[0-9]"; 
Empty set (0.00 sec)
//看名字以数字开头的
mysql> select name from tarena.user where name regexp "^[0-9]"; 
Empty set (0.00 sec)
mysql> 
```
步骤七、练习逻辑比较的使用
```sql
//查看名字叫mysql 或者uid 是 0 的 记录
mysql> select name , uid from tarena.user where name = "mysql"  or uid = 0 ;  
+-------+------+
| name  | uid  |
+-------+------+
| root  |    0 |
| mysql |   27 |
+-------+------+
2 rows in set (0.00 sec)
//查看名字叫mysql并且uid号 还必须是零的记录
mysql> select name , uid from tarena.user where name = "mysql"  and uid = 0 ;
Empty set (0.00 sec)
mysql>
 //查看uid 是0 的记录 
mysql> select name, uid from tarena.user where uid = 0 ;
+------+------+
| name | uid  |
+------+------+
| root |    0 |
+------+------+
1 row in set (0.00 sec)
//查看uid不是0的记录
mysql> select name, uid from tarena.user where not uid = 0 ; 
+-----------------+-------+
| name            | uid   |
+-----------------+-------+
| bin             |     1 |
| daemon          |     2 |
| adm             |     3 |
| lp              |     4 |
| sync            |     5 |
| shutdown        |     6 |
// 既有and又有or  优先匹配and
mysql> select name , uid from tarena.user where name = "root" or name = "bin" and uid = 1 ; 
+------+------+
| name | uid  |
+------+------+
| root |    0 |
| bin  |    1 |
+------+------+
2 rows in set (0.00 sec)
// () 先匹配or 再匹配and
mysql> select name , uid from tarena.user where (name = "root" or name = "bin") and uid = 1 ;  
+------+------+
| name | uid  |
+------+------+
| bin  |    1 |
+------+------+
1 row in set (0.00 sec)
mysql> 
```

# Exercise
## 1 简述当前主流RDBMS软件有哪些？开源且跨平台的数据库软件有哪些？
当前主流的数据库服务器软件有： Oracle 、 DB2 、 SQL SERVER 、MySQL 等 ，其中只有MySQL是既开源又跨平台的数据库服务软件。

## 2 简述MySQL数据库的服务进程名、默认端口、默认数据库目录？
服务进程名：mysqld
默认监听端口号：3306
默认数据库目录：/var/lib/mysql

## 3 简述MySQL默认的4个库叫什么名字？哪个库里的数据不占用物理磁盘空间？
MySQL默认的4个库分别是 information_schema 、performance_schema 、mysql 、sys 其中information_schema库不占用物理磁盘空间。

## 4 请列出MySQL常用的数据类型，并写出定义这些数据类型所使用的关键字。
MySQL常用的数据类型有：字符类型、数值类型、日期时间类型、枚举类型
字符类型：　char　、　varchar　、　blob、　text
数值类型：　tinyint 、smallint　、int　、bigint 、float 、 double
日期时间类型： year 、 date 、 time 、 datetime 、 timestamp
枚举类型： enum 、 set

## 5 简述以下MySQL函数的功能。
> year() 、date()　、month() 、day()　、time()、now()

year()　获取指定时间中的年
date()　获取指定时间中的年月日
month() 获取指定时间中的月
day()　 获取指定时间中的日期
time()　获取指定时间中的时间（小时分钟秒）
now()　 获取当前时间（年月日小时分钟秒）

## 6 在studentdb库里创建stu_info表，结构要求如图-1所示。
> ![在这里插入图片描述](https://img-blog.csdnimg.cn/f2bfa5bc9fc44a45b057bf1dd5bca4a6.png)
图-1

```sql
create  database  studentdb;
create  table  studentdb.stuinfo(
stu_id int(2),
name  varchar(10),
age  tinyint(2) unsigned,
sex  enum(“boy”,”girl”),
likes set(“book”,”music”,”game”,”film”)
);
```

> 如有侵权，请联系作者删除
