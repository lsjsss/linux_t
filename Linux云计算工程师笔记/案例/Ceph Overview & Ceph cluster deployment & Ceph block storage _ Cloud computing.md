@[TOC]( Ceph Overview & Ceph cluster deployment & Ceph block storage | Cloud computing )

---
# 1. 实验环境
## 1.1 问题
准备四台虚拟机，其三台作为存储集群节点，一台安装为客户端，实现如下功能：

- 创建1台客户端虚拟机
- 创建3台存储集群虚拟机
- 配置主机名、IP地址、YUM源
- 修改所有主机的主机名
- 配置无密码SSH连接
- 配置NTP时间同步
- 创建虚拟机磁盘

## 1.2 方案
使用4台虚拟机，1台客户端、3台存储集群服务器，拓扑结构如图-1所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/37b988d7ce0f4208950fb0f0c74cfef4.png)
图-1

所有主机的主机名及对应的IP地址如表-1所示。

注意：所有主机基本系统光盘的YUM源必须提前配置好。

表－1 主机名称及对应IP地址表
![在这里插入图片描述](https://img-blog.csdnimg.cn/0b776d4523e54b3bb168058fcd1c3751.png)
Ceph组件架构如图-2所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/b21de80a1f344eea9f1e1aaabe08d50f.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_17,color_FFFFFF,t_70,g_se,x_16)
图-2

Ceph会对数据进行切割处理，如图-3所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/5aa8035ee0af48c1be3a89f9f5c73c19.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_15,color_FFFFFF,t_70,g_se,x_16)
图-3

Ceph随机读写数据的思路，如图-4所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/4de12f77daad4682822cb3353c884b9a.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_15,color_FFFFFF,t_70,g_se,x_16)
图-4

Ceph集群结构如图-5所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/6d853344d1b8441698fe2880cf05273c.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_13,color_FFFFFF,t_70,g_se,x_16)
图-5

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：安装前准备**

1）为所有节点配置yum源服务器。

将真机第二阶段素材中的ceph10.iso挂载到/var/ftp/ceph目录，为所有虚拟机提供YUM源。
```shell
# mkdir  /var/ftp/ceph
# mount -t  iso9660   /.../ceph10.iso   /var/ftp/ceph           #不能照抄
```
2）为虚拟机添加磁盘：

除了client客户端，所有3台ceph服务器都添加2块20G磁盘。
```shell
[root@client ~]# lsblk                 #没有额外磁盘
[root@node1 ~]# lsblk                  #多了2块磁盘
[root@node2 ~]# lsblk                  #多了2块磁盘
[root@node3 ~]# lsblk                  #多了2块磁盘
```
3）所有主机设置防火墙和SELinux（如果已经关闭，则此步骤可以忽略）
```shell
[root@client ~]# firewall-cmd --set-default-zone=trusted
[root@client ~]# sed -i '/SELINUX/s/enforcing/permissive/' /etc/selinux/config
[root@client ~]# setenforce 0
[root@node1 ~]# firewall-cmd --set-default-zone=trusted
[root@node1 ~]# sed -i '/SELINUX/s/enforcing/permissive/' /etc/selinux/config
[root@node1 ~]# setenforce 0
[root@node2 ~]# firewall-cmd --set-default-zone=trusted
[root@node2 ~]# sed -i '/SELINUX/s/enforcing/permissive/' /etc/selinux/config
[root@node2 ~]# setenforce 0
[root@node3 ~]# firewall-cmd --set-default-zone=trusted
[root@node3 ~]# sed -i '/SELINUX/s/enforcing/permissive/' /etc/selinux/config
[root@node3 ~]# setenforce 0
```
4）配置无密码连接(包括自己远程自己也不需要密码)，在node1操作。
```shell
[root@node1 ~]# ssh-keygen   -f /root/.ssh/id_rsa    -N ''
#-f后面跟密钥的文件名称（希望创建密钥到哪个文件）
#-N ''代表不给密钥配置密钥（不能给密钥配置密码）
[root@node1 ~]# for i in 10  11  12  13
 do
     ssh-copy-id  192.168.4.$i
 done
#通过ssh-copy-id将密钥传递给192.168.4.10、192.168.4.11、192.168.4.12、192.168.4.13
```
5）修改/etc/hosts并同步到所有主机。

注意：/etc/hosts解析的域名要与本机主机名一致！！！！
```shell
 [root@node1 ~]# vim /etc/hosts     #修改文件，手动添加如下内容（不要删除文件原有内容）
... ...
192.168.4.10  client
192.168.4.11     node1
192.168.4.12     node2
192.168.4.13     node3
```
提示：/etc/hosts解析的域名必须与本机主机名一致！！！

将/etc/hosts文件拷贝给所有其他主机（client、node1、node2、node3）
```shell
[root@node1 ~]# for i in client node1  node2  node3
do
scp  /etc/hosts   $i:/etc/
done
```
6）修改所有节点都需要配置YUM源，并同步到所有主机。
```shell
[root@node1 ~]# vim /etc/yum.repos.d/ceph.repo    #新建YUM源配置文件，内容如下
[mon]
name=mon
baseurl=ftp://192.168.4.254/ceph/MON
gpgcheck=0
[osd]
name=osd
baseurl=ftp://192.168.4.254/ceph/OSD
gpgcheck=0
[tools]
name=tools
baseurl=ftp://192.168.4.254/ceph/Tools
gpgcheck=0
[root@node1 ~]# yum clean all               #清空缓存
[root@node1 ~]# yum repolist                #验证YUM源软件数量
源标识            源名称                    状态
Dvd                redhat                    9,911
Mon                mon                        41
Osd                osd                        28
Tools            tools                    33
repolist: 10,013
[root@node1 ~]# for i in  client  node1  node2  node3
do
scp  /etc/yum.repos.d/ceph.repo   $i:/etc/yum.repos.d/
done
```
7）给所有节点安装ceph相关软件包。
```shell
[root@node1 ceph-cluster]# for i in node1 node2 node3
do
    ssh  $i "yum -y install ceph-mon ceph-osd ceph-mds ceph-radosgw"
done 
```
8）Client主机配置NTP服务器。
```shell
[root@client ~]# yum -y install chrony
[root@client ~]# vim /etc/chrony.conf
    allow 192.168.4.0/24        #大约26行
    local stratum 10            #大约29行(去注释即可)
[root@client ~]# systemctl restart chronyd
```
9）node1，node2，node3修改NTP客户端配置。
```shell
[root@node1 ~]# yum -y install chrony
[root@node1 ~]# vim /etc/chrony.conf
server 192.168.4.10   iburst              #配置文件第二行，手动添加一行新内容
[root@node1 ~]# systemctl restart chronyd
[root@node1 ~]# chronyc sources -v        #查看同步结果，应该是^*
[root@node2 ~]# yum -y install chrony
[root@node2 ~]# vim /etc/chrony.conf
server 192.168.4.10   iburst              #配置文件第二行，手动添加一行新内容
[root@node2 ~]# systemctl restart chronyd
[root@node2 ~]# chronyc sources -v            #查看同步结果，应该是^*
[root@node3 ~]# yum -y install chrony
[root@node3 ~]# vim /etc/chrony.conf
server 192.168.4.10   iburst              #配置文件第二行，手动添加一行新内容
[root@node3 ~]# systemctl restart chronyd
[root@node3 ~]# chronyc sources -v       #查看同步结果，应该是^*
```

# 2. 部署ceph集群
## 2.1 问题
沿用练习一，部署Ceph集群服务器，实现以下目标：

- 安装部署工具ceph-deploy
- 创建ceph集群
- 准备日志磁盘分区
- 创建OSD存储空间
- 查看ceph状态，验证

## 2.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：安装部署软件ceph-deploy**

1）在node1安装部署工具，学习工具的语法格式。
```shell
[root@node1 ~]#  yum -y install ceph-deploy
[root@node1 ~]#  ceph-deploy  --help
[root@node1 ~]#  ceph-deploy mon --help
```
2）创建目录（目录名称可以任意，推荐与案例一致）
```shell
[root@node1 ~]#  mkdir ceph-cluster
[root@node1 ~]#  cd ceph-cluster/
```
**步骤二：部署Ceph集群**

1）创建Ceph集群配置,在ceph-cluster目录下生成Ceph配置文件（ceph.conf）。

在ceph.conf配置文件中定义monitor主机是谁。
```shell
[root@node1 ceph-cluster]# ceph-deploy new node1 node2 node3
[root@node1 ceph-cluster]# vim ceph.conf        #不要修改原始内容，在文件末尾添加一行
rbd_default_features = 1
#默认开启COW分层快照的功能
```
2）初始化所有节点的mon服务，也就是启动mon服务。

拷贝当前目录的配置文件到所有节点的/etc/ceph/目录并启动mon服务。
```shell
[root@node1 ceph-cluster]# ceph-deploy mon create-initial
#配置文件ceph.conf中有三个mon的IP，ceph-deploy脚本知道自己应该远程谁
```
3) 在每个node主机查看自己的服务(注意每台主机服务名称不同)
```shell
[root@node1 ceph-cluster]# systemctl status ceph-mon@node1
[root@node2 ~]# systemctl status ceph-mon@node2
[root@node3 ~]# systemctl status ceph-mon@node3
#备注:管理员可以自己启动（start）、重启（restart）、关闭（stop），查看状态（status）.
#提醒:这些服务在30分钟只能启动3次,超过就报错. 
#StartLimitInterval=30min
#StartLimitBurst=3
#在这个文件中有定义/usr/lib/systemd/system/ceph-mon@.service
#如果修改该文件，需要执行命令# systemctl  daemon-reload重新加载配置
```
4）查看ceph集群状态（现在状态应该是health HEALTH_ERR）
```shell
[root@node1 ceph-cluster]# ceph -s
```
【提示】：如果无法成功部署ceph集群，可以通过如下命令清理集群软件以及相关数据（注意，这些操作会删除node1-node3主机的所有ceph软件及配置文件等数据，非必要不要操作！！）。
```shell
[root@node1 ceph-cluster]# ceph-deploy  purge  node1  node2  node3
[root@node1 ceph-cluster]# ceph-deploy  purgedata  node1  node2  node3
```
**步骤三：创建OSD**

1) 初始化清空磁盘数据（仅node1操作即可）。

初始化磁盘，将所有磁盘分区格式设置为GPT格式（根据实际情况填写磁盘名称）。
```shell
[root@node1 ceph-cluster]# ceph-deploy disk  zap  node1:vdb   node1:vdc   
[root@node1 ceph-cluster]# ceph-deploy disk  zap  node2:vdb   node2:vdc
[root@node1 ceph-cluster]# ceph-deploy disk  zap  node3:vdb   node3:vdc  
#相当于ssh 远程node1，在node1执行parted /dev/vdb  mktable  gpt
#其他主机都是一样的操作
#ceph-deploy是个脚本，这个脚本会自动ssh远程自动创建gpt分区
```
思考题？
```shell
# vim test.sh
#!/bin/bash
case $1 in
user)
     useradd -u 1000 $2;;
disk)
     parted  /dev/$2  mktable  gpt;;
esac
# chmod +x test.sh
# ./test.sh  user  jerry
# ./test.sh  disk  vdc
```
执行上面的脚本没有指定账户UID，为什么会自动创建一个UID为1000的用户？

执行上面的脚本没有指定磁盘分区表类型，为什么创建的分区表类型为gpt类型？

上面的脚本如果执行时不给位置变量的参数为怎么样？

2）创建OSD存储空间（仅node1操作即可）

重要：很多同学在这里会出错！将主机名、设备名称输入错误！！！

远程所有node主机，创建分区，格式化磁盘，挂载磁盘，启动osd服务共享磁盘。
```shell
[root@node1 ceph-cluster]# ceph-deploy osd create node1:vdb  node1:vdc
#每个磁盘都会被自动分成两个分区；一个固定5G大小；一个为剩余所有容量
#5G分区为Journal日志缓存；剩余所有空间为数据盘。
[root@node1 ceph-cluster]# ceph-deploy osd create node2:vdb  node2:vdc
[root@node1 ceph-cluster]# ceph-deploy osd create node3:vdb  node3:vdc
```
提醒：ceph-deploy是个脚本，脚本会自动创建分区、格式化、挂载！

怎么验证分区了？怎么验证格式化？怎么验证挂载了？
```shell
[root@node1 ~]# df -Th
[root@node2 ~]# df -Th
[root@node3 ~]# df -Th
```
思考题：请问lsblk和df命令的区别？

3）在三台不同的主机查看OSD服务状态，可以开启、关闭、重启服务。

注意：注意看清楚下面的主机名！！！
```shell
[root@node1 ~]# systemctl status ceph-osd@0
[root@node2 ~]# systemctl status ceph-osd@2
[root@node3 ~]# systemctl status ceph-osd@4
#备注:管理员可以自己启动（start）、重启（restart）、关闭（stop），查看状态（status）.
#提醒:这些服务在30分钟只能启动3次,超过就报错.
#StartLimitInterval=30min
#StartLimitBurst=3
#在这个文件中有定义/usr/lib/systemd/system/ceph-osd@.service
#如果修改该文件，需要执行命令# systemctl  daemon-reload重新加载配置
```
常见错误及解决方法（非必须操作）。

使用osd create创建OSD存储空间时，如提示下面的错误提示：
[ceph_deploy][ERROR ] RuntimeError: bootstrap-osd keyring not found; run 'gatherkeys'

可以使用如下命令修复文件，重新配置ceph的密钥文件：
```shell
[root@node1 ceph-cluster]#  ceph-deploy gatherkeys node1 node2 node3 
```
**步骤四：验证测试**

1) 查看集群状态。
```shell
[root@node1 ~]#  ceph  -s
[root@node1 ~]#  ceph   osd   tree
```
2）常见错误（非必须操作）。

如果查看状态包含如下信息：
```shell
health: HEALTH_WARN
        clock skew detected on  node2, node3…  
```
clock skew表示时间不同步，解决办法：请先将所有主机的时间都使用NTP时间同步！！！

Ceph要求所有主机时差不能超过0.05s，否则就会提示WARN。

如果状态还是失败，可以尝试执行如下命令，重启所有ceph服务：
```shell
[root@node1 ~]#  systemctl restart ceph.target
```
# 3. 创建Ceph块存储
## 3.1 问题
沿用练习一，使用Ceph集群的块存储功能，实现以下目标：

- 创建块存储镜像
- 客户端映射镜像
- 删除镜像

## 3.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：创建镜像**

1）查看存储池，默认存储池名称为rbd。
```shell
[root@node1 ~]# ceph osd lspools
0 rbd,
#查看结果显示，共享池的名称为rbd，这个共享池的编号为0，英语词汇：pool（池塘、水塘）
```
2）创建镜像、查看镜像
```shell
[root@node1 ~]# rbd create demo-image --size 10G
#创建demo-image镜像，这里的demo-image创建的镜像名称，名称可以为任意字符。
#size可以指定镜像大小
[root@node1 ~]# rbd create rbd/jacob  --size 10G
#在rbd池中创建名称为jacob的镜像（rbd/jacob），镜像名称可以任意
[root@node1 ~]# rbd list                    #列出所有镜像
[root@node1 ~]# rbd info demo-image        #查看demo-image这个镜像的详细信息
rbd image 'demo-image':
    size 10240 MB in 2560 objects
    order 22 (4096 kB objects)
    block_name_prefix: rbd_data.d3aa2ae8944a
    format: 2
    features: layering
```
步骤二：动态调整

1）扩容容量
```shell
[root@node1 ~]# rbd resize --size 15G jacob             
#调整jacob镜像的大小，jacob是镜像的名称，size指定扩容到15G
[root@node1 ~]# rbd info jacob
```
2）缩小容量
```shell
[root@node1 ~]# rbd resize --size 7G jacob --allow-shrink
#英文词汇：allow（允许），shrink（缩小）
[root@node1 ~]# rbd info jacob
#查看jacob这个镜像的详细信息（jacob是前面创建的镜像）
```
**步骤三：通过KRBD访问**

Linux内核可用直接访问Ceph块存储，KVM可用借助于librbd访问Ceph块存储。

客户端访问结构如图-6所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/b3940b5e20ce48bfb90537619685c268.png)
图-6

1）客户端通过KRBD访问
```shell
#客户端需要安装ceph-common软件包
#拷贝配置文件（否则不知道集群在哪）
#拷贝连接密钥（否则无连接权限）
[root@client ~]# yum -y  install ceph-common
[root@client ~]# scp 192.168.4.11:/etc/ceph/ceph.conf  /etc/ceph/
[root@client ~]# scp 192.168.4.11:/etc/ceph/ceph.client.admin.keyring \
/etc/ceph/
[root@client ~]# rbd map  jacob          #客户端访问映射服务器的jacob共享镜像
[root@client ~]#  lsblk                   #查看结果（会多一块磁盘）
[root@client ~]# rbd showmapped          #查看磁盘名和共享镜像名称的对应关系
id pool image snap device    
0  rbd  jacob -    /dev/rbd0
```
2) 客户端格式化、挂载分区
```shell
[root@client ~]# mkfs.xfs /dev/rbd0                     #格式化，格式为xfs
[root@client ~]# mount /dev/rbd0 /mnt/                  #挂载（可以挂载到任意目录）
[root@client ~]# echo "test" > /mnt/test.txt           #写入数据
```
**步骤四：删除镜像**

1） 客户端撤销磁盘映射
```shell
[root@client ~]# umount /mnt                      #卸载
[root@client ~]# rbd showmapped                  #查看磁盘名和共享镜像名称的对应关系
id pool image        snap device    
0  rbd  jacob        -    /dev/rbd0
[root@client ~]# rbd unmap /dev/rbd0            #撤销磁盘映射
```
附加信息：Ceph操作思路（知识总结）

一、准备工作：

IP，主机名，hosts解析，ssh密钥，时间同步，yum源，防火墙，selinux

二、部署ceph：

1.安装软件
```shell
  ceph-deploy(脚本)
  ceph-mon  ceph-osd  ceph-mds  ceph-radosgw(集群)
```
2.修改配置启动服务mon
```shell
  mkdir  目录；cd 目录
  ceph-deploy  new  node1   node2   node3  (生成配置文件)
  ceph-deploy  mon  create-initial  (拷贝配置文件并启动mon服务)
```
3.启动osd服务共享硬盘
```shell
  ceph-deploy  disk  zap   主机名:磁盘名  ...  ...
  ceph-deploy  osd  create  主机名:磁盘   ...  ...
```
三、使用Ceph的思路:

1.块共享
```shell
  服务器: rbd  create  创建一个共享镜像
  客户端: 安装cpeh-common;  cp 配置文件和密钥
          rbd  map  |  rbd  unmap
```
附加知识（如何删除某个OSD，下面的假设是删除osd.4）
```shell
ceph osd tree
ceph osd out osd.4
ceph osd tree
ceph -s
ceph osd crush remove osd.4
ceph auth del osd.4
ceph -s
ceph osd rm osd.4
最后要找到对应的主机，umount把osd.4对应的磁盘卸载
```


# Exercise
## 1 写出Ceph核心组件？
-  OSDs：存储设备
- Monitors：集群监控组件
- MDSs：存放文件系统的元数据（对象存储和块存储不需要该组件）
- RadosGW：对象存储网关

## 2 使用什么工具可以快速部署Ceph集群存储？
ceph-deploy。

## 3 Linux客户端访问Ceph块存储设备的命令？
rbd map 镜像名称。

> 如有侵权，请联系作者删除
