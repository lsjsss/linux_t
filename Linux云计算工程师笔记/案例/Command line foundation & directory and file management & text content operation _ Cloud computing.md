@[TOC]( Command line foundation & directory and file management & text content operation | Cloud computing )

---
# 1. 命令行基础技巧
## 1.1 问题
本例要求掌握Linux命令行环境的基本操作，完成下列任务：

1. 利用Tab键快速找出下列文件：/etc/sysconfig/network-scripts/ifcfg-*、/etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
2. 练习以下快捷编辑操作：Ctrl + l、Ctrl + u、Ctrl + w；Ctrl + c、Esc + .

## 1.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：利用Tab键快速补全文档路径**

> 1）找出现有的网络连接配置文件
```shell
[root@server0 ~]# ls /etc/sysco<TAB>
[root@server0 ~]# ls /etc/sysconfig/netw<TAB>
[root@server0 ~]# ls /etc/sysconfig/network-s<TAB>
[root@server0 ~]# ls /etc/sysconfig/network-scripts/ifc<TAB>
[root@server0 ~]# ls /etc/sysconfig/network-scripts/ifcfg-<TAB><TAB>
ifcfg-br0          ifcfg-br1          ifcfg-lo
ifcfg-br0:253      ifcfg-eno16777736
```
> 2）找出Linux校验软件包的密钥文件

[root@server0 ~]# ls /etc/pki/rp<TAB>
[root@server0 ~]# ls /etc/pki/rpm-gpg/RP<TAB>
[root@server0 ~]# ls /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-r<TAB>
[root@server0 ~]# ls /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
/etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release

**步骤二：练习以下快捷编辑操作**

> 1）清理编辑的命令行

快速清屏：Ctrl + l

从当前光标处删除到行首：Ctrl + u

从当前光标处往前删除一个单词：Ctrl + w

> 2）放弃编辑的命令行

中止当前命令行：Ctrl + c

> 3）参数复用

在当前光标处粘贴上一条命令行的最后一个参数：Esc + .

# 2. 挂载并访问光盘设备
## 2.1 问题
本例要求学会mount挂载操作。主要完成下列任务：

1. 连接光盘CentOS7-1804.iso
2. 将光盘挂载到 /mnt 目录，检查 /mnt 目录内容
3. 卸载光盘设备，再次检查目录内容

## 2.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：使用ls命令列出指定的文件**

> 1）连接光盘 CentOS7-1804.iso
```shell
[root@server0 ~]# mount  /dev/cdrom  /mnt     //挂载设备
mount: /dev/sr0 写保护，将以只读方式挂载
```
> 2）将光盘挂载到 /mnt 目录，检查 /mnt 目录内容
```shell
[root@server0 ~]# ls  /mnt                 //访问设备内容
addons  images      Packages         RPM-GPG-KEY-redhat-release
EFI     isolinux    release-notes    TRANS.TBL
EULA    LiveOS      repodata
GPL     media.repo  RPM-GPG-KEY-redhat-beta
```
> 3）卸载光盘设备，再次检查目录内容
```shell
[root@server0 ~]# umount  /mnt/        //卸载设备
[root@server0 ~]# ls  /mnt/             //确认结果
```

# 3. ls列表及文档创建
## 3.1 问题
本例要求学会列表查看目录内容、新建文档相关技能，并熟悉通配符机制的应用。主要完成下列任务：

1. 使用ls命令列出指定的文件：/etc/目录下以re开头.conf结尾的文件、/dev/目录下编号是个位数的tty控制台设备
2. 一条命令创建文件夹 /protected/project/tts10

## 3.2 方案
对于通配符使用，需理解每个通配符的作用：

- *：任意多个任意字符
- ?：单个字符
- [a-z]：多个字符或连续范围中的一个，若无则忽略
- {a,min,xy}：多组不同的字符串，全匹配

## 3.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：使用ls命令列出指定的文件**

> 1）列出/etc/目录下以re开头.conf结尾的文件

使用通配符 * 代替未知的字符串。
```shell
[root@server0 ~]# ls /etc/re*.conf
/etc/request-key.conf  /etc/resolv.conf
```

> 2）列出/dev/目录下编号是个位数的tty控制台设备

使用通配符 ? 代替单个未知的字符。
```shell
[root@server0 ~]# ls /dev/tty?
/dev/tty0  /dev/tty2  /dev/tty4  /dev/tty6  /dev/tty8
/dev/tty1  /dev/tty3  /dev/tty5  /dev/tty7  /dev/tty9
```
或者更严谨一些，使用 [0-9] 代替单个数字。
```shell
[root@server0 ~]# ls /dev/tty[0-9]
/dev/tty0  /dev/tty2  /dev/tty4  /dev/tty6  /dev/tty8
/dev/tty1  /dev/tty3  /dev/tty5  /dev/tty7  /dev/tty9
```
**步骤二：新建文档**

> 1）使用mkdir新建文件夹
```shell
[root@server0 ~]# mkdir -p /protected/project/tts10
[root@server0 ~]# ls -ld /protected/project/tts10/
drwxr-xr-x. 2 root root 6 Aug 30 10:11 /protected/project/tts10/
```

# 4 案例4：复制、删除、移动
## 4.1 问题
本例要求学会对文档进行复制、删除、移动/改名相关操作，依次完成下列任务：

- 在当前目录下创建一个子目录 dir1
- 将文件夹 /boot/grub2/ 复制到目录dir1下
- 将目录 /root/ 下以 .cfg 结尾的文件复制到dir1下
- 将文件 /etc/redhat-release复制到 /root/ 下，同时改名为 version.txt
- 将文件 /root/version.txt 移动到dir1目录下
- 删除 dir1 目录下的 grub2 子目录

## 4.2 步骤
实现此案例需要按照如下步骤进行。

> 1）在当前目录下创建一个子目录 dir1
```shell
[root@server0 ~]# mkdir dir1
```

> 2）将文件夹 /boot/grub2/ 复制到目录dir1下
```shell
[root@server0 ~]# cp -r /boot/grub2/ dir1/
[root@server0 ~]# ls -ld dir1/*                                 //检查复制结果
drwxr-xr-x. 6 root root 104 Aug 30 10:27 dir1/grub2
```
> 3）将目录 /root/ 下以 .cfg 结尾的文件复制到dir1下
```shell
[root@server0 ~]# cp /root/*.cfg dir1/
[root@server0 ~]# ls -ld dir1/*                                 //检查复制结果
-rw-------. 1 root root 16793 Aug 30 10:29 dir1/anaconda-ks.cfg
drwxr-xr-x. 6 root root   104 Aug 30 10:27 dir1/grub2
```
> 4）将文件 /etc/redhat-release复制到 /root/ 下，同时改名为 version.txt
```shell
[root@server0 ~]# cp /etc/redhat-release /root/version.txt
[root@server0 ~]# ls -ld /root/version.txt                  //检查复制结果
-rw-r--r--. 1 root root 52 Aug 30 10:30 /root/version.txt
```
> 5）将文件 /root/version.txt 移动到dir1目录下
```shell
[root@server0 ~]# cp /root/version.txt dir1/
[root@server0 ~]# ls -ld dir1/*                             //检查移动/改名结果
-rw-------. 1 root root 16793 Aug 30 10:29 dir1/anaconda-ks.cfg
drwxr-xr-x. 6 root root   104 Aug 30 10:27 dir1/grub2
-rw-r--r--. 1 root root    52 Aug 30 10:31 dir1/version.txt
```
> 6）删除 dir1 目录下的grub2子目录
```shell
[root@server0 ~]# rm -rf dir1/grub2/
[root@server0 ~]# ls -ld dir1/*                             //检查删除结果
-rw-------. 1 root root 16793 Aug 30 10:29 dir1/anaconda-ks.cfg
-rw-r--r--. 1 root root    52 Aug 30 10:31 dir1/version.txt
```

# 5. 文本内容操作
## 5.1 问题
本例要求学会对文档进行复制、删除、移动/改名相关操作，依次完成下列任务：

- 在根目录下创建一个子目录 tedu
- 利用vim建立文件/tedu/stu.txt并写入内容“I Love Goddess”
- 利用grep过滤/etc/passwd中包含root的行
- 利用grep过滤/etc/passwd中以bash结尾的行

## 5.2 方案

 - vim是Linux系统上最常用的命令行交互式文本编辑器，主要工作在三种模式：命令模式、输入模式、末行模式。
- 通过vim打开一个文件时，默认处于命令模式；从命令模式按i键可以进入编辑状态，按Esc键返回命令模式；从命令模式输入冒号:可以进入末行模式，在末行模式下主要执行wq存盘与退出等基本操作。

## 5.3 步骤
实现此案例需要按照如下步骤进行。

> 1）在根目录下创建一个子目录 tedu
```shell
[root@server0 ~]# mkdir /tedu
```
> 2）利用vim建立文件/tedu/stu.txt并写入内容“I Love Goddess”
```shell
[root@server0 ~]# vim   /tedu/stu.txt
I Love Goddess 
```
> 3）利用grep过滤/etc/passwd中包含root的行
```shell
[root@server0 ~]# grep   root   /etc/passwd
```
> 4）利用grep过滤/etc/passwd中以bash结尾的行
```shell
[root@server0 ~]# grep   bash$   /etc/passwd
```

# Exercise
## 1 简述一条Linux命令行的一般组成格式
命令字 [选项]… [参数1] [参数2]…

## 2 简述绝对路径、相对路径的含义
绝对路径：以 / 开始的完整路径
相对路径：以当前工作目录为参照的路径
## 3 linux命令行常用的通配符有哪些，各自的作用是什么
针对不确定的文档名称，以特殊字符表示。

- *：任意多个任意字符
- ?：单个字符
- [a-z]：多个字符或连续范围中的一个，若无则忽略
- {a,min,xy}：多组不同的字符串，全匹配
## 4 删除文件/etc/resolv.conf，然后用vim重建此文件

> 1）确认文件原有的内容
```shell
[root@svr7 ~]# cat /etc/resolv.conf 
# Generated by NetworkManager
search ilt.example.com example.com
nameserver 172.25.254.250
```
> 2）删除文件
```shell
[root@svr7 ~]# rm -rf /etc/resolv.conf 
[root@svr7 ~]# ls -l /etc/resolv.conf                         //检查删除结果
ls: cannot access /etc/resolv.conf: No such file or directory
```
> 3）用vim重建此文件
```shell
[root@svr7 ~]# vim /etc/resolv.conf                         //保留有效配置即可
search ilt.example.com example.com
nameserver 172.25.254.250
[root@svr7 ~]# cat /etc/resolv.conf                         //检查重建结果
search ilt.example.com example.com
nameserver 172.25.254.250
```


> 如有侵权，请联系作者删除
