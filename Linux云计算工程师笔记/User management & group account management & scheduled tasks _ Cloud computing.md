
@[TOC]( User management &  group account management & scheduled tasks | Cloud computing )

---
# 1. 添加用户账号
## 1.1 问题
1. 创建一个名为tedu01的用户账号
2. 检查/etc/passwd、/etc/shadow文件的最后一行
3. 检查/home/新增加的宿主目录（家目录）
4. 新建用户tedu02，宿主目录位于/opt/tedu02
5. 新建系统账号system01，将UID设为1234，登录Shell设为/sbin/nologin
6. 新建用户admin，附加组设为adm、root

## 1.2 方案
在Linux同添加一个用户账户的命令为useradd，常用的选项较多。可以利用man命令查看其帮助信息。

本题涉及的选项：

- -u：设置 UID 标记号
- -d：指定宿主目录，缺省为 /home/用户名
- -G：指定所属的附加组
- -s：指定用户的登录解释器
## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：添加一个tedu01的用户账号**

命令操作如下所示：
```shell
[root@localhost ~]# useradd   tedu01
```
**步骤二：/etc/passwd、/etc/shadow文件的最后一行**
```shell
[root@localhost ~]# grep  tedu01 /etc/passwd /etc/shadow   //查看是否创建成功
```
**步骤三：检查/home/新增加的宿主目录（家目录）**
```shell
[root@localhost ~]# ls /home                     //查看家目录是否创建成功
[root@localhost ~]#
```
**步骤四：新建用户tedu02，宿主目录位于/opt/tedu02**
```shell
[root@localhost ~]# useradd   -d   /opt/tedu02   tedu02
[root@localhost ~]# id  tedu02
[root@localhost ~]# grep tedu02  /etc/passwd
[root@localhost ~]# ls /opt
```
**步骤五：新建系统账号system01，将UID设为1234，登录Shell设为/sbin/nologin**
```shell
[root@localhost ~]# useradd  -u  1234  -s  /sbin/nologin  system01
[root@localhost ~]# id  system01
[root@localhost ~]# grep system01 /etc/passwd
[root@localhost ~]# 
```
**步骤四：新建用户admin，附加组设为adm、root**
```shell
 [root@localhost ~]# useradd  -G  adm,root  admin
 [root@localhost ~]# id  admin
 ```
# 2. 设置用户密码
## 2.1 问题
1. 为用户tedu01设置一个密码：123456
2. 过滤/etc/shadow文件中包含tedu01的内容
3. 为用户system01设置密码，并测试是否能够登录
4. 非交互式给用户tedu02设置密码123456
5. 交互式给用户admin，设置密码为redhat

## 2.2 方案
为账户设置密码的命令为passwd，管理员root可以修改任何用户的口令，所有用户（包括普通用户）都可以修改自己的口令。

常用命令选项:

- --stdin：从标准输入（比如管道）取密码

查看结果可以利用grep命令，从/etc/shadow筛选。

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：为用户tedu01设置一个密码：123456**

命令操作如下所示：
```shell
[root@localhost ~]# echo 123456 |  passwd  --stdin   tedu01
```
**步骤二：过滤/etc/shadow文件中包含tedu01的内容**
```shell
[root@localhost ~]# grep  tedu01   /etc/shadow
```
**步骤三：为用户system01设置密码，并测试是否能够登录**

由于登录的解释器为/sbin/nologin,所以是无法登录系统
```shell
[root@localhost ~]# echo 123456  |  passwd –stdin  system01  
```
**步骤四：新建用户tedu02，宿主目录位于/opt/tedu02**
```shell
[root@localhost ~]# useradd   -d   /opt/tedu02   tedu02
[root@localhost ~]# id  tedu02
[root@localhost ~]# grep tedu02  /etc/passwd
[root@localhost ~]# ls /opt
```
**步骤五：非交互式给用户tedu02设置密码123456**
```shell
[root@localhost ~]# echo 123456  |  passwd –stdin  tedu02
```
**步骤六：交互式给用户admin，设置密码为redhat**
```shell
[root@localhost ~]# passwd admin
更改用户 admin 的密码 。
新的 密码：
无效的密码： 密码少于 8 个字符
重新输入新的 密码：
passwd：所有的身份验证令牌已经成功更新。
[root@localhost ~]#
```
# 3. 配置用户和组账号
## 3.1 问题
本例要求创建下列用户、组以及组的成员关系：

1. 新建用户 alex，其用户ID为3456，密码是flectrag
2. 创建一个名为 adminuser 的组
3. 创建一个名为 natasha 的用户，其属于 adminuser 组，这个组是该用户的从属组
4. 创建一个名为 harry 的用户，其属于 adminuser 组，这个组是该用户的从属组
5. 创建一个名为 sarah 的用户，其在系统中没有可交互的 Shell，并且不是 adminuser 组的成员
6. natasha 、harry、sarah 的密码都要设置为 flectrag
## 3.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：创建组账号**
```shell
[root@server0 ~]# groupadd  adminuser
```
**步骤二：按照要求的属性创建用户账号**
```shell
[root@server0 ~]# useradd  -u  3456  alex
[root@server0 ~]# useradd  -G  adminuser  natasha
[root@server0 ~]# useradd  -G  adminuser  harry
[root@server0 ~]# useradd  -s  /sbin/nologin  sarah
```
**步骤三：为用户设置登录密码**
```shell
[root@server0 ~]# echo  flectrag  |  passwd  --stdin  alex
更改用户 alex 的密码 。
passwd：所有的身份验证令牌已经成功更新。
[root@server0 ~]# echo  flectrag  |  passwd  --stdin  natasha
更改用户 natasha 的密码 。
passwd：所有的身份验证令牌已经成功更新。
[root@server0 ~]# echo  flectrag  |  passwd  --stdin  harry
更改用户 harry 的密码 。
passwd：所有的身份验证令牌已经成功更新。
[root@server0 ~]# echo  flectrag  |  passwd  --stdin  sarah
更改用户 sarah 的密码 。
passwd：所有的身份验证令牌已经成功更新。
```
# 4. 配置一个cron任务
## 4.1 问题
本例要求为用户 natasha 配置一个定时任务，具体要求如下：

1. 每天在本地时间 14:23 执行
2. 需要完成的任务操作为 /bin/echo hiya
## 4.2 方案
配置格式可参考 /etc/crontab 文件：
```shell
分  时  日  月  周      任务命令行（绝对路径）
```
在表示各段的时间点时，除了明确的数值以外，还可以参考以下形式：

- *：匹配范围内任意时间
- ,：分隔多个不连续的时间点
- -：指定连续时间范围
- /n：指定时间频率，每n ...
## 4.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：配置crontab任务记录**

> 1）确保系统服务crond可用
```shell
[root@server0 ~]# systemctl  restart  crond
[root@server0 ~]# systemctl  enable  crond
```

> 2）为用户natasha添加计划任务
```shell
[root@server0 ~]# crontab  -e  -u  natasha
23  14  *  *  *  /bin/echo hiya
```

**步骤二：检查任务是否执行**

> 1）将系统日期时间临时调整到任务时间点前10秒左右
```shell
[root@server0 ~]# date  -s  '14:22:50'              //设置
Sat Nov 26 14:22:50 CST 2016
[root@server0 ~]# date                              //确认日期时间
Sat Nov 26 14:22:55 CST 2016
```

> 2）等待10秒后查看/var/log/cron日志，应该会有执行记录
```shell
[root@server0 ~]# tail  /var/log/cron
.. ..
Nov 26 14:23:02 localhost CROND[3818]: (natasha) CMD (/bin/echo hiya)
```

# Exercise

## 1 采取免交互方式将用户root的密码设置为redhat
```shell
[root@server0 ~]# echo  redhat  |  passwd  --stdin  root
Changing password for user root.
passwd: all authentication tokens updated successfully.
```

## 2 新建系统账号sys01，将UID设为1234，登录Shell设为/sbin/nologin
```shell
[root@server0 ~]# useradd -u 1234 -s /sbin/nologin sys01
[root@server0 ~]# id sys01
uid=1234(sys01) gid=1234(sys01) 组=1234(sys01)
[root@server0 ~]# grep sys01 /etc/passwd
sys01:x:1234:1234::/home/sys01:/sbin/nologin
[root@server0 ~]#
```

## 3 每3小时执行一次“/bin/echo hiya”任务，简述对应的cron配置

```shell
[root@server0 ~]# crontab  -e 
0  */3  *  *  *    /bin/echo hiya
```

## 4 用户与组相关配置文件。
Linux用户的家目录、登录解释器等信息保存在（ ）文件内，而加密的密码字符串、密码有效期等信息保存在（ ）文件内。通过（ ）文件可以查看系统中有哪些组账号，以及各个组包括那些成员用户。

/etc/passwd、/etc/shadow、/etc/group

## 5 useradd命令常用选项。
使用useradd命令添加用户账号时，常用的选项有哪些、各自的作用是什么？

- -u：指定 UID 标记号
- -d：指定宿主目录，缺省为 /home/用户名
- -G：指定所属的附加组（组名或GID）
- -s：指定用户的登录解释器

## 6 为某个用户设置永久别名。
为root用户设置一个永久别名为，myls='ls -lhd'。

```shell
[root@svr5 /]# vim /root/.bashrc
# .bashrc
# User specific aliases and functions
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
alias myls='ls -lhd'                                  //添加此行
.. ..
```
当开启新的命令行终端时，检查别名即已生效。
```shell
[root@svr5 /]# alias 
alias cp='cp -i'
alias l.='ls -d .* --color=auto'
alias ll='ls -l --color=auto'
alias ls='ls --color=auto'
alias mv='mv -i'
alias myls='ls -lhd'
alias rm='rm -i'
alias which='alias | /usr/bin/which --tty-only --read-alias --show-dot --show-tilde'
[root@svr5 /]#
```

## 7 创建及修改iamkiller用户属性。
新建一个名为iamkiller的本地用户账号，要求如下：

1）宿主文件夹位于/opt/.private/iamkiller。
2）使用/sbin/nologin作为登录解释器。
3）将UID号指定为1234。
4）修改登录shell为/bin/bash。

```shell
[root@svr5 ~]# mkdir /opt/.private
[root@svr5 ~]# useradd -d /opt/.private/iamkiller -s /sbin/nologin -u 1234 iamkiller
[root@svr5 /]# usermod -s /bin/bash iamkiller
```

> 如有侵权，请联系作者删除
