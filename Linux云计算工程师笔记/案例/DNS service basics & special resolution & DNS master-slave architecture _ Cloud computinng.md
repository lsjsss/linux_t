@[TOC]( DNS service basics & special resolution & cache DNS & DNS master-slave architecture | Cloud computing )

---
# 1. 搭建单区域DNS服务器
## 1.1 问题
本例要求要求为DNS区域tedu.cn搭建一台DNS服务器，以便用户能通过域名的方式访问网站。测试阶段主要提供以下正向记录：

1. svr7.tedu.cn ---> 192.168.4.7
2. pc207.tedu.cn ---> 192.168.4.207
3. www.tedu.cn ---> 192.168.4.100
配置完成后在客户机上验证查询结果。

## 1.2 方案
快速构建DNS服务器的基本过程：

1. 安装 bind、bind-chroot 包
2. 建立主配置文件 /etc/named.conf
3. 建立地址库文件 /var/named/.. ..
4. 启动 named 服务

配置及使用DNS客户端的基本过程：
1. 修改配置文件/etc/resolv.conf，添加nameserver=DNS服务器地址
2. 使用host命令查询，提供目标域名作为参数

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：配置DNS服务器svr7**

1）安装 bind、bind-chroot 包
```shell
[root@localhost ~]# setenforce 0
[root@localhost ~]# firewall-cmd --set-default-zone=trusted
[root@svr7 ~]# yum  -y  install  bind  bind-chroot
.. ..
```
2）建立主配置文件 /etc/named.conf
```shell
[root@svr7 ~]# mv  /etc/named.conf  /etc/named.conf.origin          //备份默认配置
[root@svr7 ~]# vim  /etc/named.conf                             //建立新配置
options {
    directory  "/var/named";                          //地址库默认存放位置
};
zone  "tedu.cn" {                                  //定义正向DNS区域
    type  master;                                     //主区域
    file  "tedu.cn.zone";                             //自定义地址库文件名
};
```
3）建立地址库文件 /var/named/tedu.cn.zone
```shell
[root@svr7 ~]# cd  /var/named/                              //进地址库目录
[root@svr7 named]# cp  -p  named.localhost  tedu.cn.zone      //参考范本建地址库文件
[root@svr7 named]# vim  tedu.cn.zone                          //修订地址库记录
$TTL 1D                                          //文件开头部分可保持不改
@   IN SOA  @ rname.invalid. (
                    0   ; serial
                    1D  ; refresh
                    1H  ; retry
                    1W  ; expire
                    3H )    ; minimum
@       NS  svr7.tedu.cn.                          //本区域DNS服务器的FQDN
svr7    A   192.168.4.7                         //为NS主机提供A记录
pc207   A   192.168.4.207                         //其他正向地址记录.. ..
www  A   192.168.4.100
```
4）启动 named 服务，并设置开机自启
```shell
[root@svr7 named]# systemctl  restart  named  
[root@svr7 named]# systemctl  enable  named
Created symlink from /etc/systemd/system/multi-user.target.wants/named.service to /usr/lib/systemd/system/named.service.
```
**步骤二：配置DNS客户机pc207并测试**

1）修改配置文件/etc/resolv.conf，指定默认使用哪一台DNS服务器
```shell
[root@localhost ~]# setenforce 0
[root@localhost ~]# firewall-cmd --set-default-zone=trusted
[root@pc207 ~]# vim  /etc/resolv.conf 
nameserver  192.168.4.7
.. ..
```
2）使用host命令查询，提供目标域名作为参数
```shell
[root@pc207 ~]# host  svr7.tedu.cn
svr7.tedu.cn has address 192.168.4.7
[root@pc207 ~]# host  pc207.tedu.cn
pc207.tedu.cn has address 192.168.4.207
[root@pc207 ~]# host  www.tedu.cn
www.tedu.cn has address 192.168.4.100
```
使用host测试DNS查询结果时，如果不方便修改/etc/resolv.conf文件，也可以采用“host 目标域名 DNS服务器地址”形式临时指定使用哪一台DNS服务器。
```shell
[root@pc207 ~]# host  pc207.tedu.cn  192.168.4.7
Using domain server:
Name: 192.168.4.7
Address: 192.168.4.7#53
Aliases: 
pc207.tedu.cn has address 192.168.4.207
```

# 2. 特殊DNS解析
## 2.1 问题
沿用案例1，本例要求掌握DNS轮询、泛域名解析的配置，实现的目标如下：

1. 为站点 www.tedu.cn 提供DNS轮询解析，三台Web服务器节点的IP地址分别为：192.168.4.100、192.168.4.110、192.168.4.120
2. 配置泛域名解析实现以下解析记录：任意名称.tedu.cn ---> 119.75.217.56
3. 
## 2.2 方案
DNS轮询：FQDN ---> IP地址1、IP地址2、.. ..
泛域名解析（站点名不确定）：多个FQDN ---> 一个IP地址

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：配置DNS轮询**

1）修改DNS服务器上tedu.cn区域的地址库文件，在末尾添加轮询地址记录
```shell
[root@svr7 ~]# vim  /var/named/tedu.cn.zone 
.. ..
www        A    192.168.4.100
www        A    192.168.4.110
www        A    192.168.4.120
```

2）重启系统服务named
```shell
[root@svr7 named]# systemctl  restart  named
```

3）在客户机pc207上测试轮询记录

针对目标www.tedu.cn执行多次查询，观察第1条结果的变化：
```shell
[root@pc207 ~]# host  www.tedu.cn
www.tedu.cn has address 192.168.4.100          //第1个结果为192.168.4.100
www.tedu.cn has address 192.168.4.110
www.tedu.cn has address 192.168.4.120
[root@pc207 ~]# host  www.tedu.cn
www.tedu.cn has address 192.168.4.120          //第1个结果为192.168.4.120
www.tedu.cn has address 192.168.4.110
www.tedu.cn has address 192.168.4.100
[root@pc207 ~]# host  www.tedu.cn
www.tedu.cn has address 192.168.4.110          //第1个结果为192.168.4.110
www.tedu.cn has address 192.168.4.120
www.tedu.cn has address 192.168.4.100
```
步骤二：配置多对一的泛域名解析

1）修改DNS服务器上指定区域的地址库文件，在末尾添加*通配地址记录
```shell
[root@svr7 ~]# vim  /var/named/tedu.cn.zone 
.. ..
*       A   119.75.217.56
```
2）重启系统服务named
```shell
[root@svr7 named]# systemctl  restart  named
```
3）在客户机pc207上测试多对一的泛域名解析记录

当查询未知站点（地址库中没有明确记录）时，以 * 对应的IP地址反馈：
```shell
[root@pc207 ~]# host  station123.tedu.cn
station123.tedu.cn has address 119.75.217.56
[root@pc207 ~]# host  movie.tedu.cn
movie.tedu.cn has address 119.75.217.56
[root@pc207 ~]# host  tts8.tedu.cn
tts8.tedu.cn has address 119.75.217.56
```

# 3. 搭建并测试缓存DNS
## 3.1 问题
本例要求熟悉缓存DNS的工作过程，准备一台可上网的RHEL7虚拟机，并完成下列任务：

1. 安装 bind、bind-chroot 包
2. 搭建并测试基于全局转发器的缓存DNS

## 3.2 方案
权威/官方DNS服务器的特点：

- 至少管理一个DNS区域,，需要IANA等官方机构授权
- 典型应用：根域DNS、一级域DNS、二级域DNS、三级域DNS、.. ..

缓存DNS服务器的特点：

- 不需要管理任何DNS区域，但是能够替客户机查询，而且通过缓存、复用查询结果来加快响应速度
- 典型应用：ISP服务商、企业局域网

缓存DNS服务器的解析记录来源：

- 方式1：全局转发：将请求转发给指定的公共DNS（其他缓存DNS），请求递归服务
- 方式2：根域迭代：依次向根、一级、二级……域的DNS服务器迭代

## 3.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：为虚拟机pc207提供上网条件**

1）为虚拟机添加一块新的网卡，选择NAT或Bridge模式

若选择NAT模式（地址转换），则新加网卡的上网参数由虚拟化平台自动设置。

若选择Bridge模式（桥接），则新加网卡的上网参数需要参考真实网络的主机，必要时请网络管理员提供支持。

此处所列地址信息可帮助大家理解上网条件，但不作为练习的配置依据：
```shell
[root@pc207 ~]# ifconfig  eth1                      //检查新增网卡的IP地址
eth1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.70.129  netmask 255.255.255.0  broadcast 192.168.70.255
.. ..
[root@pc207 ~]# route  -n                          //确认已配好默认网关
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.70.2    0.0.0.0         UG    100    0        0 eth1
192.168.70.0    0.0.0.0         255.255.255.0   U     100    0        0 eth1
.. ..
[root@pc207 ~]# cat  /etc/resolv.conf              //确认第一DNS为外部可用DNS地址
nameserver 192.168.70.2
.. ..
```

2）确保从主机pc207可访问到外部DNS

访问默认DNS可用（本机正常连网需要）：
```shell
[root@pc207 ~]# host  www.qq.com
www.qq.com has address 111.30.132.101
www.qq.com has IPv6 address 240e:e1:8100:28::2:16
```
访问指定DNS可用（全局转发的前提条件）：
```shell
[root@pc207 ~]# host  www.qq.com  202.106.0.20      //国内公共DNS服务器之一
Using domain server:
Name: 202.106.0.20
Address: 202.106.0.20#53
Aliases: 
www.qq.com has address 111.30.132.101
www.qq.com is an alias for qq.com.edgesuite.net.
qq.com.edgesuite.net is an alias for a1574.b.akamai.net.
www.qq.com is an alias for qq.com.edgesuite.net.
qq.com.edgesuite.net is an alias for a1574.b.akamai.net.
```

**步骤二：将pc207配置为缓存DNS（全局转发式）**

1）安装bind、bind-chroot软件包
```shell
[root@pc207 ~]# yum  -y  install  bind  bind-chroot
.. ..
```
2）建立主配置文件/etc/named.conf

当收到来自客户机的DNS查询请求时，转发到外网的其他DNS服务器
```shell
[root@pc207 ~]# vim  /etc/named.conf
options {
    forwarders  { 202.106.0.20; };
};
```
3）启动系统服务named，并设置开机自启
```shell
[root@pc207 ~]# systemctl  restart  named
[root@pc207 ~]# systemctl  enable  named
```
4）可向缓存DNS服务器pc207查询到公共域名（百度、网易等站点）
```shell
[root@pc207 ~]# host  www.baidu.com  192.168.4.207           //查百度的站点IP
Using domain server:
Name: 192.168.4.207
Address: 192.168.4.207#53
Aliases: 
www.baidu.com is an alias for www.a.shifen.com.
www.a.shifen.com has address 111.13.100.92
www.a.shifen.com has address 111.13.100.91
[root@pc207 ~]# host  www.163.com  192.168.4.207                //查网易的站点IP
Using domain server:
Name: 192.168.4.207
Address: 192.168.4.207#53
Aliases: 
www.163.com is an alias for www.163.com.lxdns.com.
www.163.com.lxdns.com is an alias for 163.xdwscache.ourglb0.com.
163.xdwscache.ourglb0.com has address 111.11.31.104
163.xdwscache.ourglb0.com has address 111.11.31.114
```

# 4. 构建主/从DNS服务器
## 4.1 问题
准备2台虚拟机，配置实现DNS主/从结构，相关要求如下：

- 主DNS的域名为svr7.tedu.cn，IP地址为192.168.4.7/24
- 从DNS的域名为pc207.tedu.cn，IP地址为192.168.4.207
- 主、从均能够解析tts7.tedu.cn --> 118.45.29.31
- 当主DNS的tts7.tedu.cn记录的IP地址变更为4.4.4.4以后，从DNS能够自动同步此更改

## 4.2 方案
使用2台虚拟机，其中一台作为主DNS服务器（192.168.4.7）、另外一台作为从DNS服务器（192.168.4.207）；同时，这两台虚拟机中的任何一台都可以作为测试用的Linux客户机。

主DNS的配置关键——修改named.conf配置文件，为从DNS设置授权：
```shell
options {
        .. ..
        allow-transfer {
                从DNS服务器的IP地址;
        }; 
};
```
从DNS的配置关键——无需手动建立解析记录，只需修改named.conf配置文件：
```shell
zone "tedu.cn" IN {
        type slave;                                  //类型为slave
        file "slaves/tedu.cn.zone";                //下载存放位置
        masters { 主DNS服务器的IP地址; }; 
}; 
```

## 4.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：主DNS授权从DNS服务器，允许其下载地址记录**

1）修改named.conf配置文件，授权从DNS服务器，允许其下载地址记录
```shell
[root@svr7 ~]# vim /etc/named.conf
options  {
        directory  "/var/named";
        allow-transfer { 192.168.4.207;  };           //授权从DNS服务器
};
zone "tedu.cn" IN {
        type master;
        file "tedu.cn.zone";
};
.. ..
```
2）修改区域记录文件，为从DNS添加NS记录，并设置测试A记录
```shell
[root@svr7 ~]# vim /var/named/tedu.cn.zone 
$TTL   86400
@   IN   SOA   @    root.tedu.cn.  (
    2015052201                                          ;更新序列号
    4H                                                  ;刷新时间
    15M                                                 ;重试间隔
    4H                                                  ;超时时间
    1D                                                  ;无效记录的生存时间
)
@       IN      NS      svr7.tedu.cn.                  //指定主DNS记录
@       IN      NS      pc207.tedu.cn.                //指定从DNS记录
svr7    IN      A       192.168.4.7                  //主DNS的A记录
pc207   IN      A       192.168.4.207                    //从DNS的 A记录
tts7    IN      A       118.45.29.31                     //tts7.tedu.cn解析记录
.. ..                                            //其他A记录
```
3）重新加载named服务
```shell
[root@svr7 ~]# service named restart  
停止 named：.                                              [确定]
启动 named：                                               [确定]
```
**步骤二：建立从DNS服务器**

1）使用yum安装DNS服务相关软件包
```shell
[root@pc207 ~]# yum -y install bind bind-chroot
.. ..
[root@pc207 ~]# rpm -q bind bind-chroot
.. ..
```
2）建立/etc/named.conf配置文件
```shell
[root@svr7 ~]# mv  /etc/named.conf  /etc/named.conf.bak      //备份默认配置
[root@svr7 ~]# vim  /etc/named.conf              //建立新配置
options {
        directory "/var/named";
};
zone "tedu.cn" IN {                            //同步区域
        type slave;                                  //类型为从区域
        file "slaves/tedu.cn.zone";              //区域文件存储位置
        masters { 192.168.4.7; };                   //指定主DNS的IP地址
};
```
3）重新加载named服务
```shell
[root@svr7 ~]# service named restart  
停止 named：.                                              [确定]
启动 named：                                               [确定]
```
确认区域配置文件已经自动下载，即同步成功：
```shell
[root@pc207 ~]# ls /var/named/slaves/
tedu.cn.zone
```
**步骤三：客户机查询测试**

1）向主DNS查询域名tts7.tedu.cn，反馈结果应为118.45.29.31
```shell
[root@pc207 ~]# nslookup  tts7.tedu.cn  192.168.4.7
Server:        192.168.4.7
Address:    192.168.4.7#53
Name:   tts7.tedu.cn
Address:   118.45.29.31
```
2）向从DNS查询域名tts7.tedu.cn，也能获得结果为118.45.29.31
```shell
[root@pc207 ~]# nslookup  tts7.tedu.cn  192.168.4.207
Server:        192.168.4.207
Address:    192.168.4.207#53
Name:   tts7.tedu.cn
Address:   118.45.29.31
```
3）测试解析记录的同步

在主DNS上修改A记录tts7.tedu.cn，将IP地址改为4.4.4.4，同时将序列号+1更新，保存并启用新配置：
```shell
[root@svr7 ~]# vim /var/named/tedu.cn.zone
$TTL   86400
@   IN   SOA   @    root.tedu.cn.  (
    2015052202                                    //修改记录后，此序号应变更
    .. ..
)
.. ..
tts7    IN      A       4.4.4.4                     //修改tts7解析记录
[root@svr7 ~]# service named restart              //重启named服务
停止 named：                                               [确定]
启动 named：                                               [确定]
```
然后在客户端重复测试第1）和2）步骤，反馈的解析结果都应该是4.4.4.4：
```shell
[root@pc207 ~]# nslookup  tts7.tedu.cn  192.168.4.7
Server:        192.168.4.7
Address:    192.168.4.7#53
Name:   tts7.tedu.cn
Address:  4.4.4.4                              //向主DNS查询的结果
[root@pc207 ~]# nslookup  tts7.tedu.cn  192.168.4.207
Server:        192.168.4.207
Address:    192.168.4.207#53
Name:   tts7.tedu.cn                         //向从DNS查询的结果
Address:   4.4.4.4
```

# Exercise
## 1 简述DNS地址记录中类型NS、A的含义

NS记录为域名服务器记录（本域权威DNS的FQDN）；

A记录为正向解析记录（FQDN --> IP地址）。

## 2 对于DNS服务器来说，递归查询和迭代查询分别表示什么

对于一台DNS服务器来说：

若允许递归，则当客户端请求解析的域名非本DNS管辖时，本DNS会向其他DNS服务器代询；

若不允许递归，则当客户端请求解析的域名非本DNS管辖时，本DNS会放弃代询 —— 但是，如果目标地址位于已知的某个授权子域，本DNS会告知客户端对应的子DNS服务器的地址信息（即迭代）。

## 3 DNS正向解析的作用是( )
A. 将IP地址转换为域名

B. 将域名转换为IP地址

C. 将IP地址转换为主机名

D. 将主机名转化为IP地址

正确答案：B。

## 4 DNS常见的资源类型

> 配置DNS区域的解析记录时，常见的资源类型如下，请写出各自的作用：
> - A记录
> - MX记录
> - CNAME记录
> - NS记录

A记录为正向解析记录，MX记录为邮件服务器记录，CNAME记录为别名记录，NS记录为域名服务器记录

> 如有侵权，请联系作者删除
