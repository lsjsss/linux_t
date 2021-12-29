@[TOC]( SELinux & system troubleshooting & firewall policy management & service management | Cloud computing )

---
# 1 案例1：启用SELinux保护
## 1.1 问题
本例要求为虚拟机 server0、desktop0 配置SELinux：

1. 确保 SELinux 处于强制启用模式
2. 在每次重新开机后，此设置必须仍然有效

## 1.2 方案
SELinux，Security-Enhanced Linux：是由美国NSA国家安全局提供的一套基于内核的增强的强制安全保护机制，针对用户、进程、文档标记安全属性并实现保护性限制。

SELinux安全体系直接集成在Linux内核中，包括三种运行模式：

- disabled：彻底禁用，内核在启动时不加载SELinux安全体系
- enforcing：强制启用，内核加载SELinux安全体系，并强制执行保护策略
- permissive：宽松模式，内核加载SELinux安全体系，只记录不执行
执行getenforce可以查看当前所处的模式。

在disabled模式与enforcing、permissive模式之间切换时，需要重新启动Linux系统；而在enforcing模式与permissive模式之间切换时，并不需要重启，可以直接执行setenforce 1|0操作。

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：调整当前的SELinux运行模式**

1）查看当前模式
```shell
[root@server0 ~]# getenforce 
Permissive                                      //表示当前为宽松模式
```
若上述操作显示的结果为Disabled，表示SELinux机制已被禁用，只能通过步骤修改固定配置后再重启；若显示的结果为Enforcing，表示已经处于强制启用模式。

2）切换为enforcing强制启用模式

如果在操作1）中显示的结果为Permissive，则执行以下操作切换为强制启用：
```shell
[root@server0 ~]# setenforce  1                  //强制启用
[root@server0 ~]# getenforce                      //确认切换结果
Enforcing
```
如果在操作1）中显示的结果为Disabled，则无法使用setenforcing命令：
```shell
[root@desktop0 ~]# getenforce 
Disabled
[root@desktop0 ~]# setenforce 1
setenforce: SELinux is disabled 
```
**步骤二：为SELinux运行模式建立固定配置**

1）修改配置文件/etc/selinux/config
```shell
[root@server0 ~]# vim  /etc/selinux/config
SELINUX=enforcing
.. ..
```
2）重启验证结果
```shell
[root@server0 ~]# reboot
.. .. 
[root@server0 ~]# getenforce 
Enforcing
```

# 2. 使用systemctl工具
## 2.1 问题
本例要求掌握systemctl控制工具的基本操作，完成下列任务：

1. 重启 httpd、crond、bluetooth 服务，查看状态
2. 禁止 bluetooth 服务开机自启，并停用此服务
3. 设置默认级别为 multi-user.target 并确认

## 2.2 方案
systemd是一个更高效的系统&服务管理器，其相关特性如下：

- 开机服务并行启动，各系统服务间的精确依赖
- 配置目录：/etc/systemd/system/
- 服务目录：/lib/systemd/system/
systemctl是systemd的管理工具，将相关资源组织为unit配置单元进行管理。

不同的unit决定了一组相关的启动任务，service和target是最常用的配置单元：

- service：后台独立服务
- target：一套配置单元的组合，类似于传统“运行级别”

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：重启 httpd、crond、bluetooth 服务，查看状态**

1）重启系统服务httpd、crond、bluetooth
```shell
[root@svr7 ~]# systemctl  restart  httpd  crond  bluetooth
```
2）查看上述服务的状态
```shell
[root@svr7 ~]# systemctl  status  httpd  crond  bluetooth 
* httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; disabled; vendor preset: disabled)
   Active: active (running) since Fri 2017-01-06 18:18:20 CST; 18s ago
.. ..
* crond.service - Command Scheduler
   Loaded: loaded (/usr/lib/systemd/system/crond.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2017-01-06 18:18:19 CST; 19s ago
.. ..
* bluetooth.service - Bluetooth service
   Loaded: loaded (/usr/lib/systemd/system/bluetooth.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2017-01-06 18:18:19 CST; 19s ago
.. ..
```
**步骤二：禁止 bluetooth 服务开机自启，并停用此服务**

1）停用bluetooth服务
```shell
[root@svr7 ~]# systemctl  stop  bluetooth
```
2）禁止bluetooth服务开机自启
```shell
[root@svr7 ~]# systemctl  disable  bluetooth
Removed symlink /etc/systemd/system/dbus-org.bluez.service.
Removed symlink /etc/systemd/system/bluetooth.target.wants/bluetooth.service.
[root@svr7 ~]# systemctl  is-enabled  Bluetooth             //检查结果
disabled
```
**步骤三：设置默认级别为 multi-user.target 并确认**

1）查看默认运行级别
```shell
[root@svr7 ~]# systemctl  get-default 
graphical.target
```
2）将默认运行级别设置为multi-user.target
```shell
[root@svr7 ~]# systemctl  set-default  multi-user.target 
Removed symlink /etc/systemd/system/default.target.
Created symlink from /etc/systemd/system/default.target to /usr/lib/systemd/system/multi-user.target.
```
3）确认配置结果
```shell
[root@svr7 ~]# systemctl  get-default 
multi-user.target
```
根据此处的设置，重启此虚拟机后图形桌面将不再可用。

# Exercise
## 1 配置虚拟机系统每次开机后SELinux处于宽松模式

```shell
[root@server0 ~]# vim  /etc/selinux/config 
SELINUX=permissive                         
.. ..
[root@server0 ~]# reboot  
```
## 2 防火墙体系中的预设保护区域有哪些，各自的作用是什么

public：仅允许访问本机的sshd等少数几个服务

trusted：允许任何访问

block：阻塞任何来访请求

drop：丢弃任何来访的数据包

## 3 防火墙设置策略时，如何实现永久策略

添加--permanent选项

利用firewall-cmd --reload进行重新加载防火墙配置

## 4 将Linux系统的默认运行级别设为文本模式

1）修改默认运行级别（target）
```shell
[root@svr7 ~]# systemctl  set-default  multi-user.target 
Removed symlink /etc/systemd/system/default.target.
Created symlink from /etc/systemd/system/default.target to /usr/lib/systemd/system/multi-user.target.
```
2）确认修改结果
```shell
[root@svr7 ~]# systemctl  get-default 
multi-user.target
```

> 如有侵权，请联系作者删除
