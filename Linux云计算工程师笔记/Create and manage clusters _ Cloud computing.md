﻿@[TOC]( Create and manage clusters | Cloud computing )

---
# 1. 部署redis集群
## 1.1 问题
具体要求如下：
- 部署管理主机
- 创建集群
- 查看集群信息
- 访问集群

## 1.2 方案
搭建redis集群，拓扑规划如图-1所示：
![在这里插入图片描述](https://img-blog.csdnimg.cn/1ee8503790234097ad81225d6723f0ef.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图－1

IP，端口规划如表-1所示：

表-1
![在这里插入图片描述](https://img-blog.csdnimg.cn/084da6b7a61d49c187be83e86cfa6629.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：配置管理主机mgm57**

1）部署ruby脚本运行环境
```shell
[root@mgm57 ~]#yum  -y  install   rubygems 
[root@mgm57 ~]# which gem
/usr/bin/gem
[root@mgm57 ~]# ls  *.gem
redis-3.2.1.gem
[root@mgm57 ~]#
[root@mgm57 ~]# gem install redis-3.2.1.gem
Successfully installed redis-3.2.1
Parsing documentation for redis-3.2.1
Installing ri documentation for redis-3.2.1
1 gem installed
[root@mgm57 ~]#
```
2）创建管理集群脚本
```shell
[root@mgm57 ~]#mkdir  /root/bin     //创建命令检索目录
[root@mgm57 ~]#tar -zxvf redis-4.0.8.tar.gz
[root@mgm57 ~]#cd  redis-4.0.8/src/
[root@mgm57 ~]#cp  redis-trib.rb   /root/bin/ //创建管理集群脚本
[root@mgm57 ~]#chmod  +x   /root/bin/redis-trib.rb
[root@mgm57 ~]#redis-trib.rb   help  //查看命令帮助
```
**步骤二：创建集群**

1）启动服务器192.168.4.51的集群功能
```shell
[root@redisA ~]# /etc/init.d/redis_6379 stop //停止redis服务
Stopping ...
Waiting for Redis to shutdown ...
Redis stopped
[root@redisA ~]# vim /etc/redis/6379.conf //修改配置文件
bind 192.168.4.51        //修改ip
port 6351        //修改端口（可选配置）
cluster-enabled yes     //启用集群功能
cluster-config-file nodes-6379.conf //存储集群信息的配置文件
cluster-node-timeout 5000        //集群节点通信超时时间
:wq
[root@redisA ~]# rm  -rf  /var/lib/redis/6379/*   //清空数据
[root@redisA ~]# vim  +43 /etc/init.d/redis_6379
$CLIEXEC -h 192.168.4.51 -p 6351 shutdown
:wq
[root@redisA ~]# /etc/init.d/redis_6379 start
Starting Redis server...
[root@redisA ~]# netstat -utnlp  | grep redis-server
tcp  0  0 192.168.4.51:6351  0.0.0.0:*   LISTEN      21201/redis-server  
tcp  0  0 192.168.4.51:16351   0.0.0.0:*   LISTEN   21201/redis-server 
```
2）启动服务器192.168.4.52的集群功能
```shell
[root@redisB ~]# /etc/init.d/redis_6379 stop //停止redis服务
Stopping ...
Waiting for Redis to shutdown ...
Redis stopped
[root@redisB ~]# vim /etc/redis/6379.conf //修改配置文件
bind 192.168.4.52        //修改ip
port 6352        //修改端口（可选配置）
cluster-enabled yes     //启用集群功能
cluster-config-file nodes-6379.conf //存储集群信息的配置文件
cluster-node-timeout 5000        //集群节点通信超时时间
:wq
[root@redisB ~]# rm  -rf  /var/lib/redis/6379/*   //清空数据
[root@redisB ~]# vim  +43 /etc/init.d/redis_6379
$CLIEXEC -h 192.168.4.52 -p 6352 shutdown
:wq
[root@redisB ~]# /etc/init.d/redis_6379 stBrt
Stbrting Redis server...
[root@redisB ~]# netstat -utnlp  | grep redis-server
tcp  0  0 192.168.4.52:6352  0.0.0.0:*   LISTEN      21201/redis-server  
tcp  0  0 192.168.4.52:16352   0.0.0.0:*   LISTEN   21201/redis-server   
```
3）启动服务器192.168.4.53的集群功能
```shell
[root@redisC ~]# /etc/init.d/redis_6379 stop //停止redis服务
Stopping ...
Waiting for Redis to shutdown ...
Redis stopped
[root@redisC ~]# vim /etc/redis/6379.conf //修改配置文件
bind 192.168.4.53        //修改ip
port 6353        //修改端口（可选配置）
cluster-enabled yes     //启用集群功能
cluster-config-file nodes-6379.conf //存储集群信息的配置文件
cluster-node-timeout 5000        //集群节点通信超时时间
:wq
[root@redisC ~]# rm  -rf  /var/lib/redis/6379/*   //清空数据
[root@redisC ~]# vim  +43 /etc/init.d/redis_6379
$CLIEXEC -h 192.168.4.53 -p 6353 shutdown
:wq
[root@redisC ~]# /etc/init.d/redis_6379 start
Stbrting Redis server...
[root@redisC ~]# netstat -utnlp  | grep redis-server
tcp  0  0 192.168.4.53:6353  0.0.0.0:*   LISTEN      21201/redis-server  
tcp  0  0 192.168.4.53:16353   0.0.0.0:*   LISTEN   21201/redis-server   
```
4）启动服务器192.168.4.54的集群功能
```shell
[root@redisD ~]# /etc/init.d/redis_6379 stop //停止redis服务
Stopping ...
Waiting for Redis to shutdown ...
Redis stopped
[root@redisD ~]# vim /etc/redis/6379.conf //修改配置文件
bind 192.168.4.54        //修改ip
port 6354        //修改端口（可选配置）
cluster-enabled yes     //启用集群功能
cluster-config-file nodes-6379.Donf //存储集群信息的配置文件
cluster-node-timeout 5000        //集群节点通信超时时间
:wq
[root@redisD ~]# rm  -rf  /var/lib/redis/6379/*   //清空数据
[root@redisD ~]# vim  +43 /etc/init.d/redis_6379
$DLIEXED -h 192.168.4.54 -p 6354 shutdown
:wq
[root@redisD ~]# /etD/init.d/redis_6379 stdrt
Stbrting Redis server...
[root@redisD ~]# netstat -utnlp  | grep redis-server
tcp  0  0 192.168.4.54:6354  0.0.0.0:*   LISTEN      21201/redis-server  
tcp  0  0 192.168.4.54:16354   0.0.0.0:*   LISTEN   21201/redis-server   
```
5）启动服务器192.168.4.55的集群功能
```shell
[root@redisE ~]# /etc/init.d/redis_6379 stop //停止redis服务
Stopping ...
Waiting for Redis to shutdown ...
Redis stopped
[root@redisE ~]# vim /etc/redis/6379.conf //修改配置文件
bind 192.168.4.55        //修改ip
port 6355        //修改端口（可选配置）
cluster-enabled yes     //启用集群功能
cluster-config-file nodes-6379.conf //存储集群信息的配置文件
cluster-node-timeout 5000        //集群节点通信超时时间
:wq
[root@redisE ~]# rm  -rf  /var/lib/redis/6379/*   //清空数据
[root@redisE ~]# vim  +43 /etc/init.d/redis_6379
$CLIEXEC -h 192.168.4.55 -p 6355 shutdown
:wq
[root@redisE ~]# /etc/init.d/redis_6379 start
Stbrting Redis server...
[root@redisE ~]# netstat -utnlp  | grep redis-server
tcp  0  0 192.168.4.55:6355  0.0.0.0:*   LISTEN      21201/redis-server  
tcp  0  0 192.168.4.55:16355   0.0.0.0:*   LISTEN   21201/redis-server   
```
6）启动服务器192.168.4.56的集群功能
```shell
[root@redisF ~]# /etc/init.d/redis_6379 stop //停止redis服务
Stopping ...
Waiting for Redis to shutdown ...
Redis stopped
[root@redisF ~]# vim /etc/redis/6379.conf //修改配置文件
bind 192.168.4.56        //修改ip
port 6356        //修改端口（可选配置）
cluster-enabled yes     //启用集群功能
cluster-config-file nodes-6379.conf //存储集群信息的配置文件
cluster-node-timeout 5000        //集群节点通信超时时间
:wq
[root@redisF ~]# rm  -rf  /var/lib/redis/6379/*   //清空数据
[root@rediseF ~]# vim  +43 /etc/init.d/redis_6379
$CLIEXEC -h 192.168.4.56 -p 6356 shutdown
:wq
[root@redisF ~]# /etc/init.d/redis_6379 start
Stbrting Redis server...
[root@redisF ~]# netstat -utnlp  | grep redis-server
tcp  0  0 192.168.4.56:6356  0.0.0.0:*   LISTEN      21201/redis-server  
tcp  0  0 192.168.4.56:16356   0.0.0.0:*   LISTEN   21201/redis-server
```
7）在管理主机mgm57,创建集群
```shell
[root@mgm57 ~]# redis-trib.rb create  --replicas 1 \
> 192.168.4.51:6351  192.168.4.52:6352  192.168.4.53:6353 \
> 192.168.4.54:6354  192.168.4.55:6355  192.168.4.56:6356
>>> Performing hash slots allocation on 6 nodes...
Using 3 masters:
192.168.4.51:6351
192.168.4.52:6352
192.168.4.53:6353
Adding replica 192.168.4.55:6355 to 192.168.4.51:6351
Adding replica 192.168.4.56:6356 to 192.168.4.52:6352
Adding replica 192.168.4.54:6354 to 192.168.4.53:6353
M: d9f8fe6d6d9dd391be8e7904501db1535e4d17cb 192.168.4.51:6351
   slots:0-5460 (5461 slots) master
M: 324e05df3f143ef97e50d09be0328a695e655986 192.168.4.52:6352
   slots:5461-10922 (5462 slots) master
M: 9e44139cffb8ebd7ed746aabbf4bcea9bf207645 192.168.4.53:6353
   slots:10923-16383 (5461 slots) master
S: d9634ba0aa5c1a07193da4a013da6051c1515922 192.168.4.54:6354
   replicates 9e44139cffb8ebd7ed746aabbf4bcea9bf207645
S: 2d343a9df48f6f6e207949e980ef498466a44dad 192.168.4.55:6355
   replicates d9f8fe6d6d9dd391be8e7904501db1535e4d17cb
S: 894dd0008053f6fb65e9e4a36b755d9351607500 192.168.4.56:6356
   replicates 324e05df3f143ef97e50d09be0328a695e655986
Can I set the above configuration? (type 'yes' to accept): yes //同意以上配置
>>> Nodes configuration updated
>>> Assign a different config epoch to each node
>>> Sending CLUSTER MEET messages to join the cluster
Waiting for the cluster to join...
>>> Performing Cluster Check (using node 192.168.4.51:6351)
M: d9f8fe6d6d9dd391be8e7904501db1535e4d17cb 192.168.4.51:6351
   slots:0-5460 (5461 slots) master
   1 additional replica(s)
S: d9634ba0aa5c1a07193da4a013da6051c1515922 192.168.4.54:6354
   slots: (0 slots) slave
   replicates 9e44139cffb8ebd7ed746aabbf4bcea9bf207645
S: 894dd0008053f6fb65e9e4a36b755d9351607500 192.168.4.56:6356
   slots: (0 slots) slave
   replicates 324e05df3f143ef97e50d09be0328a695e655986
M: 324e05df3f143ef97e50d09be0328a695e655986 192.168.4.52:6352
   slots:5461-10922 (5462 slots) master
   1 additional replica(s)
M: 9e44139cffb8ebd7ed746aabbf4bcea9bf207645 192.168.4.53:6353
   slots:10923-16383 (5461 slots) master
   1 additional replica(s)
S: 2d343a9df48f6f6e207949e980ef498466a44dad 192.168.4.55:6355
   slots: (0 slots) slave
   replicates d9f8fe6d6d9dd391be8e7904501db1535e4d17cb
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.  //提示16384个槽分配完毕
[root@mgm57 ~]#
```
**步骤三：查看集群信息**

1）在管理主机查看集群信息
```shell
[root@mgm57 ~]# redis-trib.rb info 192.168.4.51:6351 //查看集群信息
192.168.4.51:6351 (d9f8fe6d...) -> 0 keys | 5461 slots | 1 slaves.
192.168.4.52:6352 (324e05df...) -> 0 keys | 5462 slots | 1 slaves.
192.168.4.53:6353 (9e44139c...) -> 0 keys | 5461 slots | 1 slaves.
[OK] 0 keys in 3 masters.
0.00 keys per slot on average
```
2）在管理主机检测集群
```shell
[root@mgm57 ~]# redis-trib.rb check 192.168.4.51:6351 //检测集群
>>> Performing Cluster Check (using node 192.168.4.51:6351)
M: d9f8fe6d6d9dd391be8e7904501db1535e4d17cb 192.168.4.51:6351
   slots:0-5460 (5461 slots) master
   1 additional replica(s)
S: d9634ba0aa5c1a07193da4a013da6051c1515922 192.168.4.54:6354
   slots: (0 slots) slave
   replicates 9e44139cffb8ebd7ed746aabbf4bcea9bf207645
S: 894dd0008053f6fb65e9e4a36b755d9351607500 192.168.4.56:6356
   slots: (0 slots) slave
   replicates 324e05df3f143ef97e50d09be0328a695e655986
M: 324e05df3f143ef97e50d09be0328a695e655986 192.168.4.52:6352
   slots:5461-10922 (5462 slots) master
   1 additional replica(s)
M: 9e44139cffb8ebd7ed746aabbf4bcea9bf207645 192.168.4.53:6353
   slots:10923-16383 (5461 slots) master
   1 additional replica(s)
S: 2d343a9df48f6f6e207949e980ef498466a44dad 192.168.4.55:6355
   slots: (0 slots) slave
   replicates d9f8fe6d6d9dd391be8e7904501db1535e4d17cb
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
```
3）在任意一台redis服务器本机，查看集群信息
```shell
[root@redisA ~]# redis-cli  -h 192.168.4.51 -p 6351
192.168.4.51:6351> cluster info       //查看集群信息
cluster_state:ok
……
……
cluster_known_nodes:6
cluster_size:3
192.168.4.51:6351> cluster  nodes   //查看集群节点信息
d9634ba0aa5c1a07193da4a013da6051c1515922 192.168.4.54:6354@16354 slave 9e44139cffb8ebd7ed746aabbf4bcea9bf207645 0 1561357552212 4 connected
894dd0008053f6fb65e9e4a36b755d9351607500 192.168.4.56:6356@16356 slave 324e05df3f143ef97e50d09be0328a695e655986 0 1561357554216 6 connected
d9f8fe6d6d9dd391be8e7904501db1535e4d17cb 192.168.4.51:6351@16351 myself,master - 0 1561357545000 1 connected 0-5460
324e05df3f143ef97e50d09be0328a695e655986 192.168.4.52:6352@16352 master - 0 1561357553214 2 connected 5461-10922
9e44139cffb8ebd7ed746aabbf4bcea9bf207645 192.168.4.53:6353@16353 master - 0 1561357554216 3 connected 10923-16383
2d343a9df48f6f6e207949e980ef498466a44dad 192.168.4.55:6355@16355 slave d9f8fe6d6d9dd391be8e7904501db1535e4d17cb 0 1561357553716 5 connected
192.168.4.51:6351>
```
**步骤四：访问集群**

1）在客户端连接集群中的任意一台服务器存取数据
```shell
 [root@client50 ~]# redis-cli  -c  -h 192.168.4.51 -p 6351 //连接服务器51
192.168.4.51:6351>
192.168.4.51:6351> set x 100  //存储
-> Redirected to slot [16287] located at 192.168.4.53:6353  //提示存储在53主机
OK
192.168.4.53:6353> keys *
1) "x"
192.168.4.53:6353>
192.168.4.53:6353> set y 200
OK
192.168.4.53:6353> keys *
1) "y"
2) "x"
192.168.4.53:6353> set z 300 //存储
-> Redirected to slot [8157] located at 192.168.4.52:6352 //提示存储在52主机
OK
192.168.4.52:6352> keys *  //在52主机查看数据 只有变量z 
1) "z"
192.168.4.52:6352> get x 
-> Redirected to slot [16287] located at 192.168.4.53:6353 //连接53主机获取数据
"100"
192.168.4.53:6353> keys *
1) "y"
2) "x"
192.168.4.53:6353> get z
-> Redirected to slot [8157] located at 192.168.4.52:6352
"300"
192.168.4.52:6352> set i 400
-> Redirected to slot [15759] located at 192.168.4.53:6353
OK
192.168.4.53:6353> set j 500
-> Redirected to slot [3564] located at 192.168.4.51:6351
OK
192.168.4.51:6351>
```
# 2. 添加服务器
## 2.1 问题
- 部署新redis服务器
- 添加master角色主机到集群里
- 添加slave角色主机到集群里

## 2.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：部署新redis服务器 ip为192.168.4.58**

1）装包，初始化，启用集群功能，重启服务
```shell
]#yum -y  install gcc
]#tar -zxvf redis-4.0.8.tar.gz
]#cd redis-4.0.8/
]#make
]#make install
]#./utils/install_server.sh
]# /etc/init.d/redis_6379  stop
vim /etc/redis/6379.conf
        bind 192.168.4.58
        port 6358
        cluster-enabled  yes                         //启用集群
        cluster-config-file  nodes-6379.conf      //存储集群信息文件
        cluster-node-timeout  5000
:wq
]# vim +43 /etc/init.d/redis_6379
         $CLIEXEC -h 192.168.4.58 -p 6358 shutdown
:wq
]# /etc/init.d/redis_6379  start
]# netstat -utnlp  | grep redis-server
tcp  0  0 192.168.4.58:6358  0.0.0.0:*   LISTEN      21201/redis-server  
tcp  0  0 192.168.4.58:16358   0.0.0.0:*   LISTEN   21201/redis-server   
```
**步骤二：添加master角色主机到集群里**

1）在管理主机，添加master角色主机
```shell
[root@mgm57 ~]# redis-trib.rb  add-node  192.168.4.58:6358  192.168.4.53:6353  //执行添加命令
>>> Adding node 192.168.4.58:6358 to cluster 192.168.4.53:6353
>>> Performing Cluster Check (using node 192.168.4.53:6353)
M: 9e44139cffb8ebd7ed746aabbf4bcea9bf207645 192.168.4.53:6353
   slots:10923-16383 (5461 slots) master
   1 additional replica(s)
S: d9634ba0aa5c1a07193da4a013da6051c1515922 192.168.4.54:6354
   slots: (0 slots) slave
   replicates 9e44139cffb8ebd7ed746aabbf4bcea9bf207645
M: 324e05df3f143ef97e50d09be0328a695e655986 192.168.4.52:6352
   slots:5461-10922 (5462 slots) master
   1 additional replica(s)
S: 894dd0008053f6fb65e9e4a36b755d9351607500 192.168.4.56:6356
   slots: (0 slots) slave
   replicates 324e05df3f143ef97e50d09be0328a695e655986
S: d9f8fe6d6d9dd391be8e7904501db1535e4d17cb 192.168.4.51:6351
   slots: (0 slots) slave
   replicates 2d343a9df48f6f6e207949e980ef498466a44dad
M: 2d343a9df48f6f6e207949e980ef498466a44dad 192.168.4.55:6355
   slots:0-5460 (5461 slots) master
   1 additional replica(s)
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
>>> Send CLUSTER MEET to node 192.168.4.58:6358 to make it join the cluster.
[OK] New node added correctly. //提示添加完成
[root@mgm57 ~]#
```
2） 在管理主机，查看集群新消息
```shell
[root@mgm57 ~]# redis-trib.rb info 192.168.4.53:6353  //查看集群信息
192.168.4.53:6353 (9e44139c...) -> 3 keys | 5461 slots | 1 slaves.
192.168.4.52:6352 (324e05df...) -> 2 keys | 5462 slots | 1 slaves.
192.168.4.58:6358 (4fe1fa46...) -> 0 keys | 0 slots | 0 slaves. //主服务器58
192.168.4.55:6355 (2d343a9d...) -> 3 keys | 5461 slots | 1 slaves.
[OK] 8 keys in 4 masters.
0.00 keys per slot on average.
[root@mgm57 ~]# 
```
3）在管理主机，检测集群
```shell
 [root@mgm57 ~]# redis-trib.rb check 192.168.4.53:6353    //检测集群
>>> Performing Cluster Check (using node 192.168.4.53:6353)
M: 9e44139cffb8ebd7ed746aabbf4bcea9bf207645 192.168.4.53:6353
   slots:10923-16383 (5461 slots) master
   1 additional replica(s)
S: d9634ba0aa5c1a07193da4a013da6051c1515922 192.168.4.54:6354
   slots: (0 slots) slave
   replicates 9e44139cffb8ebd7ed746aabbf4bcea9bf207645
M: 324e05df3f143ef97e50d09be0328a695e655986 192.168.4.52:6352
   slots:5461-10922 (5462 slots) master
   1 additional replica(s)
S: 894dd0008053f6fb65e9e4a36b755d9351607500 192.168.4.56:6356
   slots: (0 slots) slave
   replicates 324e05df3f143ef97e50d09be0328a695e655986
M: 4fe1fa467ad237802021f5aac5f1d5b3e0db47ef 192.168.4.58:6358
   slots: (0 slots) master  //master服务器58 ，没有hash槽
   0 additional replica(s)
S: d9f8fe6d6d9dd391be8e7904501db1535e4d17cb 192.168.4.51:6351
   slots: (0 slots) slave
   replicates 2d343a9df48f6f6e207949e980ef498466a44dad
M: 2d343a9df48f6f6e207949e980ef498466a44dad 192.168.4.55:6355
   slots:0-5460 (5461 slots) master
   1 additional replica(s)
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
[root@mgm57 ~]#
```
4）在管理主机，重新分配hash槽
```shell
[root@mgm57 ~]# redis-trib.rb  reshard   192.168.4.53:6353  
How many slots do you want to move (from 1 to 16384)?4096   //拿出4096个hash 槽给主机192.168.4.58
What is the receiving node ID?  c5e0da48f335c46a2ec199faa99b830f537dd8a0   //主机192.168.4.58的id值
Source node #1:all      //从当前所有master服务器获取hash槽
Do you want to proceed with the proposed reshard plan (yes/no)?yes //同意以上配置
...
Moving slot 12283 from 192.168.4.53:6353 to 192.168.4.58:6358: 
Moving slot 12284 from 192.168.4.53:6353 to 192.168.4.58:6358: 
Moving slot 12285 from 192.168.4.53:6353 to 192.168.4.58:6358: 
Moving slot 12286 from 192.168.4.53:6353 to 192.168.4.58:6358: 
Moving slot 12287 from 192.168.4.53:6353 to 192.168.4.58:6358:
```
5）在管理主机，查看集群信息
```shell
[root@mgm57 ~]# redis-trib.rb info 192.168.4.53:6353
192.168.4.53:6353 (9e44139c...) -> 2 keys | 4096 slots | 1 slaves.
192.168.4.52:6352 (324e05df...) -> 1 keys | 4096 slots | 1 slaves.
192.168.4.58:6358 (4fe1fa46...) -> 4 keys | 4096 slots | 0 slaves. //hash槽4096个
192.168.4.55:6355 (2d343a9d...) -> 1 keys | 4096 slots | 1 slaves.
[OK] 8 keys in 4 masters.
0.00 keys per slot on average.
[root@mgm57 ~]#  
```
**步骤三：添加slave角色主机到集群里**

1）部署新的redis服务器 192.168.4.59
```shell
]#yum -y  install gcc
]#tar -zxvf redis-4.0.8.tar.gz
]#cd redis-4.0.8/
]#make
]#make install
]#./utils/install_server.sh
]# /etc/init.d/redis_6379  stop
vim /etc/redis/6379.conf
        bind 192.168.4.59
        port 6359
        cluster-enabled  yes                         //启用集群
        cluster-config-file  nodes-6379.conf      //存储集群信息文件
        cluster-node-timeout  5000
:wq
]# vim +43 /etc/init.d/redis_6379
         $CLIEXEC -h 192.168.4.59 -p 6359 shutdown
:wq
]# /etc/init.d/redis_6379  start
]# netstat -utnlp  | grep redis-server
tcp  0  0 192.168.4.59:6359  0.0.0.0:*   LISTEN      21201/redis-server  
tcp  0  0 192.168.4.59:16359   0.0.0.0:*   LISTEN   21201/redis-server   
```
2）在管理主机，添加slave角色主机
```shell
[root@mgm57 ~]# redis-trib.rb add-node  --slave 192.168.4.59:6359  192.168.4.51:6351  //执行添加命令
>>> Adding node 192.168.4.59:6359 to cluster 192.168.4.51:6351
>>> Performing Cluster Check (using node 192.168.4.51:6351)
S: d9f8fe6d6d9dd391be8e7904501db1535e4d17cb 192.168.4.51:6351
   slots: (0 slots) slave
   replicates 2d343a9df48f6f6e207949e980ef498466a44dad
S: 894dd0008053f6fb65e9e4a36b755d9351607500 192.168.4.56:6356
   slots: (0 slots) slave
   replicates 324e05df3f143ef97e50d09be0328a695e655986
M: 2d343a9df48f6f6e207949e980ef498466a44dad 192.168.4.55:6355
   slots:1365-5460 (4096 slots) master
   1 additional replica(s)
M: 9e44139cffb8ebd7ed746aabbf4bcea9bf207645 192.168.4.53:6353
   slots:12288-16383 (4096 slots) master
   1 additional replica(s)
S: d9634ba0aa5c1a07193da4a013da6051c1515922 192.168.4.54:6354
   slots: (0 slots) slave
   replicates 9e44139cffb8ebd7ed746aabbf4bcea9bf207645
M: 324e05df3f143ef97e50d09be0328a695e655986 192.168.4.52:6352
   slots:6827-10922 (4096 slots) master
   1 additional replica(s)
M: 4fe1fa467ad237802021f5aac5f1d5b3e0db47ef 192.168.4.58:6358
   slots:0-1364,5461-6826,10923-12287 (4096 slots) master
   0 additional replica(s)
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
Automatically selected master 192.168.4.58:6358
>>> Send CLUSTER MEET to node 192.168.4.59:6359 to make it join the cluster.
Waiting for the cluster to join.
>>> Configure node as replica of 192.168.4.58:6358. //提示添加完成
[OK] New node added correctly.
[root@mgm57 ~]# 
```
3） 在管理主机，查看集群新消息
```shell
[root@mgm57 ~]# redis-trib.rb  info  192.168.4.51:6351 //查看信息
192.168.4.55:6355 (2d343a9d...) -> 3 keys | 4096 slots | 1 slaves.
192.168.4.53:6353 (9e44139c...) -> 3 keys | 4096 slots | 1 slaves.
192.168.4.52:6352 (324e05df...) -> 2 keys | 4096 slots | 1 slaves.
192.168.4.58:6358 (4fe1fa46...) -> 5 keys | 4096 slots | 1 slaves. //有1个从服务器
[OK] 13 keys in 4 masters.
0.00 keys per slot on average.
[root@mgm57 ~]# 
```
4）在管理主机，检测集群
```shell
 [root@mgm57 ~]# redis-trib.rb check 192.168.4.53:6353    //检测集群
[root@mgm57 ~]# redis-trib.rb  check  192.168.4.51:6351
>>> Performing Cluster Check (using node 192.168.4.51:6351)
S: d9f8fe6d6d9dd391be8e7904501db1535e4d17cb 192.168.4.51:6351
   slots: (0 slots) slave
   replicates 2d343a9df48f6f6e207949e980ef498466a44dad
S: 7f3fa4f20c8c516d5b412ecc22550ed8e7bb8d7a 192.168.4.59:6359 //从服务器
   slots: (0 slots) slave
   replicates 4fe1fa467ad237802021f5aac5f1d5b3e0db47ef //58主机的id值
S: 894dd0008053f6fb65e9e4a36b755d9351607500 192.168.4.56:6356
   slots: (0 slots) slave
   replicates 324e05df3f143ef97e50d09be0328a695e655986
M: 2d343a9df48f6f6e207949e980ef498466a44dad 192.168.4.55:6355
   slots:1365-5460 (4096 slots) master
   1 additional replica(s)
M: 9e44139cffb8ebd7ed746aabbf4bcea9bf207645 192.168.4.53:6353
   slots:12288-16383 (4096 slots) master
   1 additional replica(s)
S: d9634ba0aa5c1a07193da4a013da6051c1515922 192.168.4.54:6354
   slots: (0 slots) slave
   replicates 9e44139cffb8ebd7ed746aabbf4bcea9bf207645
M: 324e05df3f143ef97e50d09be0328a695e655986 192.168.4.52:6352
   slots:6827-10922 (4096 slots) master
   1 additional replica(s)
M: 4fe1fa467ad237802021f5aac5f1d5b3e0db47ef 192.168.4.58:6358 //主服务器
   slots:0-1364,5461-6826,10923-12287 (4096 slots) master
   1 additional replica(s)
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
[root@mgm57 ~]# 
[root@mgm57 ~]#
```
5）在客户端，访问从服务器59，查看数据
```shell
 [root@host50 ~]# redis-cli  -c -h 192.168.4.59 -p 6359
192.168.4.59:6359> keys * //自动同步主服务器58的数据
1) "name"
2) "name2"
3) "age"
4) "y"
5) "shcool5"
192.168.4.59:6359>  
```
# 3. 移除服务器
## 3.1 问题
- 把slave服务器移除集群
- 把master服务器移除集群

## 3.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：把slave服务器移除集群**

1）在管理主机，移除slave服务器，从服务器没有槽，直接移除即可。
```shell
 [root@mgm57 ~]# redis-trib.rb  del-node 192.168.4.51:6351 f6649ea99b2f01faca26217691222c17a3854381   //执行移除命令
>>> Removing node f6649ea99b2f01faca26217691222c17a3854381 
       from cluster 192.168.4.57:6351
>>> Sending CLUSTER FORGET messages to the cluster...
>>> SHUTDOWN the node. //停止移除服务的Redis服务
```
2）在管理主机，查看集群信息
```shell
[root@mgm57 ~]# redis-trib.rb  info  192.168.4.51:6351
192.168.4.55:6355 (2d343a9d...) -> 3 keys | 4096 slots | 1 slaves.
192.168.4.53:6353 (9e44139c...) -> 3 keys | 4096 slots | 1 slaves.
192.168.4.52:6352 (324e05df...) -> 2 keys | 4096 slots | 1 slaves.
192.168.4.58:6358 (4fe1fa46...) -> 5 keys | 4096 slots | 0 slaves.//58主机，没有从服务器
[OK] 13 keys in 4 masters.
0.00 keys per slot on average.
[root@mgm57 ~]#
```
**步骤二：把master服务器移除集群**

1）在管理主机,先删除master服务器占用的hash槽
```shell
[root@mgm57 ~]# redis-trib.rb  reshard 192.168.4.53:6353
How many slots do you want to move (from 1 to 16384)?4096 //移除4096个数槽
What is the receiving node ID?  bc5c4e082a5a3391b634cf433a6486c867cfc44b 
    //要移动给谁的id即目标主机（这里可以随机写一个master的ID）  
Source node #1: c5e0da48f335c46a2ec199faa99b830f537dd8a0
//从谁那移动即源主机（这里写4.58的ID）  
Source node #2:done           //设置完毕
...
    Moving slot 12282 from c5e0da48f335c46a2ec199faa99b830f537dd8a0
    Moving slot 12283 from c5e0da48f335c46a2ec199faa99b830f537dd8a0
    Moving slot 12284 from c5e0da48f335c46a2ec199faa99b830f537dd8a0
    Moving slot 12285 from c5e0da48f335c46a2ec199faa99b830f537dd8a0
    Moving slot 12286 from c5e0da48f335c46a2ec199faa99b830f537dd8a0
    Moving slot 12287 from c5e0da48f335c46a2ec199faa99b830f537dd8a0
Do you want to proceed with the proposed reshard plan (yes/no)?yes //提交
... 
Moving slot 12282 from 192.168.4.58:6358 to 192.168.4.53:6353: 
Moving slot 12283 from 192.168.4.58:6358 to 192.168.4.53:6353: 
Moving slot 12284 from 192.168.4.58:6358 to 192.168.4.53:6353: 
Moving slot 12285 from 192.168.4.58:6358 to 192.168.4.53:6353: 
Moving slot 12286 from 192.168.4.58:6358 to 192.168.4.53:6353: 
Moving slot 12287 from 192.168.4.58:6358 to 192.168.4.53:6353:
```
2）在管理主机,查看集群信息
```shell
[root@mgm57 ~]# redis-trib.rb  info  192.168.4.51:6351
192.168.4.55:6355 (2d343a9d...) -> 3 keys | 4096 slots | 1 slaves.
192.168.4.53:6353 (9e44139c...) -> 3 keys | 4096 slots | 1 slaves.
192.168.4.52:6352 (324e05df...) -> 2 keys | 4096 slots | 1 slaves.
192.168.4.58:6358 (4fe1fa46...) -> 0 keys | 0 slots    | 0 slaves. //零个槽
[OK] 13 keys in 4 masters.
0.00 keys per slot on average.
[root@mgm57 ~]#
```
3）在管理主机，移除master主机
```shell
[root@mgm57 ~]# redis-trib.rb del-node 192.168.4.53:6353 \ 
 c5e0da48f335c46a2ec199faa99b830f537dd8a0    //删除谁+删除的id
>>> Removing node e081313ec843655d9bc5a17f3bed3de1dccb1d2b from cluster 192.168.4.51:6351
>>> Sending CLUSTER FORGET messages to the cluster...
>>> SHUTDOWN the node.
[root@mgm57 ~]#
```
4）在管理主机,查看集群信息
```shell
[root@mgm57 ~]# redis-trib.rb  info  192.168.4.51:6351  
192.168.4.55:6355 (2d343a9d...) -> 3 keys | 4096 slots | 1 slaves.
192.168.4.53:6353 (9e44139c...) -> 3 keys | 4096 slots | 1 slaves.
192.168.4.52:6352 (324e05df...) -> 2 keys | 4096 slots | 1 slaves.
[OK] 13 keys in 3 masters. //主服务器个数3台，没有58 
0.00 keys per slot on average.  
[root@mgm57 ~]#
```
# Exercise
## 1 阐述redis集群存取数据工作原理。
当客户端存储数据到集群主机时，获取变量名与CRC16算法做hash计算，然后用计算结果与16384做取余运算，再根据余数值，把数据存储到对应的master 服务器。

## 2 阐述redis配置文件中，下列配置项的作用 。
bind IP地址 只写物理接口IP地址
daemonize yes 守护进程方式运行
port xxxx 端口号（默认的6379）
cluster-enabled yes 启用集群
cluster-config-file nodes-xxxx.conf 集群信息文件
cluster-node-timeout 5000 请求超时时间（单位毫秒）

## 3 简述访问集群命令格式？
redis-cli -c -h master_ip地址 -p master_port

常用选项：
-h IP地址
-p 端口
-c 集群模式
```shell
[root@redisA ~]# redis-cli  -c -h 192.168.4.53 -p 6353
```

> 如有侵权，请联系作者删除
