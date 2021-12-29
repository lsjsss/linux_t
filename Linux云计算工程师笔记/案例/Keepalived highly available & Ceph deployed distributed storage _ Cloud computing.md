﻿@[TOC]( Keepalived highly available & Ceph deployed distributed storage | Cloud computing )

---
# 1. Keepalived高可用
## 1.1 问题
部署两台代理服务器，实现如下效果：
- 利用keepalived实现两台代理服务器的高可用
- 配置VIP为192.168.4.80
- 修改对应的域名解析记录
## 1.2 方案
实验拓扑如图-1所示，做具体实验前请先配置好环境。

![在这里插入图片描述](https://img-blog.csdnimg.cn/85b5ce30ee73454686e71f24c0a35270.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_18,color_FFFFFF,t_70,g_se,x_16)
图-1

备注：实际操作中DNS服务代理服务器部署在同一台主机上（节约虚拟机资源）。

主机配置如表-1所示。

表-1
![在这里插入图片描述](https://img-blog.csdnimg.cn/f2ae855cc6de41c3ae616a51f9aacf23.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)


## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：配置第二台代理服务器**

1）部署HAProxy

安装软件，手动修改配置文件，添加如下内容。
```shell
[root@proxy2 ~]# yum -y install haproxy 
[root@proxy2 ~]# vim /etc/haproxy/haproxy.cfg
listen wordpress *:80        #监听80端口
  balance roundrobin        #轮询算法
  server web1 192.168.2.11:80 check inter 2000 rise 2 fall 3
  server web2 192.168.2.12:80 check inter 2000 rise 2 fall 3
  server web3 192.168.2.13:80 check inter 2000 rise 2 fall 3
[root@proxy2 ~]# systemctl start haproxy
[root@proxy2 ~]# systemctl enable haproxy
[root@proxy2 ~]# firewall-cmd --set-default-zone=trusted
[root@proxy2 ~]# setenforce  0
[root@proxy2 ~]# sed -i  '/SELINUX/s/enforcing/permissive/'  /etc/selinux/config
```
**步骤二：为两台代理服务器配置keepalived**

1）配置第一台代理服务器proxy（192.168.4.5）。
```shell
[root@proxy ~]# yum install -y keepalived
[root@proxy ~]# vim /etc/keepalived/keepalived.conf
global_defs {
  router_id  proxy1                #设置路由ID号
  vrrp_iptables                    #设置防火墙规则（手动添加该行）
}
vrrp_instance VI_1 {
  state MASTER                         #主服务器为MASTER（备服务器需要修改为BACKUP）
  interface eth0                    #网卡名称（不能照抄网卡名）
  virtual_router_id 51                
  priority 100                     #服务器优先级,优先级高优先获取VIP（实验需要修改）
  advert_int 1
  authentication {
    auth_type pass
    auth_pass 1111                #主备服务器密码必须一致
  }
  virtual_ipaddress {                #谁是主服务器谁获得该VIP（实验需要修改）
192.168.4.80 
}    
}
[root@proxy ~]# systemctl start keepalived
[root@proxy ~]# systemctl enable keepalived
```
2）配置第二台代理服务器proxy（192.168.4.6）。
```shell
[root@proxy2 ~]# yum install -y keepalived
[root@proxy2 ~]# vim /etc/keepalived/keepalived.conf
global_defs {
  router_id  proxy2                        #设置路由ID号
vrrp_iptables                               #设置防火墙规则（手动添加该行）
}
vrrp_instance VI_1 {
  state BACKUP                         #主服务器为MASTER（备服务器需要修改为BACKUP）
  interface eth0                    #网卡名称（不能照抄网卡名）
  virtual_router_id 51                
  priority 50                         #服务器优先级,优先级高优先获取VIP
  advert_int 1
  authentication {
    auth_type pass
    auth_pass 1111                       #主备服务器密码必须一致
  }
  virtual_ipaddress {                   #谁是主服务器谁获得该VIP
192.168.4.80 
}    
}
[root@proxy2 ~]# systemctl start keepalived
[root@proxy2 ~]# systemctl enable keepalived
```
**步骤三：修改DNS服务器**

1）修改网站域名对应的解析记录，解析到新的VIP地址。

192.168.4.5为DNS服务器，DNS配置文件相关知识请参考第一阶段课程。
```shell
[root@proxy ~]# vim /var/named/lab.com.zone
$TTL 1D
@       IN SOA  @ rname.invalid. (
                                        0       ; serial
                                        1D      ; refresh
                                        1H      ; retry
                                        1W      ; expire
                                        3H )    ; minimum
@       NS      dns.lab.com.
dns     A       192.168.4.5
www     A       192.168.4.80
```
2）重启DNS服务
```shell
[root@proxy ~]# systemctl restart named
```
# 2. 部署Ceph分布式存储
## 2.1 问题
部署Ceph分布式存储，实现如下效果：

- 使用三台服务器部署Ceph分布式存储
- 实现Ceph文件系统共享
- 将网站数据从NFS迁移到Ceph存储

## 2.2 方案
实验拓扑如图-2所示，做具体实验前请先配置好环境。

![在这里插入图片描述](https://img-blog.csdnimg.cn/7235f82ba38a4f33aef22add7d07b6a7.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-2
![在这里插入图片描述](https://img-blog.csdnimg.cn/db5af21690a64063a17558c315ada996.png)

备注：实际操作中DNS服务代理服务器部署在同一台主机上（节约虚拟机资源）。

主机配置如表-2所示。

表-2
![在这里插入图片描述](https://img-blog.csdnimg.cn/608b230403d2429984b458a09e7067f3.png)

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：准备实验环境**

1）把3台虚拟机全部关机,添加光盘和磁盘:

每台虚拟机都添加一个光驱；

做如下相同操作:

右击虚拟机,选【设置】---【添加】---【CD|DVD驱动器】--【完成】；

点击刚刚新建的光盘[CD|DVD],勾选使用ISO映像文件--[浏览]；

找到自己真机的ceph10.iso加载即可。

添加磁盘：所有3台ceph服务器都添加2块20G磁盘。

启动所有虚拟机后，查看磁盘情况:
```shell
    [root@node1 ~]# lsblk
    [root@node2 ~]# lsblk
    [root@node3 ~]# lsblk
```
所有主机设置防火墙和SELinux
```shell
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
2）所有主机挂载ceph光盘和系统光盘（根据实际情况挂载，不能照抄）
```shell
[root@node1 ~]# umount /dev/sr0
[root@node1 ~]# umount /dev/sr1
[root@node1 ~]# mkdir /ceph
[root@node1 ~]# vim /etc/fstab
    /dev/sr0    /ceph     iso9660   defaults   0  0
    /dev/sr1    /media    iso9660   defaults   0  0
[root@node1 ~]# mount -a
[root@node2 ~]# umount /dev/sr0
[root@node2 ~]# umount /dev/sr1
[root@node2 ~]# mkdir /ceph
[root@node2 ~]# vim /etc/fstab
    /dev/sr0    /ceph     iso9660   defaults   0  0
    /dev/sr1    /media    iso9660   defaults   0  0
[root@node2 ~]# mount -a
[root@node3 ~]# umount /dev/sr0
[root@node3 ~]# umount /dev/sr1
[root@node3 ~]# mkdir /ceph
[root@node3 ~]# vim /etc/fstab
    /dev/sr0    /ceph     iso9660   defaults   0  0
    /dev/sr1    /media    iso9660   defaults   0  0
[root@node3 ~]# mount -a
```
3）在node1配置SSH密钥，让node1可用无密码连接node1,node2,node3
```shell
[root@node1 ~]# ssh-keygen  -f /root/.ssh/id_rsa  -N  ''
#-f后面跟密钥文件的名称（创建密钥到哪个文件）
#-N  ''设置密钥的密码为空（不要给密钥配置密码）
[root@node1 ~]# for i in   41  42  43
do
ssh-copy-id  192.168.2.$i
done
#通过ssh-copy-id将密钥传递给node1，node2，node3
```
4)修改/etc/hosts域名解析记录（不要删除原文件的数据），同步给所有ceph节点。
```shell
[root@node1 ~]# vim /etc/hosts      #修改文件，手动添加如下内容（不要删除原文件的数据）
192.168.2.41    node1
192.168.2.42     node2
192.168.2.43    node3
[root@node1 ~]# for i in 41 42 43
do
     scp /etc/hosts 192.168.2.$i:/etc
done
```
5）为所有ceph节点配置yum源，并将配置同步给所有节点

提示：前面已经将ceph的光盘挂载到/ceph目录。
```shell
[root@node1 ~]# cat /etc/yum.repos.d/ceph.repo
[mon]
name=mon
baseurl=file:///ceph/MON
gpgcheck=0
[osd]
name=osd
baseurl=file:///ceph/OSD
gpgcheck=0
[tools]
name=tools
baseurl=file:///ceph/Tools
gpgcheck=0
[root@node1 ~]# yum repolist                #验证YUM源软件数量
源标识            源名称                    状态
Dvd                redhat                    9,911
Mon                mon                        41
Osd                osd                        28
Tools            tools                    33
repolist: 10,013
[root@node1 ~]# for i in 41 42 43
do
     scp /etc/yum.repos.d/ceph.repo 192.168.2.$i:/etc/yum.repos.d/
done
```
6）配置NTP服务器同步时间。

node1做服务器。
```shell
[root@node1 ~]# vim /etc/chrony.conf
allow 192.168.2.0/24        #修改26行
local stratum 10            #修改29行(去注释即可)
[root@node1 ~]# systemctl restart chronyd
```
node2和node3做客户端
```shell
[root@node2 ~]# vim /etc/chrony.conf
server 192.168.2.41   iburst              #配置文件第二行，手动加入该行内容
[root@node2 ~]# systemctl restart chronyd
[root@node2 ~]# chronyc sources -v
[root@node3 ~]# vim /etc/chrony.conf
server 192.168.2.41   iburst              #配置文件第二行，手动加入该行内容
[root@node3 ~]# systemctl restart chronyd
[root@node3 ~]# chronyc sources -v
```
**步骤二：部署ceph集群**

1）给node1主机安装ceph-deploy，创建工作目录，初始化配置文件。
```shell
[root@node1 ~]# yum -y install ceph-deploy
[root@node1 ~]# mkdir ceph-cluster
[root@node1 ~]# cd ceph-cluster
```
2）给所有ceph节点安装ceph相关软件包
```shell
[root@node1 ceph-cluster]# for i in node1 node2 node3
do
     ssh $i "yum -y install ceph-mon ceph-osd ceph-mds"
done
```
3）初始化mon服务
```shell
[root@node1 ceph-cluster]# ceph-deploy new node1 node2 node3
#生成ceph配置文件
[root@node1 ceph-cluster]# ceph-deploy mon create-initial
#拷贝ceph配置文件给node1,node2,node3，启动所有主机的mon服务
[root@node1 ceph-cluster]# ceph -s                    #查看状态（此时失败是正常的）
    cluster 9f3e04b8-7dbb-43da-abe6-b9e3f5e46d2e
     health HEALTH_ERR
     monmap e2: 3 mons at
 {node1=192.168.2.41:6789/0,node2=192.168.2.42:6789/0,node3=192.168.2.43:6789/0}
     
osdmap e45: 0 osds: 0 up, 0 in
```
4）使用ceph-deploy工具初始化数据磁盘（仅node1操作），硬盘名称根据实际情况填写，不能照抄。
```shell
[root@node1 ceph-cluster]# ceph-deploy disk  zap  node1:sdb  node1:sdc    
[root@node1 ceph-cluster]# ceph-deploy disk  zap  node2:sdb  node2:sdc
[root@node1 ceph-cluster]# ceph-deploy disk  zap  node3:sdb  node3:sdc
```
5）初始化OSD集群，磁盘名称根据实际情况填写。
```shell
[root@node1 ceph-cluster]# ceph-deploy osd create  node1:sdb  node1:sdc  
#每个磁盘都会被自动分成两个分区；一个固定5G大小；一个为剩余所有容量
#5G分区为Journal缓存；剩余所有空间为数据盘。
[root@node1 ceph-cluster]# ceph-deploy osd create  node2:sdb  node2:sdc
[root@node1 ceph-cluster]# ceph-deploy osd create  node3:sdb  node3:sdc 
[root@node1 ceph-cluster]# ceph -s                 #查看集群状态，状态为OK
```
**步骤三：部署ceph文件系统**

1）启动mds服务（可以在node1或node2或node3启动，也可以在多台主机启动mds）
```shell
[root@node1 ceph-cluster]# ceph-deploy mds create node3
```
2）创建存储池（文件系统由inode和block组成）
```shell
[root@node1 ceph-cluster]# ceph osd pool create cephfs_data 64
[root@node1 ceph-cluster]# ceph osd pool create cephfs_metadata 64
[root@node1 ceph-cluster]# ceph osd lspools      #查看共享池
0 rbd,1 cephfs_data,2 cephfs_metadata
```
3）创建文件系统
```shell
[root@node1 ceph-cluster]# ceph fs new myfs1 cephfs_metadata cephfs_data
[root@node1 ceph-cluster]# ceph fs ls
name: myfs1, metadata pool: cephfs_metadata, data pools: [cephfs_data ]
```
**步骤四：迁移网站数据到ceph集群**

1）卸载web1，web2，web3的NFS共享。

暂停服务防止有人实时读写文件。
```shell
[root@web1 ~]# /usr/local/nginx/sbin/nginx -s stop
[root@web2 ~]# /usr/local/nginx/sbin/nginx -s stop
[root@web3 ~]# /usr/local/nginx/sbin/nginx -s stop
[root@web1 ~]# umount /usr/local/nginx/html
[root@web2 ~]# umount /usr/local/nginx/html
[root@web3 ~]# umount /usr/local/nginx/html
[root@web1 ~]# vim /etc/fstab
#192.168.2.31:/web_share/html /usr/local/nginx/html/ nfs defaults 0 0
[root@web2 ~]# vim /etc/fstab
#192.168.2.31:/web_share/html /usr/local/nginx/html/ nfs defaults 0 0
[root@web3 ~]# vim /etc/fstab
#192.168.2.31:/web_share/html /usr/local/nginx/html/ nfs defaults 0 0
```
2）web服务器永久挂载Ceph文件系统（web1、web2、web3都需要操作）。

在任意ceph节点，如node1查看ceph账户与密码。
```shell
[root@node1 ~]# cat /etc/ceph/ceph.client.admin.keyring 
[client.admin]
    key = AQA0KtlcRGz5JxAA/K0AD/uNuLI1RqPsNGC7zg==
```
/etc/rc.local是开机启动脚本，任何命令放在该文件中都是开机自启。

ceph-common是ceph的客户端软件。
```shell
[root@web1 ~]# yum -y install ceph-common
[root@web2 ~]# yum -y install ceph-common
[root@web3 ~]# yum -y install ceph-common
[root@web1 ~]#  mount -t ceph 192.168.2.41:6789:/ /usr/local/nginx/html/ \
-o name=admin,secret=AQA0KtlcRGz5JxAA/K0AD/uNuLI1RqPsNGC7zg==
[root@web1 ~]# echo 'mount -t ceph 192.168.2.41:6789:/ /usr/local/nginx/html/ \
-o name=admin,secret=AQA0KtlcRGz5JxAA/K0AD/uNuLI1RqPsNGC7zg==' >> /etc/rc.local 
[root@web1 ~]# chmod +x /etc/rc.local
[root@web2 ~]#  mount -t ceph 192.168.2.41:6789:/ /usr/local/nginx/html/ \
-o name=admin,secret=AQA0KtlcRGz5JxAA/K0AD/uNuLI1RqPsNGC7zg==
[root@web2 ~]# echo 'mount -t ceph 192.168.2.41:6789:/ /usr/local/nginx/html/ \
-o name=admin,secret=AQA0KtlcRGz5JxAA/K0AD/uNuLI1RqPsNGC7zg==' >> /etc/rc.local 
[root@web2 ~]# chmod +x /etc/rc.local
[root@web3 ~]#  mount -t ceph 192.168.2.41:6789:/ /usr/local/nginx/html/ \
-o name=admin,secret=AQA0KtlcRGz5JxAA/K0AD/uNuLI1RqPsNGC7zg==
[root@web3 ~]# echo 'mount -t ceph 192.168.2.41:6789:/ /usr/local/nginx/html/ \
-o name=admin,secret=AQA0KtlcRGz5JxAA/K0AD/uNuLI1RqPsNGC7zg==' >> /etc/rc.local 
[root@web3 ~]# chmod +x /etc/rc.local
```
另一种解决方案，还可以通过fstab实现永久挂载。

提示：如果希望使用fstab实现永久挂载，客户端需要额外安装libcephfs1软件包。
```shell
[root@web1 ~]# yum -y install libcephfs1
[root@web1 ~]# vim /etc/fstab
… …
192.168.2.41:6789:/ /usr/local/nginx/html/    ceph   defaults,_netdev,name=admin,secret=AQCVcu9cWXkgKhAAWSa7qCFnFVbNCTB2DwGIOA== 0 0
```
第三种挂载方案：对于高可用的问题，可以在mount时同时写入多个IP。
```shell
临时命令：
[root@web1 ~]# mount -t ceph  \
192.168.2.41:6789,192.168.2.42:6789,192.168.2.43:6789:/ /usr/local/nginx/html  \
-o name=admin,secret=密钥
永久修改：
[root@web1 ~]# vim /etc/fstab
192.168.2.41:6789,192.168.2.42:6789,192.168.2.43:6789:/ /usr/local/nginx/html/ \
ceph defaults,_netdev,name=admin,secret=密钥 0 0
```
3)迁移NFS服务器中的数据到Ceph存储

登陆NFS服务器备份数据，将备份数据拷贝给web1或web2或web3，tar备份数据时注意使用-p选项保留文件权限。
```shell
[root@nfs ~]# cd /web_share/html/
[root@nfs html]# tar -czpf /root/html.tar.gz ./*
[root@nfs html]# scp /root/html.tar.gz 192.168.2.11:/usr/local/nginx/html/
```
登陆web1将数据恢复到Ceph共享目录
```shell
[root@web1 html]# tar -xf html.tar.gz
[root@web1 html]# rm -rf html.tar.gz
```
4）恢复web服务
```shell
[root@web1 ~]# /usr/local/nginx/sbin/nginx
[root@web2 ~]# /usr/local/nginx/sbin/nginx
[root@web3 ~]# /usr/local/nginx/sbin/nginx
```
附加知识（常见面试题）

1) 如何使用awk查看TCP连接状态？

答：ss -ant |awk '{print $1}'
netstat -ant |awk '{print $6}'

2) 有个txt文件内容如下：
http://a.domain.com/l.html
http://b.domain.com/l.html
http://c.domain.com/l.html
http://a.domain.com/2.html
http://b.domain.com/2.html
http://a.domain.com/3.html

要求：编写脚本获取主机名、域名，并统计每个域名出现的次数，并排序。

答：
```shell
#！/bin/bash
awk -F"[/.]" '{print $3}' txt    #单独获取主机名
awk -F"[/]" '{print $3}'  txt    #获取完整域名
awk -F"[/]" '{IP[$3]++} END{for(i in IP){print IP[i],i}}' txt | sort -n
```
3) 至少说出一种linux下实现高可用的方案名称？

答：keepalived，HeartBeat

4) 简述下负载均衡与高可用的概念？

答：
LB（Load_balancing）: 多台服务器平均响应客户端的多次连接请求。
HA（High Availability）: 主备模式，主服务器宕机后，备用服务器才接替工作。

5) 列举几种你知道的LVS调度算法？

答：
轮询（Round Robin）
加权轮询（Weighted Round Robin）
最少连接（Least Connections）
加权最少连接（ Weighted Least Connections ）
源地址哈希值（source hash）

6) 如果你们公司的网站访问很慢，你会如何排查？

答：
查看流量(Zabbix,ifconfig,sar,ping延迟… …)
系统负载(Zabbix,uptime,sar,top,ps,free查看CPU和内存)
日志（数据库日志-慢查询日志、web服务器日志、ELK）
DNS解析；ss端口状态、并发量；本机时间（时间错误会导致服务器故障）
浏览器F12（开发者工具）

7) 你会用什么方法来查看某个应用服务的流量使用情况?

答：
ifconfig eth0（查看网卡整体流量）
iftop（需要安装iftop软件包，实时查看具体IP、端口的流量，iftop -P）
iptraf-ng (需要安装iptraf-ng软件包，实时查看IP、端口的流量)
sar -n DEV（需要安装sysstat软件包，查看历史网卡流量，或者实时查看流量）
nethogs eth0（需要安装nethogs软件包，实时查看进程流量）

查看网站的访问日志（利用awk统计资源的大小并求和）
通过zabbix查看软件流量

> 如有侵权，请联系作者删除
