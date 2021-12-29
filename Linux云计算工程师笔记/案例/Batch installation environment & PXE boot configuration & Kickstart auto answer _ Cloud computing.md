@[TOC]( Batch installation environment & PXE boot configuration & Kickstart auto answer & Cobbler installation platform | Cloud computing )

---
# 1 案例1：配置并验证DHCP服务
## 1.1 问题
本例要求为PXE客户机提供地址分配服务，在主机 svr7 上搭建支持PXE的DHCP服务器，提供的地址参数如下：

- IP地址范围 192.168.4.10~200/24
- PXE引导服务器位于 192.168.4.7、引导文件 pxelinux.0

然后在主机 pc207 上使用dhclient命令测试 DHCP地址分配服务。

## 1.2 方案
DHCP地址分配的四次会话：DISCOVERY --> OFFER --> REQUEST -->ACK 。

DHCP服务器基本概念：

- DHCP租期：允许客户机租用IP地址的时间期限，单位为秒
- DHCP作用域：分配给客户机的IP地址所在的网段
- DHCP地址池：用来动态分配的IP地址的范围

DHCP服务端：软件包dhcp、系统服务dhcpd
DHCP服务端配置文件：/etc/dhcp/dhcpd.conf

传输协议及端口：UDP 67（服务器）、UDP 68（客户端）

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：配置DHCP服务端**

1）安装dhcp软件包
```shell
[root@svr7 ~]# yum  -y  install  dhcp
.. ..
```

2）建立dhcpd.conf服务配置
```shell
[root@svr7 ~]# vim  /etc/dhcp/dhcpd.conf
subnet 192.168.4.0 netmask 255.255.255.0 {
     range  192.168.4.10 192.168.4.200;
     next-server  192.168.4.7;
     filename  "pxelinux.0";
}
```
3）启动系统服务dhcpd，并设置开机自启
```shell
[root@svr7 ~]# systemctl  restart  dhcpd
[root@svr7 ~]# systemctl  enable  dhcpd
Created symlink from /etc/systemd/system/multi-user.target.wants/dhcpd.service to /usr/lib/systemd/system/dhcpd.service.
```
4）确认dhcpd服务状态
```shell
[root@svr7 ~]# netstat  -anptu  |  grep  dhcpd
udp        0      0 0.0.0.0:67              0.0.0.0:*                           58693/dhcpd         
.. ..
```
**步骤二：在客户端测试DHCP服务**

1）使用dhclient命令测试，观察获取IP地址的过程
```shell
[root@pc207 ~]# dhclient  -d  eth0
Internet Systems Consortium DHCP Client 4.2.5
Copyright 2004-2013 Internet Systems Consortium.
All rights reserved.
For info, please visit https://www.isc.org/software/dhcp/
.. ..
DHCPDISCOVER on eth0 to 255.255.255.255 port 67 interval 7 (xid=0x6707682f)
DHCPREQUEST on eth0 to 255.255.255.255 port 67 (xid=0x6707682f)
DHCPOFFER from 192.168.4.7
DHCPACK from 192.168.4.7 (xid=0x6707682f)
bound to 192.168.4.10 -- renewal in 18008 seconds.
^C                                   //按Ctrl+c键退出测试
```
2）若因操作异常导致IP故障，可恢复客户机原有IP配置
```shell
[root@pc207 ~]# pkill  -9  dhclient                      //杀死dhclient进程
[root@pc207 ~]# nmcli  connection  up  eth0              //激活原配置
.. ..
```
# 2. PXE基础装机环境
## 2.1 问题
本例要求为后续的PXE服务器构建提供Linux软件仓库，完成下列任务：

1. 部署Web目录/var/www/html/dvd
2. 挂载Linux光盘镜像文件到该目录
3. 访问 http://192.168.4.7/dvd测试，确保可用

## 2.2 方案
PXE网络装机的整体思路 —— 装机条件准备：

- 准备CentOS7安装源（HTTP方式YUM库）
- 启用DHCP服务

PXE网络装机的整体思路 —— PXE引导配置：

- 启用TFTP服务，提供装机用的内核、初始化文件
- 提供PXE引导程序、配置启动菜单

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：通过 HTTP 方式发布CentOS7软件源**

1）快速构建httpd服务器（若已构建，此步可跳过）
```shell
[root@room9pc13 ~]# yum  -y  install  httpd          //装包
[root@room9pc13 ~]# systemctl  restart  httpd         //启动服务
[root@room9pc13 ~]# systemctl  enable  httpd          //设置开机自启
```
2）准备yum仓库，部署到Web子目录
```shell
[root@room9pc13 ~]# mkdir  /var/www/html/dvd      //建挂载点
[root@room9pc13 ~]# vim  /etc/fstab
.. ..
/dev/cdrom  /var/www/html/dvd  iso9660  defaults  0  0
[root@room9pc13 ~]# mount  -a                         
[root@room9pc13 ~]# ls  /var/www/html/dvd/         //确认部署位置
```
**步骤二：确保yum仓库HTTP资源可用**

从浏览器访问http://192.168.4.7/dvd/，可看到仓库资源。

# 3. 配置PXE引导
## 3.1 问题
本例要求为PXE装机提供引导服务，并提供必要的素材，完成下列任务：

1. 启用TFTP服务器，部署引导文件（内核vmlinuz、初始文件initrd.img、网卡启动程序pxelinux.0）
2. 创建pxelinux.cfg/配置目录，在此目录下建立默认引导文件default

## 3.2 方案
TFTP，Trivial File Transfer Protocol：简单文件传输协议，通过UDP 69端口提供小文件的传输服务，默认应将资源部署到/var/lib/tftpboot目录下，不支持认证和目录访问等复杂FTP操作。

网卡启动程序pxelinux.0由软件包syslinux提供。

PXE安装用的内核及初始化文件可从CentOS7的光盘目录/images/pxeboot/下提取。

PXE启动配置相关资料可参考CentOS7的光盘目录/isolinux/，其中包括图形支持模块vesamenu.c32、背景图片spash.png、菜单配置文件isolinux.cfg（使用时改名为default）。

## 3.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：快速构建TFTP服务器**

1）安装tftp-server软件包
```shell
[root@svr7 ~]# yum -y install tftp-server 
.. ..
```
2）启动系统服务tftp，并设置开机自启
```shell
[root@svr7 ~]# systemctl  restart  tftp
```
**步骤二：部署启动文件**

1）拷贝pxelinux.0程序，部署到TFTP目录

在软件包syslinux提供的目录下找到pxelinux.0程序
```shell
[root@svr7 ~]# yum  -y  install  syslinux
[root@svr7 ~]# rpm  -ql  syslinux  |  grep pxelinux.0
/usr/share/syslinux/gpxelinux.0
/usr/share/syslinux/pxelinux.0
```
将其拷贝到/var/lib/tftpboot/目录下，确认部署结果：
```shell
[root@svr7 ~]# cp  /usr/share/syslinux/pxelinux.0  /var/lib/tftpboot/
[root@svr7 ~]# ls  /var/lib/tftpboot/
pxelinux.0
```
2）拷贝引导装机的内核、初始镜像，部署到TFTP目录

当文件较多时，可以在TFTP目录下创建子目录：
```shell
[root@svr7 ~]# mkdir  /var/lib/tftpboot/CentOS7
```
再通过CentOS7光盘目录找到PXE版内核vmlinuz、初始镜像initrd.img，将其拷贝到上述子目录：
```shell
[root@svr7 ~]# cd  /var/lib/tftpboot/CentOS7/
[root@svr7 CentOS7]# wget  http://192.168.4.7/dvd/isolinux/vmlinuz
[root@svr7 CentOS7]# wget  http://192.168.4.7/dvd/isolinux/initrd.img
                                              //下载内核、初始化文件
```
确认部署结果：
```shell
[root@svr7 pxeboot]# ls  -R  /var/lib/tftpboot/
/var/lib/tftpboot/:
pxelinux.0  CentOS7
/var/lib/tftpboot/CentOS7:
initrd.img  vmlinuz
```
**步骤三：配置启动菜单**

1）创建配置目录
```shell
[root@svr7 ~]# mkdir  /var/lib/tftpboot/pxelinux.cfg
```
2）以光盘中的isolinux目录为模板，拷贝必要的文件
```shell
[root@svr7 ~]# cd  /var/lib/tftpboot/
[root@svr7 tftpboot]# wget  http://192.168.4.7/dvd/isolinux/vesamenu.c32 
                                                      //提供图形支持
[root@svr7 tftpboot]# wget  http://192.168.4.7/dvd/isolinux/splash.png  
                                                            //准备背景图片
[root@svr7 tftpboot]# wget  -O  pxelinux.cfg/default  http://192.168.4.7/dvd/isolinux/isolinux.cfg 
                                                         //建立菜单配置
[root@svr7 isolinux]# ls  -R  /var/lib/tftpboot/          //确认部署结果
/var/lib/tftpboot/:
pxelinux.0  pxelinux.cfg  CentOS7  splash.png  vesamenu.c32
/var/lib/tftpboot/pxelinux.cfg:
default
/var/lib/tftpboot/CentOS7:
initrd.img  vmlinuz
```
3）调整启动参数
```shell
[root@svr7 ~]# vim  /var/lib/tftpboot/pxelinux.cfg/default
default vesamenu.c32                              //默认交给图形模块处理
timeout 600                                      //选择限时为60秒（单位1/10秒）
.. ..
menu title  PXE  Installation  Server             //启动菜单标题信息
.. ..
label  linux                                  //菜单项标签
    menu  label  ^Install CentOS7 Linux 7
    kernel  CentOS7/vmlinuz                      //内核的位置
    append  initrd=CentOS7/initrd.img  
                                                 //初始镜像、安装源位置
label local                                     //从硬盘启动
    menu  default                              //默认启动方式
    menu label Boot from ^local drive
    localboot 0xffff
menu  end
```
**步骤四：访问TFTP服务端确保可用**

1）在pc207上安装tftp命令工具
```shell
[root@pc207 ~]# yum  -y  install  tftp
.. ..
```
2）在pc207上访问svr7上的TFTP服务端，下载文件测试
```shell
[root@pc207 ~]# tftp  192.168.4.7  -c  get pxelinux.0
[root@pc207 ~]# ls  -lh  pxelinux.0                      //检查下载结果
-rw-r--r--. 1 root root 27K 1月  13 15:48 pxelinux.0
```

# 4. PXE+kickstart自动装机
## 4.1 问题
本例要求在PXE服务器上为CentOS7客户机准备ks应答文件，完成下列任务：

1. 实现全自动的安装及配置
2. 能够自动配好YUM仓库

然后在客户机上验证PXE+kickstart全自动装机过程：

1. 再次将测试客户机从PXE启动并安装
2. 完成后，重启客户机并验证结果

## 4.2 方案
使用图形配置工具system-config-kickstart来生成应答文件

## 4.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：准备应答文件**

找一台CentOS7系统的模板虚拟机，使用配置工具生成应答文件。

1）在模板机上安装system-config-kickstart软件包
```shell
[root@svr7 ~]# yum  -y  install  system-config-kickstart
.. ..
```
2）调整模板机的yum仓库设置

清理掉无关的yum源，只保留为客户机安装CentOS7系统所必要的yum源，并且将源的ID修改为development。
```shell
[root@svr7 ~]# vim  /etc/yum.repos.d/dvd.repo
[development]
name = CentOS Linux 7
baseurl = http://192.168.4.7/dvd
gpgcheck = 0
```
3）运行system-config-kickstart工具，创建应答文件

在支持图形程序的环境运行system-config-kickstart，即可打开该配置工具（如图-5所示）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/d51f785b3587496c8b68c5804addc4f5.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-5

通过“文件”菜单打开/root/anaconda-ks.cfg文件，作为应答配置模板，这样可以节省很多时间（如图-6所示）。根据需要确认默认语言、时区，设置根口令、磁盘分区规划等基本信息。

![在这里插入图片描述](https://img-blog.csdnimg.cn/c53101536b9840adafc2b656e8752a22.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-6

在安装方法部分，选择“执行新安装”，并正确设置HTTP安装源的访问地址信息（如图-7所示）。

/

图-7

在分区信息部分，选择清除主引导记录、删除所有现存分区、初始化磁盘标签，并手动添加/boot 200MB、SWAP分区 2000MB、/分区 所有剩余空间（如图-8所示）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/3c6fe26ac91c411193433b12b8158d97.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-8

在网络配置部分，确认已添加第一块网卡，设为DHCP自动获取（如图-9所示）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/6b1ac7e9774942dea8b30965c4617007.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-9

在防火墙配置部分，禁用SELinux、禁用防火墙（如图-10所示）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/5fe95055870b46998573e7782bc7f835.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-10

在软件包选择部分，根据客户机的实际需要定制。比如若要使用图形桌面环境，建议将GNOME相关的包勾选上（如图-11所示）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/698bf12a47774848aeb3c1f23ddaec47.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-11

确认上述调整后，通过“文件”菜单将其保存为/root/ks.cfg。

4）应答文件微调整

删除掉随模板机配置残留的不可用仓库记录（比如以repo --name开头的Server-HighAvailability、Server-ResilientStorage、autopart等行）
```shell
[root@svr7 ~]# vim  /root/ks.cfg
install                                                  //安装基本信息设置
xconfig  --startxonboot
keyboard --vckeymap=cn --xlayouts='cn'
rootpw --iscrypted $1$.48kBNVL$e.Ym0L/RzkJonYwbg9Brq1
timezone Asia/Shanghai
url --url="http://192.168.4.254/dvd"                  //安装源设置
lang zh_CN
firewall --disabled
#repo --name="Server-HighAvailability" --baseurl=file:///run/install/repo/addons/HighAvailability
#repo --name="Server-ResilientStorage" --baseurl=file:///run/install/repo/addons/ResilientStorage
#autopart --type=lvm                                      //分区设置
zerombr
clearpart --all --initlabel
part /boot --fstype="xfs" --size=200
part swap --fstype="swap" --size=2000
part / --fstype="xfs" --grow --size=1
.. ..
%post --interpreter=/bin/bash                          //安装后脚本设置
%end
%packages                                              //软件包设置
@^graphical-server-environment
@base
@core
@desktop-debugging
@development
.. ..
initial-setup
initial-setup-gui
-NetworkManager
-NetworkManager-team
.. ..
%end
```
**步骤二：部署应答文件**

1）将应答文件部署在客户机可访问的位置

部署并确认文件：
```shell
[root@room9pc13 ~]# cp  /root/ks.cfg  /var/www/html/
[root@room9pc13 ~]# ls  -lh  /var/www/html/ks.cfg          //检查部署的文件
-rw-r--r--. 1 root root 4.5K 1月  13 20:20 /var/www/html/ks.cfg
```
在客户端下载应答文件，确保可访问：
```shell
[root@pc207 ~]# wget  http://192.168.4.7/ks.cfg
.. ..
2017-01-13 20:22:19 (183 MB/s) - “ks.cfg” 已保存 [4508] 
[root@pc207 ~]# ls  -lh  ks.cfg                 //检查下载的文件
-rw-r--r--. 1 root root 4.5K 1月  13 20:22 ks.cfg
```
2）在PXE服务器上修改default引导配置，调用应答文件

找到相应的label启动项，在append后添加ks=应答文件地址，去掉原有的inst.stage2参数设置：
```shell
[root@svr7 ~]# vim  /var/lib/tftpboot/pxelinux.cfg/default
.. ..
label linux
    menu label ^Install CentOS7 Linux 7
    kernel CentOS7/vmlinuz
    append initrd=CentOS7/initrd.img ks=http://192.168.4.7/ks.cfg 
.. ..
```
**步骤三：验证PXE+kickstart自动应答**

1）新建一台虚拟机裸机，确认支持PXE网卡启动

新建一台虚拟机裸机，注意以下事项：将内存设为2G、硬盘设为20G；网络类型要与pxesverver服务器的相同，比如选择vmnet1。

2）启动虚拟机裸机，验证PXE网络安装过程

正常PXE引导，选择第一个启动项回车确认即快速进入全自动安装，后续过程基本无需人工干预（如图-13所示）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/c64feab1e5e246d7b9c919b3af90f058.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图-13


# Exercise
## 1 简述DHCP租期、作用域、地址池的含义
租期：允许客户机租用IP地址的时间期限，单位为秒
作用域：分配给客户机的IP地址所在的网段
地址池：用来动态分配的IP地址的范围

## 2 为了指引客户机访问PXE服务器，对应的DHCP配置是什么
需要告知客户机TFTP引导服务器的地址、需要下载的启动文件名：
```shell
next-server  192.168.4.7;          //PXE引导服务器
filename  "pxelinux.0";             //引导文件名
```
## 3 PXE服务器提供vmlinuz和initrd.img文件的作用分别是什么
vmlinuz：为将要安装的客户机系统提供引导，并加载安装程序；

initrd.img：为在客户机上加载并运行vmlinuz内核提供临时的Linux环境。

## 4 简要说明PXE装机引导的基本过程

1. 客户端向DHCP服务器请求分配IP地址；
2. DHCP服务器为客户端分配IP地址，告知Boot server；
3. 客户端向Boot server请求下载启动文件；
4. Boot server向客户端提供启动文件；
5. 客户端向文件共享服务器请求应答文件；
6. 客户端根据应答文件信息，安装操作系统。

## 5 使用system-config-kickstart工具时需要注意什么

注意事项：

1）运行此工具的客户机最好与将要安装的客户机使用相同的操作系统。

2）仅配置对应的YUM源，源ID设为 development。

3）可以加载应答文件模板/root/anaconda-ks.cfg再修改，提高效率。

> 如有侵权，请联系作者删除
