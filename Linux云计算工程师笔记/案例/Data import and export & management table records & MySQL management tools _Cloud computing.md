@[TOC]( Data import and export & management table records & matching conditions & MySQL management tools | Cloud computing )

---
# 1. 字段约束
## 1.1 问题
- 练习基本约束的使用
- 练习主键的使用
- 练习复合主键的使用
- 练习外键的使用

具体要求如下：
如图-1所示设置约束条件

## 1.2 步骤
**步骤一：练习基本约束的使用**

1. 创建如图-1所示的约束条件

![在这里插入图片描述](https://img-blog.csdnimg.cn/d588514fdabc4ee5a5a80e40d9441b1c.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图－1
```sql
]# mysql  -uroot   -pNSD123...a   //管理员登录
Mysql>
mysql> create database if not exists db2; //建库
Query OK, 1 row affected, 1 warning (0.00 sec)
mysql> create table  db2.t2 (      
class   char(9),      
name    char(10) not null  ,     
age     tinyint  not null default  19 ,     
likes   set("a","b","c","d")  default  "a,b" 
);
mysql> desc db2.t2; //查看表结构
+-------+----------------------+------+-----+---------+-------+
| Field | Type                 | Null | Key | Default | Extra |
+-------+----------------------+------+-----+---------+-------+
| class | char(9)              | YES  |     | NULL    |       |
| name  | char(10)             | NO   |     | NULL    |       |
| age   | tinyint(4)           | NO   |     | 19      |       |
| likes | set('a','b','c','d') | YES  |     | a,b     |       |
+-------+----------------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
mysql>
mysql> insert into  t2  values (null,"bob",29,"c,d"); //插入符合约束的记录
Query OK, 1 row affected (0.05 sec)
mysql> insert into  t2(class,name) values ("nsd1902","tom");//测试默认值
Query OK, 1 row affected (0.05 sec)
mysql> insert into  t2  values (null,null,null,null);
ERROR 1048 (23000): Column 'name' cannot be null  //不允许赋null值
MariaDB [db2]>
mysql> select  * from db2.t1;  //查看记录
+---------+------+-----+-------+
| class   | name | age | likes |
+---------+------+-----+-------+
| NULL    | bob  |  29 | c,d   |
| nsd1902 | tom  |  19 | a,b   |
+---------+------+-----+-------+
2 rows in set (0.00 sec)
mysql>
```
**步骤二：练习主键的使用**
字段设置了主键标签后，字段的值必须唯一且不允许赋null值
1. 建表时，创建主键
```sql
Mysql> create  database if not  exists db2;
mysql> CREATE TABLE db2.biao01(
    -> id int(4) PRIMARY KEY,                      //在字段后加primary key 命令
    -> name varchar(8)
    -> );
Query OK, 0 rows affected (0.19 sec)
mysql> DESC db2.biao01; //查看表结构 字段有PRI标记
+-------+------------+------+-----+---------+-------+
| Field | Type       | Null | Key | Default | Extra |
+-------+------------+------+-----+---------+-------+
| id    | int(4)     | NO   | PRI | NULL    |       |
| name  | varchar(8) | YES  |     | NULL    |       |
+-------+------------+------+-----+---------+-------+
2 rows in set (0.00 sec)
```
或者：
```sql
mysql> CREATE TABLE db2.biao02(
    -> id int(4),
    -> name varchar(8),
    -> PRIMARY KEY(id)              //所有字段定义完，最后使用primary key()命令指定
    -> );
Query OK, 0 rows affected (0.17 sec)
```
2. 删除与添加主键
如果要移除某个表的PRIMARY KEY约束，需要通过ALTER TABLE指令修改。比如，以下操作将清除biao01表的主键索引。
```sql
mysql> DESC db2.biao01;  //删除前 字段id 有主键标记PRI
+-------+------------+------+-----+---------+-------+
| Field | Type       | Null | Key | Default | Extra |
+-------+------------+------+-----+---------+-------+
| id    | int(4)     | NO   | PRI | NULL    |       |
| name  | varchar(8) | YES  |     | NULL    |       |
+-------+------------+------+-----+---------+-------+
2 rows in set (0.00 sec)
mysql> ALTER TABLE db2.biao01 DROP PRIMARY KEY;  //删除主键
Query OK, 0 rows affected (0.49 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> DESC db2.biao01; //再次查看没有PRI标记了
+-------+------------+------+-----+---------+-------+
| Field | Type       | Null | Key | Default | Extra |
+-------+------------+------+-----+---------+-------+
| id    | int(4)     | NO   |     | NULL    |       |
| name  | varchar(8) | YES  |     | NULL    |       |
+-------+------------+------+-----+---------+-------+
2 rows in set (0.00 sec)
mysql> ALTER TABLE db2.biao01 add PRIMARY KEY(id);  //添加主键
Query OK, 0 rows affected (0.49 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> DESC db2.biao01;  //查看 字段id 有主键标记PRI
+-------+------------+------+-----+---------+-------+
| Field | Type       | Null | Key | Default | Extra |
+-------+------------+------+-----+---------+-------+
| id    | int(4)     | NO   | PRI | NULL    |       |
| name  | varchar(8) | YES  |     | NULL    |       |
+-------+------------+------+-----+---------+-------+
2 rows in set (0.00 sec)
```
3. 与auto_increment连用
字段必须整型数值类型且是主键，插入记录不给字段赋值，通过自加1的计算结果给字段赋值。
```sql
//给字段加增长属性
mysql> CREATE TABLE db2.tea6( id int primary key  AUTO_INCREMENT,  
name varchar(4) , age int(2)  );
mysql> desc db2.tea6;   //字段多的auto_increment
+-------+------------+------+-----+---------+----------------+
| Field | Type       | Null | Key | Default | Extra          |
+-------+------------+------+-----+---------+----------------+
| id    | int(11)    | NO   | PRI | NULL    | auto_increment |
| name  | varchar(4) | YES  |     | NULL    |                |
| age   | int(2)     | YES  |     | NULL    |                |
+-------+------------+------+-----+---------+----------------+
3 rows in set (0.00 sec)
mysql> 
//自加1计算结果赋值测试
mysql> insert into db2.tea6(name,age) values("nb",25),("yaya",19);
Query OK, 2 rows affected (0.02 sec)
Records: 2  Duplicates: 0  Warnings: 0
mysql> select  * from db2.tea6;
+----+------+------+
| id | name | age  |
+----+------+------+
|  1 | nb   |   25 |  第1条记录编号1
|  2 | yaya |   19 |  第2条记录编号2
+----+------+------+
2 rows in set (0.00 sec)
mysql> insert into db2.tea6(name,age) values("jim",29);  //插入第3条记录
Query OK, 1 row affected (0.03 sec)
mysql> select  * from db2.tea6;
+----+------+------+
| id | name | age  |
+----+------+------+
|  1 | nb   |   25 |
|  2 | yaya |   19 |
|  3 | jim  |   29 | //第3条记录编号为3 
+----+------+------+
3 rows in set (0.00 sec)
mysql> 
```
Auto_increment 依赖 primay key , 有自增长设置是 字段的主键 不能被删除，
要先删除自增长 ，主键才能删除。
```sql
mysql> ALTER TABLE db2.tea6 DROP PRIMARY KEY; //删除主键报错
ERROR 1075 (42000): Incorrect table definition; there can be only one auto column and it must be defined as a key
mysql> ALTER TABLE tea6 MODIFY id int(4) NOT NULL; //删除auto_increment
Query OK, 0 rows affected (0.75 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> ALTER TABLE db2.tea6 DROP PRIMARY KEY;                  //删除主键
Query OK, 0 rows affected (0.39 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> desc db2.tea6;                                         //确认清除结果
+-------+------------+------+-----+---------+-------+
| Field | Type       | Null | Key | Default | Extra |
+-------+------------+------+-----+---------+-------+
| id    | int(4)     | NO   |     | NULL    |       |
| name  | varchar(4) | NO   |     | NULL    |       |
| age   | int(2)     | NO   |     | NULL    |       |
+-------+------------+------+-----+---------+-------+
3 rows in set (0.01 sec)
```
**步骤三：练习复合主键的使用**

1. 创建复合主键
复合主键：表中的多个字段一起做主键，复合主键字段的值不允许同时相同
```sql
//把字段cip和port 一起设置为主键
mysql> create table db2.t5(
cip  char(15) ,  //客户端地址
port smallint , //服务端口号
status enum("deny","allow") , //对服务的访问状态
primary key(cip,port)  //指定主键字段
);
Query OK, 0 rows affected (0.19 sec)
mysql> desc db2.t5;// 2个字段都有主键的PRI标记
+--------+----------------------+------+-----+---------+-------+
| Field  | Type                 | Null | Key | Default | Extra |
+--------+----------------------+------+-----+---------+-------+
| cip    | char(15)             | NO   | PRI | NULL    |       |
| port   | smallint(6)          | NO   | PRI | NULL    |       |
| status | enum('deny','allow') | YES  |     | NULL    |       |
+--------+----------------------+------+-----+---------+-------+
3 rows in set (0.00 sec)
```
2. 验证复合主键
```sql
//插入记录
mysql>insert into db2.t5 
values ("1.1.1.1",22,"allow"),("1.1.1.1",80,"deny"),("2.1.1.1",80,"allow");
Query OK, 3 rows affected (0.03 sec)
Records: 3  Duplicates: 0  Warnings: 0
mysql> select * from db2.t5;
+---------+------+--------+
| cip     | port | status |
+---------+------+--------+
| 1.1.1.1 |   22 | allow  | 
| 1.1.1.1 |   80 | deny   | //与第1条地址重复 但端口没有重复
| 2.1.1.1 |   80 | allow  | //与第2条端口重复 但地址没有重复
+---------+------+--------+
3 rows in set (0.01 sec)
//主键字段值同时重复报错
mysql> insert into db2.t5 values ("2.1.1.1",80,"deny");
ERROR 1062 (23000): Duplicate entry '2.1.1.1-80' for key 'PRIMARY'
```
**步骤四：练习外键的使用**

1. 创建参考表员工表（yg表)
```sql
mysql> CREATE TABLE db2.yg(
    -> yg_id int primary key AUTO_INCREMENT,   //员工编号（ 自增长）
    -> name char(16)  //员工姓名
    -> )engine=innodb;
Query OK, 0 rows affected (0.15 sec)
Mysql>
//查看表结构
mysql> desc db2.yg;
+-------+----------+------+-----+---------+----------------+
| Field | Type     | Null | Key | Default | Extra          |
+-------+----------+------+-----+---------+----------------+
| yg_id | int(11)  | NO   | PRI | NULL    | auto_increment |
| name  | char(16) | YES  |     | NULL    |                |
+-------+----------+------+-----+---------+----------------+
2 rows in set (0.00 sec)
mysql> 
```
2. 创建gz表，用来记录员工的工资信息

其中gz_id需要参考员工工号，即gz表的gz_id字段设为外键，将yg表的yg_id字段作为参考键：
```sql
mysql> CREATE TABLE db2.gz(
    -> gz_id  int,
    -> gz float(7,2),
    -> FOREIGN KEY(gz_id) REFERENCES yg(yg_id)  //创建外键
    -> ON UPDATE CASCADE ON DELETE CASCADE      //同步更新、同步删除
    -> )engine=innodb;
Query OK, 0 rows affected (0.23 sec)
Mysql>
mysql> show create table db2.gz \G     //查看外键 ，外键名gz_ibfk_1
*************************** 1. row ***************************
       Table: gz
Create Table: CREATE TABLE `gz` (
  `gz_id` int(11) DEFAULT NULL,
  `gz` float(7,2) DEFAULT NULL,
  KEY `gz_id` (`gz_id`),
  CONSTRAINT `gz_ibfk_1` FOREIGN KEY (`gz_id`) REFERENCES `yg` (`yg_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1
1 row in set (0.00 sec)
mysql> 
//外键删除演示  通过外键名 删除字段的外键设置
mysql> alter table db2.gz drop foreign key  gz_ibfk_1;
Query OK, 0 rows affected (0.04 sec)
Records: 0  Duplicates: 0  Warnings: 0
//查看后没有外键了
mysql> show create table db2.gz \G
*************************** 1. row ***************************
       Table: gz
Create Table: CREATE TABLE `gz` (
  `gz_id` int(11) DEFAULT NULL,
  `gz` float(7,2) DEFAULT NULL,
  KEY `gz_id` (`gz_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
1 row in set (0.00 sec)
//添加外键
mysql> alter table db2.gz add  FOREIGN KEY (gz_id) REFERENCES  yg (yg_id) ON DELETE CASCADE ON UPDATE CASCADE;
Query OK, 0 rows affected (0.62 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> 
//再次查看 
mysql> show create table db2.gz \G   
*************************** 1. row ***************************
       Table: gz
Create Table: CREATE TABLE `gz` (
  `gz_id` int(11) DEFAULT NULL,
  `gz` float(7,2) DEFAULT NULL,
  KEY `gz_id` (`gz_id`),
  CONSTRAINT `gz_ibfk_1` FOREIGN KEY (`gz_id`) REFERENCES `yg` (`yg_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1
1 row in set (0.00 sec)
mysql> 
```
3. 验证外键
```sql
//yg表插入记录 （添加2个员工）
mysql> insert into db2.yg (name ) values ("jerry"),("tom");
Query OK, 2 rows affected (0.03 sec)
Records: 2  Duplicates: 0  Warnings: 0
//查看yg表记录 ,只有编号1 和 2 的员工
mysql> select  * from db2.yg;
+-------+-------+
| yg_id | name  |
+-------+-------+
|     1 | jerry |
|     2 | tom   |
+-------+-------+
2 rows in set (0.00 sec)
mysql> 
//向工资表里插入记录,  
mysql> insert into  db2.gz values (1,20000),(2,30000);  //工号1和2 的可以正常插入
Query OK, 2 rows affected (0.04 sec)
Records: 2  Duplicates: 0  Warnings: 0
mysql> select  * from db2.gz;
+-------+----------+
| gz_id | gz       |
+-------+----------+
|     1 | 20000.00 |
|     2 | 30000.00 |
+-------+----------+
2 rows in set (0.00 sec)
mysql> 
mysql> insert into  db2.gz values (3,50000); //没有工号3的员工报错
ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails (`db2`.`gz`, CONSTRAINT `gz_ibfk_1` FOREIGN KEY (`gz_id`) REFERENCES `yg` (`yg_id`) ON DELETE CASCADE ON UPDATE CASCADE)
mysql> 
//员工表添加第3条记录
mysql> insert into db2.yg(name) values("lili");  
Query OK, 1 row affected (0.03 sec)
mysql> select  * from db2.yg;  //有编号是3的员工了
+-------+-------+
| yg_id | name  |
+-------+-------+
|     1 | jerry |
|     2 | tom   |
|     3 | lili  |
+-------+-------+
3 rows in set (0.00 sec)
mysql> insert into  db2.gz values (3,50000);  //工资表添加记录成功
Query OK, 1 row affected (0.05 sec)
mysql> select  * from db2.gz;  //查看工资表记录
+-------+----------+
| gz_id | gz       |
+-------+----------+
|     1 | 20000.00 |
|     2 | 30000.00 |
|     3 | 50000.00 |
+-------+----------+
3 rows in set (0.00 sec)
mysql> 
```
4. 验证同步更新与删除
```sql
//将yg表中Jerry用户的yg_id修改为8
mysql> update yg set yg_id=8 where name="jerry";
Query OK, 1 row affected (0.04 sec)
Rows matched: 1  Changed: 1  Warnings: 0
mysql> select  * from db2.yg;
+-------+-------+
| yg_id | name  |
+-------+-------+
|     2 | tom   |
|     3 | lili  |
|     8 | jerry |
+-------+-------+
3 rows in set (0.00 sec)
mysql> 
//同时也会发现，gz表中Jerry用户的gz_id也跟着变了：
mysql> select  * from db2.gz;
+-------+----------+
| gz_id | gz       |
+-------+----------+
|     8 | 20000.00 |
|     2 | 30000.00 |
|     3 | 50000.00 |
+-------+----------+
3 rows in set (0.00 sec)
mysql> 
//删除工号是8的员工
mysql> delete from db2.yg where yg_id = 8;
Query OK, 1 row affected (0.03 sec)
mysql> select  * from db2.yg;
+-------+------+
| yg_id | name |
+-------+------+
|     2 | tom  |
|     3 | lili |
+-------+------+
2 rows in set (0.00 sec)
mysql> 
 //工资表的编号8的记录也没有了
mysql> select  * from db2.gz;
+-------+----------+
| gz_id | gz       |
+-------+----------+
|     2 | 30000.00 |
|     3 | 50000.00 |
+-------+----------+
2 rows in set (0.00 sec)
mysql> 
```
# 2. MySQL索引
## 2.1 问题
- 练习创建索引
- 练习查看索引
- 练习删除索引
- 练习添加索引

## 2.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：练习创建索引**

创建表的时候指定INDEX索引字段
```sql
mysql> create database if not exists  home; //创建库home
Query OK, 1 row affected (0.00 sec)
```
允许有多个INDEX索引字段。比如，以下操作在home库中创建了tea4表，将其中的id、name作为索引字段：
```sql
mysql> USE home;
Database changed
mysql> CREATE TABLE tea4(
    -> id char(6) NOT NULL,
    -> name varchar(6) NOT NULL,
    -> age int(3) NOT NULL,
    -> gender ENUM('boy','girl') DEFAULT 'boy',
    -> INDEX(id),INDEX(name)
    -> );
Query OK, 0 rows affected (0.59 sec)
```
**步骤二：查看索引**

查看新建tea4表的字段结构，可以发现两个非空索引字段的KEY标志为MUL：
```sql
mysql> DESC tea4;
+--------+--------------------+------+-----+---------+-------+
| Field  | Type               | Null | Key | Default | Extra |
+--------+--------------------+------+-----+---------+-------+
| id     | char(6)            | NO   | MUL | NULL    |       |
| name   | varchar(6)         | NO   | MUL | NULL    |       |
| age    | int(3)             | NO   |     | NULL    |       |
| gender | enum('boy','girl') | YES  |     | boy     |       |
+--------+--------------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
//查看详细信息
mysql> SHOW INDEX FROM tea4\G
*************************** 1. row ***************************
        Table: tea4
   Non_unique: 1
     Key_name: id
 Seq_in_index: 1
  Column_name: id
    Collation: A
  Cardinality: 0
     Sub_part: NULL
       Packed: NULL
         Null: 
   Index_type: BTREE                          //使用B树算法
      Comment: 
Index_comment: 
*************************** 2. row ***************************
        Table: tea4
   Non_unique: 1
     Key_name: nianling                       //索引名称
 Seq_in_index: 1
  Column_name: age                            //字段名称
    Collation: A
  Cardinality: 0
     Sub_part: NULL
       Packed: NULL
         Null: 
   Index_type: BTREE
      Comment: 
Index_comment: 
Mysql>
```
**步骤三：删除索引**

比如，删除tea4表中名称为named的INDEX索引字段：
```sql
mysql> drop INDEX name ON tea4;                  //删除name字段的索引
Query OK, 0 rows affected (0.18 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> DESC tea4;                                      //确认删除结果
+--------+--------------------+------+-----+---------+-------+
| Field  | Type               | Null | Key | Default | Extra |
+--------+--------------------+------+-----+---------+-------+
| id     | char(6)            | NO   | MUL | NULL    |       |
| name   | varchar(6)         | NO   |     | NULL    |       |
| age    | int(3)             | NO   |     | NULL    |       |
| gender | enum('boy','girl') | YES  |     | boy     |       |
+--------+--------------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
```
**步骤四：添加索引**

比如，针对tea4表的age字段建立索引，名称为 nianling：
```sql
mysql> CREATE INDEX nianling ON tea4(age);      //针对指定字段创建索引
Query OK, 0 rows affected (0.62 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql> DESC tea4;                                  //确认创建结果
+--------+--------------------+------+-----+---------+-------+
| Field  | Type               | Null | Key | Default | Extra |
+--------+--------------------+------+-----+---------+-------+
| id     | char(6)            | NO   | MUL | NULL    |       |
| name   | varchar(6)         | NO   |     | NULL    |       |
| age    | int(3)             | NO   | MUL | NULL    |       |
| gender | enum('boy','girl') | YES  |     | boy     |       |
+--------+--------------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
Mysql>
```
# 3. 用户授权
## 3.1 问题
1. 添加用户dba007，对所有库和所有表有完全权限、且有授权权限，密码为123qqq…A 客户端为网络中的所有主机。
2. 撤销root从本机访问权限，然后恢复。
3. 允许192.168.4.0/24网段主机使用root连接数据库服务器，对所有库和所有表有完全权限、密码为123qqq…A 。
4. 允许任意主机使用webuser用户连接数据库服务器，仅对tarena库有查询,插入,更新,删除记录的权限，密码为123qqq…A
5. 撤销webuser用户的权限，使其仅有查询记录权限。
6. 删除dba007用户

## 3.2 步骤
实现此案例需要按照如下步骤进行。在数据库服务器192.168.4.50主机做用户授权，在能与192.168.4.50主机能ping同的其他主机测试50主机的用户授权，在测试主机执行 which mysql || yum -y install mysql-community-client 提供连接命令mysql

**步骤一：用户授权**
1. 添加用户dba007，对所有库和所有表有完全权限、且有授权权限，密码为123qqq…A 客户端为网络中的所有主机。
```sql
// 50主机管理员root登录
[root@host50 ~]# mysql -uroot -pNSD123...a
//加用户dba007，对所有库和所有表有完全权限、且有授权权限，密码为123qqq…A  客户端为网络中的所有主机。
mysql> grant all on *.* to dba007@"%" identified by "123qqq...A" with grant option;
Query OK, 0 rows affected, 1 warning (0.00 sec)
//查看授权用户dba007的权限 （通过编号2的练习 测试 dba007用户的权限）
mysql> show grants for  dba007@"%";
+---------------------------------------------------------------+
| Grants for dba007@%                                           |
+---------------------------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'dba007'@'%' WITH GRANT OPTION |
+---------------------------------------------------------------+
1 row in set (0.00 sec)
mysql> 
```
2. 撤销root从本机访问的权限，然后恢复
```shell
//在任何客户端使用dba007用户 连接50主机
[root@host51 ~]# mysql -h192.168.4.50 -udba007 -p123qqq...A
Mysql>
//查看可以使用root用来连接的客户端地址
mysql> select host,user from mysql.user where user="root";
+-------------+------+
| host        | user |
+-------------+------+
| 192.168.4.% | root | //192.168.4.0/24 网段所有主机
| localhost   | root |  //本机登录
+-------------+------+
2 rows in set (0.00 sec)
mysql> 
//查看root用户本机登录的访问权限
mysql> show grants for root@"localhost";
+---------------------------------------------------------------------+
| Grants for root@localhost                                           |
+---------------------------------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION |
| GRANT PROXY ON ''@'' TO 'root'@'localhost' WITH GRANT OPTION        |  //可以把自己的权限复制给其他用户
+---------------------------------------------------------------------+
2 rows in set (0.00 sec)
mysql> 
//撤销授权权限
mysql> revoke grant option on  *.* from  root@"localhost";
Query OK, 0 rows affected (0.00 sec)
//撤销对库的权限
mysql> revoke all on  *.* from  root@"localhost";
Query OK, 0 rows affected (0.00 sec)
//查看权限
mysql> show grants for root@"localhost";
+--------------------------------------------------------------+
| Grants for root@localhost                                    |
+--------------------------------------------------------------+
| GRANT USAGE ON *.* TO 'root'@'localhost'                     |无权限
| GRANT PROXY ON ''@'' TO 'root'@'localhost' WITH GRANT OPTION |
+--------------------------------------------------------------+
2 rows in set (0.00 sec)
//测试权限撤销： 在50主机使用root用户登录
[root@host50 ~]# mysql -hlocalhost -uroot -pNSD123...a
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 38
Server version: 5.7.17 MySQL Community Server (GPL)
Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql>   //可以登录
//查看登录用户信息
mysql> select user();
+----------------+
| user()         |
+----------------+
| root@localhost |
+----------------+
1 row in set (0.00 sec)
mysql> 
//查看访问权限
mysql> show grants;
+--------------------------------------------------------------+
| Grants for root@localhost                                    |
+--------------------------------------------------------------+
| GRANT USAGE ON *.* TO 'root'@'localhost'                     |
| GRANT PROXY ON ''@'' TO 'root'@'localhost' WITH GRANT OPTION |
+--------------------------------------------------------------+
2 rows in set (0.00 sec)
mysql> 
//测试权限
mysql> show databases;  //只能看到虚拟库
+--------------------+
| Database           |
+--------------------+
| information_schema |
+--------------------+
1 row in set (0.00 sec)
mysql> create database gamedb;  //创建新库 被拒绝
ERROR 1044 (42000): Access denied for user 'root'@'localhost' to database 'gamedb'
mysql> select  * from tarena.user; //查看表记录被拒绝
ERROR 1142 (42000): SELECT command denied to user 'root'@'localhost' for table 'user'
mysql> 
    Mysql> exit; //断开连接
```
在网络中的任意主机使用dba007连接50主机，恢复root本地登录权限
```shell
[root@dbsvr1 ~]# mysql -h192.168.4.50 -udba007 -p123qqq...A //dba007用户登录
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 24
Server version: 5.7.17 MySQL Community Server (GPL)
Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql>
//设置root用户本机登录的权限 
mysql> grant all on  *.* to root@"localhost" identified by "NSD123...a" with grant option;
Query OK, 0 rows affected, 1 warning (0.00 sec)
mysql> SHOW GRANTS FOR root@localhost;              //查看权限
+---------------------------------------------------------------------+
| Grants for root@localhost                                           |
+---------------------------------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION | //有了
| GRANT PROXY ON ''@'' TO 'root'@'localhost' WITH GRANT OPTION        |
+---------------------------------------------------------------------+
2 rows in set (0.00 sec)
mysql> exit                                      //退出当前MySQL连接
Bye
//在50本机使用root用户登录
[root@dbsvr1 ~]# mysql -u root -p                 //重新以root登入
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 25
Server version: 5.7.17 MySQL Community Server (GPL)
Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql> CREATE DATABASE newdb2014;                  //成功创建新库
Query OK, 1 row affected (0.00 sec)
```
3. 允许root从192.168.4.0/24访问，对所有库表有完全权限，密码为123qqq…A
```sql
//在50本机使用root用户登录
[root@host50 ~]# mysql -hlocalhost -uroot -pNSD123...a
Mysql>
//用户授权：允许root从192.168.4.0/24访问，对所有库表有完全权限，密码为123qqq…A
mysql> GRANT all ON *.* TO root@'192.168.4.%' IDENTIFIED BY  "123qqq...A";
Query OK, 0 rows affected, 1 warning (0.00 sec)
mysql> 
//再次从192.168.4.0/24网段的客户机访问
[root@host51 ~]# mysql -h192.168.4.50 -uroot -p123qqq...A
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 32
Server version: 5.7.17 MySQL Community Server (GPL)
Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql> 
mysql> select user();  //查看登录用户信息
+-------------------+
| user()            |
+-------------------+
| root@192.168.4.51 | 
+-------------------+
1 row in set (0.00 sec)
mysql> 
mysql> show grants;  查看访问权限
+-----------------------------------------------------+
| Grants for root@192.168.4.%                         |
+-----------------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'root'@'192.168.4.%' |
+-----------------------------------------------------+
1 row in set (0.00 sec)
mysql> 
//测试权限 （建库、表 ，记录的增删改查 ，库表的删除 ）
mysql> CREATE DATABASE rootdb;                  //创建新库rootdb
Query OK, 1 row affected (0.06 sec)
mysql> SHOW DATABASES; //查看已有库
+--------------------+
| Database           |
+--------------------+
| information_schema |
| home               |
| mysql              |
| performance_schema |
| rootdb             |   //新建的rootdb库
| sys                |
| userdb             |
+--------------------+
7 rows in set (0.01 sec)
```
4. 允许任意主机使用webuser用户连接数据库服务器，仅对tarena库有查询,插入,更新,删除记录的权限，密码为123qqq…A
```sql
//数据库管理员本机登录
[root@host50 ~]# mysql -hlocalhost -uroot -pNSD123...a
mysql> grant select,insert,update,delete on tarena.* to webuser@"%" identified by "123qqq...A";
Query OK, 0 rows affected, 1 warning (0.00 sec)
mysql> show grants for webuser@"%";  //查看webuser用户权限 ，对所有库表没有任何软件仅对tarena库有权限
+---------------------------------------------------------------------+
| Grants for webuser@%                                                |
+---------------------------------------------------------------------+
| GRANT USAGE ON *.* TO 'webuser'@'%'                                 |
| GRANT SELECT, INSERT, UPDATE, DELETE ON `tarena`.* TO 'webuser'@'%' |
+---------------------------------------------------------------------+
2 rows in set (0.00 sec)
mysql> 
//测试授权：在任何主机使用webuser用户连接50主机
[root@host51 ~]# mysql -h192.168.4.50 -uwebuser -p123qqq...A  
mysql> select user(); //查看用户信息
+----------------------+
| user()               |
+----------------------+
| webuser@192.168.4.51 |
+----------------------+
1 row in set (0.00 sec)
mysql> show grants;  //查看权限
+---------------------------------------------------------------------+
| Grants for webuser@%                                                |
+---------------------------------------------------------------------+
| GRANT USAGE ON *.* TO 'webuser'@'%'                                 |
| GRANT SELECT, INSERT, UPDATE, DELETE ON `tarena`.* TO 'webuser'@'%' |
+---------------------------------------------------------------------+
2 rows in set (0.00 sec)
mysql>
//执行除select  insert  update  delete 之外的权限被拒绝
mysql> drop table tarena.user;
ERROR 1142 (42000): DROP command denied to user 'webuser'@'192.168.4.51' for table 'user'
mysql> 
Mysql>exit  //断开连接
```
5. 撤销webuser用户权限，使其仅有查询记录权限。
```sql
//在50主机管理员登录
[root@host50 ~]# mysql -hlocalhost -uroot -pNSD123...a
mysql>
//撤销 webuser用户权限，使其仅有查询记录权限。
mysql> revoke insert,update,delete on tarena.* from webuser@"%";
Query OK, 0 rows affected (0.00 sec)
//查看webuser用户权限
mysql> show grants for webuser@"%";
+---------------------------------------------+
| Grants for webuser@%                           |
+---------------------------------------------+
| GRANT USAGE ON *.* TO 'webuser'@'%'          |
| GRANT SELECT ON `tarena`.* TO 'webuser'@'%' | //只剩select权限了
+---------------------------------------------+
2 rows in set (0.00 sec)
```
6. 删除dba007用户
```sql
// 在50主机管理员登录
[root@host50 ~]# mysql -hlocalhost -uroot -pNSD123...a
Mysql>
//查看已有的授权用户 是否有dba007用户
mysql> select user , host from mysql.user where user="dba007";
+--------+------+
| user   | host |
+--------+------+
| dba007 | %    |
+--------+------+
1 row in set (0.00 sec)
//删除dba007用户
mysql> drop user dba007@"%";
Query OK, 0 rows affected (0.00 sec)
//再次查看没有dba007用户了
mysql> select user , host from mysql.user where user="dba007";
Empty set (0.00 sec)
Mysql>
//在客户端使用dba007用户连接50主机 被拒绝
[root@host51 ~]# mysql -h192.168.4.50 -udba007 -p123qqq...A
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 1045 (28000): Access denied for user 'dba007'@'192.168.4.51' (using password: YES)
[root@host51 ~]# 
```


# Exercise
## 1 简述MySQL数据库中插入、更新、查询、删除表记录的指令格式。
1. 插入记录指令格式
```sql
insert  into   库.表   values(值列表);   //一次插入一条记录 给记录的所有字段赋值
insert  into   库.表   values(值列表),(值列表);  
//一次插入多条记录 给记录的所有字段赋值
insert  into   库.表(字段名列表)   values(值列表); 
//一次插入1条记录 给记录的指定字段赋值
insert  into   库.表(字段名列表)   values(值列表)，(值列表); 
//一次插入多条记录 给记录的指定字段赋值
```
2. 更新记录指令格式
```sql
update  表名  set   字段名=值，字段名="值";         //批量修改
update  表名  set   字段名=值，字段名="值" where  条件; 
//修改符合条件的记录字段的值
```
3. 查询记录指令格式:
```sql
select  字段列表   from  表名; 
//查询所有记录指定字段的值。
select  字段列表   from  表名  where  条件表达式列表；
//查询与条件匹配记录指定字段的值。
```
4. 删除表记录指令格式：
```sql
delete  from  表名；         //删除表的所有记录。
delete  from  表名  where  条件；     //只删除符合条件的记录
```
## 2 查询综合练习题，按要求写出对应查询语句。
> 1. 添加记录编号字段id 在所有字段上方，字段值可以自动增长。
> 2. 显示uid 是四位数的用户的用户名和uid号。
> 3. 显示名字是以字母r 开头 且是以字母d结尾的用户名和uid号。
> 4. 查看gid 小于10的用户使用shell的种类。
> 5. 查看shell不是/bin/bash用户中uid号最大用户名及uid号。
> 6. 统计uid是3位数的用户的个数。

1. 添加记录编号字段id 在所有字段上方，字段值可以自动增长。
```sql
alter  table  userdb.userlist  add  id  int(2) primary key  auto_increment  first;
```
2. 显示uid 是四位数的用户的用户名和uid号。
```sql
select  name,uid  from userdb.userlist where uid >=1000 and uid<=9999; 或 select  name,uid  from userdb.userlist where uid  between  1000  and  9999; 或  select  name,uid  from userdb.userlist where uid regexp ‘^....$’;
```
3. 显示名字是以字母r 开头 且是以字母d结尾的用户名和uid号。
```sql
select name,uid  from userdb.userlist where  name regexp ‘^r.*d$’;
或
select user from mysql.user where user regexp '^r' and user regexp 'd$';
```
4. 查看gid 小于10的用户使用shell的种类。
```sql
select shell from userdb.userlist where uid<10 group by shell;
或
Select distinct shell from userdb.userlist where uid<10； 
```
5. 查看shell不是/bin/bash用户中uid号最大用户名及uid号。
```sql
select name,uid  from userdb.userlist where shell!=”/bin/bash” order by uid desc limit 1;
```
6. 统计uid是3位数的用户的个数。
```sql
select count(name) from userdb.userlist where uid >=100 and uid<=999;
```

> 如有侵权，请联系作者删除
