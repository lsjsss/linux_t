# Day1

Linux系统简介

Linux是一种操作系统!!

操作系统:一堆软件的集合,让计算机的硬件正常工作

Unix/Linux发展史

• UNIX诞生,1970-1-1                                     

• Linux之父,Linus Torwalds
– 1991年10月,发布0.02版(第一个公开版)内核
– 1994年03月,发布1.0版内核
– 标准读音: 哩呐科斯

     内核:合理控制众多硬件
    
    用户------>内核-------->硬件
    版本号:主版本.次版本.修订号

Linux发行版本
• 发行版的名称/版本由发行方决定
– Red Hat Enterprise Linux 5/6/7
– Suse Linux Enterprise 12
– Debian Linux 7.8
– Ubuntu Linux 14.10/15.04

Red Hat系列版本
• 红帽 Linux 企业版
– 简称RHEL(Red Hat Enterprise Linux)
– http://www.redhat.com/

• Fedora Core 社区版
– http://fedoraproject.org/

• CentOS,社区企业操作系统
– Community Enterprise Operating System
– http://www.centos.org/

#################################################
利用虚拟机安装Linux系统
1.建立一台全新的虚拟机
  Ctrl+ALT=鼠标回到真机

2.Linux目录结构    树型结构                   

    根目录(/):Linux系统起点(所有数据都在此目录下)
    /dev:存放设备(键盘 鼠标  显示器 硬盘......)相关的数据

磁盘表示方式
目录名+磁盘名字

​		

hd,表示IDE设备
sd,表示SCSI设备

  /dev/hda:第一块IDE设备         /dev/hdb:第二块IDE设备
  /dev/sda:第一块SCSI设备       /dev/sdb:第二块SCSI设备

##################################################
利用root管理员进行登录虚拟机CentOS7

获取命令行界面
• 虚拟控制台切换( Ctrl + Alt + Fn 组合键)
– tty1:图形桌面
– tty2~tty6:字符控制台

图形获取命令行界面:鼠标右击空白处---->打开终端

#####################################################
• 命令行提示标识的含义
– [当前用户@主机名    当前所在的目录]$



– 若当前用户是root,则最后一个字符为 #
[root@svr7 桌面]#
– 否则,最后一个字符为 $
[teacher@svr7 桌面]$

快捷键：
放大字体：Ctrl+Shift+
缩小字体：Ctrl- 


##################################################


查看及切换目录
• pwd — Print Working Directory
– 用途:查看当前工作目录

• cd — Change Directory
– 用途:切换工作目录
– 格式:cd [目标文件夹位置]

• ls — List
– 格式:ls [选项]... [目录或文件名]...
蓝色:目录    黑色:文本文件

	[root@localhost ~]# pwd             #显示当前所在位置
	[root@localhost ~]# cd   /          #切换到根目录
	[root@localhost /]# pwd 
	[root@localhost /]# ls              #显示当前目录下内容
	[root@localhost /]# cd    /root     #切换到root目录
	[root@localhost ~]# pwd
	[root@localhost ~]# ls
	[root@localhost ~]# cd /home
	[root@localhost home]# pwd
	[root@localhost home]# ls
	[root@localhost home]# cd /boot
	[root@localhost boot]# pwd
	[root@localhost boot]# ls
	[root@localhost /]# ls  /home
	[root@localhost /]# ls  /abc
	[root@localhost /]# ls  /root
	[root@localhost /]# ls /root/anaconda-ks.cfg


​		
查看文本文件内容:

cat   
格式：cat    [目标文件]
		
		# cat /root/anaconda-ks.cfg


	查看系统版本信息
	# cat   /etc/redhat-release 
	CentOS Linux release 7.5.1804 (Core) 
	
	快捷键：TAB键：自动补齐命令
	
	查看CPU信息，查看内存
	# lscpu 
	# cat   /proc/cpuinfo
	# cat   /proc/meminfo






查看主机名和IP地址	
	# hostname
	 # hostname A.tedu.cn                  #修改主机名为A.tedu.cn(临时设置)
   	# hostname
  	# exit
	注：新开一个终端验证

	 # ifconfig
	 # ifconfig ens33 192.168.4.2/24     #修改ens33IP地址为192.168.4.2(临时设置)
	# ifconfig



创建目录和文本文件
mkdir--Make   Directory
格式：mkdir    [/路径/目录名]


[root@A ~]# pwd
[root@A ~]# mkdir abc              #创建abc目录
[root@A ~]# ls
[root@A ~]# ls /root
[root@A ~]# mkdir /def
[root@A ~]# ls def
[root@A ~]#  ls /def
[root@A ~]#  ls /
[root@A ~]# touch a.txt                  #创建a.txt文件
[root@A ~]#  ls
[root@A ~]#   touch /b.txt
[root@A ~]#  ls /b.txt 
[root@A ~]# cat /b.txt
[root@A ~]# 


关机与重启：

poweroff               #关机

reboot                 #重启



# Day2

Linux的目录结构

/(根目录)： Linux的起点（存放所有数据）
/dev:    存放所有设备（键盘、鼠标、显示器、硬盘.....）的文件

磁盘表示方法：设备所在目录+磁盘名

/dev/hde5:  第五块IDE设备第5个分区
/dev/hdd4:  第四块IDE设备第4个分区
/dev/sdb3:  第二块SCSI设备第3个分区
/dev/sde2:  第五块SCSI设备第2个分区

第三块IDE设备第4个分区表示方式：/dev/hdc4
+++++++++++++++++++++++++++++++++++++++++++++++++++++
蓝色：目录
黑色：文本文件
绿色：可执行程序

查看文本文件内容：cat
格式：cat    文件名

[root@localhost /]# cat /etc/passwd

less：分屏阅读工具
格式： less    文件名
支持上下键翻页，查看完按  q  键  退出

[root@localhost /]#  less  /etc/passwd

查看系统版本信息：
[root@localhost /]# cat /etc/redhat-release 
CentOS Linux release 7.5.1804 (Core) 
[root@localhost /]# 

查看CPU信息：
 [root@localhost /]# cat /proc/cpuinfo 
 [root@localhost /]# lscpu

查看内存信息：
 [root@localhost /]# cat /proc/meminfo

查看主机名：
[root@localhost /]# hostname
localhost.localdomain
[root@localhost /]# hostname A.tedu.cn                     #新开一个终端验证
[root@localhost /]# hostname
[root@localhost /]#        

查看IP地址：
[root@localhost /]# ifconfig 
[root@localhost /]#  ifconfig  ens33
[root@localhost /]#  ifconfig  ens33 192.168.4.1/24              #临时设置IP地址为192.168.4.1
[root@localhost /]#  ifconfig  ens33

创建文档

创建目录：mkdir ---------Make   Directory  
格式：mkdir     [/路径/]目录名

[root@A ~]# mkdir abc
[root@A ~]# ls /root/
[root@A ~]# mkdir /opt/abc
[root@A ~]# ls /opt/
[root@A ~]# ls /opt/abc/
[root@A ~]# 

创建文本文件（新建空文件）：touch   
格式：touch     [/路径/]文件名

[root@A ~]# touch a.txt
[root@A ~]# touch /opt/b.txt
[root@A ~]# cat /opt/b.txt
[root@A ~]# 

文本内容操作：
格式： head   -n  数字   文件名                                    #查看文件的前n行内容
            tail   -n  数字   文件名                                       # 查看文件的后n行内容
注：1）-n  数字可以简写为 -数字
       2）不加数字默认查看的是前10行内容和后10行内容

[root@A ~]# head -2 /etc/passwd                       #查看 /etc/passwd文件前2行内容
[root@A ~]# tail -2 /etc/passwd                          #查看/etc/passwd文件后2行内容

grep工具：
用途：输出包含指定字符串的行
格式：grep     '查找条件'         文件名

[root@A ~]# grep 'root'  /etc/passwd
root:x:0:0:root:/root:/bin/bash
operator:x:11:0:operator:/root:/sbin/nologin
[root@A ~]# 

关机和重启
[root@A ~]#  poweroff
[root@A ~]#  reboot















