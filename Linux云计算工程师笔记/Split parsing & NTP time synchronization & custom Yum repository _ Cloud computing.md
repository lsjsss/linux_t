@[TOC]( Split parsing & NTP time synchronization & email communication & custom Yum repository | Cloud computing )

---
# 1 案例1：NTP时间同步
## 1.1 问题
本例要求配置一台NTP时间服务器，需要完成下列任务：

1. 部署一台NTP时间服务器
2. 设置时间服务器上层与0.centos.pool.ntp.org同步
3. 设置本地服务器层级数量为10
4. 允许192.168.4.0/24网络的主机同步时间
5. 客户端验证时间是否同步
## 1.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：虚拟机A构建NTP时间服务器**

1）使用yum安装bind、bind-chroot软件包
```shell
[root@svr7 ~]# yum -y install chrony
已加载插件：fastestmirror, langpacks
Loading mirror speeds from cached hostfile
dvd                                               | 3.6 kB     00:00     
软件包 chrony-3.2-2.el7.x86_64 已安装并且是最新版本
无须任何处理
[root@svr7 ~]# rpm -q chrony
chrony-3.2-2.el7.x86_64
[root@svr7 ~]#
```
2）修改配置文件/etc/chrony.conf
```shell
[root@proxy ~]# vim  /etc/chrony.conf
server 0.centos.pool.ntp.org iburst         //server用户客户端指向上层NTP服务器
allow 192.168.4.0/24        //允许那个IP或网络访问NTP
local stratum 10            //设置NTP服务器的层数量
.. ..
```
3）重启chronyd服务
```shell
[root@mail ~]# systemctl  restart chronyd
[root@svr7 ~]# firewall-cmd --set-default-zone=trusted   #设置防火墙
```

**步骤二：虚拟机B构建NTP时间同步的客户端**

1）修改/etc/chrony.conf文件
```shell
[root@pc207 ~]# vim /etc/chrony.conf
server 192.168.4.7 iburst
```
2）重启chronyd服务
```shell
[root@pc207 ~]# systemctl  restart chronyd
[root@svr7 ~]# firewall-cmd --set-default-zone=trusted  #设置防火墙
```
3）修改时间进行测试
```shell
[root@pc207 ~]# date -s "2008-9-1"
2008年 09月 01日 星期一 00:00:00 CST
[root@pc207 ~]# date
2008年 09月 01日 星期一 00:00:01 CST
[root@pc207 ~]# systemctl restart chronyd
[root@pc207 ~]# date
2008年 09月 01日 星期一 00:01:42 CST
[root@pc207 ~]# date
2020年 04月 13日 星期一 18:44:56 CST
[root@pc207 ~]# chronyc  sources –v     #专业查看时间服务端信息命令
```

# 2. 准备邮件案例环境
## 2.1 问题
本例要求配置一台智能DNS服务器，针对同一个FQDN，当不同的客户机来查询时能够给出不同的答案。需要完成下列任务：

1. 准备DNS服务器
2. 主机名：mail.example.com
3. IP地址：192.168.4.7/24
4. 为 example.com 域提供邮件相关解析

## 2.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：为tedu.cn域搭建DNS服务**

1）使用yum安装bind、bind-chroot软件包
```shell
[root@mail ~]# yum -y install bind bind-chroot
.. ..
```
2）建立配置文件named.conf
```shell
[root@mail ~]# mv /etc/named.conf /etc/named.conf.bak     //备份默认配置
[root@mail ~]# vim /etc/named.conf
options  {
        directory  "/var/named";
};
zone "example.com" IN {                                  //定义DNS父域
        type master;
        file "example.com.zone";
};
```
3）建立解析记录文件

注意添加mail.tedu.cn的解析记录：
```shell
[root@mail ~]# vim /var/named/example.com.zone
$TTL   86400
@   IN   SOA   @    root.example.com.  (
    2015052201 
    4H 
    15M 
    4H
    1D
)
example.com.      IN      NS        svr7.example.com.
example.com.       IN      MX   10      mail.example.com.
svr7    IN      A       192.168.4.7 
mail    IN      A       192.168.4.7
```

4）启动named服务
```shell
[root@mail ~]# systemctl  restart named
```
5）将本机配置为DNS客户端，测试域名解析

修改/etc/resolv.conf文件，添加本机作为DNS服务器：
```shell
[root@mail ~]# vim /etc/resolv.conf
nameserver 192.168.4.7
```
查询区域example.com的MX记录，结果为mail.example.com.：
```shell
[root@pc205 ~]# host -t mx example.com
tedu.cn mail is handled by 10 mail.example.com.
```
查询域名mail.example.com的A记录，结果为192.168.4.7：
```shell
[root@pc205 ~]# host mail.example.com
mail.example.com has address 192.168.4.7
```
# Exercise
## 1 缓存域名服务器提供的解析结果属于（ ）类型的记录

> A. 权威解析 
> B. 非权威解析 
> C. 正向解析 
> D. 反向解析

正确答案：B选项，非权威解析。

## 2 配置缓存DNS服务器时，为客户机提供的解析记录如何获取

方式1，全局转发：将请求转发给指定的公共DNS，请求递归服务；

方式2，根域迭代：依次向根、一级、二级……域的DNS服务器迭代。

> 如有侵权，请联系作者删除
