@[TOC]( Zookeeper high availability cluster & distributed message queue Kafka & set up high availability Hadoop cluster | Cloud computing )

---

# 1. 组建zookeeper集群

## 1.1 问题

本案例要求：

- 组建 zookeeper 集群
- 1 个 leader
- 2 个 follower
- 1 个 observer

## 1.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：安装Zookeeper**

1）编辑/etc/hosts ,所有集群主机可以相互 ping 通（在hadoop1上面配置，同步到node-0001，node-0002，node-0003）

```shell
[root@hadoop1 hadoop]# vim /etc/hosts
192.168.1.50  hadoop1
192.168.1.51  node-0001
192.168.1.52  node-0002
192.168.1.53  node-0003
192.168.1.56  newnode
[root@nn01 hadoop]# for i in {52..54}  \
do    \
scp /etc/hosts 192.168.1.$i:/etc/    \
done        //同步配置
hosts       100%  253   639.2KB/s   00:00    
hosts       100%  253   497.7KB/s   00:00    
hosts       100%  253   662.2KB/s   00:00  
```

2）安装 java-1.8.0-openjdk-devel,由于之前的hadoop上面已经安装过，这里不再安装，若是新机器要安装

3）zookeeper 解压拷贝到 /usr/local/zookeeper

```shell
[root@hadoop1 ~]# tar -xf zookeeper-3.4.13.tar.gz 
[root@hadoop1 ~]# mv zookeeper-3.4.13 /usr/local/zookeeper
```

4）配置文件改名，并在最后添加配置

```shell
[root@hadoop1 ~]# cd /usr/local/zookeeper/conf/
[root@hadoop1 conf]# ls
configuration.xsl  log4j.properties  zoo_sample.cfg
[root@hadoop1 conf]# mv zoo_sample.cfg  zoo.cfg
[root@hadoop1 conf]# chown root.root zoo.cfg
[root@hadoop1 conf]# vim zoo.cfg
server.1=node-0001:2888:3888
server.2=node-0002:2888:3888
server.3=node-0003:2888:3888
server.4=hadoop1:2888:3888:observer
```

5）拷贝 /usr/local/zookeeper 到其他集群主机

```shell
[root@hadoop1 conf]# for i in {52..54}; do rsync -aSH --delete /usr/local/zookeeper/ 192.168.1.$i:/usr/local/zookeeper  -e 'ssh' & done
[4] 4956
[5] 4957
[6] 4958
```

6）创建 mkdir /tmp/zookeeper，每一台都要

```shell
[root@hadoop1 conf]# mkdir /tmp/zookeeper
[root@hadoop1 conf]# ssh node-0001 mkdir /tmp/zookeeper
[root@hadoop1 conf]# ssh node-0002 mkdir /tmp/zookeeper
[root@hadoop1 conf]# ssh node-0003 mkdir /tmp/zookeeper
```

7）创建 myid 文件，id 必须与配置文件里主机名对应的 server.(id) 一致

```shell
[root@hadoop1 conf]# echo 4 >/tmp/zookeeper/myid
[root@hadoop1 conf]# ssh node-0001 'echo 1 >/tmp/zookeeper/myid'
[root@hadoop1 conf]# ssh node-0002 'echo 2 >/tmp/zookeeper/myid'
[root@hadoop1 conf]# ssh node-0003 'echo 3 >/tmp/zookeeper/myid'
```

8）启动服务，单启动一台无法查看状态，需要启动全部集群以后才能查看状态，每一台上面都要手工启动（以hadoop1为例子）

```shell
[root@hadoop1 conf]# /usr/local/zookeeper/bin/zkServer.sh start
ZooKeeper JMX enabled by default
Using config: /usr/local/zookeeper/bin/../conf/zoo.cfg
Starting zookeeper ... STARTED
```

注意：刚启动zookeeper查看状态的时候报错，启动的数量要保证半数以上，这时再去看就成功了

9）查看状态

```shell
[root@hadoop1 conf]# /usr/local/zookeeper/bin/zkServer.sh status
ZooKeeper JMX enabled by default
Using config: /usr/local/zookeeper/bin/../conf/zoo.cfg
Mode: observe
[root@hadoop1 conf]# /usr/local/zookeeper/bin/zkServer.sh stop  
//关闭之后查看状态其他服务器的角色
ZooKeeper JMX enabled by default
Using config: /usr/local/zookeeper/bin/../conf/zoo.cfg
Stopping zookeeper ... STOPPED
```



# 2. 测试集群的远程管理和高可用

## 2.1 问题

本案例要求：

- 测试集群的远程管理和高可用

## 2.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：测试集群的远程管理和高可用**

```shell
[root@hadoop1 conf]# socat - TCP:node1:2181
stat
... ...
Outstanding: 0
Zxid: 0x0
Mode: follower
Node count: 4
[root@hadoop1 conf]# vim api.sh
#!/bin/bash
function getstatus(){
    exec 9<>/dev/tcp/$1/2181 2>/dev/null
    echo stat >&9
    MODE=$(cat <&9 |grep -Po "(?<=Mode:).*")
    exec 9<&-
    echo ${MODE:-NULL}
}
for i in node{1..3} hadoop1;do
    echo -ne "${i}\t"
    getstatus ${i}
done
[root@hadoop1 conf]# chmod 755 api.sh
[root@hadoop1 conf]# ./api.sh 
node-0001        follower
node-0002        leader
node-0003        follower 
hadoop1        observer
```



# 3. 在node节点上搭建3台kafka

## 3.1 问题

本案例要求：

- 在node节点上搭建3台kafka
- node-0001
- node-0002
- node-0003
- 发布订阅消息测试

## 3.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：搭建Kafka集群**

1）解压 kafka 压缩包

Kafka在node-0001，node-0002，node-0003上面操作即可

```shell
[root@node-0001 hadoop]# tar -xf kafka_2.12-2.1.0.tgz
```

2）把 kafka 拷贝到 /usr/local/kafka 下面

```shell
[root@node-0001 ~]# mv kafka_2.12-2.1.0 /usr/local/kafka
```

3）修改配置文件 /usr/local/kafka/config/server.properties

```shell
[root@node-0001 ~]# cd /usr/local/kafka/config
[root@node-0001 config]# vim server.properties
broker.id=22
zookeeper.connect=node-0001:2181,node-0002:2181,node-0003:2181
```

4）拷贝 kafka 到其他主机，并修改 broker.id ,不能重复

```shell
[root@node-0001 config]# for i in 53 54; do rsync -aSH --delete /usr/local/kafka 192.168.1.$i:/usr/local/; done
[1] 27072
[2] 27073
[root@node-0002 ~]# vim /usr/local/kafka/config/server.properties        
//node-0002主机修改
broker.id=23
[root@node-0003 ~]# vim /usr/local/kafka/config/server.properties        
//node-0003主机修改
broker.id=24
```

5）启动 kafka 集群（node-0001，node-0002，node-0003启动）

```shell
[root@node-0001 local]# /usr/local/kafka/bin/kafka-server-start.sh -daemon /usr/local/kafka/config/server.properties 
[root@node-0001 local]# jps        //出现kafka
26483 DataNode
27859 Jps
27833 Kafka
26895 QuorumPeerMain
```

6）验证配置，创建一个 topic

```shell
[root@node-0001 local]# /usr/local/kafka/bin/kafka-topics.sh --create --partitions 1 --replication-factor 1 --zookeeper localhost:2181 --topic mymsg
    
Created topic "mymsg".
```

\7) 模拟生产者，发布消息

```shell
[root@node-0002 ~]# /usr/local/kafka/bin/kafka-console-producer.sh --broker-list  localhost:9092 --topic mymsg
        //写一个数据
ccc
ddd
```

9）模拟消费者，接收消息

```shell
[root@node-0003 ~]# /usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic mymsg
        //这边会直接同步
ccc
ddd
```

注意：kafka比较吃内存，做完这个kafka的实验可以把它停了



# 4. 准备实验环境

## 4.1 问题

本案例要求：

- 所有节点
- 192.168.1.50 hadoop1
- 192.168.1.56 hadoop2
- 192.168.1.51 node-0001
- 192.168.1.52 node-0002
- 192.168.1.53 node-0003
- 新机器安装 java-1.8.0-openjdk-devel
- 新机器配置 /etc/hosts
- 新机器配置 ssh 免密钥登录
- 修改配置文件

## 4.2 方案

配置Hadoop的高可用，解决NameNode单点故障问题，使用之前搭建好的hadoop集群，新添加一台hadoop2，ip为192.168.1.56，具体要求如图-1所示：

![img](https://img-blog.csdnimg.cn/img_convert/6b896447f79e0a29676117c72736ec4a.png)

图-1

## 4.3 步骤

实现此案例需要按照如下步骤进行。

**步骤一：hadoop的高可用**

1）停止所有服务（由于 kafka的实验做完之后就已经停止，这里不在重复）

```shell
[root@hadoop1 ~]# cd /usr/local/hadoop/
[root@hadoop1 hadoop]# ./sbin/stop-all.sh  //停止所有服务 
```

2）启动zookeeper（需要一台一台的启动）这里以hadoop1为例子

```shell
[root@hadoop1 hadoop]# /usr/local/zookeeper/bin/zkServer.sh start
[root@hadoop1 hadoop]# sh /usr/local/zookeeper/conf/api.sh //利用之前写好的脚本查看
node-0001        follower
node-0002        leader
node-0003        follower
hadoop1        observer
```

3）新加一台机器hadoop2，这里之前有一台newnode，可以用这个作为hadoop2

```shell
[root@newnode ~]# echo hadoop2 > /etc/hostname 
[root@newnode ~]# hostname hadoop2
```

4）修改vim /etc/hosts

```shell
[root@hadoop1 hadoop]# vim /etc/hosts
192.168.1.50  hadoop1
192.168.1.56  hadoop2
192.168.1.51  node-0001
192.168.1.52  node-0002
192.168.1.53  node-0003
```

5）同步到hadoop2，node-0001，node-0002，node-0003

```shell
[root@hadoop1 hadoop]# for i in {51..53} 56; do rsync -aSH --delete /etc/hosts 192.168.1.$i:/etc/hosts  -e 'ssh' & done
[1] 14355
[2] 14356
[3] 14357
[4] 14358
```

6）配置SSH信任关系

注意：hadoop1和hadoop2互相连接不需要密码，hadoop2连接自己和node-0001，node-0002，node-0003同样不需要密码

```shell
[root@hadoop2 ~]# vim /etc/ssh/ssh_config
Host *
        GSSAPIAuthentication yes
        StrictHostKeyChecking no
[root@hadoop1 hadoop]# cd /root/.ssh/
[root@hadoop1 .ssh]# scp id_rsa id_rsa.pub  hadoop2:/root/.ssh/    
//把hadoop1的公钥私钥考给hadoop2
```

7）所有的主机删除/var/hadoop/*

```shell
[root@hadoop1 .ssh]# rm -rf /var/hadoop/*
```



# 5. 配置namenode与resourcemanager高可用

## 5.1 问题

本案例要求：

- 配置 namenode 与 resourcemanager 高可用
- hadoop-env.sh
- core-site.xml
- hdfs-site.xml
- mapred-site.xml
- yarn-site.xml
- slaves

## 5.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：hadoop的高可用**

1）配置 core-site

```shell
[root@hadoop1 .ssh]# vim /usr/local/hadoop/etc/hadoop/core-site.xml
<configuration>
<property>
        <name>fs.defaultFS</name>
        <value>hdfs://nsdcluster</value>    
//nsdcluster是随便起的名。相当于一个组，访问的时候访问这个组
    </property>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/var/hadoop</value>
    </property>
    <property>
        <name>ha.zookeeper.quorum</name>
        <value>node-0001:2181,node-0002:2181,node-0003:2181</value>    //zookeepe的地址
    </property>
    <property>
        <name>hadoop.proxyuser.nfs.groups</name>
        <value>*</value>
    </property>
    <property>
        <name>hadoop.proxyuser.nfs.hosts</name>
        <value>*</value>
    </property>
</configuration>
```

2）配置 hdfs-site

```shell
[root@hadoop1 ~]# vim /usr/local/hadoop/etc/hadoop/hdfs-site.xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>2</value>
    </property>
    <property>
        <name>dfs.nameservices</name>
        <value>nsdcluster</value>
    </property>
    <property>
        <name>dfs.ha.namenodes.nsdcluster</name>                
//nn1,nn2名称固定，是内置的变量，nsdcluster里面有nn1，nn2
        <value>nn1,nn2</value>
    </property>
    <property>
        <name>dfs.namenode.rpc-address.nsdcluster.nn1</name>        
//声明nn1 8020为通讯端口，是hadoop1的rpc通讯端口
        <value>hadoop1:8020</value>
    </property>
    <property>
        <name>dfs.namenode.rpc-address.nsdcluster.nn2</name>        
//声明nn2是谁，hadoop2的rpc通讯端口
        <value>hadoop2:8020</value>
    </property>
    <property>
        <name>dfs.namenode.http-address.nsdcluster.nn1</name>    
//hadoop1的http通讯端口
        <value>hadoop1:50070</value>
    </property>
    <property>
        <name>dfs.namenode.http-address.nsdcluster.nn2</name>     
//hadoop1和hadoop2的http通讯端口
        <value>hadoop2:50070</value>
    </property>
    <property>
        <name>dfs.namenode.shared.edits.dir</name>        
//指定namenode元数据存储在journalnode中的路径
        <value>qjournal://node-0001:8485;node-0002:8485;node-0003:8485/nsdcluster</value>
    </property>
    <property>
        <name>dfs.journalnode.edits.dir</name>            
//指定journalnode日志文件存储的路径
        <value>/var/hadoop/journal</value>
    </property>
    <property>
        <name>dfs.client.failover.proxy.provider.nsdcluster</name>    
//指定HDFS客户端连接active namenode的java类
        <value>org.apache.hadoop.hdfs.server.namenode.ha.ConfiguredFailoverProxyProvider</value>
    </property>
    <property>
        <name>dfs.ha.fencing.methods</name>                    //配置隔离机制为ssh
        <value>sshfence</value>
    </property>
    <property>
        <name>dfs.ha.fencing.ssh.private-key-files</name>    //指定密钥的位置
        <value>/root/.ssh/id_rsa</value>
    </property>
    <property>
        <name>dfs.ha.automatic-failover.enabled</name>        //开启自动故障转移
        <value>true</value>                
    </property>
</configuration>
```

3）配置yarn-site

```shell
[root@hadoop1 ~]# vim /usr/local/hadoop/etc/hadoop/yarn-site.xml
<configuration>
<!-- Site specific YARN configuration properties -->
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.resourcemanager.ha.enabled</name>
        <value>true</value>
    </property> 
    <property>
        <name>yarn.resourcemanager.ha.rm-ids</name>        //rm1,rm2代表hadoop1和hadoop2
        <value>rm1,rm2</value>
    </property>
    <property>
        <name>yarn.resourcemanager.recovery.enabled</name>
        <value>true</value>
    </property>
    <property>
        <name>yarn.resourcemanager.store.class</name>
        <value>org.apache.hadoop.yarn.server.resourcemanager.recovery.ZKRMStateStore</value>
    </property>
    <property>
        <name>yarn.resourcemanager.zk-address</name>
        <value>node-0001:2181,node-0002:2181,node-0003:2181</value>
    </property>
    <property>
        <name>yarn.resourcemanager.cluster-id</name>
        <value>yarn-ha</value>
    </property>
    <property>
        <name>yarn.resourcemanager.hostname.rm1</name>
        <value>hadoop1</value>
    </property>
    <property>
        <name>yarn.resourcemanager.hostname.rm2</name>
        <value>hadoop2</value>
    </property>
</configuration>
```



# 6. 启动服务，验证高可用

## 6.1 问题

本案例要求：

- 启动服务，验证高可用
- 分析数据时停止一个活跃节点
- 验证高可用状态及数据

## 6.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：hadoop高可用的验证**

1）同步到hadoop2，node-0001，node-0002，node-0003

```shell
[root@hadoop1 ~]# for i in {51..53} 56; do rsync -aSH --delete /usr/local/hadoop/ 192.168.1.$i:/usr/local/hadoop  -e 'ssh' & done
[1] 25411
[2] 25412
[3] 25413
[4] 25414
```

2）删除所有机器上面的/user/local/hadoop/logs，方便排错

```shell
[root@hadoop1 ~]# for i in {50..53} 56; do ssh 192.168.1.$i rm -rf /usr/local/hadoop/logs ; done
```

3）同步配置

```shell
[root@hadoop1 ~]# for i in {51..53} 56; do rsync -aSH --delete /usr/local/hadoop 192.168.1.$i:/usr/local/hadoop -e 'ssh' & done
[1] 28235
[2] 28236
[3] 28237
[4] 28238
```

4）初始化ZK集群

```shell
[root@hadoop1 ~]# /usr/local/hadoop/bin/hdfs zkfc -formatZK 
...
18/09/11 15:43:35 INFO ha.ActiveStandbyElector: Successfully created /hadoop-ha/nsdcluster in ZK    //出现Successfully即为成功
...
```

5）在node-0001，node-0002，node-0003上面启动journalnode服务（以node-0001为例子）

```shell
[root@node-0001 ~]# /usr/local/hadoop/sbin/hadoop-daemon.sh start journalnode 
starting journalnode, logging to /usr/local/hadoop/logs/hadoop-root-journalnode-node-0001.out
[root@node-0001 ~]# jps
29262 JournalNode
26895 QuorumPeerMain
29311 Jps
```

6）格式化，先在node-0001，node-0002，node-0003上面启动journalnode才能格式化

```shell
[root@hadoop1 ~]# /usr/local/hadoop//bin/hdfs  namenode  -format   
//出现Successfully即为成功
[root@hadoop1 hadoop]# ls /var/hadoop/
dfs
```

7）hadoop2数据同步到本地 /var/hadoop/dfs

```shell
[root@hadoop2 ~]# cd /var/hadoop/
[root@hadoop2 hadoop]# ls
[root@hadoop2 hadoop]# rsync -aSH  hadoop1:/var/hadoop/  /var/hadoop/
[root@hadoop2 hadoop]# ls
dfs
```

8）初始化 JNS

```shell
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/hdfs namenode -initializeSharedEdits
18/09/11 16:26:15 INFO client.QuorumJournalManager: Successfully started new epoch 1        //出现Successfully，成功开启一个节点
```

9）停止 journalnode 服务（node-0001，node-0002，node-0003）

```shell
[root@node-0001 hadoop]# /usr/local/hadoop/sbin/hadoop-daemon.sh stop journalnode
stopping journalnode
[root@node-0001 hadoop]# jps
29346 Jps
26895 QuorumPeerMain
```

**步骤二：启动集群**

1）hadoop1上面操作

```shell
[root@hadoop1 hadoop]# /usr/local/hadoop/sbin/start-all.sh  //启动所有集群
This script is Deprecated. Instead use start-dfs.sh and start-yarn.sh
Starting namenodes on [hadoop1 hadoop2]
hadoop1: starting namenode, logging to /usr/local/hadoop/logs/hadoop-root-namenode-hadoop1.out
hadoop2: starting namenode, logging to /usr/local/hadoop/logs/hadoop-root-namenode-hadoop2.out
node-0002: starting datanode, logging to /usr/local/hadoop/logs/hadoop-root-datanode-node-0002.out
node-0003: starting datanode, logging to /usr/local/hadoop/logs/hadoop-root-datanode-node-0003.out
node-0001: starting datanode, logging to /usr/local/hadoop/logs/hadoop-root-datanode-node-0001.out
Starting journal nodes [node-0001 node-0002 node-0003]
node-0001: starting journalnode, logging to /usr/local/hadoop/logs/hadoop-root-journalnode-node-0001.out
node-0003: starting journalnode, logging to /usr/local/hadoop/logs/hadoop-root-journalnode-node-0003.out
node-0002: starting journalnode, logging to /usr/local/hadoop/logs/hadoop-root-journalnode-node-0002.out
Starting ZK Failover Controllers on NN hosts [hadoop1 hadoop2]
hadoop1: starting zkfc, logging to /usr/local/hadoop/logs/hadoop-root-zkfc-hadoop1.out
hadoop2: starting zkfc, logging to /usr/local/hadoop/logs/hadoop-root-zkfc-hadoop2.out
starting yarn daemons
starting resourcemanager, logging to /usr/local/hadoop/logs/yarn-root-resourcemanager-hadoop1.out
node-0002: starting nodemanager, logging to /usr/local/hadoop/logs/yarn-root-nodemanager-node-0002.out
node-0001: starting nodemanager, logging to /usr/local/hadoop/logs/yarn-root-nodemanager-node-0001.out
node-0003: starting nodemanager, logging to /usr/local/hadoop/logs/yarn-root-nodemanager-node-0003.out
```

2）hadoop2上面操作

```shell
[root@hadoop2 hadoop]# /usr/local/hadoop/sbin/yarn-daemon.sh start resourcemanager
starting resourcemanager, logging to /usr/local/hadoop/logs/yarn-root-resourcemanager-hadoop2.out
```

3）查看集群状态

```shell
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/hdfs haadmin -getServiceState nn1
active
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/hdfs haadmin -getServiceState nn2
standby
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/yarn rmadmin -getServiceState rm1
active
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/yarn rmadmin -getServiceState rm2
standby
```

4）查看节点是否加入

```shell
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/hdfs dfsadmin -report
...
Live datanodes (3):    //会有三个节点
...
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/yarn  node  -list
Total Nodes:3
         Node-Id         Node-State    Node-Http-Address    Number-of-Running-Containers
     node-0002:43307            RUNNING           node-0002:8042                               0
     node-0001:34606            RUNNING           node-0001:8042                               0
     node-0003:36749            RUNNING           node-0003:8042  
```

**步骤三：访问集群**

1）查看并创建

```shell
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/hadoop  fs -ls  /
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/hadoop  fs -mkdir /aa //创建aa
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/hadoop  fs -ls  /        //再次查看
Found 1 items
drwxr-xr-x   - root supergroup          0 2018-09-11 16:54 /aa
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/hadoop  fs -put *.txt /aa
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/hadoop  fs -ls hdfs://nsdcluster/aa  
//也可以这样查看
Found 3 items
-rw-r--r--  2 root supergroup 86424 2018-09-11 17:00 hdfs://nsdcluster/aa/LICENSE.txt
-rw-r--r--  2 root supergroup 14978 2018-09-11 17:00 hdfs://nsdcluster/aa/NOTICE.txt
-rw-r--r--  2 root supergroup 1366 2018-09-11 17:00 hdfs://nsdcluster/aa/README.txt
```

2）验证高可用，关闭 active namenode

```shell
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/hdfs haadmin -getServiceState nn1
active
[root@hadoop1 hadoop]# /usr/local/hadoop/sbin/hadoop-daemon.sh stop namenode
stopping namenode
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/hdfs haadmin -getServiceState nn1      
//再次查看会报错
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/hdfs haadmin -getServiceState nn2  
//hadoop2由之前的standby变为active
active
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/yarn rmadmin -getServiceState rm1
active
[root@hadoop1 hadoop]# /usr/local/hadoop/sbin/yarn-daemon.sh stop resourcemanager  
//停止resourcemanager 
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/yarn rmadmin -getServiceState rm2
active
```

3） 恢复节点

```shell
[root@hadoop1 hadoop]# /usr/local/hadoop/sbin/hadoop-daemon.sh start namenode       
//启动namenode
[root@hadoop1 hadoop]# /usr/local/hadoop/sbin/yarn-daemon.sh start resourcemanager 
//启动resourcemanager
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/hdfs haadmin -getServiceState nn1      
//查看
[root@hadoop1 hadoop]# /usr/local/hadoop/bin/yarn rmadmin -getServiceState rm1      
//查看
```



# Exercise

## 1 简述什么是Zookeeper以及其作用

什么是Zookeeper：

Zookeeper是一个开源的分布式应用程序协调服务



作用：

用来保证数据在集群间的事务一致性

## 2 简述Zookeeper角色与特性

Leader：接受所有Follower的提案请求并统一协调发起提案的投票，负责与所有的Follower进行内部数据交换

Follower：直接为客户端服务并参与提案的投票，同时与Leader进行数据交换

Observer：直接为客户端服务但并不参与提案的投票，同时也与Leader进行数据交换

## 3 如何利用 api 查看Zookeeper的状态

```shell
[root@nn01 conf]# /usr/local/zookeeper/bin/zkServer.sh start
[root@nn01 conf]# vim api.sh
#!/bin/bash
function getstatus(){
    exec 9<>/dev/tcp/$1/2181 2>/dev/null
    echo stat >&9
    MODE=$(cat <&9 |grep -Po "(?<=Mode:).*")
    exec 9<&-
    echo ${MODE:-NULL}
}
for i in node{1..3} nn01;do
    echo -ne "${i}\t"
    getstatus ${i}
done
[root@nn01 conf]# chmod 755 api.sh
[root@nn01 conf]# ./api.sh 
node1    follower
node2    leader
node3    follower 
nn01    observer
```

## 4 如何在Kafka集群里创建一个topic

```shell
[root@node1 local]# /usr/local/kafka/bin/kafka-topics.sh --create --partitions 1 --replication-factor 1 --zookeeper node3:2181 --topic aa    
Created topic "aa".
```



> 如有侵权，请联系作者删除
