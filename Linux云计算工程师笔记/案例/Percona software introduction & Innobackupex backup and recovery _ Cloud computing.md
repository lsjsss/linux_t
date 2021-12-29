@[TOC]( Percona software introduction & Innobackupex backup and recovery | Cloud computing )

---
# 1. 完全备份与恢复
## 1.1 问题
1. 练习物理备份与恢复
2. 练习mysqldump备份与恢复

## 1.2 步骤
在192.168.4.50按照如下步骤完成。

**步骤一：练习物理备份与恢复**
```shell
//创建备份文件存储目录
[root@host50 ~]# mkdir /bakdir
//拷贝数据库目录
[root@host50 ~]# cp -r /var/lib/mysql  /bakdir/mysql.bak
//打包压缩数据库目录
[root@host50 ~]# cd  /var/lib/mysql/
[root@host50 ~]# tar –zcvf /bakdir/mysql.tar.gz  ./*
//查看备份文件
[root@host50 ~]# ls /bakdir/
mysql.bak  mysql.tar.gz
[root@host50 ~]#
```
2)恢复数据

50主机使用备份文件恢复数据
```shell
[root@host50 ~]# systemctl  stop mysqld
[root@host50 ~]# rm  -rf /var/lib/mysql/*
[root@host50 ~]# cp -r /bakdir/mysql.bak/* /var/lib/mysql/
或
[root@host50 ~]# tar -zxvf /bakdir/mysql.tar.gz  -C /var/lib/mysql/
[root@host50 ~]# chown  -R mysql:mysql /var/lib/mysql
[root@host50 ~]# systemctl  start mysqld
[root@host50 ~]# mysql -uroot -pNSD123...a -e 'use tarena; show tables'
mysql: [Warning] Using a password on the command line interface can be insecure.
+------------------+
| Tables_in_tarena |
+------------------+
| departments      |
| emp_sal_view     |
| employees        |
| salary           |
| t1               |
| t2               |
| t3               |
| t4               |
| t5               |
| user             |
| user3            |
| v1               |
| v2               |
| v4               |
| v6               |
| v7               |
+------------------+
[root@host50 ~]#
```
**步骤二：练习mysqldump备份与恢复**

在50主机做备份和恢复的练习

1）完全备份
Mysql服务的备份文件通常以.sql结尾
```shell
//备份所有数据
[root@host50 ~]# mysqldump -uroot -pNSD123...a  --all-databases > /bakdir/all.sql
mysqldump: [Warning] Using a password on the command line interface can be insecure.
[root@host50 ~]#
//仅备份mysql库的所有的数据 
[root@host50 ~]# mysqldump -uroot -pNSD123...a  -B mysql > /bakdir/mysql.sql
mysqldump: [Warning] Using a password on the command line interface can be insecure.
[root@host50 ~]# 
//一起备份tarena库和db1 库的所有数据
[root@host50 ~]# mysqldump -uroot -pNSD123...a  -B tarena db1  > /bakdir/tarna_db1.sql
mysqldump: [Warning] Using a password on the command line interface can be insecure.
[root@host50 ~]# 
//只备份tarena库里的user表所有数据
[root@host50 ~]# mysqldump -uroot -pNSD123...a  tarena user  > /bakdir/tarna_user.sql
mysqldump: [Warning] Using a password on the command line interface can be insecure.
[root@host50 ~]# 
//同时备份tarena库下的 employees表和salary表的所有数据
[root@host50 ~]# mysqldump -uroot -pNSD123...a  tarena employees  salary  > /bakdir/tarna_employees_salary.sql
mysqldump: [Warning] Using a password on the command line interface can be insecure.
//查看备份文件
[root@host50 ~]# ls /bakdir/*.sql
/bakdir/all.sql  /bakdir/mysql.sql  /bakdir/tarna_db1.sql  /bakdir/tarna_employees_salary.sql  /bakdir/tarna_user.sql
[root@host50 ~]#
```
2）完全恢复
```shell
在50主机删除的数据后，使用备份文件恢复

//删除表里的记录
[root@host50 ~]# mysql -uroot -pNSD123...a -e 'delete from tarena.user'
mysql: [Warning] Using a password on the command line interface can be insecure.
//表记录行数为0
[root@host50 ~]# mysql -uroot -pNSD123...a -e 'select count(*) from tarena.user'
mysql: [Warning] Using a password on the command line interface can be insecure.
+----------+
| count(*) |
+----------+
|        0 |
+----------+
[root@host50 ~]#
//使用备份文件恢复数据
[root@host50 ~]# mysql -uroot -pNSD123...a  tarena < /bakdir/tarna_user.sql 
mysql: [Warning] Using a password on the command line interface can be insecure.
[root@host50 ~]# 
//查看表记录
[root@host50 ~]# mysql -uroot -pNSD123...a -e 'select count(*) from tarena.user'
mysql: [Warning] Using a password on the command line interface can be insecure.
+----------+
| count(*) |
+----------+
|       23 |
+----------+
[root@host50 ~]#
//删除工资表salary
[root@host50 ~]# mysql -uroot -pNSD123...a -e 'drop table tarena.salary'
mysql: [Warning] Using a password on the command line interface can be insecure.
//删除员工表employees
[root@host50 ~]# mysql -uroot -pNSD123...a -e 'drop table tarena.employees'
mysql: [Warning] Using a password on the command line interface can be insecure.
[root@host50 ~]#
//使用备份文件恢复数据
[root@host50 ~]# mysql -uroot -pNSD123...a  tarena < /bakdir/tarna_employees_salary.sql 
mysql: [Warning] Using a password on the command line interface can be insecure.
[root@host50 ~]# 
//查看表记录
[root@host50 ~]# mysql -uroot -pNSD123...a -e 'select count(*) from tarena.salary'
mysql: [Warning] Using a password on the command line interface can be insecure.
+----------+
| count(*) |
+----------+
|     8055 |
+----------+
//查看表记录
[root@host50 ~]# mysql -uroot -pNSD123...a -e 'select count(*) from tarena.employees'
mysql: [Warning] Using a password on the command line interface can be insecure.
+----------+
| count(*) |
+----------+
|      137 |
+----------+
[root@host50 ~]#
[root@host50 ~]# mysql -uroot -pNSD123...a -e 'show databases'
mysql: [Warning] Using a password on the command line interface can be insecure.
+--------------------+
| Database           |
+--------------------+
| information_schema |
| DB1                |
| db1                |
| db2                |
| mydb               |
| mysql              |
| performance_schema |
| sys                |
| tarena             |
+--------------------+
[root@host50 ~]#
```
3）其他主机拷贝50主机的备份文件恢复数据

51主机拷贝50主机的mysql库备份文件，实现与50主机的登录用户一致
```shell
//拷贝50主机的mysql.sql 文件
[root@host51 ~]# scp  192.168.4.50:/bakdir/mysql.sql /root/
Warning: Permanently added '192.168.4.50' (ECDSA) to the list of known hosts.
root@192.168.4.50's password: #50主机的密码 
mysql.sql                                                                                                                          100% 1082KB  45.9MB/s   00:00    
[root@host51 ~]#
#覆盖目标库的同名库数据恢复
[root@host51 ~]# mysql -uroot -pNSD123...a  < /root/mysql.sql 
mysql: [Warning] Using a password on the command line interface can be insecure.
[root@host51 ~]# 
[root@host51 ~]# 
//查看授权用户和50主机的用户一样
[root@host51 ~]# mysql -uroot -pNSD123...a  -e 'select user from mysql.user'
mysql: [Warning] Using a password on the command line interface can be insecure.
+-----------+
| user      |
+-----------+
| mysqla    |
| mysqlb    |
| plj       |
| repluser  |
| webuser   |
| yaya      |
| root      |
| mysql.sys |
| root      |
+-----------+
[root@host51 ~]#
```
# 2. binlog日志
## 2.1 问题
## 2.2 步骤
实现此案例需要在192.168.4.50按照如下步骤进行。

**步骤一：启用binlog日志**

1）修改配置文件，并重启服务。
```shell
[root@host50 ~]# vim  /etc/my.cnf
[mysqld]
    server_id=1  //指定server_id
log-bin=/mylog/db50  //指定日志目录及名称                           
:wq
[root@host50 ~]# mkdir  /mylog   //创建目录
[root@host50 ~]# chown  mysql  /mylog   //修改所有者
[root@host50 ~]# setenforce 0 //禁用selinux
[root@host50 ~]# systemctl  restart mysqld.service  //重启服务
```
2）查看日志信息
```shell
[root@host50 ~]# 
[root@localhost ~]# mysql -uroot -p123qqq...A //管理员登录
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 3
Server version: 5.7.17-log MySQL Community Server (GPL)
……
……
mysql> show master status; //查看日志信息
+-------------+----------+--------------+------------------+-------------------+
| File        | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+-------------+----------+--------------+------------------+-------------------+
| db50.000001 |      154 |              |                  |                   |
+-------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)
mysql>
```
**步骤二:手动创建新日志**

1）手动创建3个新的日志文件
```shell
mysql>
mysql> flush logs;  //刷新日志
Query OK, 0 rows affected (0.14 sec)
mysql> flush logs; //刷新日志
Query OK, 0 rows affected (0.11 sec)
mysql> flush logs; //刷新日志
Query OK, 0 rows affected (0.12 sec)
mysql> system ls /mylog/  //查看日志文件
db50.000001  db50.000002  db50.000003  db50.000004  db50.index
mysql> 
mysql> show master status; //查看日志信息
+-------------+----------+--------------+------------------+-------------------+
| File        | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+-------------+----------+--------------+------------------+-------------------+
| db50.000004 |      154 |              |                  |                   |
+-------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)
mysql>
```
**步骤三:删除binlog日志文件**

1）删除编号3之前的日志文件
```shell
 mysql>
 mysql> purge  master  logs  to  "db50.000003"; //删除日志
Query OK, 0 rows affected (0.05 sec)
mysql> system ls /mylog/    //查看日志文件
db50.000003  db50.000004  db50.index
mysql> 
mysql> system  cat /mylog/db50.index //查看索引文件
/mylog/db50.000003
/mylog/db50.000004
mysql>
```
# 3. 使用binlog日志恢复数据
## 3.1 问题
1. 修改日志格式 修改为mixed
2. 创建库表并插入记录 创建db4库和tb1表并插入3条记录
3. 记录插入和删除 删除tb1表中刚插入的3条记录
4. 恢复记录 使用binlog日志恢复删除的3条记录

## 3.2 步骤
实现此案例需要在192.168.4.50主机按照如下步骤进行。

**步骤一：修改日志格式**

1）修改格式为 mixed
```shell
[root@host50 ~]# vim /etc/my.cnf
[mysqld]
server_id=50
log_bin=db50
binlog_format="mixed"  #指定日志格式
:wq
[root@host50 ~]# systemctl  restart mysqld
[root@host50 ~]# mysql -uroot -pNSD123...a  #管理员登录
mysql> show variables like "binlog_format"; #查看日志格式
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| binlog_format | MIXED |
+---------------+-------+
1 row in set (0.00 sec)
mysql>
mysql> show master status\G  #查看日志信息
*************************** 1. row ***************************
             File: db50.000001
         Position: 154
     Binlog_Do_DB: 
 Binlog_Ignore_DB: 
Executed_Gtid_Set: 
1 row in set (0.00 sec)
mysql>
```
步骤二：创建库表并插入记录

1）创建db4库
```shell
mysql> create database db4 ;
Query OK, 1 row affected (0.03 sec)
```
2）建表tb1表 表结构自定义即可
```shell
mysql> create table db4.tb1(name char(10));
Query OK, 0 rows affected (0.26 sec)
```
3)插入3条表记录
```shell
mysql> insert into db4.tb1 values("tom");
Query OK, 1 row affected (0.07 sec)
mysql> insert into db4.tb1 values("lucy");
Query OK, 1 row affected (0.06 sec)
mysql> insert into db4.tb1 values("lili");
Query OK, 1 row affected (0.03 sec)
//查看日志信息
mysql> show master status\G
*************************** 1. row ***************************
             File: db50.000001
         Position: 1297
     Binlog_Do_DB: 
 Binlog_Ignore_DB: 
Executed_Gtid_Set: 
1 row in set (0.00 sec)
mysql>
```
**步骤三：删除表记录**

1）删除tb1表中刚插入的3条记录
```shell
mysql> select  * from   db4.tb1;
+------+
| name |
+------+
| tom  |
| lucy |
| lili |
+------+
3 rows in set (0.00 sec)
mysql> delete from  db4.tb1;
Query OK, 3 rows affected (0.05 sec)
mysql>
```
**步骤四：恢复记录**

1）使用binlog日志恢复删除的3条记录
```shell
//通过查看日志内容  获取sql命令的范围
mysql> show binlog events in "db50.000001";
+-------------+------+----------------+-----------+-------------+---------------------------------------+
| Log_name    | Pos  | Event_type     | Server_id | End_log_pos | Info                                  |
+-------------+------+----------------+-----------+-------------+---------------------------------------+
| db50.000001 |    4 | Format_desc    |        50 |         123 | Server ver: 5.7.17-log, Binlog ver: 4 |
| db50.000001 |  123 | Previous_gtids |        50 |         154 |                                       |
| db50.000001 |  154 | Anonymous_Gtid |        50 |         219 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'  |
| db50.000001 |  219 | Query          |        50 |         310 | create database db4                   |
| db50.000001 |  310 | Anonymous_Gtid |        50 |         375 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'  |
| db50.000001 |  375 | Query          |        50 |         479 | create table db4.tb1(name char(10))   |
| db50.000001 |  479 | Anonymous_Gtid |        50 |         544 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'  |
| db50.000001 |  544 | Query          |        50 |         618 | BEGIN                                 |
| db50.000001 |  618 | Query          |        50 |         720 | insert into db4.tb1 values("tom")     |
| db50.000001 |  720 | Xid            |        50 |         751 | COMMIT /* xid=7 */                    |
| db50.000001 |  751 | Anonymous_Gtid |        50 |         816 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'  |
| db50.000001 |  816 | Query          |        50 |         890 | BEGIN                                 |
| db50.000001 |  890 | Query          |        50 |         993 | insert into db4.tb1 values("lucy")    |
| db50.000001 |  993 | Xid            |        50 |        1024 | COMMIT /* xid=8 */                    |
| db50.000001 | 1024 | Anonymous_Gtid |        50 |        1089 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'  |
| db50.000001 | 1089 | Query          |        50 |        1163 | BEGIN                                 |
| db50.000001 | 1163 | Query          |        50 |        1266 | insert into db4.tb1 values("lili")    |
| db50.000001 | 1266 | Xid            |        50 |        1297 | COMMIT /* xid=9 */                    |
| db50.000001 | 1297 | Anonymous_Gtid |        50 |        1362 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'  |
| db50.000001 | 1362 | Query          |        50 |        1436 | BEGIN                                 |
| db50.000001 | 1436 | Query          |        50 |        1525 | delete from  db4.tb1                  |
| db50.000001 | 1525 | Xid            |        50 |        1556 | COMMIT /* xid=12 */                   |
+-------------+------+----------------+-----------+-------------+---------------------------------------+
22 rows in set (0.00 sec)
mysql> exit
//恢复数据
[root@host50 ~]# mysqlbinlog --start-position=618 --stop-position=1362  /var/lib/mysql/db50.000001   | mysql -uroot -pNSD123...a
//查看数据
[root@host50 ~]# mysql -uroot -pNSD123...a -e 'select  * from db4.tb1'
mysql: [Warning] Using a password on the command line interface can be insecure.
+------+
| name |
+------+
| tom  |
| lucy |
| lili |
+------+
[root@host50 ~]#
```
# 4. innobackupex完全备份与恢复
## 4.1 问题
1. 安装percona软件
2. 备份所有数据到/allbak目录下
3. 使用备份文件恢复数据
## 4.2 步骤
实现此案例需要按照如下步骤进行

在192.168.4.50主机 备份数据,在192.168.4.50主机或52主机练习数据恢复。

**步骤一：安装percona软件**

1) 在50主机安装软件
```shell
[root@host50 ~]# rpm -ivh libev-4.15-1.el6.rf.x86_64.rpm //安装依赖软件(此软件操作系统光盘没有 需从网上自己下载 安装没有依赖)
[root@host50 ~]# yum -y  install percona-xtrabackup-24-2.4.7-1.el7.x86_64.rpm
警告：percona-xtrabackup-24-2.4.6-2.el7.x86_64.rpm: 头V4 DSA/SHA1 Signature, 密钥 ID cd2efd2a: NOKEY
准备中...                          ################################# [100%]
正在升级/安装...
   1:percona-xtrabackup-24-2.4.6-2.el7################################# [ 33%]
   2:percona-xtrabackup-test-24-2.4.6-################################# [ 67%]
   3:percona-xtrabackup-24-debuginfo-2################################# [100%]
```
2）查看命令帮助信息
```shell
[root@host50 ~]# innobackupex --help  //查看命令选项
[root@host50 ~]#
[root@host50 ~]# man  innobackupex //查看详细帮助 (按q 退出)
```
**步骤二：备份所有数据到/allbak目录下**

1）备份所有数据

备份50主机的所有数据
```shell
//备份50主机所有数据
[root@host50 ~]# innobackupex -uroot -pNSD123...a  /allbak --no-timestamp 
......
......
170425 11:06:00 [00] Copying ib_buffer_pool to /backup/ib_buffer_pool
170425 11:06:00 [00]        ...done
170425 11:06:00 Backup created in directory '/backup/'
170425 11:06:00 [00] Writing backup-my.cnf
170425 11:06:00 [00]        ...done
170425 11:06:00 [00] Writing xtrabackup_info
170425 11:06:00 [00]        ...done
xtrabackup: Transaction log of lsn (2543884) to (2543893) was copied.
170425 11:06:01 completed OK    //提示OK 表示备份成功
```
2）查看备份文件

备份目录下：有数据 和 记录备份信息的配置文件
```shell
[root@host50 ~]# ls /allbak
backup-my.cnf  ib_buffer_pool  mysql      sys                   xtrabackup_info
db1  ibdata1      performance_schema  xtrabackup_checkpoints  xtrabackup_logfile
//保存备份信息的配置文件
[root@host50 ~]# cat /allbak/xtrabackup_checkpoints 
backup_type = full-backuped   #备份类型
from_lsn = 0  #备份数据的起始范围
to_lsn = 9513407 #备份数据的结束范围
last_lsn = 9513416 #增量备份数据的参考点
compact = 0
recover_binlog_info = 0
[root@host50 ~]# 
```
**步骤三：使用备份文件恢复数据**

1）在50本机使用备份文件恢复数据
```shell
[root@host50 ~]# rm -rf /var/lib/mysql/*     //清空数据库目录   
[root@host50 ~]#
[root@host50 ~]# systemctl  stop mysqld         //停止服务
 
//确保数据库目录为空
[root@host50 ~]# ls /var/lib/mysql
[root@host50 ~]# 
//准备恢复数据
[root@host50 ~]# cat /allbak/xtrabackup_checkpoints   #执行准备恢复数据前的信息
backup_type = full-backuped  #类型
from_lsn = 0
to_lsn = 9513407
last_lsn = 9513416
compact = 0
recover_binlog_info = 0
[root@host50 ~]# 
[root@host50 ~]# innobackupex  --apply-log  /allbak #准备恢复数据
[root@host50 ~]# cat /allbak/xtrabackup_checkpoints   #执行准备恢复后查看
backup_type = full-prepared  #类型
from_lsn = 0
to_lsn = 9513407
last_lsn = 9513416
compact = 0
recover_binlog_info = 0
[root@host50 ~]# 
//拷贝数据
[root@host50 ~]# innobackupex --copy-back /allbak
......
......
210915 14:25:06 [01] Copying ./xtrabackup_master_key_id to /var/lib/mysql/xtrabackup_master_key_id
210915 14:25:06 [01]        ...done
210915 14:25:07 [01] Copying ./ibtmp1 to /var/lib/mysql/ibtmp1
210915 14:25:07 [01]        ...done
210915 14:25:07 completed OK!
[root@host50 ~]# 
//修改所有者和组
[root@host50 ~]# chown -R mysql:mysql /var/lib/mysql
//启动数据库服务
[root@host50 ~]# systemctl  start  mysqld
//连接服务查看数据
[root@host50 ~]# mysql -uroot -pNSD123...a -e 'use tarena;show tables'
mysql: [Warning] Using a password on the command line interface can be insecure.
+------------------+
| Tables_in_tarena |
+------------------+
| departments      |
| emp_sal_view     |
| employees        |
| salary           |
| t1               |
| t2               |
| t3               |
| t4               |
| t5               |
| user             |
| user3            |
| v1               |
| v2               |
| v4               |
| v6               |
| v7               |
+------------------+
[root@host50 ~]# 
```
2）在51主机使用备份文件恢复数据
```shell
//安装软件提供innobackupex命令
[root@host51 ~]# rpm -ivh  libev-4.15-1.el6.rf.x86_64.rpm
[root@host51 ~]# yum -y  install percona-xtrabackup-24-2.4.7-1.el7.x86_64.rpm
    //误删除数据
[root@host51 ~]# systemctl  stop mysqld    #停止服务
[root@host51 ~]# rm -rf /var/lib/mysql/*   #清空数据库
//拷贝50主机的备份目录
[root@host51 ~]# scp -r 192.168.4.51:/allbak  /root/
//使用备份目录恢复数据（因为50主机已经做过准备恢复数据了）
[root@host51 ~]# innobackupex  --copy-back /opt/allbak/
[root@host51 ~]# chown  -R mysql:mysql /var/lib/mysql
//启动服务查看数据
[root@host51 ~]# systemctl  start mysqld 
[root@host51 ~]# mysql -uroot -pNSD123...a -e 'use tarena;show tables'
mysql: [Warning] Using a password on the command line interface can be insecure.
+------------------+
| Tables_in_tarena |
+------------------+
| departments      |
| emp_sal_view     |
| employees        |
| salary           |
| t1               |
| t2               |
| t3               |
| t4               |
| t5               |
| user             |
| user3            |
| v1               |
| v2               |
| v4               |
| v6               |
| v7               |
+------------------+
[root@host51 ~]# 
```
# 5. 恢复单张表
## 5.1 问题
1. 删除表记录
2. 恢复表记录
## 5.2 步骤
实现此案例需要按照如下步骤进行(在50主机完成实验)。

**步骤一：删除表记录**
```shell
[root@host50 ~]# mysql –uroot  -pNSD123…a
//删除表记录 以user表为例  
mysql> delete from tarena .user;
Query OK, 23 rows affected (0.03 sec)
```
步骤二：恢复表记录
```shell
//删除表空间
mysql> alter table tarena.user discard  tablespace;
Query OK, 0 rows affected (0.06 sec)
mysql> system ls /var/lib/mysql/tarena/user.*  #只剩表结构文件
/var/lib/mysql/tarena/user.frm
mysql>exit;
[root@host50 ~]# ls /allbak/tarena/user.*   #导出表信息前查看user表文件
/allbak/tarena/user.frm  /allbak/tarena/user.ibd
//导出表信息
[root@host50 ~ ]# innobackupex --apply-log --export  /allbak
……
……
InnoDB: FTS optimize thread exiting.
InnoDB: Starting shutdown...
InnoDB: Shutdown completed; log sequence number 9514071
210915 16:51:04 completed OK!
[root@host50 ~]# 
//执行导出信息命令后查看user表文件
[root@host50 ~]# ls -l /allbak/tarena/user.*
-rw-r--r-- 1 root root   737 9月  15 16:51 /allbak/tarena/user.cfg
-rw-r----- 1 root root 16384 9月  15 16:51 /allbak/tarena/user.exp
-rw-r----- 1 root root  8784 9月  15 11:13 /allbak/tarena/user.frm
-rw-r----- 1 root root 98304 9月  15 11:13 /allbak/tarena/user.ibd
[root@host50 ~]#
//拷贝表信息文件到数据库目录下
[root@host50 ~]# cp /allbak/tarena/user.{cfg,exp,ibd} /var/lib/mysql/tarena/
//修改表信息文件的所有者及组用户为mysql
[root@host50 ~]# chown mysql:mysql /var/lib/mysql/tarena/user.*    
//管理员登录
[root@host50 ~]# mysql -uroot -pNSD123...a   
mysql: [Warning] Using a password on the command line interface can be insecure.
//没有表记录
mysql> select  count(*) from tarena.user;
ERROR 1814 (HY000): Tablespace has been discarded for table 'user'
mysql>
//导入表信息
mysql> alter table tarena.user import  tablespace ;
Query OK, 0 rows affected (0.34 sec)
//查看表记录
mysql> select  count(*) from tarena.user;
+----------+
| count(*) |
+----------+
|       23 |
+----------+
1 row in set (0.00 sec)
mysql> exit 
//删除数据库目录下的表信息文件
[root@host50 ~]# rm -rf /var/lib/mysql/tarena/user.cfg 
[root@host50 ~]# rm -rf /var/lib/mysql/tarena/user.exp
# 6. 增量备份与恢复
## 6.1 问题
- 完全备份
- 增量备份
- 删除数据
- 恢复数据

## 6.2 步骤
实现此案例需要在192.168.4.50主机按照如下步骤进行。

**步骤一：完全备份**

1）备份所有数据
```shell
//备份所有数据到 /fullbak目录
[root@host50 ~]# innobackupex  -uroot -pNSD123...a /fullbak  --no-timestamp
……
……
210917 10:42:13 [00] Writing /fullbak/xtrabackup_info
210917 10:42:13 [00]        ...done
xtrabackup: Transaction log of lsn (11194613) to (11194622) was copied.
210917 10:42:13 completed OK!
[root@host50 ~]#
//查看备份目录
[root@host50 ~]# ls /fullbak/
backup-my.cnf  DB1  db4             ibdata1  mysql               sys     xtrabackup_binlog_info  xtrabackup_info
db1            db2  ib_buffer_pool  mydb     performance_schema  tarena  xtrabackup_checkpoints  xtrabackup_logfile
[root@host50 ~]#
//查看备份信息
[root@host50 ~]# cat /fullbak/xtrabackup_checkpoints 
backup_type = full-backuped  #完全备份
from_lsn = 0  #备份起始位置
to_lsn = 11194613 #备份结束位置
last_lsn = 11194622 #增量备份参考点
compact = 0
recover_binlog_info = 0
[root@host50 ~]#
```
步骤二：增量备份 （每次执行备份，值备份新数据,在50主机执行）

1）第一次增量备份
```shell
//插入新记录(可以插入多行)
[root@host50 ~]# mysql -uroot -pNSD123...a  -e  'insert into tarena.user(name,uid)values("a",1001)'
mysql: [Warning] Using a password on the command line interface can be insecure.
[root@host50 ~]# mysql -uroot -pNSD123...a  -e  'insert into tarena.user(name,uid)values("a",1001)'
mysql: [Warning] Using a password on the command line interface can be insecure.
[root@host50 ~]# mysql -uroot -pNSD123...a  -e  'insert into tarena.user(name,uid)values("a",1001)'
mysql: [Warning] Using a password on the command line interface can be insecure.
[root@host50 ~]# mysql -uroot -pNSD123...a  -e  'insert into tarena.user(name,uid)values("a",1001)'
mysql: [Warning] Using a password on the command line interface can be insecure.
[root@host50 ~]# mysql -uroot -pNSD123...a  -e  'insert into tarena.user(name,uid)values("a",1001)'
mysql: [Warning] Using a password on the command line interface can be insecure.
[root@host50 ~]# mysql -uroot -pNSD123...a  -e  'insert into tarena.user(name,uid)values("a",1001)'
mysql: [Warning] Using a password on the command line interface can be insecure.
[root@host50 ~]#
//增量备份 ，数据存储目录/new1dir
[root@host50 ~]# innobackupex -uroot -pNSD123...a  --incremental /new1dir --incremental-basedir=/fullbak --no-timestamp
……
……
210917 11:01:46 [00] Writing /new1dir/backup-my.cnf
210917 11:01:46 [00]        ...done
210917 11:01:46 [00] Writing /new1dir/xtrabackup_info
210917 11:01:46 [00]        ...done
xtrabackup: Transaction log of lsn (11198109) to (11198118) was copied.
210917 11:01:47 completed OK!
[root@host50 ~]# 
//查看备份目录列表
[root@host50 ~]# ls /new1dir/
backup-my.cnf  DB1  db4             ibdata1.delta  mydb   performance_schema  tarena                  xtrabackup_checkpoints  xtrabackup_logfile
db1            db2  ib_buffer_pool  ibdata1.meta   mysql  sys                 xtrabackup_binlog_info  xtrabackup_info
[root@host50 ~]# 
//查看备份信息
[root@host50 ~]# cat /new1dir/xtrabackup_checkpoints 
backup_type = incremental  #增量备份
from_lsn = 11194613 #备份起始位置
to_lsn = 11198109 #备份结束位置
last_lsn = 11198118 #增量备份参考点
compact = 0
recover_binlog_info = 0
[root@host50 ~]#
```
2) 第二次增量备份
```shell
//增量备份 数据存储在 /new2dir 目录

[root@host50 ~]# innobackupex -uroot -pNSD123...a --incremental /new2dir --incremental-basedir=/new1dir --no-timestamp
……
……
MySQL binlog position: filename 'db50.000001', position '6612'
210917 11:28:12 [00] Writing /new2dir/backup-my.cnf
210917 11:28:12 [00] ...done
210917 11:28:12 [00] Writing /new2dir/xtrabackup_info
210917 11:28:12 [00] ...done
xtrabackup: Transaction log of lsn (11201887) to (11201896) was copied.
210917 11:28:12 completed OK!
[root@host50 ~]#

//查看备份目录
[root@host50 ~]# ls /new2dir/
backup-my.cnf DB1 db4 ibdata1.delta mydb performance_schema tarena xtrabackup_checkpoints xtrabackup_logfile
db1 db2 ib_buffer_pool ibdata1.meta mysql sys xtrabackup_binlog_info xtrabackup_info
[root@host50 ~]#

//查看备份信息
[root@host50 ~]# cat /new2dir/xtrabackup_checkpoints
backup_type = incremental #增量备份
from_lsn = 11198109 #备份起始位置
to_lsn = 11201887 #备份结束位置
last_lsn = 11201896 #增量备份参考点
compact = 0
recover_binlog_info = 0
[root@host50 ~]#
```
**步骤三：删除数据**

1) 停止服务，并清空数据
```shell
[root@host50 ~]# systemctl  stop  mysqld
[root@host50 ~]# rm -rf /var/lib/mysql/*
```
**步骤四：恢复数据**

1）准备恢复数据
```shell
//恢复前查看备份信息文件
[root@host50 ~]# cat /fullbak/xtrabackup_checkpoints 
backup_type = full-backuped   #类型
from_lsn = 0
to_lsn = 11194613
last_lsn = 11194622    #结束位置
compact = 0
recover_binlog_info = 0
[root@host50 ~]#
//准备恢复数据
[root@host50 ~]# innobackupex  --apply-log --redo-only /fullbak 
……
xtrabackup: starting shutdown with innodb_fast_shutdown = 1
InnoDB: Starting shutdown...
InnoDB: Shutdown completed; log sequence number 11194631
InnoDB: Number of pools: 1
210917 11:59:14 completed OK!
[root@host50 ~]#
//查看备份信息文件
[root@host50 ~]# cat /fullbak/xtrabackup_checkpoints 
backup_type = log-applied   #类型
from_lsn = 0
to_lsn = 11194613
last_lsn = 11194622   #结束位置
compact = 0
recover_binlog_info = 0
[root@host50 ~]#
```
2）合并数据
```shell
//合并第1次增量备份数据
[root@host50 ~]# innobackupex  --apply-log --redo-only /fullbak  --incremental-dir=/new1dir
……
……
210917 12:08:16 [01]        ...done
210917 12:08:16 [00] Copying /new1dir//xtrabackup_binlog_info to ./xtrabackup_binlog_info
210917 12:08:16 [00]        ...done
210917 12:08:16 [00] Copying /new1dir//xtrabackup_info to ./xtrabackup_info
210917 12:08:16 [00]        ...done
210917 12:08:16 completed OK!
[root@host50 ~]# 
//查看合并后的备份信息
[root@host50 ~]# cat /fullbak/xtrabackup_checkpoints 
backup_type = log-applied
from_lsn = 0
to_lsn = 11198109
last_lsn = 11198118 # 变成和第1次增量备份位置一样
compact = 0
recover_binlog_info = 0
[root@host50 ~]#
//查看第1次增量备份结束的位置
[root@host50 ~]# cat /new1dir/xtrabackup_checkpoints 
backup_type = incremental
from_lsn = 11194613
to_lsn = 11198109
last_lsn = 11198118 #结束位置
compact = 0
recover_binlog_info = 0
[root@host50 ~]#
//合并第2次增量备份数据
[root@host50 ~]# innobackupex  --apply-log --redo-only /fullbak  --incremental-dir=/new2dir
……
……
210917 12:13:39 [01]        ...done
210917 12:13:40 [00] Copying /new2dir//xtrabackup_binlog_info to ./xtrabackup_binlog_info
210917 12:13:40 [00]        ...done
210917 12:13:40 [00] Copying /new2dir//xtrabackup_info to ./xtrabackup_info
210917 12:13:40 [00]        ...done
210917 12:13:40 completed OK!
[root@host50 ~]# 
//查看备份信息
[root@host50 ~]# cat /fullbak/xtrabackup_checkpoints 
backup_type = log-applied
from_lsn = 0
to_lsn = 11201887  #结束位置是第2次增量备份的位置
last_lsn = 11201896  
compact = 0
recover_binlog_info = 0
[root@host50 ~]# 
//查看第2次增量备份的位置
[root@host50 ~]# cat /new2dir/xtrabackup_checkpoints 
backup_type = incremental
from_lsn = 11198109
to_lsn = 11201887 #增量备份结束位置
last_lsn = 11201896
compact = 0
recover_binlog_info = 0
[root@host50 ~]#
//删除合并数据后的增量备份目录
[root@host50 ~]# 
[root@host50 ~]# rm -rf /new1dir/
[root@host50 ~]# rm -rf /new2dir/
[root@host50 ~]#
```
3）恢复数据
```shell
//拷贝数据
[root@host50 ~]# innobackupex  --copy-back /fullbak/
……
……
210917 12:22:54 [01]        ...done
210917 12:22:54 [01] Copying ./xtrabackup_master_key_id to /var/lib/mysql/xtrabackup_master_key_id
210917 12:22:54 [01]        ...done
210917 12:22:54 [01] Copying ./xtrabackup_info to /var/lib/mysql/xtrabackup_info
210917 12:22:54 [01]        ...done
210917 12:22:54 completed OK!
[root@host50 ~]#
//修改所有者和组
[root@host50 ~]# chown  -R mysql:mysql /var/lib/mysql
//查看修改
[root@host50 ~]# ls -l /var/lib/mysql
总用量 77872
drwxr-x--- 2 mysql mysql       76 9月  17 12:22 db1
drwxr-x--- 2 mysql mysql      142 9月  17 12:22 DB1
drwxr-x--- 2 mysql mysql      164 9月  17 12:22 db2
drwxr-x--- 2 mysql mysql       50 9月  17 12:22 db4
-rw-r----- 1 mysql mysql     1065 9月  17 12:22 ib_buffer_pool
-rw-r----- 1 mysql mysql 79691776 9月  17 12:22 ibdata1
drwxr-x--- 2 mysql mysql       66 9月  17 12:22 mydb
drwxr-x--- 2 mysql mysql     4096 9月  17 12:22 mysql
drwxr-x--- 2 mysql mysql     8192 9月  17 12:22 performance_schema
drwxr-x--- 2 mysql mysql     8192 9月  17 12:22 sys
drwxr-x--- 2 mysql mysql     4096 9月  17 12:22 tarena
-rw-r----- 1 mysql mysql       17 9月  17 12:22 xtrabackup_binlog_pos_innodb
-rw-r----- 1 mysql mysql      523 9月  17 12:22 xtrabackup_info
-rw-r----- 1 mysql mysql        1 9月  17 12:22 xtrabackup_master_key_id
[root@host50 ~]#
//启动服务
[root@host50 ~]# systemctl  start mysqld
//查看数据
[root@host50 ~]# mysql -uroot -pNSD123...a -e ' show databases'
mysql: [Warning] Using a password on the command line interface can be insecure.
+--------------------+
| Database           |
+--------------------+
| information_schema |
| DB1                |
| db1                |
| db2                |
| db4                |
| mydb               |
| mysql              |
| performance_schema |
| sys                |
| tarena             |
+--------------------+
[root@host50 ~]#
```
# Exercise
## 1 阐述innobackupex完全备份与恢复操作命令。
备份数据
```shell
[root@dbsvr1 ~]# innobackupex  -u root -p 123456  /backup  --no-timestamp              
```
恢复数据
```shell
[root@dbsvr1 ~]# systemctl stop  mysqld
[root@dbsvr1 ~]# rm -rf  /var/lib/mysql/*
[root@dbsvr1 ~]# innobackupex –-apply-log  /backup
[root@dbsvr1 ~]# innobackupex --copy-back  /backup  
[root@dbsvr1 ~]# chown  -R  mysql:mysql  /var/lib/mysql
[root@dbsvr1 ~]# systemctl start  mysqld
```
## 2 阐述innobackupex恢复单张表数据的步骤。
删除表空间
导出表信息
拷贝表信息文件到数据库目录下
修改表信息文件的所有者及组用户为mysql
导入表空间
删除数据库目录下的表信息文件
查看表记录

## 3 阐述innobackupex增量恢复数据的步骤与命令。
准备恢复数据
```shell    
innobackupex --apply-log --redo-only   完全备份目录 
```
合并日志
```shell
innobackupex --apply-log --redo-only  完全备份目录 --incremental-dir=增量备份目录 
```
拷贝文件
```shell
innobackupex --copy-back  完全备份文件目录   
```
> 如有侵权，请联系作者删除
