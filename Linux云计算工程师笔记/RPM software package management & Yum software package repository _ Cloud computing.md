@[TOC]( RPM software package management & Yum software package repository | Cloud computing )

---
# 1. 查询已安装的软件信息
## 1.1 问题
列出当前主机已安装的所有RPM软件
查看firefox软件包的安装清单
查询ifconfig命令程序是安装哪个软件包后产生的
查看firefox软件包的用途
## 1.2 方案
查询所有已安装的rpm包，可以利用命令rpm -qa。

查询一个软件安装清单，可以利用命令rpm -ql 软件名。

查询一个文件是由哪个软件包安装后产生，可以利用命令rpm -qf 文件绝对路径。本题中首先要找到，ifconfig命令的可执行程序在哪里，可以利用which命令。

查看软件的用途，可以利用命令rpm -qi 软件名。

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：列出当前主机已安装的所有RPM软件**

命令操作如下所示：

```shell
[root@localhost ~]# rpm -qa
```

**步骤二：查看firefox软件包的安装清单**

命令操作如下所示：
```shell
[root@localhost ~]# rpm -ql firefox
```
**步骤三：查询ifconfig命令程序是安装哪个软件包后产生的**

命令操作如下所示：
```shell
[root@localhost ~]# which ifconfig    #查询命令所对应的程序
/sbin/ifconfig
[root@localhost ~]# rpm -qf /sbin/ifconfig
net-tools-1.60-110.el6_2.x86_64
[root@localhost ~]#
```

**步骤四：查看firefox软件包的用途**

命令操作如下所示：
```shell
[root@localhost ~]# rpm -qi firefox
Name        : firefox                      Relocations: (not relocatable)
Version     : 17.0.10                           Vendor: Red Hat, Inc.
Release     : 1.el6_4                       Build Date: 2013年10月23日 星期三 21时14分43秒
Install Date: 2015年01月06日 星期二 20时59分04秒      Build Host: x86-027.build.eng.bos.redhat.com
Group       : Applications/Internet         Source RPM: firefox-17.0.10-1.el6_4.src.rpm
Size        : 30424459                         License: MPLv1.1 or GPLv2+ or LGPLv2+
Signature   : RSA/8, 2013年10月29日 星期二 16时20分45秒, Key ID 199e2f91fd431d51
Packager    : Red Hat, Inc. <http://bugzilla.redhat.com/bugzilla>
URL         : http://www.mozilla.org/projects/firefox/
Summary     : Mozilla Firefox Web browser
Description :
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.
[root@localhost ~]#
```
# 2. 查询待安装的.rpm包
## 2.1 问题
1. 查询光盘中的 lynx 软件包的用途、安装清单
2. 查询光盘中的 wireshark 软件包的用途、安装清单
## 2.2 方案
注意在查询未安装的.rpm包信息时，提供的命令参数应该是准确的包文件路径，仅指定软件名是不行的。指定文件路径时，多利用Tab键补全。提前将RHEL6系统光盘挂载到/media目录，以便使用相关包文件。

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：查询光盘中的 lynx 软件包的用途、安装清单**

首先将光盘设备手动挂载到/media目录，进行查询操作。

命令操作如下所示：
```shell
[root@localhost ~]# mount /dev/cdrom /media/
mount: block device /dev/sr0 is write-protected, mounting read-only
[root@localhost ~]# mount | tail -1
/dev/sr0 on /media type iso9660 (ro)
[root@localhost ~]# rpm -qpi /media/Packages/lynx-2.8.8-0.3.dev15.el7.x86_64.rpm 
……
[root@localhost ~]# rpm -qpl /media/Packages/lynx-2.8.8-0.3.dev15.el7.x86_64.rpm
……
```

**步骤二：查询光盘中的 wireshark 软件包的用途、安装清单**

命令操作如下所示：
```shell
[root@localhost ~]# rpm -qpi /media/Packages/wireshark-1.10.14-14.el7.x86_64.rpm
……
[root@localhost ~]# rpm -qpl /media/Packages/wireshark-1.10.14-14.el7.x86_64.rpm
……
```
# 3. RPM软件的安装和卸载
## 3.1 问题
1. 找出vim、vi是由哪两个包产生的
2. 删除vim、vi命令程序
3. 修复vim、vi
4. 安装bind-chroot包,体验Linux依赖关系

## 3.2 方案
本题的思路是，首相通过which命令查找到vim、vi命令可执行程序所在位置，在通过“rpm –qf 文件绝对路径”命令查看该可执行程序，是由那个包产生的。删除该可执行程序后，再将软件包安装重新产生即可。但在安装时需注意，系统会提示改程序已经安装，需加上“—force”选项强制安装。

## 3.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：找出vim、vi是由那两个包产生的**

命令操作如下所示：
```shell
[root@localhost ~]# which vi  vim
/usr/bin/vi
/usr/bin/vim 
[root@localhost ~]# rpm -qf /usr/bin/vi
vim-minimal-7.4.160-4.el7.x86_64 
[root@localhost ~]# rpm -qf /usr/bin/vim
vim-enhanced-7.4.160-4.el7.x86_64
```

**步骤二：删除vim、vi命令程序**

命令操作如下所示：
```shell
[root@localhost ~]# rm -rf /usr/bin/vi /usr/bin/vim
[root@localhost ~]#
```

**步骤三：修复vim、vi**

首先将光盘设备手动挂载到/media目录，进行修复操作。

命令操作如下所示：
```shell
[root@localhost ~]# mount /dev/cdrom /media/
mount: block device /dev/sr0 is write-protected, mounting read-only
[root@localhost ~]# rpm -ivh --force /media/Packages/vim-minimal-7.4.160-4.el7.x86_64……
 [root@localhost ~]# rpm -ivh --force /media/Packages/vim-enhanced-7.4.160-4.el7.x86_64
……
 [root@localhost ~]#
 ```
 
**步骤四：安装bind-chroot包,体验Linux依赖关系**

命令操作如下所示：
```shell
[root@localhost ~]# cd  /media/Packages
[root@svr5 Packages]# rpm  -ivh  bind-chroot-9.9.4-61.el7.x86_64.rpm 
error: Failed dependencies:
……
 [root@svr5 Packages]# rpm  -ivh  bind-9.9.4-61.el7.x86_64.rpm 
Preparing...                ########################################### [100%]
   1:bind                   ########################################### [100%]
[root@svr5 Packages]# rpm  -ivh  bind-chroot-9.9.4-61.el7.x86_64.rpm 
Preparing...                ########################################### [100%]
   1:bind-chroot            ########################################### [100%]
```
   
# 4. 配置Yum仓库及客户端及验证
## 4.1 问题
1. 将光盘挂载到/dvd，搭建本地Yum
2. 将本机设置为客户端，进行Yum验证
3. 查询Yum库中是否有firefox包
4. 使用yum命令安装bind包
5. 利用Yum安装bind
6. 利用Yum卸载bind
7. 利用yum search查询与httpd相关的包
8. 利用yum info查询firefox包描述信息

## 4.2 方案
YUM服务器配置思路：

>第一步：确保光驱电源加电，放入Linux光盘的iso镜像
第二步：ls -l /dev/cdrom 查看linux系统是否识别光驱设备
第三步：创建挂载目录:mkdir /dvd （或也可以使用linux系统提供的挂载目录/media、/mnt）
第四步：利用mount命令挂载:mount /dev/cdrom /dvd
第五步：查看挂载情况：mount | grep dvd



YUM客户端配置思路：

>第一步：切换路径到客户端配置文件路径下：cd /etc/yum.repos.d/
> 第二步：排除其他文件的干扰
> ```shell
> [root@localhost ~]# mkdir /etc/yum.repos.d/repo
> [root@localhost ~]# mv /etc/yum.repos.d/*.repo > /etc/yum.repos.d/repo
> ```
> 
> 第三步：更改配置文件dvd.repo。

必须更改的字段：

- 【】”内容要唯一所以要更改，注意不要有空格
- “baseurl”此字段指定软件包目录，注意路径写对。file：后要有三个“/”
- “enabled”此字段要至于“1”，代表启用

Yum在使用方面，几乎rpm能够做到的事情，Yum也能够做到。此外Yum还具备自动解决依赖关系的功能。

常用的Yum操作：
- yum install 软件名：安装一个软件包
- yum remove 软件名：卸载一个软件包

## 4.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：搭建一个本地Yum，将光盘手动挂载到/dvd**

命令操作如下所示：
```shell
[root@localhost ~]# mkdir /dvd
[root@localhost ~]# ls /dvd
[root@localhost ~]# mount /dev/cdrom /dvd/
mount: /dev/sr0 写保护，将以只读方式挂载
[root@localhost ~]# ls /dvd/
[root@localhost ~]# ls /dvd/Packages/
```

步骤二：将本地设置为客户端，进行Yum验证

**Yum客户端需编辑配置文件，命令操作如下所示：**
```shell
[root@localhost ~]# ls /etc/yum.repos.d/
[root@localhost ~]# mkdir /etc/yum.repos.d/repo
[root@localhost ~]# mv /etc/yum.repos.d/*.repo  /etc/yum.repos.d/repo 
[root@localhost ~]# ls /etc/yum.repos.d/
[root@localhost ~]# vim /etc/yum.repos.d/dvd.repo
[centos] #仓库标识,可以任意
name=hehe lele CentOS7         #仓库的描述信息，可以任意
baseurl=file:///dvd             #指定服务端位置，file://代表本地为服务端
enabled=1                     #是否启用本文件
gpgcheck=0                     #是否检测红帽签名信息
[root@localhost ~]# yum repolist         #列出仓库信息
```

**步骤三：查询yum库中是否有firefox包**

命令操作如下所示：
```shell
[root@localhost /]# yum list | grep firefox
```

**步骤四：利用yum安装bind包**
命令操作如下所示：
```shell
[root@localhost /]# yum -y install bind
……
```
**步骤二：利用Yum卸载bind**
命令操作如下所示：
```shell
[root@localhost /]# yum -y remove bind
……
```
**步骤四：利用yum search查询与httpd相关的包**
命令操作如下所示：
```shell
[root@localhost /]# yum search httpd
……
```
**步骤四：利用yum info查询firefox包描述信息**

命令操作如下所示：
```shell
root@localhost /]# yum info firefox
……
```

# Exercise
## 1 Linux中查询已安装软件包信息。
使用rpm命令查询已经安装的软件包时，常见的用法如下所示，请补充完整。

rpm （ ）列出已安装的所有软件包

rpm （ ） 软件名：查看指定软件的详细信息

rpm （ ） 软件名：查看指定软件的文件安装清单

- -qa
- -qi
- -ql
## 2 Linux中查询未安装软件包信息。
使用rpm命令查询尚未安装的 .rpm 文件时，常见的用法如下所示，请补充完整。

rpm （ ） *.rpm安装文件：查看该软件包的详细信息
rpm （ ） *.rpm安装文件：查看如果安装该软件将会提供的文件清单

- -qpi
- -qpl

## 3 删除hostname命令的执行程序，并修复。
```shell
[root@svr5 ~]# hostname 
svr5.tarena.com
[root@svr5 ~]# which hostname
/usr/bin/hostname
[root@svr5 ~]# rm -rf /usr/bin/hostname 
[root@svr5 ~]# hostname 
-bash: /bin/hostname: 没有那个文件或目录
[root@svr5 ~]# rpm -qf /usr/bin/hostname
hostname-3.13-3.el7.x86_64 
[root@svr5 ~]# rpm –ivh –force  /dvd/Packages/hostname-3.13-3.el7.x86_64 
Preparing...                ########################################### [100%]
   1:net-tools              ########################################### [100%]
[root@svr5 ~]# hostname 
svr5.tarena.com
```

## 4 YUM简介。什么是YUM，其作用是什么，主要支持哪几种方式提供软件源？


是一种基于“C/S”结构的RPM软件更新机制，所有的软件包由集中的软件仓库提供，能够自动分析并解决软件包之间的依赖关系。

支持的软件源主要包括：

- 本地文件夹：file://.. ..
- FTP服务器：ftp://.. ..
- HTTP服务器：http://
## 5 简述yum客户端配置文件中主要参数的含义
```shell
[root@server0 ~]# cat  /etc/yum.repos.d/rhel_dvd.repo 
[rhel_dvd]                              //仓库标识
gpgcheck = 0                             //不做签名检查
enabled = 1                             //启用此仓库
baseurl = file:///dvd                  //软件仓库的访问地址
```

> 如有侵权，请联系作者删除
