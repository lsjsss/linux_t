@[TOC]( Data analysis & node management & setting up NFS gateway service | Cloud computing )

---

# 1. 数据分析

## 1.1 问题

本案例要求统计分析练习：

- 使用 客户端 在 hdfs 上创建 input 目录
- 并上传 *.txt 文件到 input 目录
- 调用集群对上传文件进行分析，统计出现次数最多的单词

## 1.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：词频统计**

```shell
[root@hadoop1 hadoop]# ./bin/hadoop fs -ls /        //查看集群文件系统的根，没有内容
[root@hadoop1 hadoop]# ./bin/hadoop fs -mkdir  /aaa        
//在集群文件系统下创建aaa目录
[root@hadoop1 hadoop]# ./bin/hadoop fs -ls /        //再次查看，有刚创建的aaa目录
Found 1 items
drwxr-xr-x   - root supergroup          0 2018-09-10 09:56 /aaa
[root@hadoop1 hadoop]#  ./bin/hadoop fs -touchz  /fa    //在集群文件系统下创建fa文件
[root@hadoop1 hadoop]# ./bin/hadoop fs -put *.txt /aaa     
//上传*.txt到集群文件系统下的aaa目录
[root@hadoop1 hadoop]#  ./bin/hadoop fs -ls /aaa    //查看
Found 3 items
-rw-r--r--   2 root supergroup      86424 2018-09-10 09:58 /aaa/LICENSE.txt
-rw-r--r--   2 root supergroup      14978 2018-09-10 09:58 /aaa/NOTICE.txt
-rw-r--r--   2 root supergroup       1366 2018-09-10 09:58 /aaa/README.txt
[root@hadoop1 hadoop]# ./bin/hadoop fs -get  /aaa  //下载集群文件系统的aaa目录
[root@hadoop1 hadoop]# ./bin/hadoop jar  \
 share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.7.jar  wordcount /aaa /bbb    //hadoop集群分析大数据，hadoop集群/aaa里的数据存到hadoop集群/bbb下
[root@hadoop1 hadoop]# ./bin/hadoop fs -cat /bbb/*        //查看集群里的数据
```



# 2. 节点扩容

## 2.1 问题

本案例要求实现节点扩容：

- 最低配置：2CPU，2G内存，10G硬盘
- 虚拟机IP：192.168.1.54 newnode
- 增加 datanode和nodemanager

## 2.2 方案

另外准备两台主机，newnode和nfsgw，作为新添加的节点和网关，具体要求如表-2所示：

表-2

![img](https://img-blog.csdnimg.cn/img_convert/ad34eb23d521ee48b2f9223f20e19d38.png)

## 2.3 步骤

实现此案例需要按照如下步骤进行。

**步骤一：增加节点**

1）增加一个新的节点newnode

```shell
[root@hadoop5 ~]# echo newnode > /etc/hostname     //更改主机名为newnode
[root@hadoop5 ~]# hostname newnode
[root@newnode ~]# yum -y install java-1.8.0-openjdk-devel
[root@newnode ~]# mkdir /var/hadoop
[root@hadoop1 .ssh]# ssh-copy-id 192.168.1.64
[root@hadoop1 .ssh]# vim /etc/hosts
192.168.1.50  hadoop1
192.168.1.51  node-0001
192.168.1.52  node-0002
192.168.1.53  node-0003
192.168.1.54  newnode
[root@hadoop1 .ssh]# scp /etc/hosts 192.168.1.54:/etc/
[root@hadoop1 ~]# cd /usr/local/hadoop/
[root@hadoop1 hadoop]# vim ./etc/hadoop/slaves
node-0001
node-0002
node-0003
newnode
[root@hadoop1 hadoop]# for i in {51..54}; do rsync -aSH --delete /usr/local/hadoop/
\ 192.168.1.$i:/usr/local/hadoop/  -e 'ssh' & done        //同步配置
[1] 1841
[2] 1842
[3] 1843
[4] 1844
[root@newnode ~]# cd /usr/local/hadoop/
[root@newnode hadoop]# ./sbin/hadoop-daemon.sh start datanode  //启动
```

2）查看状态

```shell
[root@newnode hadoop]# jps
24439 Jps
24351 DataNode
```

3）设置同步带宽

```shell
[root@newnode hadoop]# ./bin/hdfs dfsadmin -setBalancerBandwidth 60000000
Balancer bandwidth is set to 60000000
[root@newnode hadoop]# ./sbin/start-balancer.sh
```



# 3. 缩减集群节点

## 3.1 问题

本案例要求缩减集群：

- 把刚刚加入集群的newnode节点从集群中删除
- 为了能看到三种状态，先往 HDFS 上传一些文件
- 记录每台主机的数据量，然后执行迁移数据

## 3.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：缩减集群**

1）删除节点

```shell
[root@hadoop1 hadoop]# vim /usr/local/hadoop/etc/hadoop/slaves        
//去掉之前添加的newnode
node-0001
node-0002
node-0003
[root@hadoop1 hadoop]# vim /usr/local/hadoop/etc/hadoop/hdfs-site.xml        
//在此配置文件里面加入下面四行
<property>                                      
    <name>dfs.hosts.exclude</name>
    <value>/usr/local/hadoop/etc/hadoop/exclude</value>
</property>
[root@hadoop1 hadoop]# vim /usr/local/hadoop/etc/hadoop/exclude
newnode
```

5）导出数据

```shell
[root@hadoop1 hadoop]# ./bin/hdfs dfsadmin -refreshNodes
Refresh nodes successful
[root@hadoop1 hadoop]# ./bin/hdfs dfsadmin -report  
//查看newnode显示Decommissioned
Name: 192.168.1.64:50010 (newnode)
Hostname: newnode
Decommission Status : Decommissioned
Configured Capacity: 2135949312 (1.99 GB)
DFS Used: 4096 (4 KB)
Non DFS Used: 1861509120 (1.73 GB)
DFS Remaining: 274436096 (261.72 MB)
DFS Used%: 0.00%
DFS Remaining%: 12.85%
Configured Cache Capacity: 0 (0 B)
Cache Used: 0 (0 B)
Cache Remaining: 0 (0 B)
Cache Used%: 100.00%
Cache Remaining%: 0.00%
Xceivers: 1
Last contact: Tue Mar 05 17:17:09 CST 2019
[root@newnode hadoop]# ./sbin/hadoop-daemon.sh stop datanode    //停止datanode
stopping datanode
[root@newnode hadoop]# ./sbin/yarn-daemon.sh start nodemanager             
//yarn 增加 nodemanager
[root@newnode hadoop]# ./sbin/yarn-daemon.sh stop  nodemanager  //停止nodemanager
stopping nodemanager
[root@newnode hadoop]# ./bin/yarn node -list        
//yarn 查看节点状态，还是有newnode节点，要过一段时间才会消失
Total Nodes:4
         Node-Id         Node-State    Node-Http-Address    Number-of-Running-Containers
     node-0003:34628            RUNNING           node-0003:8042                               0
     node-0002:36300            RUNNING           node-0002:8042                               0
     newnode:42459            RUNNING           newnode:8042                               0
     node-0001:39196            RUNNING           node-0001:8042  
```



# 4. 创建账户并授权

## 4.1 问题

本案例要求：

- 在 namenode 和 nfsgw 添加用户 nfsuser
- 为 nfsuser 完成HDFS集群授权
- 最低配置：1cpu，1G内存，10G硬盘
- 虚拟机IP：192.168.1.55 nfsgw

## 4.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：基础准备**

1）更改主机名，配置/etc/hosts（/etc/hosts在hadoop1和nfsgw上面配置）

```shell
[root@localhost ~]# echo nfsgw > /etc/hostname 
[root@localhost ~]# hostname nfsgw
[root@hadoop1 hadoop]# vim /etc/hosts
192.168.1.50  hadoop1
192.168.1.51  node-0001
192.168.1.52  node-0002
192.168.1.53  node-0003
192.168.1.54  newnode
192.168.1.55  nfsgw
```

2）创建代理用户（hadoop1和nfsgw上面操作），以hadoop1为例子

```shell
[root@hadoop1 hadoop]# groupadd -g 800 nfsuser
[root@hadoop1 hadoop]# useradd -u 800 -g 800 -r -d /var/hadoop nfsuser
```

3）配置core-site.xml

```shell
[root@hadoop1 hadoop]# ./sbin/stop-all.sh   //停止所有服务
This script is Deprecated. Instead use stop-dfs.sh and stop-yarn.sh
Stopping namenodes on [hadoop1]
hadoop1: stopping namenode
node-0002: stopping datanode
newnode: no datanode to stop
node-0003: stopping datanode
node-0001: stopping datanode
Stopping secondary namenodes [hadoop1]
hadoop1: stopping secondarynamenode
stopping yarn daemons
stopping resourcemanager
node-0002: stopping nodemanager
node-0003: stopping nodemanager
newnode: no nodemanager to stop
node-0001: stopping nodemanager
...
[root@hadoop1 hadoop]# cd etc/hadoop
[root@hadoop1 hadoop]# >exclude
[root@hadoop1 hadoop]# vim core-site.xml
    <property>
        <name>hadoop.proxyuser.nfsuser.groups</name>
        <value>*</value>
    </property>
    <property>
        <name>hadoop.proxyuser.nfsuser.hosts</name>
        <value>*</value>
    </property>
```

4）同步配置到node-0001，node-0002，node-0003

```shell
[root@hadoop1 hadoop]# for i in {51..53}; do rsync -aSH --delete /usr/local/hadoop/ 192.168.1.$i:/usr/local/hadoop/  -e 'ssh' & done
[4] 2722
[5] 2723
[6] 2724
```

5）启动集群

```shell
[root@hadoop1 hadoop]# /usr/local/hadoop/sbin/start-dfs.sh
```

6）查看状态

```shell
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/hdfs  dfsadmin -report
```



# 5. 在nfsgw上运行网关服务

## 5.1 问题

本案例要求在 nfsgw 上运行网关服务：

- Hadoop portmap
- Hadoop nfs3

## 5.2 步骤

实现此案例需要按照如下步骤进行。

**步骤二：NFSGW配置**

1）卸载rpcbind 和 nfs-utils

```shell
[root@nfsgw ~]# yum  remove  -y  rpcbind  nfs-utils
```

2）安装java-1.8.0-openjdk-devel和rsync

```shell
[root@nfsgw ~]# yum -y install java-1.8.0-openjdk-devel
[root@hadoop1 hadoop]# rsync -avSH --delete \ 
/usr/local/hadoop/ 192.168.1.55:/usr/local/hadoop/  -e 'ssh'
```

3）创建数据根目录 /var/hadoop（在NFSGW主机上面操作）

```shell
[root@nfsgw ~]# mkdir /var/hadoop
```

4）创建转储目录，并给用户nfs 赋权

```shell
[root@nfsgw ~]# mkdir /var/nfstmp
[root@nfsgw ~]# chown nfsuser:nfsuser /var/nfstmp
```

5）给/usr/local/hadoop/logs赋权（在NFSGW主机上面操作）

```shell
[root@nfsgw ~]# setfacl -m user:nfsuser:rwx /usr/local/hadoop/logs
[root@nfsgw ~]# vim /usr/local/hadoop/etc/hadoop/hdfs-site.xml
    <property>
        <name>nfs.exports.allowed.hosts</name>
        <value>* rw</value>
    </property>
    <property>
        <name>nfs.dump.dir</name>
        <value>/var/nfstmp</value>
    </property>
```

6）可以创建和删除即可

```shell
[root@nfsgw ~]# su - nfs
[nfs@nfsgw ~]$ cd /var/nfstmp/
[nfs@nfsgw nfstmp]$ touch 1
[nfs@nfsgw nfstmp]$ ls
1
[nfs@nfsgw nfstmp]$ rm -rf 1
[nfs@nfsgw nfstmp]$ ls
[nfs@nfsgw nfstmp]$ cd /usr/local/hadoop/logs/
[nfs@nfsgw logs]$ touch 1
[nfs@nfsgw logs]$ ls
1 hadoop-root-secondarynamenode-hadoop1.log    yarn-root-resourcemanager-hadoop1.log
hadoop-root-namenode-hadoop1.log hadoop-root-secondarynamenode-hadoop1.out    yarn-root-resourcemanager-hadoop1.out
hadoop-root-namenode-hadoop1.out    hadoop-root-secondarynamenode-hadoop1.out.1
hadoop-root-namenode-hadoop1.out.1  SecurityAuth-root.audit
[nfs@nfsgw logs]$ rm -rf 1
[nfs@nfsgw logs]$ ls
```

7）启动服务

```shell
[root@nfsgw ~]# /usr/local/hadoop/sbin/hadoop-daemon.sh --script ./bin/hdfs start portmap        //portmap服务只能用root用户启动
starting portmap, logging to /usr/local/hadoop/logs/hadoop-root-portmap-nfsgw.out
[root@nfsgw ~]# jps
23714 Jps
23670 Portmap
[root@nfsgw ~]# su - nfsuser
Last login: Mon Sep 10 12:31:58 CST 2018 on pts/0
[nfsuser @nfsgw ~]$ cd /usr/local/hadoop/
[nfsuser@nfsgw hadoop]$ ./sbin/hadoop-daemon.sh  --script ./bin/hdfs start nfs3  
//nfs3只能用代理用户启动
starting nfs3, logging to /usr/local/hadoop/logs/hadoop-nfsuser-nfs3-nfsgw.out
[nfs@nfsgw hadoop]$ jps                    
1362 Jps
1309 Nfs3 
[root@nfsgw hadoop]# jps            //root用户执行可以看到portmap和nfs3
1216 Portmap
1309 Nfs3
1374 Jps
```



# 6. 挂载NFS

## 6.1 问题

本案例要求：

- 在newnode挂载 NFS 并实现开机自启
- 想一想如何实现 NFS 的高可用？

## 6.2 步骤

实现此案例需要按照如下步骤进行。

**步骤二：NFSGW测试**

1）实现客户端挂载（客户端可以用newnode这台主机）

```shell
[root@newnode ~]# rm -rf /usr/local/hadoop
[root@newnode ~]# yum -y install nfs-utils
[root@newnode ~]# mount -t nfs -o \
vers=3,proto=tcp,nolock,noatime,sync,noacl 192.168.1.55:/  /mnt/  //挂载
[root@newnode ~]# cd /mnt/
[root@newnode mnt]# ls
aaa  bbb  fa  system  tmp
[root@newnode mnt]# touch a
[root@newnode mnt]# ls
a  aaa  bbb  fa  system  tmp
[root@newnode mnt]# rm -rf a
[root@newnode mnt]# ls
aaa  bbb  fa  system  tmp
```

8）实现开机自动挂载

```shell
[root@newnode ~]# vim /etc/fstab
192.168.1.55:/  /mnt/ nfs  vers=3,proto=tcp,nolock,noatime,sync,noacl,_netdev 0 0 
[root@newnode ~]# mount -a
[root@newnode ~]# df -h
192.168.1.26:/   64G  6.2G   58G  10% /mnt
[root@newnode ~]# rpcinfo -p 192.168.1.55
   program vers proto   port  service
    100005    3   udp   4242  mountd
    100005    1   tcp   4242  mountd
    100000    2   udp    111  portmapper
    100000    2   tcp    111  portmapper
    100005    3   tcp   4242  mountd
    100005    2   tcp   4242  mountd
    100003    3   tcp   2049  nfs
    100005    2   udp   4242  mountd
    100005    1   udp   4242  mountd
```



# Exercise

## 1 如何查看Hadoop集群文件系统的根以及怎么创建

查看

```shell
 [root@nn01 hadoop]# /usr/local/hadoop/bin/hadoop fs -ls /
```

创建

```shell
[root@nn01 hadoop]# /usr/local/hadoop/bin/hadoop fs -mkdir  /aaa    
```

## 2 如何增加一个新的节点

1）增加一个新的节点node4

```shell
[root@hadoop5 ~]# echo node4 > /etc/hostname     //更改主机名为node4
[root@hadoop5 ~]# hostname node4
[root@node4 ~]# yum -y install rsync
[root@node4 ~]# yum -y install java-1.8.0-openjdk-devel
[root@node4 ~]# mkdir /var/hadoop
[root@nn01 .ssh]# ssh-copy-id 192.168.1.25
[root@nn01 .ssh]# vim /etc/hosts
192.168.1.21  nn01
192.168.1.22  node1
192.168.1.23  node2
192.168.1.24  node3
192.168.1.25  node4
[root@nn01 .ssh]# scp /etc/hosts 192.168.1.25:/etc/
[root@nn01 ~]# cd /usr/local/hadoop/
[root@nn01 hadoop]# vim ./etc/hadoop/slaves
node1
node2
node3
node4
[root@nn01 hadoop]# for i in {22..25}; do rsync -aSH --delete /usr/local/hadoop/
\ 192.168.1.$i:/usr/local/hadoop/  -e 'ssh' & done        //同步配置
[1] 1841
[2] 1842
[3] 1843
[4] 1844
[root@node4 hadoop]# ./sbin/hadoop-daemon.sh start datanode  //启动
2）查看状态    
[root@node4 hadoop]# jps
24439 Jps
24351 DataNode
```

## 3 如何设置同步带宽

```
[root@node4 hadoop]# ./bin/hdfs dfsadmin -setBalancerBandwidth 60000000
Balancer bandwidth is set to 60000000
[root@node4 hadoop]# ./sbin/start-balancer.sh
```

## 4 启动NFS需要注意什么

portmap服务只能用root用户启动，nfs3只能用代理用户启动，用root用户执行jps可以看到portmap和nfs3，代理用户执行jps看不到portmap

```shell
[root@nfsgw ~]# /usr/local/hadoop/sbin/hadoop-daemon.sh --script ./bin/hdfs start portmap        //portmap服务只能用root用户启动
starting portmap, logging to /usr/local/hadoop/logs/hadoop-root-portmap-nfsgw.out
[root@nfsgw ~]# jps
23714 Jps
23670 Portmap
[root@nfsgw ~]# su - nfs
Last login: Mon Sep 10 12:31:58 CST 2018 on pts/0
[nfs@nfsgw ~]$ cd /usr/local/hadoop/
[nfs@nfsgw hadoop]$ ./sbin/hadoop-daemon.sh  --script ./bin/hdfs start nfs3  
//nfs3只能用代理用户启动
starting nfs3, logging to /usr/local/hadoop/logs/hadoop-nfs-nfs3-nfsgw.out
[nfs@nfsgw hadoop]$ jps                    
1362 Jps
1309 Nfs3 
[root@nfsgw hadoop]# jps            //root用户执行可以看到portmap和nfs3
1216 Portmap
1309 Nfs3
1374 Jps
```



> 如有侵权，请联系作者删除


