@[TOC]( Table structure & MySQL key values | Cloud computing )

---
# 1. 表管理
## 1.1 问题
具体要求如下：
- 建库练习
- 建表练习
- 管理表记录练习

## 1.2 步骤
在host50主机做如下练习

**步骤一：建库练习**
库，用来存放表的目录，默认创建在数据库目录下
1. 库的查看创建与删除
```sql
[root@host50 ~]# mysql -uroot -pNSD123...a   数据库管理员登录
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 26
Server version: 5.7.17 MySQL Community Server (GPL)
Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql> select user() ; 查看登录的用户
+----------------+
| user()         |
+----------------+
| root@localhost |  用户@客户端地址 （在本机管理员登录）
+----------------+
1 row in set (0.00 sec)
mysql> 
mysql> show databases;  查看已有的库
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| tarena             |
+--------------------+
5 rows in set (0.00 sec)
mysql> 
mysql> select database() ;  查看当前所在的库
+------------+
| database() |
+------------+
| NULL       |  表示没有在任何一个库，此时所在的位置是/var/lib/mysql 目录
+------------+
1 row in set (0.00 sec)
mysql> 
mysql> use tarena; 切换库到tarena库里
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A
Database changed
mysql> 
mysql> select database() ;  再次查看所在的库 
+------------+
| database() |
+------------+
| tarena     |  在tarena库里 所在位置 /var/lib/mysql/tarena 目录
+------------+
1 row in set (0.00 sec)
mysql> 
mysql> show tables;  查看库下已有的表
+------------------+
| Tables_in_tarena |
+------------------+
| departments      |
| employees        |
| salary           |
| user             |
+------------------+
4 rows in set (0.01 sec)
mysql> 
mysql> create database db1; 创建新库
Query OK, 1 row affected (0.00 sec)
mysql> show databases;  此时查看已有库
+--------------------+
| Database           |
+--------------------+
| information_schema |
| db1                |      刚创建的db1库 ， 在数据库目录/var/lib/myql 下会有对应名称的db1目录
| mysql              |
| performance_schema |
| sys                |
| tarena             |
+--------------------+
6 rows in set (0.00 sec)
mysql> 
mysql> system  ls -ld /var/lib/mysql/db1  使用system 命令 在登录状态下执行系统命令
drwxr-x--- 2 mysql mysql 20 9月   7 13:52 /var/lib/mysql/db1
mysql> 
mysql> create database DB1; 库名区别字母大小写 
Query OK, 1 row affected (0.00 sec)
mysql> create database DB1; 库名具有唯一性 所以会报错
ERROR 1007 (HY000): Can't create database 'DB1'; database exists
mysql> 
mysql>  create database if not exists  DB1; 加if not exists语句避免重名报错 
Query OK, 1 row affected, 1 warning (0.01 sec)
mysql> 
mysql> drop database  db1;删除库，如果库里有表会一并被删除
Query OK, 0 rows affected (0.00 sec)
mysql> drop database  db1;  删除没有的库，会报错
ERROR 1008 (HY000): Can't drop database 'db1'; database doesn't exist
mysql> 
mysql> drop database  if exists db1;  加if  exists 语句 避免报错
Query OK, 0 rows affected, 1 warning (0.00 sec)
mysql>
```
**步骤二：建表练习**
表：存储数据的文件。创建在所在库对应的目录下，表必须创建在库里

表的创建与删除
```sql
mysql> create table DB1.t1( 姓名 char(10) , 班级  char(7) ); 在DB1库里创建t1表
Query OK, 0 rows affected (0.20 sec)
mysql> desc DB1.t1;  查看表头名称
+--------+----------+------+-----+---------+-------+
| Field  | Type     | Null | Key | Default | Extra |
+--------+----------+------+-----+---------+-------+
| 姓名   | char(10) | YES  |     | NULL    |       |
| 班级   | char(7)  | YES  |     | NULL    |       |
+--------+----------+------+-----+---------+-------+
2 rows in set (0.00 sec)
mysql> drop table DB1.t1;  删除创建的表
Query OK, 0 rows affected (0.11 sec)
mysql> 
为了便于操作通常使用英文定义表头名和表名
mysql> create table DB1.t1 ( name  char(15) , class char(10));
Query OK, 0 rows affected (0.25 sec)
mysql> desc DB1.t1; 查看表头
+-------+----------+------+-----+---------+-------+
| Field | Type     | Null | Key | Default | Extra |
+-------+----------+------+-----+---------+-------+
| name  | char(15) | YES  |     | NULL    |       |
| class | char(10) | YES  |     | NULL    |       |
+-------+----------+------+-----+---------+-------+
2 rows in set (0.00 sec)
mysql> 
```
修改表
Alter table 库.表 add 字段名 类型(宽度) [约束条件] ;
```sql
mysql> alter table  DB1.t1 add school  char(20) ; 添加1个新字段school
Query OK, 0 rows affected (0.36 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> desc DB1.t1;  默认新添加的字段追加在已有列的末尾
+--------+----------+------+-----+---------+-------+
| Field  | Type     | Null | Key | Default | Extra |
+--------+----------+------+-----+---------+-------+
| name   | char(15) | YES  |     | NULL    |       |
| class  | char(10) | YES  |     | NULL    |       |
| school | char(20) | YES  |     | NULL    |       |
+--------+----------+------+-----+---------+-------+
3 rows in set (0.00 sec)
mysql> 
一起添加2个字段 分别是 mail 和  address 
mysql> alter table  DB1.t1 add mail char(50) , add address  char(80) ;
Query OK, 0 rows affected (0.37 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> desc DB1.t1;  查看新添加的表头，都在追加在末尾
+---------+----------+------+-----+---------+-------+
| Field   | Type     | Null | Key | Default | Extra |
+---------+----------+------+-----+---------+-------+
| name    | char(15) | YES  |     | NULL    |       |
| class   | char(10) | YES  |     | NULL    |       |
| school  | char(20) | YES  |     | NULL    |       |
| mail    | char(50) | YES  |     | NULL    |       |
| address | char(80) | YES  |     | NULL    |       |
+---------+----------+------+-----+---------+-------+
5 rows in set (0.00 sec)
mysql> 
添加新表头number 在第1列的位置
mysql> alter table  DB1.t1 add number int first ;
Query OK, 0 rows affected (0.32 sec)
Records: 0  Duplicates: 0  Warnings: 0
添加新表头在city 放在name的后边
mysql> alter table DB1.t1 add  city  char(10) after name;
Query OK, 0 rows affected (0.42 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> desc DB1.t1;
+---------+----------+------+-----+---------+-------+
| Field   | Type     | Null | Key | Default | Extra |
+---------+----------+------+-----+---------+-------+
| number  | int(11)  | YES  |     | NULL    |       |
| name    | char(15) | YES  |     | NULL    |       |
| city    | char(10) | YES  |     | NULL    |       |
| class   | char(10) | YES  |     | NULL    |       |
| school  | char(20) | YES  |     | NULL    |       |
| mail    | char(50) | YES  |     | NULL    |       |
| address | char(80) | YES  |     | NULL    |       |
+---------+----------+------+-----+---------+-------+
7 rows in set (0.00 sec)
mysql> 
mysql> alter table DB1.t1 drop city;  一次删除一个表头
Query OK, 0 rows affected (0.31 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> alter table DB1.t1 drop class , drop school; 一起删除多个表头
Query OK, 0 rows affected (0.32 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> desc DB1.t1;  查看表头
+---------+----------+------+-----+---------+-------+
| Field   | Type     | Null | Key | Default | Extra |
+---------+----------+------+-----+---------+-------+
| number  | int(11)  | YES  |     | NULL    |       |
| name    | char(15) | YES  |     | NULL    |       |
| mail    | char(50) | YES  |     | NULL    |       |
| address | char(80) | YES  |     | NULL    |       |
+---------+----------+------+-----+---------+-------+
4 rows in set (0.00 sec)
mysql> 
mysql> alter table DB1.t1 modify number tinyint after name; 修改类型和位置，
Query OK, 0 rows affected (0.71 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> desc DB1.t1;  查看修改，把类型修改为tinyint  并移动name表头的后边
+---------+------------+------+-----+---------+-------+
| Field   | Type       | Null | Key | Default | Extra |
+---------+------------+------+-----+---------+-------+
| name    | char(15)   | YES  |     | NULL    |       |
| number  | tinyint(4) | YES  |     | NULL    |       |
| mail    | char(50)   | YES  |     | NULL    |       |
| address | char(80)   | YES  |     | NULL    |       |
+---------+------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
mysql> 
mysql> alter table  DB1.t1 change  address homedir char(80); 只修改表头名，类型原样抄下来
Query OK, 0 rows affected (0.05 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> desc DB1.t1;查看修改，address 修改为了 homedir
+---------+------------+------+-----+---------+-------+
| Field   | Type       | Null | Key | Default | Extra |
+---------+------------+------+-----+---------+-------+
| name    | char(15)   | YES  |     | NULL    |       |
| number  | tinyint(4) | YES  |     | NULL    |       |
| mail    | char(50)   | YES  |     | NULL    |       |
| homedir | char(80)   | YES  |     | NULL    |       |
+---------+------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
mysql> 
mysql> alter table  DB1.t1 change mail email varchar(60); 表头名和类型一起修改
Query OK, 0 rows affected (0.44 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> desc DB1.t1;查看修改表头名类型都变了
+---------+-------------+------+-----+---------+-------+
| Field   | Type        | Null | Key | Default | Extra |
+---------+-------------+------+-----+---------+-------+
| name    | char(15)    | YES  |     | NULL    |       |
| number  | tinyint(4)  | YES  |     | NULL    |       |
| email   | varchar(60) | YES  |     | NULL    |       |
| homedir | char(80)    | YES  |     | NULL    |       |
+---------+-------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
mysql> use DB1;  切换到 DB1库
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A
Database changed
mysql>  show tables;  查看已有表
+---------------+
| Tables_in_DB1 |
+---------------+
| t1            |
+---------------+
1 row in set (0.00 sec)
mysql> alter table DB1.t1 rename stuinfo; 修改表名为 stuinfo
Query OK, 0 rows affected (0.07 sec)
mysql> show tables; 查看表名 已经改变
+---------------+
| Tables_in_DB1 |
+---------------+
| stuinfo       |
+---------------+
1 row in set (0.00 sec)
mysql> 
```
复制表

原表的主键 外键 普通索引不会被复制给新表
新表的数据和表头有select查询语句决定
```sql
mysql> create table DB1.t2  select  * from tarena.user;  复制表结构及数据
mysql> use DB1;  切换到DB1库
Database changed
mysql> show tables; 查看表
+---------------+
| Tables_in_DB1 |
+---------------+
| stuinfo        |
| t2              | 多了t2表
+---------------+
2 rows in set (0.00 sec)
mysql> select  * from  DB1.t2;  查看记录
mysql> create table DB1.t3  select  name , uid,gid  from tarena.user; 只复制原表的3个表头的记录
Query OK, 27 rows affected (0.30 sec)
Records: 27  Duplicates: 0  Warnings: 0
mysql> desc DB1.t3;
+-------+----------+------+-----+---------+-------+
| Field | Type     | Null | Key | Default | Extra |
+-------+----------+------+-----+---------+-------+
| name  | char(20) | YES  |     | NULL    |       |
| uid   | int(11)  | YES  |     | NULL    |       |
| gid   | int(11)  | YES  |     | NULL    |       |
+-------+----------+------+-----+---------+-------+
3 rows in set (0.00 sec)
mysql> select  * from DB1.t3; 查询表记录
只复制表结构
mysql> create table DB1.t4  select  * from  tarena.user where  1  = 2 ;
Query OK, 0 rows affected (0.26 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> show tables; 查看表
+---------------+
| Tables_in_DB1 |
+---------------+
| stuinfo       |
| t2            |
| t3            |
| t4            | 多了 t4表
+---------------+
4 rows in set (0.00 sec)
mysql> desc t4;  有表结构
+----------+-------------+------+-----+---------+-------+
| Field    | Type        | Null | Key | Default | Extra |
+----------+-------------+------+-----+---------+-------+
| id       | int(11)     | NO   |     | 0       |       |
| name     | char(20)    | YES  |     | NULL    |       |
| password | char(1)     | YES  |     | NULL    |       |
| uid      | int(11)     | YES  |     | NULL    |       |
| gid      | int(11)     | YES  |     | NULL    |       |
| comment  | varchar(50) | YES  |     | NULL    |       |
| homedir  | varchar(80) | YES  |     | NULL    |       |
| shell    | char(30)    | YES  |     | NULL    |       |
+----------+-------------+------+-----+---------+-------+
8 rows in set (0.00 sec)
mysql> select  * from DB1.t4;  没有记录
Empty set (0.00 sec)
mysql> 
```
**步骤三、管理表记录**

1. 插入表记录
```sql
添加1行给所有表头赋值
mysql> insert into DB1.stuinfo  values ("yaya",1,"yaya@tedu.cn","beijing");
Query OK, 1 row affected (0.03 sec)
添加多行给所有表头赋值
mysql> insert into DB1.stuinfo  values ("plj",8,"plj@163.com","shanghai"),("jing",9,"jing@163.com","beijing");
Query OK, 2 rows affected (0.04 sec)
Records: 2  Duplicates: 0  Warnings: 0
mysql> select  * from DB1.stuinfo; 查看表记录
+------+--------+--------------+----------+
| name | number | email        | homedir  |
+------+--------+--------------+----------+
| yaya |      1 | yaya@tedu.cn | beijing  |
| plj  |      8 | plj@163.com  | shanghai |
| jing |      9 | jing@163.com | beijing  |
+------+--------+--------------+----------+
3 rows in set (0.00 sec)
mysql> 
添加1行 ，给指定的表头赋值，
mysql> insert into DB1.stuinfo (name,homedir)values("nb","nb@tedu.cn");
Query OK, 1 row affected (0.04 sec)
添加多行，给指定表头赋值
mysql> insert into DB1.stuinfo (name,homedir)values("nb2","nb2@tedu.cn"),("nb3","nb3@tedu.cn");
Query OK, 2 rows affected (0.03 sec)
Records: 2  Duplicates: 0  Warnings: 0
没有赋值的表头number和email 没有数据 ，值是 null （空）
mysql> select  * from DB1.stuinfo;
+------+--------+--------------+-------------+
| name | number | email        | homedir     |
+------+--------+--------------+-------------+
| yaya |      1 | yaya@tedu.cn | beijing     |
| plj  |      8 | plj@163.com  | shanghai    |
| jing |      9 | jing@163.com | beijing     |
| nb   |   NULL | NULL         | nb@tedu.cn  |
| nb2  |   NULL | NULL         | nb2@tedu.cn |
| nb3  |   NULL | NULL         | nb3@tedu.cn |
+------+--------+--------------+-------------+
6 rows in set (0.00 sec)
mysql> 
使用select 查询结果插入数据
mysql> insert into DB1.stuinfo (select * from DB1.stuinfo); 把已经插入的记录全都重新插入一遍。
Query OK, 6 rows affected (0.04 sec)
Records: 6  Duplicates: 0  Warnings: 0
mysql> select  * from DB1.stuinfo;  查看记录
+------+--------+--------------+-------------+
| name | number | email        | homedir     |
+------+--------+--------------+-------------+
| yaya |      1 | yaya@tedu.cn | beijing     |
| plj  |      8 | plj@163.com  | shanghai    |
| jing |      9 | jing@163.com | beijing     |
| nb   |   NULL | NULL         | nb@tedu.cn  |
| nb2  |   NULL | NULL         | nb2@tedu.cn |
| nb3  |   NULL | NULL         | nb3@tedu.cn |
| yaya |      1 | yaya@tedu.cn | beijing     |
| plj  |      8 | plj@163.com  | shanghai    |
| jing |      9 | jing@163.com | beijing     |
| nb   |   NULL | NULL         | nb@tedu.cn  |
| nb2  |   NULL | NULL         | nb2@tedu.cn |
| nb3  |   NULL | NULL         | nb3@tedu.cn |
+------+--------+--------------+-------------+
12 rows in set (0.00 sec)
mysql> 
给指定的表头使用使用查询结果赋值
mysql> insert into DB1.stuinfo(name,number) (select name , number from DB1.stuinfo where number in (1,8,9));
Query OK, 6 rows affected (0.04 sec)
Records: 6  Duplicates: 0  Warnings: 0
mysql> select  * from DB1.stuinfo;
+------+--------+--------------+-------------+
| name | number | email        | homedir     |
+------+--------+--------------+-------------+
| yaya |      1 | yaya@tedu.cn | beijing     |
| plj  |      8 | plj@163.com  | shanghai    |
| jing |      9 | jing@163.com | beijing     |
| nb   |   NULL | NULL         | nb@tedu.cn  |
| nb2  |   NULL | NULL         | nb2@tedu.cn |
| nb3  |   NULL | NULL         | nb3@tedu.cn |
| yaya |      1 | yaya@tedu.cn | beijing     |
| plj  |      8 | plj@163.com  | shanghai    |
| jing |      9 | jing@163.com | beijing     |
| nb   |   NULL | NULL         | nb@tedu.cn  |
| nb2  |   NULL | NULL         | nb2@tedu.cn |
| nb3  |   NULL | NULL         | nb3@tedu.cn |
| yaya |      1 | NULL         | NULL        |此行向下新插入的行
| plj  |      8 | NULL         | NULL        |
| jing |      9 | NULL         | NULL        |
| yaya |      1 | NULL         | NULL        |
| plj  |      8 | NULL         | NULL        |
| jing |      9 | NULL         | NULL        |
+------+--------+--------------+-------------+
18 rows in set (0.00 sec)
mysql> 
使用set语句插入记录 
mysql> insert into  DB1.stuinfo set name="plj" , number=10;
```
2）修改表记录
```sql
mysql> select name , homedir from DB1.stuinfo;
+--------+-------------+
| name   | homedir     |
+--------+-------------+
| yaya   | beijing     |
| plj    | shanghai    |
| jing   | beijing     |
| nb     | nb@tedu.cn  |
| nb2    | nb2@tedu.cn |
| nb3    | nb3@tedu.cn |
| yaya   | beijing     |
| plj    | shanghai    |
| jing   | beijing     |
| nb     | nb@tedu.cn  |
| nb2    | nb2@tedu.cn |
| nb3    | nb3@tedu.cn |
| yaya   | NULL        |
| plj    | NULL        |
| jing   | NULL        |
| yaya   | NULL        |
| plj    | NULL        |
| jing   | NULL        |
| panglj | NULL        |
| plj    | NULL        |
| plj    | NULL        |
+--------+-------------+
21 rows in set (0.00 sec)
只修改与条件匹配的表头值  把邮箱地址是空的都修改成stu@163.com 
mysql> update DB1.stuinfo set email="stu@163.com" where email is null;
Query OK, 15 rows affected (0.05 sec)
Rows matched: 15  Changed: 15  Warnings: 0
mysql>
不加条件批量修改
mysql> update DB1.stuinfo set homedir="beijing";
Query OK, 17 rows affected (0.04 sec)
Rows matched: 21  Changed: 17  Warnings: 0
mysql> 
```
3）删除表记录
```sql
mysql> delete from DB1.stuinfo where number is null; 只删除number字段没有数据的记录
Query OK, 7 rows affected (0.04 sec)
mysql> 
清空表记录
mysql> TRUNCATE TABLE DB1.stuinfo;
Query OK, 0 rows affected (0.14 sec)
mysql> select  * from DB1.stuinfo;
Empty set (0.00 sec)
mysql> 
或
mysql> delete from  DB1.stuinfo;
Query OK, 0 rows affected (0.00 sec)
mysql> 
```
# 2. 数据类型
## 2.1 问题
按要求建表：如图-1 和 图-2

![在这里插入图片描述](https://img-blog.csdnimg.cn/fb4e547afe3b4e2192f4b406b9d10d6d.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-1

![在这里插入图片描述](https://img-blog.csdnimg.cn/af6b0f19c20b4cac946f0680e6367e40.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-2

## 2.2 步骤
在host50主机做如下练习
**步骤一：创建图-1表**
```sql
[root@host50 ~]# mysql -uroot -pNSD123...a 管理员登录
Mysql> 
mysql> create database db1;  创建db1库
Query OK, 1 row affected (0.00 sec)
mysql> create table db1.t1(  创建t4表
    -> name  char(4),
    -> your_start  year,
    -> up_time time,
    -> birthday date,
    -> party datetime
    -> );
Query OK, 0 rows affected (0.25 sec)
mysql> desc db1.t1; 查看表结构
+------------+----------+------+-----+---------+-------+
| Field      | Type     | Null | Key | Default | Extra |
+------------+----------+------+-----+---------+-------+
| name       | char(4)  | YES  |     | NULL    |       |
| your_start | year(4)  | YES  |     | NULL    |       |
| up_time    | time     | YES  |     | NULL    |       |
| birthday   | date     | YES  |     | NULL    |       |
| party      | datetime | YES  |     | NULL    |       |
+------------+----------+------+-----+---------+-------+
5 rows in set (0.00 sec)
mysql> 
```
步骤二：创建图-2表
```sql
mysql> create table db1.t2 (   建表
    -> stu_num  int  ,
    -> name  char(5),
    -> age tinyint unsigned,
    -> pay float ,
    -> money float(5,2)
    -> );
Query OK, 0 rows affected (0.28 sec)
mysql> desc db1.t2; 查看表结构
+---------+---------------------+------+-----+---------+-------+
| Field   | Type                | Null | Key | Default | Extra |
+---------+---------------------+------+-----+---------+-------+
| stu_num | int(11)             | YES  |     | NULL    |       |
| name    | char(5)             | YES  |     | NULL    |       |
| age     | tinyint(3) unsigned | YES  |     | NULL    |       |
| pay     | float               | YES  |     | NULL    |       |
| money   | float(5,2)          | YES  |     | NULL    |       |
+---------+---------------------+------+-----+---------+-------+
5 rows in set (0.00 sec)
mysql> 
```
# 3. 数据批量处理
## 3.1 问题
- 修改检索目录为/myload
- 将/etc/passwd文件导入db1库的t3表里
- 将db1库t3表所有记录导出, 存到/myload/user.txt 文件里。

**步骤一：修改检索目录为/myload**

1. 修改配置文件，重启服务
```sql
]# vim  /etc/my.cnf
        [mysqld]
        secure_file_priv="/myload”
:wq
]# mkdir  /myload  
]# chown  mysql  /myload 
]#  setenforce 0   禁用selinux
]# systemctl  restart mysqld
]# ]# mysql -uroot -pNSD123...a  管理员登录
mysql> show  variables  like  “secure_file_priv”;  //查看
 +------------------+-----------------------+
| Variable_name    | Value                          |
+------------------+-----------------------+
| secure_file_priv   | /myload/   |
+------------------+-----------------------+     
Mysql>           
```
2. 创建存储数据的库和表
```sq
mysql> CREATE DATABASE  if not exists db1; 建库
create table db1.t3(    
        name char(50),
        password  char(1),      
        uid int,
        gid int,
        comment  char(150),     
        homedir char(50),       
        shell   char(50)        
);  建表
Query OK, 0 rows affected (0.70 sec)
Mysql>
```
**步骤二：将/etc/passwd文件导入db1库的t3表里**

1）拷贝文件到检索目录下
```sql
]# cp  /etc/passwd   /myload/
```
2）导入数据
```sql
]#  mysql –uroot –ptarena
mysql> load data infile "/myload/passwd" into table db1.t3
       fields terminated by ":" lines terminated by "\n" ;   导入数据
mysql> select  * from  db1.t3;  //查看表记录
```
**步骤三：将db1库t3表所有记录导出, 存到/myload/user.txt 文件里。**

1）查询要导出的数据
```sql
mysql> select  * from  db1.t3 ；            
```
2）导出数据
```sql
mysql> select  * from  db1.t3  into outfile "/myload/user.txt";
```
3）查看文件内容
```shell
cat  /myload/user.txt  
```

# Exercise
## 1 简述索引的优点与缺点？
- 索引的优点：加快查询表记录的速度。
- 索引的缺点：会减慢写的速度(如： insert 、update )，占用物理存储空间。

## 2 简述普通索引与主键的约束规则。
1. index普通索引
- 一个表中可以有多个INDEX字段
- 字段的值允许有重复，且可以赋NULL值
- 经常把做查询条件的字段设置为INDEX字段
- INDEX字段的KEY标志是MUL

2. primary key 主键
- 一个表中只能有一个primary key字段
- 对应的字段值不允许有重复，且不允许赋NULL值
- 如果有多个字段都作为PRIMARY KEY，称为复合主键，必须一起创建。
- 主键字段的KEY标志是PRI 、通常与 AUTO_INCREMENT 连用
- 经常把表中能够唯一标识记录的字段设置为主键字段[如：记录编号字段]

## 3 根据图-1显示，修改studentdb.stu_info表的结构,原表结构见DAY01练习的图-1。

> ![在这里插入图片描述](https://img-blog.csdnimg.cn/b7ec14a2293f43e486bd78faf2c9c9aa.png)
图-1

```sql
mysql> alter table studentdb.stuinfo  add  id int(2) zerofill  primary key auto_increment first;
mysql> create unique index stu_id on studentdb.stuinfo(stu_id);
mysql> alter table studentdb.stuinfo add mail varchar(50) default "student@tedu.cn" after name;
mysql> alter table studentdb.stuinfo add tel char(11) not null ,add qq varchar(11);
mysql> alter table studentdb.stuinfo add pay float(7,2) not null default 18800 after sex;
mysql> create index name on studentdb.stuinfo(name);
```
## 4 简述在表中创建外键字段要满足那些条件？
foreign key 外键使用规则如下：
表的存储引擎必须是innodb
字段的数据类型要匹配
被参考的字段必须是key 中的一种 (通常使用primary key)

> 如有侵权，请联系作者删除
