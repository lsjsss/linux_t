@[TOC]( Configure the Linux network & log management | Cloud computing )

---
# 1. 搭建Yum仓库
## 1.1 问题
1. 在根下创建/mydvd目录
2. 将CentOS光盘镜像挂载到/mydvd目录
3. 编辑客户端配置文件，完成Yum仓库搭建
4. 利用Yum安装lftp
5. 利用/etc/fstab文件，实现开机自动挂载

## 1.2 方案
在真机搭建Yum仓库服务端时，真机是没有光驱设备的。我们采用的方法是，直接挂载光盘ISO镜像文件，挂载时要加上必要的参数“loop”，其命令为：
```shell
mount      /ISO/CentOS7-1804.iso  /mydvd/
```
利用命令挂载，是临时生效的。所以要写入“fstab”文件中实现永久开机挂载。配置文件/etc/fstab里，各个字段的意义一定要熟悉：
```shell
设备文件  类型  挂载参数  备份标记  检测顺序
```
本实验挂载的对象是ISO镜像：
```shell
/ISO/CentOS7-1804.iso  /Mydvd  iso9660 defaults 0 0
```

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：创建/Mydvd目录**

命令操作如下所示：
```shell
[root@svr7 ~]# mkdir /mydvd
[root@svr7 ~]# ls -ld /mydvd/
drwxr-xr-x. 2 root root 4096 5月  11 15:12 /Mydvd/
[root@svr7 ~]#
```

**步骤二：挂载光盘ISO镜像**

命令操作如下所示：
```shell
[root@svr7 ~]#mount  /ISO/CentOS7-1804.iso  /mydvd/
[root@svr7 ~]# ls /mydvd/
EFI               Packages                  RELEASE-NOTES-pa-IN.html
EULA              README                    RELEASE-NOTES-pt-BR.html
EULA_de           RELEASE-NOTES-as-IN.html  RELEASE-NOTES-ru-RU.html
……
 [root@svr7 ~]#
 ```
**步骤三：配置Yum客户端配置文件**

命令操作如下所示：
```shell
[root@svr7 /]# cd /etc/yum.repos.d/
[root@svr7 yum.repos.d]# cp rhel-source.repo centos6.5.repo
[root@svr7 yum.repos.d]# vim centos6.5.repo
[rhel-CentOS]
name=CentOS
baseurl=file:///mydvd
enabled=1
gpgcheck=0                      //必须有此字段，若不检测软件签名则“gpgkey”配置可不写
[root@svr7 yum.repos.d]# yum  repolist 
```
**步骤四：安装常用软件lftp，此软件为访问ftp的客户端软件**

命令操作如下所示：
```shell
[root@svr7 /]# yum -y install  lftp
```
**步骤五：利用/etc/fstab文件，实现开机自动挂载**

命令操作如下所示：
```shell
[root@svr7 /]# tail -n 1 /etc/fstab
/ISO/CentOS7-1804.iso  /mydvd  iso9660 defaults 0 0
[root@svr7 /]#
```

# 2. 系统日志分析
## 2.1 问题
本例要求熟悉Linux系统中的常见日志文件，使用必要的命令工具完成下列任务：

 1. 列出所有包含关键词8909的系统日志消息
 2. 查看启动时识别的鼠标设备信息
 3. 列出最近2条成功/不成功的用户登录消息
 4. 列出最近10条重要程度在 ERR 及以上的日志消息
 5. 列出所有与服务httpd相关的消息
 6. 列出前4个小时内新记录的日志

## 2.2 方案
常见的系统日志及各自用途：

- /var/log/messages，记录内核消息、各种服务的公共消息
- /var/log/dmesg，记录系统启动过程的各种消息
- /var/log/cron，记录与cron计划任务相关的消息
- /var/log/maillog，记录邮件收发相关的消息
- /var/log/secure，记录与访问限制相关的安全消息

日志消息的优先级（高-->低）：
- EMERG（紧急）：级别0，系统不可用的情况
- ALERT（警报）：级别1，必须马上采取措施的情况
- CRIT（严重）：级别2，严重情形
- ERR（错误）：级别3，出现错误
- WARNING（警告）：级别4，值得警告的情形
- NOTICE（注意）：级别5，普通但值得引起注意的事件
- INFO（信息）：级别6，一般信息
- DEBUG（调试）：级别7，程序/服务调试消息

RHEL7提供的journalctl日志工具的常见用法：
- journalctl | grep 关键词
- journalctl -u 服务名 -p 优先级
- journalctl -n 消息条数
- journalctl --since="yyyy-mm-dd HH:MM:SS" --until="yyyy-mm-dd HH:MM:SS"
## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：分析系统日志及用户日志**

1）列出所有包含关键词8909的系统日志消息

简单模拟一个故障（SELinux阻止Web开放8909端口）：
```shell
[root@svr7 ~]# vim  /etc/httpd/conf.d/8909.conf          //添加开8909端口配置
Listen 8909
[root@svr7 ~]# setenforce 1                             //开启强制模式
[root@svr7 ~]# systemctl  restart  httpd                 //起服务失败
Job for httpd.service failed because the control process exited with error code. See "systemctl status httpd.service" and "journalctl -xe" for details.
```
从日志文件/var/log/messages中检索信息：
```shell
[root@svr7 ~]# grep  8909  /var/log/messages 
Jan  6 17:53:48 svr7 setroubleshoot: SELinux is preventing /usr/sbin/httpd from name_bind access on the tcp_socket port 8909. For complete SELinux messages. run sealert -l 6d37b8f0-ab8a-4082-9295-c784f4f57190
Jan  6 17:53:48 svr7 python: SELinux is preventing /usr/sbin/httpd from name_bind access on the tcp_socket port 8909.#012#012*****  Plugin bind_ports (92.2 confidence) suggests   ************************#012#012If you want to allow /usr/sbin/httpd to bind to network port 8909#012Then you need to modify the port type.#012Do#012# semanage port -a -t PORT_TYPE -p tcp 8909#012    where PORT_TYPE is one of the following: http_cache_port_t, http_port_t, jboss_management_port_t, jboss_messaging_port_t, ntop_port_t, puppet_port_t.#012#012*****  Plugin catchall_boolean (7.83 confidence) suggests   ******************#012#012If you want to allow nis to enabled#012Then you must tell SELinux about this by enabling the 'nis_enabled' boolean.#012#012Do#012setsebool -P nis_enabled 1#012#012*****  Plugin catchall (1.41 confidence) suggests   **************************#012#012If you believe that httpd should be allowed name_bind access on the port 8909 tcp_socket by default.#012Then you should report this as a bug.#012You can generate a local policy module to allow this access.#012Do#012allow this access for now by executing:#012# grep httpd /var/log/audit/audit.log | audit2allow -M mypol#012# semodule -i mypol.pp#012
.. ..
```

使用完毕记得删除测试配置文件：
```shell
[root@svr7 ~]# rm  -rf  /etc/httpd/conf.d/8909.conf
[root@svr7 ~]# systemctl  restart  httpd
```
2）查看启动时识别的鼠标设备信息
```shell
[root@svr7 ~]# dmesg  |  grep  -i  mouse
[    1.020385] mousedev: PS/2 mouse device common for all mice
[    1.249422] input: ImPS/2 Generic Wheel Mouse as /devices/platform/i8042/serio1/input/input2
[    2.279665] usb 2-1: Product: VMware Virtual USB Mouse
[    2.603999] input: VMware VMware Virtual USB Mouse as /devices/pci0000:00/0000:00:11.0/0000:02:00.0/usb2/2-1/2-1:1.0/input/input3
[    2.604222] hid-generic 0003:0E0F:0003.0001: input,hidraw0: USB HID v1.10 Mouse [VMware VMware Virtual USB Mouse] on usb-0000:02:00.0-1/input0
```
3）列出最近2条成功/不成功的用户登录消息

查看成功登录的事件消息：
```shell
[root@svr7 ~]# last  -2
zhsan    pts/2        192.168.4.207    Fri Jan  6 18:00 - 18:00  (00:00)    
root     pts/2        192.168.4.110    Fri Jan  6 17:26 - 17:59  (00:33)    
wtmp begins Thu Aug  4 00:10:16 2016
```
查看失败登录的事件消息：
```shell
[root@svr7 ~]# lastb  -2
anonymou ssh:notty    192.168.4.207    Fri Jan  6 18:00 - 18:00  (00:00)    
anonymou ssh:notty    192.168.4.207    Fri Jan  6 18:00 - 18:00  (00:00)    
btmp begins Fri Jan  6 18:00:34 2017
```
**步骤二：使用journalctl日志提取工具**

1）列出最近10条重要程度在 ERR 及以上的日志消息
```shell
[root@svr7 ~]# journalctl  -p err  -n  10
-- Logs begin at Thu 2017-01-05 15:50:08 CST, end at Fri 2017-01-06 18:01:01 CST. --
Jan 06 14:56:57 svr7 setroubleshoot[23702]: SELinux is preventing /usr/sbin/vsftpd from getattr access on the file /rhel7/repodata/repomd.xml. For complete SELinux mes
Jan 06 14:56:57 svr7 setroubleshoot[23702]: SELinux is preventing /usr/sbin/vsftpd from read access on the file repomd.xml. For complete SELinux messages. run sealert 
Jan 06 14:56:57 svr7 setroubleshoot[23702]: SELinux is preventing /usr/sbin/vsftpd from read access on the file repomd.xml. For complete SELinux messages. run sealert 
Jan 06 14:56:57 svr7 setroubleshoot[23702]: SELinux is preventing /usr/sbin/vsftpd from lock access on the file /rhel7/repodata/repomd.xml. For complete SELinux messag
Jan 06 17:53:48 svr7 setroubleshoot[33743]: Plugin Exception restorecon_source
Jan 06 17:53:48 svr7 setroubleshoot[33743]: SELinux is preventing /usr/sbin/httpd from name_bind access on the tcp_socket port 8909. For complete SELinux messages. run
Jan 06 17:53:53 svr7 setroubleshoot[33743]: SELinux is preventing /usr/sbin/httpd from name_connect access on the tcp_socket port 8909. For complete SELinux messages. 
Jan 06 17:53:54 svr7 systemd[1]: Failed to start The Apache HTTP Server.
.. ..
lines 1-11/11 (END)
```
2）列出所有与服务httpd相关的消息
```shell
[root@svr7 ~]# journalctl   -u  httpd
-- Logs begin at Thu 2017-01-05 15:50:08 CST, end at Fri 2017-01-06 18:01:01 CST. --
Jan 06 14:57:16 svr7 systemd[1]: Starting The Apache HTTP Server...
Jan 06 14:57:16 svr7 httpd[23812]: AH00557: httpd: apr_sockaddr_info_get() failed for svr7
Jan 06 14:57:16 svr7 httpd[23812]: AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 127.0.0.1. Set the 'ServerName' directi
Jan 06 14:57:16 svr7 systemd[1]: Started The Apache HTTP Server.
Jan 06 17:53:44 svr7 systemd[1]: Stopping The Apache HTTP Server...
Jan 06 17:53:46 svr7 systemd[1]: Starting The Apache HTTP Server...
Jan 06 17:53:46 svr7 httpd[33741]: AH00557: httpd: apr_sockaddr_info_get() failed for svr7
.. ..
```
3）列出前4个小时内新记录的日志

根据当前日期时间往前推4个小时，确定--since起始和--until结束时刻:
```shell
[root@svr7 ~]# journalctl  --since  "2017-01-06 14:11"  --until  "2017-01-06 18:11"
-- Logs begin at Thu 2017-01-05 15:50:08 CST, end at Fri 2017-01-06 18:10:01 CST. --
Jan 06 14:20:01 svr7 systemd[1]: Started Session 160 of user root.
Jan 06 14:20:01 svr7 CROND[22869]: (root) CMD (/usr/lib64/sa/sa1 1 1)
Jan 06 14:20:01 svr7 systemd[1]: Starting Session 160 of user root.
Jan 06 14:30:01 svr7 systemd[1]: Started Session 161 of user root.
Jan 06 14:30:01 svr7 CROND[23028]: (root) CMD (/usr/lib64/sa/sa1 1 1)
Jan 06 14:31:39 svr7 systemd[1]: Starting Session 162 of user root.
Jan 06 14:32:17 svr7 sshd[23046]: pam_unix(sshd:session): session closed for user root
Jan 06 14:31:39 svr7 systemd[1]: Started Session 162 of user root.
Jan 06 14:31:39 svr7 sshd[23046]: pam_unix(sshd:session): session opened for user root by (uid=0)
Jan 06 14:31:39 svr7 systemd-logind[985]: New session 162 of user root.
.. .
```

# Exercise
##  1 Linux网络管理的一些常用命令。
> 以下列出了Linux网络管理的一些常用命令，请写出各自的作用。
ifconfig （ ）
hostname （ ）
route （ ）
ping （ ）


查看网络接口信息，临时调整IP地址、关闭或启用接口
查看及设置本机的主机名
查看及设置本机的路由表条目，包括默认网关
测试从本机到目标主机的网络连通性
## 2 SSH协议简介。
> OpenSSH服务器使用的协议、默认端口、主配置文件分别是什么？SSH与Telnet应用的区别在哪里？

OpenSSH使用TCP协议，默认端口是22，主配置文件/etc/ssh/sshd_config。

SSH的英文全称是Secure SHell，即安全外壳。SSH会把传输过程中的数据加密，且支持压缩以提高传输速度；而Telnet在网络上以明文传送口令和数据，安全级别低，容易受到攻击。
> 如有侵权，请联系作者删除
