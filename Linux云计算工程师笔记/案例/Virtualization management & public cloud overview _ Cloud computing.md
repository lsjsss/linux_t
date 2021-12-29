@[TOC]( Cloud computing underlying technology secrets & virtualization management & public cloud overview | Cloud computing )

---
# 1 案例1：安装虚拟机软件

## 1.1 问题

本案例要求创建虚拟机，安装虚拟化平台：

- 最低配置： 2CPU，4G内存
- 安装虚拟化平台 libvirtd
- qemu-kvm
- libvirt-daemon
- libvirt-daemon-driver-qemu
- libvirt-client

## 1.2 步骤

实现此案例需要按照如下步骤进行。

步骤一：创建虚拟机，由于之前已经创建过很多次虚拟机，这里按照以下要求创建即可

最小安装，能访问互联网

IP地址：192.168.1.xx/24

硬件最低配置：2CPU，16G内存

步骤二：安装虚拟化平台

查看是否支持虚拟化

```shell
[root@localhost ~]# grep -P "vmx|svm" /proc/cpuinfoflags        : ... ... vmx[root@localhost ~]# lsmod |grep kvmkvm_intel               174841      6 kvm                        578518      1 kvm_intelirqbypass                 13503      1 kvm
```

创建虚拟机 2cpu，4G内存（默认用户名: root 密码: a）

```shell
[root@localhost ~]# base-vm create ecsvm ecs create                                              [  OK  ][root@localhost ~]# 
```

验证 yum 仓库的配置

```shell
[root@localhost ~]# yum makecacheLoaded plugins: fastestmirrorDetermining fastest mirrorslocal_repo                                   | 3.6 kB   00:00     (1/4): local_repo/group_gz                | 166 kB   00:00     (2/4): local_repo/filelists_db            | 6.9 MB   00:00     (3/4): local_repo/primary_db              | 5.9 MB   00:00     (4/4): local_repo/other_db              | 2.5 MB   00:00     Metadata Cache Created[root@localhost ~]# yum repolistLoaded plugins: fastestmirrorLoading mirror speeds from cached hostfilerepo id                           repo name                               statuslocal_repo                        CentOS-7 - Base                         9,911repolist: 9,911[root@localhost ~]#
```

安装 libvirtd

```shell
[root@localhost ~]# yum install -y qemu-kvm \                                   libvirt-daemon \                                   libvirt-daemon-driver-qemu \                                   libvirt-client[root@localhost ~]# systemctl enable --now libvirtd[root@localhost ~]# virsh version
```



# 2 案例2：创建虚拟磁盘，配置虚拟网络

## 2.1 问题

本案例要求创建虚拟机的硬盘文件：

- 后端数据盘：cirros.qcow2
- 创建前端盘：/var/lib/libvirt/images/vmhost.img
- 前端盘的大小是 30G
- 创建虚拟机的网络设备
- 写配置文件 vbr.xml
- 定义ip范围，与真机不要冲突
- 创建 vbr 网络设备

## 2.2 方案

虚拟机组成 硬盘文件 /var/lib/libvirt/images/ 配置文件 /etc/libvirt/qemu/

虚拟化实验图例效果如图-1所示。

![img](https://img-blog.csdnimg.cn/img_convert/f8e9b1815e8740d04f8e5f40f9a4c1d7.png)

图-1

## 2.3 步骤

实现此案例需要按照如下步骤进行。

**步骤一：准备虚拟机**

上传 cirros.qcow2 到虚拟机，通过 qemu-img 创建虚拟机磁盘。命令格式: qemu-img 子命令 子命令参数 虚拟机磁盘文件 大小。

```shell
[root@localhost ~]# cp cirros.qcow2 /var/lib/libvirt/images/[root@localhost ~]# cd /var/lib/libvirt/images/[root@localhost ~]# qemu-img create -f qcow2 -b cirros.qcow2 vmhost.img 30G[root@localhost ~]# qemu-img info vmhost.img #查看信息
```

**步骤二：虚拟网络配置**

1）虚拟网络管理命令如表-1所示。

表-1

2）创建配置文件 /etc/libvirt/qemu/networks/vbr.xml

```shell
[root@localhost ~]# vim /etc/libvirt/qemu/networks/vbr.xml<network>  <name>vbr</name>  <forward mode='nat'/>  <bridge name='vbr' stp='on' delay='0'/>  <ip address='192.168.100.254' netmask='255.255.255.0'>    <dhcp>      <range start='192.168.100.100' end='192.168.100.200'/>    </dhcp>  </ip></network>
```

3）创建虚拟交换机

```shell
[root@localhost ~]# cd /etc/libvirt/qemu/networks/[root@localhost ~]# virsh net-define vbr.xml[root@localhost ~]# virsh net-start vbr[root@localhost ~]# virsh net-autostart vbr[root@localhost ~]# ifconfig # 查看验证
```

虚拟机管理命令如表-2所示。

表-2

**步骤三：虚拟网络配置**

虚拟机配置文件

官方文档地址 https://libvirt.org/format.html

整体流程

1、拷贝 node_base.xml 到虚拟机中

2、拷贝 node_base.xml 到 /etc/libvirt/qemu/虚拟机名字.xml

3、修改配置文件，启动运行虚拟机

```shell
[root@localhost ~]# cp node_base.xml /etc/libvirt/qemu/vmhost.xml[root@localhost ~]# vim /etc/libvirt/qemu/vmhost.xml2:    <name>vmhost</name>3:    <memory unit='KB'>1024000</memory>4:    <currentMemory unit='KB'>1024000</currentMemory>5:    <vcpu placement='static'>2</vcpu>26:    <source file='/var/lib/libvirt/images/vmhost.img'/>
```



# 3 案例3：创建虚拟机

## 3.1 问题

本案例要求创建虚拟机：

- 熟悉 virsh 命令及子命令
- 通过命令行创建虚拟机

## 3.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：创建虚拟机**

```shell
[root@localhost ~]# virsh list[root@localhost ~]# virsh define /etc/libvirt/qemu/vmhost.xml[root@localhost ~]# virsh start vmhost[root@localhost ~]# virsh console vmhost # 两次回车退出使用 ctrl + ]
```



# 4 案例4：华为云用户注册

## 4.1 问题

本案例要求注册华为云账户：

- 用户注册
- 在华为云上注册用户并完成实名认证
- 绑定合作伙伴

## 4.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：注册**

网址：https://www.huaweicloud.com

效果如图-2所示。

![img](https://img-blog.csdnimg.cn/img_convert/f3c0a8c79fc4d60095fa4e29d12f67ad.png)

图-2

实名认证，效果如图-3和图-4所示。

![img](https://img-blog.csdnimg.cn/img_convert/c2c979452904bd1c4f68cf9b27ea3f69.png)

图-3

![img](https://img-blog.csdnimg.cn/img_convert/1ef5fe0e8481028381f7cc30109e41a5.png)

图-4



# 5 案例5：熟悉常见云主机管理工具

## 5.1 问题

本案例要求在Windows上完成xshell软件的安装：

- 使用xshell连接到linux
- 上传下载文件

## 5.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：Windows 上完成 Xshell 软件的安装，并开启 zmodem 的配置**

1) 开启 zmodem 的配置 如图-5所示：

![img](https://img-blog.csdnimg.cn/img_convert/9ade488f8442257440548ddc18fccee0.png)

图-5

2) 安装lrzsz

```shell
[root@localhost ~]# yum -y install lrzsz
```

> 如有侵权，请联系作者删除
