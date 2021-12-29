@[TOC]( Software package management & Systemd service management & VPN server | Cloud computing )

---
# 1. 制作nginx的RPM包
## 1.1 问题
本案例使用nginx-1.12.2版本的源码软件，生成对应的RPM包软件，具体要求如下：

软件名称为nginx

软件版本为1.12.2

RPM软件包可以查询描述信息

RPM软件包可以安装及卸载

## 1.2 方案
安装rpm-build软件包，编写SPEC配置文件，创建新的RPM软件包。

配置文件中的描述信息如表-1：

表－1 SPEC描述信息

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：安装rpm-build软件**

1）安装rpm-build软件包
```shell
[root@web1 ~]# yum -y install  rpm-build
```
2）生成rpmbuild目录结构
```shell
[root@web1 ~]# rpmbuild -ba nginx.spec                //会报错，没有文件或目录
[root@web1 ~]# ls /root/rpmbuild                    //自动生成的目录结构
BUILD  BUILDROOT  RPMS  SOURCES  SPECS  SRPMS
```
3）准备工作，将源码软件复制到SOURCES目录
```shell
[root@web1 ~]# cp nginx-1.12.2.tar.gz /root/rpmbuild/SOURCES/
```
4）创建并修改SPEC配置文件
```shell
[root@web1 ~]# vim /root/rpmbuild/SPECS/nginx.spec 
Name:nginx                                        #源码包软件名称
Version:1.12.2                                    #源码包软件的版本号
Release:    10                                        #制作的RPM包版本号
Summary: Nginx is a web server software.            #RPM软件的概述    
License:GPL                                        #软件的协议
URL:    www.test.com                                    #网址
Source0:nginx-1.12.2.tar.gz                        #源码包文件的全称
#BuildRequires:                                    #制作RPM时的依赖关系
#Requires:                                        #安装RPM时的依赖关系
%description
nginx [engine x] is an HTTP and reverse proxy server.    #软件的详细描述
%post
useradd nginx                               #非必需操作：安装后脚本(创建账户)
%prep
%setup -q                                #自动解压源码包，并cd进入目录
%build
./configure
make %{?_smp_mflags}
%install
make install DESTDIR=%{buildroot}
%files
%doc
/usr/local/nginx/*                    #对哪些文件与目录打包
%changelog
```
**步骤二：使用配置文件创建RPM包**

1）安装依赖软件包
```shell
[root@web1 ~]# yum -y install  gcc  pcre-devel openssl-devel
```
2）rpmbuild创建RPM软件包
```shell
[root@web1 ~]# rpmbuild -ba /root/rpmbuild/SPECS/nginx.spec
[root@web1 ~]# ls /root/rpmbuild/RPMS/x86_64/nginx-1.12.2-10.x86_64.rpm
```
**步骤三：安装软件**
```shell
[root@web1 ~]# yum install /root/rpmbuild/RPMS/x86_64/nginx-1.12.2-10.x86_64.rpm 
[root@web1 ~]# rpm -qa |grep nginx
[root@web1 ~]# ls /usr/local/nginx/
```
# 2. 配置GRE VPN
## 2.1 问题
本案例要求搭建一个GRE VPN环境，并测试该VPN网络是否能够正常通讯，要求如下：

- 启用内核模块ip_gre
- 创建一个虚拟VPN隧道(10.10.10.0/24)
- 实现两台主机点到点的隧道通讯

## 2.2 方案
使用lsmod查看当前计算机已经加载的模块，使用modprobe加载Linux内核模块，使用modinfo可以查看内核模块的信息。

准备实验所需的虚拟机环境，实验环境所需要的主机及对应的IP设置列表如表-1所示，正确配置IP地址、主机名称，并且为每台主机配置YUM源。

表－1 主机列表
![在这里插入图片描述](https://img-blog.csdnimg.cn/ae2ef4015fc94be0973b594c7fae7e7e.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)


实验拓扑如图-1所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/029d16b00536439cb7a19f5546adea06.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-1

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：启用GRE模块（client和proxy都需要操作）**

1）查看计算机当前加载的模块
```shell
[root@client ~]# lsmod                        //显示模块列表
[root@client ~]# lsmod  | grep ip_gre            //确定是否加载了gre模块
```
2)加载模块ip_gre
```shell
[root@client ~]# modprobe  ip_gre 
```
3）查看模块信息
```shell
[root@client ~]# modinfo ip_gre
filename:       /lib/modules/3.10.0-693.el7.x86_64/kernel/net/ipv4/ip_gre.ko.xz
… …  
```
**步骤二：Client主机创建VPN隧道**

1）创建隧道
```shell
[root@client ~]# ip tunnel add tun0  mode gre \ 
>  remote 201.1.2.5 local 201.1.2.10
//ip tunnel add创建隧道（隧道名称为tun0），ip tunnel help可以查看帮助
//mode设置隧道使用gre模式
//local后面跟本机的IP地址，remote后面是与其他主机建立隧道的对方IP地址
```
2）启用该隧道（类似与设置网卡up）
```shell
[root@client ~]# ip link show
[root@client ~]# ip link set tun0 up         //设置UP
[root@client ~]# ip link show
```
3）为VPN配置隧道IP地址
```shell
[root@client ~]# ip addr add 10.10.10.10/24 peer 10.10.10.5/24 \
>  dev tun0
//为隧道tun0设置本地IP地址（10.10.10.10.10/24）
//隧道对面的主机IP的隧道IP为10.10.10.5/24
[root@client ~]# ip a s                      //查看IP地址
```
**步骤三：Proxy主机创建VPN隧道**

1）查看计算机当前加载的模块
```shell
[root@client ~]# lsmod                        //显示模块列表
[root@client ~]# lsmod  | grep ip_gre            //确定是否加载了gre模块
```
2)加载模块ip_gre
```shell
[root@client ~]# modprobe  ip_gre
```
3）创建隧道
```shell
[root@proxy ~]# ~]# ip tunnel add tun0  mode gre \ 
>  remote 201.1.2.10 local 201.1.2.5
//ip tunnel add创建隧道（隧道名称为tun0），ip tunnel help可以查看帮助
//mode设置隧道使用gre模式
//local后面跟本机的IP地址，remote后面是与其他主机建立隧道的对方IP地址
```
4）启用该隧道（类似与设置网卡up）
```shell
[root@proxy ~]# ip a  s
[root@proxy ~]# ip link set tun0 up         //设置UP
[root@proxy ~]# ip a  s
```
5）为VPN配置隧道IP地址
```shell
[root@proxy ~]# ip addr add 10.10.10.5/24 peer 10.10.10.10/24 \
>  dev tun0
//为隧道tun0设置本地IP地址（10.10.10.10.5/24）
//隧道对面的主机IP的隧道IP为10.10.10.10/24
[root@proxy ~]# ip a s                      //查看IP地址
```
6)测试连通性
```shell
[root@client ~]#  ping 10.10.10.5
[root@proxy ~]#   ping 10.10.10.10
```
# 3. 创建PPTP VPN
## 3.1 问题
本案例要求搭建一个PPTP VPN环境，并测试该VPN网络是否能够正常通讯，要求如下:

- 使用PPTP协议创建一个支持身份验证的隧道连接
- 使用MPPE对数据进行加密
- 为客户端分配192.168.3.0/24的地址池
- 客户端连接的用户名为jacob，密码为123456

## 3.2 方案
准备实验所需的虚拟机环境，实验环境所需要的主机及对应的IP设置列表如表-2所示，正确配置IP地址、主机名称，并且为每台主机配置YUM源。

表－2 主机列表
![在这里插入图片描述](https://img-blog.csdnimg.cn/ce05726ecea94731af23b4efac36d851.png)
实验拓扑如图-2所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/3c96f8290d05495caa939ec57e642af0.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-2

## 3.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：部署VPN服务器**

1）安装软件包（软件包参考lnmp_soft/vpn/）
```shell
[root@proxy ~]# yum install pptpd-1.4.0-2.el7.x86_64.rpm
[root@proxy ~]# rpm -qc pptpd
/etc/ppp/options.pptpd
/etc/pptpd.conf
/etc/sysconfig/pptpd
```
2)修改配置文件
```shell
[root@proxy ~]# vim /etc/pptpd.conf
.. ..
localip 201.1.2.5                                    //服务器本地IP
remoteip 192.168.3.1-50                            //分配给客户端的IP池
[root@proxy ~]# vim /etc/ppp/options.pptpd
require-mppe-128                                    //使用MPPE加密数据
ms-dns 8.8.8.8                                    //DNS服务器
[root@proxy ~]# vim /etc/ppp/chap-secrets            //修改账户配置文件
jacob           *               123456      *
//用户名     服务器名称    密码      客户端IP
```
3）启动服务
```shell
[root@proxy ~]# systemctl start pptpd
[root@proxy ~]# systemctl enable pptpd
```
4）翻墙设置（非必需操作）
```shell
[root@proxy ~]# echo "1" > /proc/sys/net/ipv4/ip_forward    //开启路由转发
[root@proxy ~]# iptables -t nat -A POSTROUTING -s 192.168.3.0/24 \
>  -j SNAT --to-source 201.1.2.5
```
**步骤二：客户端设置**

启动一台Windows虚拟机，将虚拟机网卡桥接到public2，配置IP地址为201.1.2.20。

新建网络连接（具体操作如图-3所示），输入VPN服务器账户与密码（具体操作如图-4所示），连接VPN并测试网络连通性（如图-5所示）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/dbd46844b22744fb8a0dd6304cea0e90.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-3

![在这里插入图片描述](https://img-blog.csdnimg.cn/7dce6bd2cefd4d27b0e0fb7c55501d17.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-4

![在这里插入图片描述](https://img-blog.csdnimg.cn/b393d20d748c4957bfedbf8374851656.png)
图-5

# 4. 创建L2TP+IPSec VPN
## 4.1 问题
本案例要求搭建一个L2TP+IPSec VPN环境，并测试该VPN网络是否能够正常通讯，具体要求如下：

- 使用L2TP协议创建一个支持身份验证与加密的隧道连接
- 使用IPSec对数据进行加密
- 为客户端分配192.168.3.0/24的地址池
- 客户端连接的用户名为：jacob，密码为：123456
- 预共享密钥为：randpass

## 4.2 方案
准备实验所需的虚拟机环境，实验环境所需要的主机及对应的IP设置列表如表-3所示，正确配置IP地址、主机名称，并且为每台主机配置YUM源。

表－3 主机列表
![在这里插入图片描述](https://img-blog.csdnimg.cn/187e7659d24c4713bda8bc86e58fe420.png)

实验拓扑如图-6所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/db25f10da9f24bac82b87eee943de40f.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-6

## 4.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：部署IPSec服务**

1）安装软件包
```shell
[root@client ~]# yum -y install libreswan
```
2)新建IPSec密钥验证配置文件
```shell
[root@client ~]# cat /etc/ipsec.conf                //仅查看一下该主配置文件
.. ..
include /etc/ipsec.d/*.conf                    //加载该目录下的所有配置文件
[root@client ~]# vim /etc/ipsec.d/myipsec.conf            
//新建该文件，参考lnmp_soft/vpn/myipsec.conf    
conn IDC-PSK-NAT
    rightsubnet=vhost:%priv                        
    also=IDC-PSK-noNAT
conn IDC-PSK-noNAT
    authby=secret                                    //加密认证
        ike=3des-sha1;modp1024                        //加密算法
        phase2alg=aes256-sha1;modp2048                //加密算法
    pfs=no
    auto=add
    keyingtries=3
    rekey=no
    ikelifetime=8h
    keylife=3h
    type=transport
    left=201.1.2.10                                //重要，服务器本机的外网IP
    leftprotoport=17/1701
    right=%any                                    //允许任何客户端连接
    rightprotoport=17/%any
```
3)创建IPSec预定义共享密钥
```shell
[root@client ~]# vim /etc/ipsec.secrets                 //修改该文件
include /etc/ipsec.d/*.secrets
201.1.2.10   %any:    PSK    "randpass"                 //randpass为预共享密钥
//201.1.2.10是VPN服务器的IP
//%any:任何客户端都可以连接服务器
//PSK（pre share key）中文预共享密钥
```
4)启动IPSec服务
```shell
[root@client ~]# systemctl start ipsec        
[root@client ~]# netstat -ntulp |grep 500
udp        0      0 127.0.0.1:4500          0.0.0.0:*           3148/pluto          
udp        0      0 192.168.4.10:4500      0.0.0.0:*           3148/pluto          
udp        0      0 201.1.2.10:4500         0.0.0.0:*           3148/pluto          
udp        0      0 127.0.0.1:500           0.0.0.0:*           3148/pluto          
udp        0      0 192.168.4.10:500       0.0.0.0:*           3148/pluto          
udp        0      0 201.1.2.10:500          0.0.0.0:*           3148/pluto          
udp6       0      0 ::1:500                 :::*                 3148/pluto
```
**步骤二：部署XL2TP服务**

1）安装软件包（软件包参考lnmp_soft/vpn/）
```shell
[root@client ~]# yum  install xl2tpd-1.3.8-2.el7.x86_64.rpm
```
2) 修改xl2tp配置文件（修改3个配置文件的内容）
```shell
[root@client ~]#  vim  /etc/xl2tpd/xl2tpd.conf                //修改主配置文件
[global]
.. ..    
[lns default]
.. ..
ip range = 192.168.3.128-192.168.3.254                    //分配给客户端的IP池
local ip = 201.1.2.10                                    //VPN服务器的IP地址
[root@client ~]# vim /etc/ppp/options.xl2tpd            //认证配置
require-mschap-v2                                         //添加一行，强制要求认证
#crtscts                                                //注释或删除该行
#lock                                                //注释或删除该行
root@client ~]# vim /etc/ppp/chap-secrets                    //修改密码文件
jacob   *       123456  *                //账户名称   服务器名称   密码   客户端IP
```
3）启动服务
```shell
[root@client ~]# systemctl start xl2tpd
[root@client ~]# ss  -ntulp |grep xl2tpd        
udp     0      0 0.0.0.0:1701      0.0.0.0:*          3580/xl2tpd
```
4）翻墙设置（非必需操作）
```shell
[root@client ~]# echo "1" > /proc/sys/net/ipv4/ip_forward    #开启路由转发
[root@client ~]# iptables -t nat -A POSTROUTING -s 192.168.3.0/24 \
>  -j SNAT --to-source 201.1.2.10
```
**步骤三：客户端设置**

启动一台Windows虚拟机，将虚拟机网卡桥接到public2，配置IP地址为201.1.2.20。

1. 新建网络连接（参考案例2），输入VPN服务器账户与密码（参考案例2）。

设置VPN连接的属性，预共享密钥是IPSec配置文件中填写的randpass，具体操作如图-7所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/ed6107739cf6460da477c39bb2d5648b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-7

2. 设置Windows注册表（不修改注册表，连接VPN默认会报789错误），具体操作如下：

- 单击"开始"，单击"运行"，键入"regedit"，然后单击"确定"
- 找到下面的注册表子项，然后单击它：
- HKEY_LOCAL_MACHINE\ System\CurrentControlSet\Services\Rasman\Parameters
- 在"编辑"菜单上，单击"新建"->"DWORD值"
- 在"名称"框中，键入"ProhibitIpSec"
- 在"数值数据"框中，键入"1"，然后单击"确定"
- 退出注册表编辑器，然后重新启动计算机
- 连接VPN并测试网络连通性（参考案例2）。

# 5. 编写systemd Unit文件
## 5.1 问题
本案例要求熟练掌握systemd进程如何管理其他服务器，具体要求如下：

- 熟悉systemctl常用命令
- 通过systemd管理shell脚本
- 通过systemd管理Nginx服务

## 5.2 方案
Unit文件语法格式参考表-4。

表－4 Unit文件语法描述
![在这里插入图片描述](https://img-blog.csdnimg.cn/48b03cc9d1034f55935945af146227d4.png)


## 5.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：熟悉systemctl常用命令**

1）命令列表
```shell
[root@web1 ~]# systemctl                             #列出所有启动的服务
[root@web1 ~]# systemctl status   <服务名称>            #查看服务状态
[root@web1 ~]# systemctl start     <服务名称>        #启动服务状态
[root@web1 ~]# systemctl stop      <服务名称>        #关闭服务状态
[root@web1 ~]# systemctl restart  <服务名称>        #重启服务状态
[root@web1 ~]# systemctl enable  <服务名称>            #设置开机自启
[root@web1 ~]# systemctl enable --now  <服务名称>    #设置开机自启并启动
[root@web1 ~]# systemctl disable  <服务名称>        #禁止开机自启
[root@web1 ~]# systemctl enable  <服务名称>            #设置开机自启
[root@web1 ~]# systemctl is-active <服务名称>        #查看是否激活
[root@web1 ~]# systemctl is-enabled  <服务名称>        #查看是否开启自启
[root@web1 ~]# systemctl reboot                    #重启计算机
[root@web1 ~]# systemctl poweroff                     #关闭计算机
```
**步骤二：使用systemd管理shell脚本**

1）编写shell脚本
```shell
[root@web1 ~]# vim /root/test.sh 
#!/bin/bash
while : 
do
    echo NB
    echo DACHUI
done
[root@web1 ~]# chmod +x /root/test.sh
```
2）编写Unit文件
```shell
[root@web1 ~]# cp /usr/lib/systemd/system/{crond.service,test.service}
[root@web1 ~]# vim /usr/lib/systemd/system/test.service
[Unit]
Description=my test script
After=time-sync.target
[Service]
ExecStart=/root/test.sh
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
[Install]
WantedBy=multi-user.target
```
**步骤二：使用systemd管理Nginx服务**

1）编写Unit文件
```shell
[root@web1 ~]# vim /usr/lib/systemd/system/nginx.service
[Unit]
Description=The Nginx HTTP Server        #描述信息
After=network.target remote-fs.target nss-lookup.target
[Service]
Type=forking
#仅启动一个主进程的服务为simple，需要启动若干子进程的服务为forking
ExecStart=/usr/local/nginx/sbin/nginx
ExecReload=/usr/local/nginx/sbin/nginx -s reload
ExecStop=/bin/kill -s QUIT ${MAINPID}
[Install]
WantedBy=multi-user.target
```

# Exercise
## 1 列出常见的VPN技术？

GRE、PPTP、L2TP+IPSEc、SSL VPN。

## 2 PPTP使用什么进行数据加密？

MPPEP支持MPPE(Microsoft Point-to-Point Encryption)加密

## 3 systemctl常用命令有哪些？
```shell
[root@web1 ~]# systemctl                             #列出所有启动的服务
[root@web1 ~]# systemctl status   <服务名称>            #查看服务状态
[root@web1 ~]# systemctl start     <服务名称>        #启动服务状态
[root@web1 ~]# systemctl stop      <服务名称>        #关闭服务状态
[root@web1 ~]# systemctl restart  <服务名称>        #重启服务状态
[root@web1 ~]# systemctl enable  <服务名称>            #设置开机自启
[root@web1 ~]# systemctl enable --now  <服务名称>    #设置开机自启并启动
[root@web1 ~]# systemctl disable  <服务名称>        #禁止开机自启
[root@web1 ~]# systemctl enable  <服务名称>            #设置开机自启
[root@web1 ~]# systemctl is-active <服务名称>        #查看是否激活
[root@web1 ~]# systemctl is-enabled  <服务名称>        #查看是否开启自启
[root@web1 ~]# systemctl reboot                    #重启计算机
[root@web1 ~]# systemctl poweroff                     #关闭计算机
```

## 4 systemd的Unit文件哪些语句可以控制进程启动顺序？
- After
- Before

## 5 Centos系统中使用什么工具可以打包RPM包
- rpm-build工具

> 如有侵权，请联系作者删除
