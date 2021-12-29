@[TOC]( PXC & MySQL storage engine | Cloud computing )

---
# 1 案例1：安装软件
## 1.1 问题
- 环境准备
- 安装软件包
## 1.2 方案
准备3台虚拟主机，配置ip地址和主机名。具体如图-1所示：（不需要安装任何MySQL服务软件）
![在这里插入图片描述](https://img-blog.csdnimg.cn/c9bbd9491c7b40668d227d702e7e7677.png)
图-1

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：环境准备**

配置主机名与ip地址绑定

配置服务器192.168.4.71
```shell
]#  vim /etc/hosts
192.168.4.71     pxcnode71
192.168.4.72     pxcnode72
192.168.4.73     pxcnode73 
:wq
]#hostname  pxcnode71
```
配置服务器192.168.4.72
```shell
]#  vim /etc/hosts
192.168.4.71     pxcnode71
192.168.4.72     pxcnode72
192.168.4.73     pxcnode73 
:wq
]#hostname  pxcnode72
```
配置服务器192.168.4.73
```shell
]#  vim /etc/hosts
192.168.4.71     pxcnode71
192.168.4.72     pxcnode72
192.168.4.73     pxcnode73 
:wq
]#hostname  pxcnode73
```
在任意一台服务器上ping 对方的主机名，ping通为配置成功。
```shell
[root@host71 ~]# ping -c 2  pxcnode71  //成功
PING pxcnode71 (192.168.4.71) 56(84) bytes of data.
64 bytes from pxcnode71 (192.168.4.71): icmp_seq=1 ttl=255 time=0.011 ms
64 bytes from pxcnode71 (192.168.4.71): icmp_seq=2 ttl=255 time=0.020 ms
--- pxcnode71 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 999ms
rtt min/avg/max/mdev = 0.011/0.015/0.020/0.006 ms
[root@host71 ~]# 
[root@host71 ~]# 
[root@host71 ~]# ping -c 2  pxcnode72 //成功
PING pxcnode72 (192.168.4.72) 56(84) bytes of data.
64 bytes from pxcnode72 (192.168.4.72): icmp_seq=1 ttl=255 time=0.113 ms
64 bytes from pxcnode72 (192.168.4.72): icmp_seq=2 ttl=255 time=0.170 ms
--- pxcnode72 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1000ms
rtt min/avg/max/mdev = 0.113/0.141/0.170/0.030 ms
[root@host71 ~]# 
[root@host71 ~]# 
[root@host71 ~]# ping -c 2  pxcnode73 //成功
PING pxcnode73 (192.168.4.73) 56(84) bytes of data.
64 bytes from pxcnode73 (192.168.4.73): icmp_seq=1 ttl=255 time=0.198 ms
64 bytes from pxcnode73 (192.168.4.73): icmp_seq=2 ttl=255 time=0.155 ms
--- pxcnode73 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1000ms
rtt min/avg/max/mdev = 0.155/0.176/0.198/0.025 ms
[root@host71 ~]#
```
步骤二：安装软件包

1）在192.168.4.71 服务器安装软件包

软件包之间有依赖注意软件包安装顺序
```shell
]# rpm -ivh libev-4.15-1.el6.rf.x86_64.rpm    //安装依赖
]# yum  -y  install  percona-xtrabackup-24-2.4.13-1.el7.x86_64.rpm
 ]# rpm -ivh qpress-1.1-14.11.x86_64.rpm     //安装依赖
 ]# tar -xvf  Percona-XtraDB-Cluster-5.7.25-31.35-r463-el7-x86_64-bundle.tar
 ]# yum -y  install  Percona-XtraDB-Cluster-*.rpm
```
2）在192.168.4.72 服务器安装软件包
```shell
]# rpm -ivh libev-4.15-1.el6.rf.x86_64.rpm    //安装依赖
]# yum  -y  install  percona-xtrabackup-24-2.4.13-1.el7.x86_64.rpm
]# rpm -ivh qpress-1.1-14.11.x86_64.rpm     //安装依赖
]# tar -xvf  Percona-XtraDB-Cluster-5.7.25-31.35-r463-el7-x86_64-bundle.tar
]# yum -y  install  Percona-XtraDB-Cluster-*.rpm
```
3）在192.168.4.73 服务器安装软件包
```shell
]# rpm -ivh libev-4.15-1.el6.rf.x86_64.rpm    //安装依赖
]# yum  -y  install  percona-xtrabackup-24-2.4.13-1.el7.x86_64.rpm
]# rpm -ivh qpress-1.1-14.11.x86_64.rpm     //安装依赖
]# tar -xvf  Percona-XtraDB-Cluster-5.7.25-31.35-r463-el7-x86_64-bundle.tar
]# yum -y  install  Percona-XtraDB-Cluster-*.rpm
```
# 2. 配置服务
## 2.1 问题
- 修改mysqld.cnf文件
- 修改mysqld_safe.cnf文件
- 修改wsrap.cnf文件
- 启动服务
## 2.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：修改mysqld.cnf文件**

1）分别修改3台服务器的mysqld.cnf文件
```shell
[root@pxcnode71 ~]# vim /etc/percona-xtradb-cluster.conf.d/mysqld.cnf
[mysqld]
server-id=71                      //server-id 不允许重复
datadir=/var/lib/mysql                  //数据库目录
socket=/var/lib/mysql/mysql.sock         //socket文件
log-error=/var/log/mysqld.log        //日志文件
pid-file=/var/run/mysqld/mysqld.pid    //pid文件
log-bin                    //启用binlog日志
log_slave_updates            //启用链式复制
expire_logs_days=7            //日志文件保留天数
:wq
```
修改服务器192.168.4.72
```shell
[root@pxcnode72 ~]# vim /etc/percona-xtradb-cluster.conf.d/mysqld.cnf
[mysqld]
server-id=72                      //server-id 不允许重复
datadir=/var/lib/mysql                  //数据库目录
socket=/var/lib/mysql/mysql.sock         //socket文件
log-error=/var/log/mysqld.log        //日志文件
pid-file=/var/run/mysqld/mysqld.pid    //pid文件
log-bin                    //启用binlog日志
log_slave_updates            //启用链式复制
expire_logs_days=7            //日志文件保留天数
:wq
```
修改服务器192.168.4.73
```shell
[root@pxcnode73 ~]# vim /etc/percona-xtradb-cluster.conf.d/mysqld.cnf
[mysqld]
server-id=73                      //server-id 不允许重复
datadir=/var/lib/mysql                  //数据库目录
socket=/var/lib/mysql/mysql.sock         //socket文件
log-error=/var/log/mysqld.log        //日志文件
pid-file=/var/run/mysqld/mysqld.pid    //pid文件
log-bin                    //启用binlog日志
log_slave_updates            //启用链式复制
expire_logs_days=7            //日志文件保留天数
:wq
```
**步骤二：修改mysqld_safe.cnf文件**

1）分别修改3台服务器的mysqld_safe.cnf （使用默认配置即可）
```shell
//修改服务器192.168.4.71
[root@pxcnode71 ~]# vim /etc/percona-xtradb-cluster.conf.d/mysqld_safe.cnf
[mysqld_safe]
pid-file = /var/run/mysqld/mysqld.pid
socket   = /var/lib/mysql/mysql.sock
nice     = 0
:wq
//修改服务器192.168.4.72
[root@pxcnode72 ~]# vim /etc/percona-xtradb-cluster.conf.d/mysqld_safe.cnf
[mysqld_safe]
pid-file = /var/run/mysqld/mysqld.pid
socket   = /var/lib/mysql/mysql.sock
nice     = 0
:wq
//修改服务器192.168.4.73
[root@pxcnode73 ~]# vim /etc/percona-xtradb-cluster.conf.d/mysqld_safe.cnf
[mysqld_safe]
pid-file = /var/run/mysqld/mysqld.pid
socket   = /var/lib/mysql/mysql.sock
nice     = 0
:wq
```
**步骤三：修改wsrep.cnf文件**

分别修改3台服务器的wsrep.cnf,其中成员列表、集群名、SST用户和密码必须相同
```shell
//修改服务器192.168.4.71
[root@pxcnode71 ~]# vim /etc/percona-xtradb-cluster.conf.d/wsrep.cnf
wsrep_cluster_address=gcomm://192.168.4.71,192.168.4.72,192.168.4.73//成员列表
wsrep_node_address=192.168.4.71 //本机ip
wsrep_cluster_name=pxc-cluster //集群名
wsrep_node_name=pxcnode71 //本机主机名
wsrep_sst_auth="sstuser:123qqq...A" //SST数据同步授权用户及密码
:wq
//修改服务器192.168.4.72
[root@pxcnode72 ~]# vim /etc/percona-xtradb-cluster.conf.d/wsrep.cnf
wsrep_cluster_address=gcomm://192.168.4.71,192.168.4.72,192.168.4.73//成员列表
wsrep_node_address=192.168.4.72 //本机ip
wsrep_cluster_name=pxc-cluster //集群名
wsrep_node_name=pxcnode72 //本机主机名
wsrep_sst_auth="sstuser:123qqq...A" //SST数据同步授权用户及密码
:wq
//修改服务器192.168.4.73
[root@pxcnode73 ~]# vim /etc/percona-xtradb-cluster.conf.d/wsrep.cnf
wsrep_cluster_address=gcomm://192.168.4.71,192.168.4.72,192.168.4.73//成员列表
wsrep_node_address=192.168.4.73 //本机ip
wsrep_cluster_name=pxc-cluster //集群名
wsrep_node_name=pxcnode73 //本机主机名
wsrep_sst_auth="sstuser:123qqq...A" //SST数据同步授权用户及密码
:wq
```
**步骤四：启动服务**

1）集群初始化

注意：在任意一台服务器上执行即可且只能执行一遍，首次启动服务时间比较长
```shell
[root@pxcnode71 ~]# ]# systemctl  start mysql@bootstrap.service  //启动集群服务
[root@pxcnode71 ~]# grep pass /var/log/mysqld.log     //查看数据库管理员初始登录密码
2019-06-20T12:29:42.489377Z 1 [Note] A temporary password is generated for root@localhost: W.HiOb8(ok)_
[root@pxcnode71 ~]#mysql –uroot –p’ W.HiOb8(ok)_’ //使用初始密码登录
Mysql> alter user  root@”localhost” identified by “123456”;//修改登录密码
MySQL> exit; //断开连接
[root@pxcnode71 ~]#mysql –uroot –p123456 //使用修改后的密码登录
Mysql> garnt reload, lock tables,replication client,process on *.*  to
sstuser@"localhost” identified by  “123qqq…A”; //添加SST用户
MySQL> exit;
[root@pxcnode71 ~]#
```
2）启动数据库服务

启动主机pxcnode72的数据库服务，会自动同步pxcnode71主机的root初始密码和授权用户sstuser
```shell
[root@pxcnode72 ~]# systemctl  start mysql  //启动数据库服务
[root@pxcnode72 ~]#
[root@pxcnode72 ~]# netstat -utnlp  | grep :3306
tcp6       0      0 :::3306                 :::*                    LISTEN      12794/mysqld        
[root@pxcnode72 ~]# netstat -utnlp  | grep :4567 //查看集群端口
tcp        0      0 0.0.0.0:4567            0.0.0.0:*               LISTEN      12794/mysqld        
[root@host72 ~]#
```
启动主机pxcnode73的数据库服务，会自动同步pxcnode71主机的root初始密码和授权用户sstuser
```shell
[root@pxcnode73 ~]# systemctl  start mysql  //启动数据库服务
[root@pxcnode73 ~]#
[root@pxcnode73 ~]# netstat -utnlp  | grep :3306
tcp6       0      0 :::3306                 :::*                    LISTEN      12794/mysqld        
[root@pxcnode73 ~]# netstat -utnlp  | grep :4567 //查看集群端口
tcp        0      0 0.0.0.0:4567            0.0.0.0:*               LISTEN      12794/mysqld        
[root@host73 ~]#
```
# 3. 测试配置
## 3.1 问题
1. 查看集群信息
2. 访问集群，存取数据
3. 测试故障自动恢复

## 3.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：查看集群信息**

1）启动数据库服务

在任意一台数据查看都可以。
```shell
[root@pxcnode71 ~]# mysql -uroot -p123456
wsrep_incoming_addresses 192.168.4.71:3306,192.168.4.72:3306,192.168.4.73:3306 //集群成员列表 
wsrep_cluster_size       3 //集群服务器台数
wsrep_cluster_status   Primary     //主机状态                           
wsrep_connected        ON            //连接状态
wsrep_ready             ON           //服务状态
```
**步骤二：访问集群，存取数据**

1）添加访问数据的连接用户 （在任意一台服务器上添加都可以，另外的2台服务器会自动同步授权用户）
```shell
[root@pxcnode72 ~]# mysql  -uroot  -p123456
mysql> grant all on  gamedb.*  to yaya@"%" identified by "123456"; //添加授权用户
Query OK, 0 rows affected, 1 warning (0.18 sec)
[root@pxcnode71 ~]# mysql -uroot -p123456 -e  'show grants for yaya@"%" ' //查看
mysql: [Warning] Using a password on the command line interface can be insecure.
+--------------------------------------------------+
| Grants for yaya@%                                |
+--------------------------------------------------+
| GRANT USAGE ON *.* TO 'yaya'@'%'                 |
| GRANT ALL PRIVILEGES ON `gamedb`.* TO 'yaya'@'%' |
+--------------------------------------------------+
[root@pxcnode71 ~]#
[root@pxcnode73 ~]# mysql -uroot -p123456 -e  'show grants for yaya@"%" ' //查看
mysql: [Warning] Using a password on the command line interface can be insecure.
+--------------------------------------------------+
| Grants for yaya@%                                |
+--------------------------------------------------+
| GRANT USAGE ON *.* TO 'yaya'@'%'                 |
| GRANT ALL PRIVILEGES ON `gamedb`.* TO 'yaya'@'%' |
+--------------------------------------------------+
[root@pxcnode73 ~]#
```
2）客户端连接集群存取数据 （连接任意一台数据库服务器的ip地址都可以）

连接数据服务器主机73
```shell
client50 ~]# mysql -h192.168.4.73 -uyaya -p123456 //连接服务器73
mysql>
mysql> create database gamedb; //建库
Query OK, 1 row affected (0.19 sec)
mysql>  create table  gamedb.a(id int primary key auto_increment,name char(10));//建表
Query OK, 0 rows affected (1.02 sec)
mysql> insert into gamedb.a(name)values("bob"),("tom"); //插入记录
Query OK, 2 rows affected (0.20 sec)
Records: 2  Duplicates: 0  Warnings: 0
```
3）在另外2台数据库服务器查看数据，客户端连接数据库服务器71主机查看数据。
```shell
client50 ~]# mysql -h192.168.4.71 -uyaya -p123456 //连接服务器71
mysql> select  * from  gamedb.a; //查看记录
+----+-------+
| id | name  |
+----+-------+
|  2 | bob   |
|  5 | tom   |
```
4）客户端连接数据库服务器73主机查看数据
```shell
client50 ~]# mysql -h192.168.4.73 -uyaya -p123456 //连接服务器73
mysql> select  * from  gamedb.a; //查看记录
+----+-------+
| id | name  |
+----+-------+
|  2 | bob   |
|  5 | tom   |
```
**步骤三：测试故障自动恢复**

1）停止数据库服务

停止三台服务器的任意一台主机的数据库服务都不会影响数据的存取。
```shell
[root@pxcnode71 ~]# systemctl  stop  mysql  //停止71主机的数据库服务
```
2）在客户端连接剩下两台服务器，任意一台都可以访问数据
```shell
Client50 ~]# client50 ~]# mysql -h192.168.4.72 -uyaya -p123456 //连接服务器72
mysql> insert into gamedb.a(name)values("bob2"),("tom2");
mysql> insert into gamedb.a(name)values("jerry"),("jack");
Query OK, 2 rows affected (0.20 sec)
Records: 2  Duplicates: 0  Warnings: 0 
```
客户端50，连接数据库主机73，查看数据
```shell
client50 ~]# mysql -h192.168.4.73 -uyaya -p123456 //连接服务器73
mysql> select  * from  gamedb.a;
+----+-------+
| id | name  |
+----+-------+
|  2 | bob   |
|  5 | tom   |
|  7 | bob2  |
|  9 | tom2  |
| 11 | jerry |
| 13 | jack  |
+----+-------+
6 rows in set (0.00 sec)
```
3）启动71主机的数据库服务

数据库服务运行后，会自动同步宕机期间的数据。
```shell
client50 ~]# mysql -h192.168.4.71 -uyaya -p123456 //连接服务器71
mysql> select  * from  gamedb.a;
+----+-------+
| id | name  |
+----+-------+
|  2 | bob   |
|  5 | tom   |
|  7 | bob2  |
|  9 | tom2  |
| 11 | jerry |
| 13 | jack  |
+----+-------+
rows in set (0.00 sec)
```
# 4. MySQL存储引擎
## 4.1 问题
具体如下：
1. MySQL服务存储引擎管理
2. 表存储引擎管理

## 4.2 步骤
实现此案例需要在192.168.4.50主机按照如下步骤进行。

**步骤一：MySQL服务存储引擎管理**

1）查看存储引擎

执行SHOW ENGINES\G指令可列表查看，MySQL 5.6可用的存储引擎有9种（除最后的FEDERATED以外，其他8种都支持），其中默认采用的存储引擎为InnoDB
```shell
//管理员登录
[root@host50 ~]# mysql -uroot -pNSD123...a 
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 4
Server version: 5.7.17-log MySQL Community Server (GPL)
……
……
mysql> 
//查看存储引擎
mysql> SHOW ENGINES\G
*************************** 1. row ***************************
      Engine: InnoDB //默认存储引擎
     Support: DEFAULT                              
     Comment: Supports transactions, row-level locking, and foreign keys
Transactions: YES
          XA: YES
  Savepoints: YES
*************************** 2. row ***************************
      Engine: MRG_MYISAM
     Support: YES
     Comment: Collection of identical MyISAM tables
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 3. row ***************************
      Engine: MEMORY
     Support: YES
     Comment: Hash based, stored in memory, useful for temporary tables
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 4. row ***************************
      Engine: BLACKHOLE
     Support: YES
     Comment: /dev/null storage engine (anything you write to it disappears)
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 5. row ***************************
      Engine: MyISAM
     Support: YES
     Comment: MyISAM storage engine
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 6. row ***************************
      Engine: CSV
     Support: YES
     Comment: CSV storage engine
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 7. row ***************************
      Engine: ARCHIVE
     Support: YES
     Comment: Archive storage engine
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 8. row ***************************
      Engine: PERFORMANCE_SCHEMA
     Support: YES
     Comment: Performance Schema
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 9. row ***************************
      Engine: FEDERATED
     Support: NO                             
     Comment: Federated MySQL storage engine
Transactions: NULL
          XA: NULL
  Savepoints: NULL
9 rows in set (0.01 sec)
```
2）修改服务默认使用的存储引擎

在 mysql> 环境中，可以直接通过SET指令更改默认的存储引擎（只在本次连接会话过程中有效，退出重进即失效） 。比如临时修改为MyISAM，可执行下列操作：
```shell
mysql> SET default_storage_engine=MyISAM;              //改用MyISAM引擎
Query OK, 0 rows affected (0.00 sec)
mysql> SHOW VARIABLES LIKE 'default_storage_engine';          //确认结果
+------------------------+--------+
| Variable_name          | Value  |
+------------------------+--------+
| default_storage_engine | MyISAM |
+------------------------+--------+
1 row in set (0.00 sec)
```
若希望直接修改MySQL服务程序所采用的默认存储引擎，应将相关设置写入配置文件/etc/my.cnf，并重启服务后生效。比如：
```shell
[root@dbsvr1 ~]# vim /etc/my.cnf
[mysqld]
.. ..
default_storage_engine=myisam                              //改用myisam引擎
[root@dbsvr1 ~]# systemctl  restart mysqld.service           //重启服务
```
重新登入确认修改结果：
```shell
[root@dbsvr1 ~]# mysql -uroot –Pnsd123…a
……
……
mysql> SHOW VARIABLES LIKE 'default_storage_engine';
+------------------------+--------+
| Variable_name          | Value  |
+------------------------+--------+
| default_storage_engine | MYISAM |                  //默认引擎已修改
+------------------------+--------+
1 row in set (0.00 sec)
mysql> exit
Bye
```
**步骤二：表存储引擎管理**

1）查看表使用的存储引擎

通过查看建表命令，显示表使用的存储引擎
```shell
mysql> show create table user \G  //查看建表命令
*************************** 1. row ***************************
       Table: user
Create Table: CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(50) DEFAULT NULL,
  `age` tinyint(3) unsigned DEFAULT '19',
  `password` char(1) DEFAULT NULL,
  `uid` int(11) DEFAULT NULL,
  `gid` int(11) DEFAULT NULL,
  `comment` char(150) DEFAULT NULL,
  `homedir` char(50) DEFAULT NULL,
  `shell` char(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=latin1  //存储引擎是InnoDB
1 row in set (0.00 sec)
mysql>
```
2）设置表使用的存储引擎
```shell
//建表时，指定表使用的存储引擎
mysql> create table tarena.stuinfo( name char(10) , age int ) engine=memory;
Query OK, 0 rows affected (0.06 sec)
//查看表文件
mysql> system ls /var/lib/mysql/tarena/stuinfo.*
/var/lib/mysql/tarena/stuinfo.frm
mysql> 
//修改表使用的存储引擎
mysql> alter table tarena.stuinfo engine=innodb;
Query OK, 0 rows affected (0.06 sec)
Records: 0  Duplicates: 0  Warnings: 0
//查看表文件
mysql> system ls /var/lib/mysql/tarena/stuinfo.*
/var/lib/mysql/tarena/stuinfo.frm
/var/lib/mysql/tarena/stuinfo.ibd  
mysql> 
//不指定存储引擎，使用服务默认存储引擎
mysql> create table tarena.stuinfo2( name char(10) , age int );
Query OK, 0 rows affected (0.20 sec)
//查看表文件
mysql> system ls /var/lib/mysql/tarena/stuinfo2.*
/var/lib/mysql/tarena/stuinfo2.frm  
/var/lib/mysql/tarena/stuinfo2.MYD
/var/lib/mysql/tarena/stuinfo2.MYI
mysql> 
```
# 5. 事务特性
## 5.1 问题
具体操作如下：
1. 练习事务回滚
2. 练习事务隔离级别

## 5.2 步骤
实现此案例需要在192.168.4.50主机按照如下步骤进行。

**步骤一：练习事务回滚**

1）事务的创建
```shell
[root@host50 ~]# mysql -uroot –Pnsd123…a  //管理员登录
mysql> 
//查看自动提交状态
mysql> show variables like '%autocommit%';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| autocommit    | ON    |
+---------------+-------+
1 row in set (0.00 sec)
```
显示事务：
```shell
mysql> set autocommit=0;  //只对当前会话生效
Query OK, 0 rows affected (0.00 sec)
mysql> show variables like '%autocommit%';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| autocommit    | OFF   |
+---------------+-------+
1 row in set (0.00 sec)
```
2）事务执行步骤

第一步：开启事务
```shell
set aotocommit=0;
start transaction;    # 可选
```
第二步:编写事务语句
```shell
INSERT、UPDATE、DELETE  语句
```
第三步:结束事务
```shell
commit | rollback;
```
3）事务示例
```shell
//创建银行表
mysql> create table tarena.bank(
    ->   id int primary key,
    ->   name varchar(20),
    ->   balance int
    -> )engine=innodb;
//插入记录
mysql> insert into tarena.bank values(1,"jim",10000),(2,"tom",20000);
Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0
//查看记录
mysql> select  * from tarena.bank;
+----+------+---------+
| id | name | balance |
+----+------+---------+
|  1 | jim  |   10000 |
|  2 | tom  |   20000 |
+----+------+---------+
2 rows in set (0.00 sec)
//验证事务
Mysql> set autocommit=0; #关闭自动提交
//修改字段值
mysql> update tarena.bank set balance=balance-800 where id = 1; #减800
Query OK, 1 row affected (0.05 sec)
Rows matched: 1  Changed: 1  Warnings: 0
mysql> update tarena.bank set balance=balance+800 where id = 2; #加800
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
//查看修改
mysql> select  * from tarena.bank;
+----+------+---------+
| id | name | balance |
+----+------+---------+
|  1 | jim  |    9200 |
|  2 | tom  |   20800 |
+----+------+---------+
2 rows in set (0.00 sec)
mysql>
//打开新终端，连接数据库服务，查看记录
mysql> select  * from tarena.bank;#发现记录没改，因为对方没有提交
+----+------+---------+
| id | name | balance |
+----+------+---------+
|  1 | jim  |   10000 |
|  2 | tom  |   20000 |
+----+------+---------+
2 rows in set (0.00 sec)
mysql>
//回到 set autocommit = 0 的 终端
mysql> rollback ; #执行回滚命令，因为没有提交可以回滚
Query OK, 0 rows affected (0.26 sec)
mysql> select  * from  tarena.bank;#数据被回滚到没有修改前。
+----+------+---------+
| id | name | balance |
+----+------+---------+
|  1 | jim  |   10000 |
|  2 | tom  |   20000 |
+----+------+---------+
2 rows in set (0.00 sec)
mysql>
```
4）SAVEPOINT应用
使用mysql中的savepoint保存点来实现事务的部分回滚

语法:
```shell
SAVEPOINT identifier
ROLLBACK [WORK] TO [SAVEPOINT] identifier
RELEASE SAVEPOINT identifier
```
说明:
使用 SAVEPOINT identifier 来创建一个名为identifier的回滚点
ROLLBACK TO identifier，回滚到指定名称的SAVEPOINT，这里是identifier
使用 RELEASE SAVEPOINT identifier 来释放删除保存点identifier
如果当前事务具有相同名称的保存点，则将删除旧的保存点并设置一个新的保存点。
如果执行START TRANSACTION，COMMIT和ROLLBACK语句，则将删除当前事务的所有保存点。

SAVEPOINT示例:
```shell
//关闭自动提交
mysql> set autocommit=0;
Query OK, 0 rows affected (0.00 sec)
//修改记录
mysql>  update tarena.bank set balance=balance+500 where id = 1;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
//修改前定义保存点名称为a
mysql> savepoint a;
Query OK, 0 rows affected (0.00 sec)
//执行修改
mysql>  update tarena.bank set balance=balance+400 where id = 2;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
//查看记录
mysql> select  * from tarena.bank;
+----+------+---------+
| id | name | balance |
+----+------+---------+
|  1 | jim  |   10500 |
|  2 | tom  |   20400 |
+----+------+---------+
2 rows in set (0.00 sec)
//回滚到保存点a
mysql> rollback to a;
Query OK, 0 rows affected (0.00 sec)
//查看数据
mysql> select  * from tarena.bank;
+----+------+---------+
| id | name | balance |
+----+------+---------+
|  1 | jim  |   10500 |
|  2 | tom  |   20000 |   #数据还原了
+----+------+---------+
2 rows in set (0.00 sec)
```
**步骤二：练习事务隔离级别**
1）查看当前事务隔离级别
```shell
mysql> select @@tx_isolation;  #可重复读
+-----------------+
| @@tx_isolation  |
+-----------------+
| REPEATABLE-READ | 
+-----------------+
1 row in set (0.00 sec)
mysql> mysql>
```
2）修改事务隔离级别
```shell
//设置事务隔离级别 读未提交
mysql> set session transaction isolation level read uncommitted ;
Query OK, 0 rows affected (0.00 sec)
mysql> select @@tx_isolation; 
+------------------+
| @@tx_isolation   |
+------------------+
| READ-UNCOMMITTED |
+------------------+
1 row in set (0.00 sec)
mysql>
mysql> select  * from tarena.bank;
+----+------+---------+
| id | name | balance |
+----+------+---------+
|  1 | jim  |   10500 |
|  2 | tom  |   20000 |
+----+------+---------+
2 rows in set (0.00 sec)
mysql>
mysql> set autocommit=0;
mysql> update tarena.bank set balance=balance+100 where id =1 ;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
mysql> select  * from tarena.bank;
+----+------+---------+
| id | name | balance |
+----+------+---------+
|  1 | jim  |   10600 |
|  2 | tom  |   20000 |
+----+------+---------+
2 rows in set (0.00 sec)
mysql>
//没有查看到改变数据
mysql> select  * from tarena.bank;
+----+------+---------+
| id | name | balance |
+----+------+---------+
|  1 | jim  |   10500 |
|  2 | tom  |   20000 |
+----+------+---------+
2 rows in set (0.00 sec)
mysql>
//设置事务隔离级别 读未提交
mysql> set session transaction isolation level read uncommitted;
Query OK, 0 rows affected (0.00 sec)
//可以查看到数据了 ，此时id 值 1 的用户已经增加了
mysql> select  * from tarena.bank;  
+----+------+---------+
| id | name | balance |
+----+------+---------+
|  1 | jim  |   10600 |
|  2 | tom  |   20000 |
+----+------+---------+
2 rows in set (0.00 sec)
mysql> 
mysql> rollback;  #执行回滚
Query OK, 0 rows affected (0.00 sec)
mysql> select  * from tarena.bank; #查看数据
+----+------+---------+
| id | name | balance |
+----+------+---------+
|  1 | jim  |   10500 |
|  2 | tom  |   20000 |
+----+------+---------+
2 rows in set (0.00 sec)
mysql>
mysql> select  * from tarena.bank; #id值1 的 数据又减少了
+----+------+---------+
| id | name | balance |
+----+------+---------+
|  1 | jim  |   10500 |
|  2 | tom  |   20000 |
+----+------+---------+
2 rows in set (0.00 sec)
```

# Exercise
## 1 简述MySQL体系结构的组成，并描述每个组成部分的作用。
mysql体系结构包括如下组成部分：

## 2 简述innodb存储引擎和myisam存储引擎的特点。
innodb的特点：支持行级锁、支持外键 、 支持事务 、支持事务回滚。
myisam的特点：支持表级锁、不支持外键 、不支持事务 、不支持事务回滚

## 3 简述PXC集群相关端口号及作用。

> 如有侵权，请联系作者删除
