@[TOC]( Incremental recovery & data query expansion | Cloud computing )

---
# 1. MySQL视图
## 1.1 问题
具体如下：
1. 视图基本使用练习
2. 视图进阶练习

## 1.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：视图基本使用练习**
```sql
// 创建包含员工名、email和部门名的视图
mysql> use tarena;
mysql> create view emp_view
    -> as
    ->   select name, email, dept_name
    ->   from employees as e
    ->   inner join departments as d
    ->   on e.dept_id=d.dept_id;
Query OK, 0 rows affected (0.01 sec)
// 查询视图中数据
mysql> select * from emp_view;
mysql> select * from emp_view where dept_name='运维部';
+-----------+--------------------+-----------+
| name      | email              | dept_name |
+-----------+--------------------+-----------+
| 廖娜      | liaona@tarena.com  | 运维部    |
| 窦红梅    | douhongmei@tedu.cn | 运维部    |
| 聂想      | niexiang@tedu.cn   | 运维部    |
| 陈阳      | chenyang@tedu.cn   | 运维部    |
| 戴璐      | dailu@tedu.cn      | 运维部    |
| 陈斌      | chenbin@tarena.com | 运维部    |
+-----------+--------------------+-----------+
6 rows in set (0.00 sec)
//创建包含员工名、工资总额的视图
mysql> create view emp_sal_view
    -> as
    ->   select name, date, basic+bonus as total
    ->   from employees as e
    ->   inner join salary as s
    ->   on e.employee_id=s.employee_id;
Query OK, 0 rows affected (0.00 sec)
mysql> select * from emp_sal_view where year(date)=2020 and month(date)=12;
   //创建包涵用户名、uid号、shell的视图
   mysql> create view  tarena.v1  as select name , uid ,shell  from  tarena.user;
Query OK, 0 rows affected (0.02 sec)
//查看条目数
mysql> select count(*) from tarena.v1;
+----------+
| count(*) |
+----------+
|       23 |
+----------+
1 row in set (0.00 sec)
//查看视图表结构
mysql> desc tarena.v1;
+-------+----------+------+-----+---------+-------+
| Field | Type     | Null | Key | Default | Extra |
+-------+----------+------+-----+---------+-------+
| name  | char(20) | YES  |     | NULL    |       |
| uid   | int(11)  | YES  |     | NULL    |       |
| shell | char(30) | YES  |     | NULL    |       |
+-------+----------+------+-----+---------+-------+
3 rows in set (0.00 sec)
mysql> 
//查看已有的表
mysql> show tables;
+------------------+
| Tables_in_tarena |
+------------------+
| departments      |
| emp_sal_view     | 视图表
| emp_view         |视图表
| employees        |
| salary           |
| user             |
| v1               |视图表
+------------------+
7 rows in set (0.00 sec)
mysql> 
//查看所有表的状态(7张表 7行状态信息)
 mysql> show table status \G
*************************** 1. row ***************************
           Name: departments   #表名
         Engine: InnoDB
        Version: 10
     Row_format: Dynamic
           Rows: 8
 Avg_row_length: 2048
    Data_length: 16384
Max_data_length: 0
   Index_length: 0
      Data_free: 0
 Auto_increment: 9
    Create_time: 2021-09-09 18:04:21
    Update_time: 2021-09-09 18:04:21
     Check_time: NULL
      Collation: utf8mb4_general_ci
       Checksum: NULL
 Create_options: 
        Comment:  #没有说明
*************************** 2. row ***************************
           Name: emp_sal_view
         Engine: NULL
        Version: NULL
     Row_format: NULL
           Rows: NULL
 Avg_row_length: NULL
    Data_length: NULL
Max_data_length: NULL
   Index_length: NULL
      Data_free: NULL
 Auto_increment: NULL
    Create_time: NULL
    Update_time: NULL
     Check_time: NULL
      Collation: NULL
       Checksum: NULL
 Create_options: NULL
        Comment: VIEW
*************************** 3. row ***************************
           Name: emp_view  #视图名
         Engine: NULL
        Version: NULL
     Row_format: NULL
           Rows: NULL
 Avg_row_length: NULL
    Data_length: NULL
Max_data_length: NULL
   Index_length: NULL
      Data_free: NULL
 Auto_increment: NULL
    Create_time: NULL
    Update_time: NULL
     Check_time: NULL
      Collation: NULL
       Checksum: NULL
 Create_options: NULL
        Comment: VIEW     #视图表
*************************** 4. row ***************************
           Name: employees
         Engine: InnoDB
        Version: 10
     Row_format: Dynamic
           Rows: 133
 Avg_row_length: 123
    Data_length: 16384
Max_data_length: 0
   Index_length: 16384
      Data_free: 0
 Auto_increment: 134
    Create_time: 2021-09-09 18:04:21
    Update_time: 2021-09-09 18:04:21
     Check_time: NULL
      Collation: utf8mb4_general_ci
       Checksum: NULL
 Create_options: 
        Comment: 
*************************** 5. row ***************************
           Name: salary
         Engine: InnoDB
        Version: 10
     Row_format: Dynamic
           Rows: 8066
 Avg_row_length: 44
    Data_length: 360448
Max_data_length: 0
   Index_length: 163840
      Data_free: 0
 Auto_increment: 9577
    Create_time: 2021-09-09 18:04:21
    Update_time: 2021-09-10 10:12:50
     Check_time: NULL
      Collation: utf8mb4_general_ci
       Checksum: NULL
 Create_options: 
        Comment: 
*************************** 6. row ***************************
           Name: user
         Engine: InnoDB
        Version: 10
     Row_format: Dynamic
           Rows: 23
 Avg_row_length: 712
    Data_length: 16384
Max_data_length: 0
   Index_length: 0
      Data_free: 0
 Auto_increment: 28
    Create_time: 2021-09-09 18:04:23
    Update_time: 2021-09-10 10:20:13
     Check_time: NULL
      Collation: latin1_swedish_ci
       Checksum: NULL
 Create_options: 
        Comment: 
*************************** 7. row ***************************
           Name: v1
         Engine: NULL
        Version: NULL
     Row_format: NULL
           Rows: NULL
 Avg_row_length: NULL
    Data_length: NULL
Max_data_length: NULL
   Index_length: NULL
      Data_free: NULL
 Auto_increment: NULL
    Create_time: NULL
    Update_time: NULL
     Check_time: NULL
      Collation: NULL
       Checksum: NULL
 Create_options: NULL
        Comment: VIEW
7 rows in set (0.00 sec)
mysql> 
//只查看指定表的状态  
mysql> show table status  where name="v1" \G
*************************** 1. row ***************************
           Name: v1
         Engine: NULL
        Version: NULL
     Row_format: NULL
           Rows: NULL
 Avg_row_length: NULL
    Data_length: NULL
Max_data_length: NULL
   Index_length: NULL
      Data_free: NULL
 Auto_increment: NULL
    Create_time: NULL
    Update_time: NULL
     Check_time: NULL
      Collation: NULL
       Checksum: NULL
 Create_options: NULL
        Comment: VIEW
1 row in set (0.00 sec)
mysql> 
//只查看是视图的表
mysql> show table status  where comment="view" \G
*************************** 1. row ***************************
           Name: emp_sal_view
         Engine: NULL
        Version: NULL
     Row_format: NULL
           Rows: NULL
 Avg_row_length: NULL
    Data_length: NULL
Max_data_length: NULL
   Index_length: NULL
      Data_free: NULL
 Auto_increment: NULL
    Create_time: NULL
    Update_time: NULL
     Check_time: NULL
      Collation: NULL
       Checksum: NULL
 Create_options: NULL
        Comment: VIEW
*************************** 2. row ***************************
           Name: emp_view
         Engine: NULL
        Version: NULL
     Row_format: NULL
           Rows: NULL
 Avg_row_length: NULL
    Data_length: NULL
Max_data_length: NULL
   Index_length: NULL
      Data_free: NULL
 Auto_increment: NULL
    Create_time: NULL
    Update_time: NULL
     Check_time: NULL
      Collation: NULL
       Checksum: NULL
 Create_options: NULL
        Comment: VIEW
*************************** 3. row ***************************
           Name: v1
         Engine: NULL
        Version: NULL
     Row_format: NULL
           Rows: NULL
 Avg_row_length: NULL
    Data_length: NULL
Max_data_length: NULL
   Index_length: NULL
      Data_free: NULL
 Auto_increment: NULL
    Create_time: NULL
    Update_time: NULL
     Check_time: NULL
      Collation: NULL
       Checksum: NULL
 Create_options: NULL
        Comment: VIEW
3 rows in set (0.00 sec)
mysql> 
//查看视图对应的基表
mysql> show create view v1 \G
*************************** 1. row ***************************
                View: v1
         Create View: CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v1` AS select `user`.`name` AS `name`,`user`.`uid` AS `uid`,`user`.`shell` AS `shell` from `user`
character_set_client: utf8
collation_connection: utf8_general_ci
1 row in set (0.00 sec)
mysql> 
//在视图表里查看bin用户信息
mysql> select * from v1 where name = "bin";
+------+------+---------------+
| name | uid  | shell         |
+------+------+---------------+
| bin  |    2 | /sbin/nologin |
+------+------+---------------+
1 row in set (0.00 sec)
//在基表里查bin用户信息
mysql> select * from user where name = "bin";
+----+------+----------+------+------+---------+---------+---------------+
| id | name | password | uid  | gid  | comment | homedir | shell         |
+----+------+----------+------+------+---------+---------+---------------+
|  2 | bin  | x        |    2 |    1 | bin     | /bin    | /sbin/nologin |
+----+------+----------+------+------+---------+---------+---------------+
1 row in set (0.00 sec)
mysql> 
//修改视图表bin用户的shell 
mysql> update v1 set shell=null where  name ="bin";
Query OK, 1 row affected (0.02 sec)
Rows matched: 1  Changed: 1  Warnings: 0
//user表里bin用户的 shell 也改变了 
mysql> select * from user where name = "bin";
+----+------+----------+------+------+---------+---------+-------+
| id | name | password | uid  | gid  | comment | homedir | shell |
+----+------+----------+------+------+---------+---------+-------+
|  2 | bin  | x        |    2 |    1 | bin     | /bin    | NULL  |
+----+------+----------+------+------+---------+---------+-------+
1 row in set (0.00 sec)
mysql> 
//在视图表里删除bin用户
mysql> delete from v1 where name = "bin" ;
Query OK, 1 row affected (0.03 sec)
//user表里bin用户也没有了 
mysql> select * from user where name = "bin";
Empty set (0.00 sec)
mysql> 
//在user表里添加新记录
mysql>insert 
into user(name,password,uid,gid,comment,homedir,shell)values("yaya","x",999,999,"test user","/home/yaya","/bin/bash")；
Query OK, 1 row affected (0.04 sec)
//视图表v1 也多了1条记录
mysql> select * from v1 where name = "yaya";
+------+------+-----------+
| name | uid  | shell     |
+------+------+-----------+
| yaya |  999 | /bin/bash |
+------+------+-----------+
1 row in set (0.00 sec)
mysql> 
//在视图表里添加新记录
mysql> insert into  v1  values("jing",1000,"/bin/bash");
Query OK, 1 row affected (0.09 sec)
//在user表里也能查看到
mysql> select  * from user where name = "jing";
+----+------+----------+------+------+---------+---------+-----------+
| id | name | password | uid  | gid  | comment | homedir | shell     |
+----+------+----------+------+------+---------+---------+-----------+
| 29 | jing | NULL     | 1000 | NULL | NULL    | NULL    | /bin/bash |
+----+------+----------+------+------+---------+---------+-----------+
1 row in set (0.00 sec)
mysql> 
//在user 表里删除记录
mysql> delete from user where name = "jing";
Query OK, 1 row affected (0.02 sec)
//在视图表v1里查不到了 
mysql> select  * from v1 where name = "jing";
Empty set (0.00 sec)
mysql> 
//删除视图 emp_view
mysql> drop view emp_view;  
Query OK, 0 rows affected (0.00 sec)
mysql> 
```
**步骤二：视图进阶练习**
1. OR REPLACE修改视图
```sql
mysql> use tarena ;
Database changed
   //创建视图v2
mysql> create view v2 as select name,uid from tarena.user ;
Query OK, 0 rows affected (0.02 sec)
mysql> create view v2 as select name,uid , gid , shell  from tarena.user ;
ERROR 1050 (42S01): Table 'v2' already exists  #提示v2已经存在
mysql> create OR REPLACE view v2 as select name,uid , gid, shell  from tarena.user ;
Query OK, 0 rows affected (0.03 sec)  #命令执行成功
//创建练习的user3
mysql> create table tarena.user3  
select name , uid from  tarena.user where id <= 4;
Query OK, 3 rows affected (0.23 sec)
Records: 3  Duplicates: 0  Warnings: 0
mysql> select  * from tarena.user3;
+--------+------+
| name   | uid  |
+--------+------+
| root   |    1 |
| daemon |    3 |
| adm    |    4 |
+--------+------+
3 rows in set (0.00 sec)
mysql> 
//内连接查询
mysql> select  * from user3  inner join user where user3.uid=user.uid ;
+--------+------+----+--------+----------+------+------+---------+----------+---------------+
| name   | uid  | id | name   | password | uid  | gid  | comment | homedir  | shell         |
+--------+------+----+--------+----------+------+------+---------+----------+---------------+
| root   |    1 |  1 | root   | x        |    1 |    0 | root    | /root    | /bin/bash     |
| daemon |    3 |  3 | daemon | x        |    3 |    2 | daemon  | /sbin    | /sbin/nologin |
| adm    |    4 |  4 | adm    | x        |    4 |    4 | adm     | /var/adm | /sbin/nologin |
+--------+------+----+--------+----------+------+------+---------+----------+---------------+
3 rows in set (0.01 sec)
//创建视图表v4
mysql> create view  v4 as select  * from user3  inner join user where user3.uid=user.uid ;
ERROR 1060 (42S21): Duplicate column name 'name' 报错
mysql> 
//定义字段别名
mysql> create view  v4 as 
select  user3.name as username , user3.uid as user_id , user.*  from 
user3  inner join user 
where user3.uid=user.uid ;
Query OK, 0 rows affected (0.03 sec)
mysql> select  * from v4;
+----------+---------+----+--------+----------+------+------+---------+----------+---------------+
| username | user_id | id | name   | password | uid  | gid  | comment | homedir  | shell         |
+----------+---------+----+--------+----------+------+------+---------+----------+---------------+
| root     |       1 |  1 | root   | x        |    1 |    0 | root    | /root    | /bin/bash     |
| daemon   |       3 |  3 | daemon | x        |    3 |    2 | daemon  | /sbin    | /sbin/nologin |
| adm      |       4 |  4 | adm    | x        |    4 |    4 | adm     | /var/adm | /sbin/nologin |
+----------+---------+----+--------+----------+------+------+---------+----------+---------------+
3 rows in set (0.00 sec)
mysql> 
```
3. With check option

local 仅检查当前视图的限制
cascaded 同时要满足基表的限制（默认值）
```sql
//创建视图v6 并指定检测方式
mysql> create view v6 as select  name , uid  from tarena.user 
where uid  <= 10  with check option;
Query OK, 0 rows affected (0.04 sec)
//查看默认检测方式
mysql> show create view v6  \G
*************************** 1. row ***************************
                View: v6
         Create View: CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v6` AS select `user`.`name` AS `name`,`user`.`uid` AS `uid` from `user` where (`user`.`uid` <= 10) WITH CASCADED CHECK OPTION
character_set_client: utf8
collation_connection: utf8_general_ci
1 row in set (0.00 sec)
mysql> 
mysql>
//创建视图v7 基表是 视图v6
mysql> create view v7 as select  * from v6 
where uid >= 5 with local check option;
Query OK, 0 rows affected (0.04 sec)
//查看检测方式
mysql> show create view v7  \G
*************************** 1. row ***************************
                View: v7
         Create View: CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v7` AS select `v6`.`name` AS `name`,`v6`.`uid` AS `uid` from `v6` where (`v6`.`uid` >= 5) WITH LOCAL CHECK OPTION
character_set_client: utf8
collation_connection: utf8_general_ci
1 row in set (0.00 sec)
mysql> 
//测试验证方式
mysql> update v7 set uid = 1 where name="lp"; #不满足v7自身的条件uid>=5 
ERROR 1369 (HY000): CHECK OPTION failed 'tarena.v7'
mysql> 
mysql> update v7 set uid = 12 where name="lp"; #超出基表v6条件 uid<= 10
ERROR 1369 (HY000): CHECK OPTION failed 'tarena.v7'
mysql> 
mysql> update v7 set uid = 9 where name="lp"; #uid=9 #既满足自身条件又满足基表条件
Query OK, 1 row affected (0.03 sec)
Rows matched: 1  Changed: 1  Warnings: 0
mysql> 
mysql> update v6 set uid = 20 where name = "lp"; #不满足自身的条件uid<=10
ERROR 1369 (HY000): CHECK OPTION failed 'tarena.v6'
mysql> 
mysql> update v6 set uid = 2 where name = "lp"; #满足自身的条件uid<=10
Query OK, 1 row affected (0.04 sec)
Rows matched: 1  Changed: 1  Warnings: 0
mysql> 
```
## 2. 存储过程基本管理
## 2.1 问题
具体如下：
1. 练习创建存储过程
2. 练习存储过程的查看、调用、删除

## 2.2 步骤
实现此案例需要按照如下步骤进行。
**步骤一：练习创建存储过程**

语法
```sql
DELIMITER  //
CREATE PROCEDURE 存储过程名()
BEGIN
    一组合法的sql语句;
END
DELIMITER ;
```
命令行结束符

MySQL默认以";"为分隔符，如果没有声明分割符，则编译器会把存储过程当成SQL语句进行处理，因此编译过程会报错，所以要事先用“DELIMITER //”声明当前段分隔符，让编译器把两个"//"之间的内容当做存储过程的代码，不会执行这些代码，通过“DELIMITER ;”把分隔符还原。

示例
```sql
mysql> drop database if exists mydb;
mysql> create database if not exists mydb default charset utf8mb4;
mysql> use mydb;
mysql> create table departments like tarena.departments; //复制表结构
mysql> select  * from  departments;
Empty set (0.00 sec)
mysql> desc departments;
+-----------+-------------+------+-----+---------+----------------+
| Field     | Type        | Null | Key | Default | Extra          |
+-----------+-------------+------+-----+---------+----------------+
| dept_id   | int(4)      | NO   | PRI | NULL    | auto_increment |
| dept_name | varchar(10) | YES  |     | NULL    |                |
+-----------+-------------+------+-----+---------+----------------+
2 rows in set (0.00 sec)
mysql> delimiter //
mysql> create procedure dep_pro()
    begin
      insert into departments values
      (1, '人事部'), (2, '财务部');
     end //
Query OK, 0 rows affected (0.00 sec)
mysql> delimiter ;
```
**步骤二:练习存储过程的查看、调用、删除**
```sql
//查看所有的存储过程
mysql> select  db , name  from mysql.proc where type="procedure";
+--------+-------------------------------------+
| db     | name                                |
+--------+-------------------------------------+
| mydb   | dep_pro                             |
| sys    | create_synonym_db                   |
| sys    | diagnostics                         |
| sys    | execute_prepared_stmt               |
| sys    | ps_setup_disable_background_threads |
| sys    | ps_setup_disable_consumer           |
| sys    | ps_setup_disable_instrument         |
| sys    | ps_setup_disable_thread             |
| sys    | ps_setup_enable_background_threads  |
| sys    | ps_setup_enable_consumer            |
| sys    | ps_setup_enable_instrument          |
| sys    | ps_setup_enable_thread              |
| sys    | ps_setup_reload_saved               |
| sys    | ps_setup_reset_to_default           |
| sys    | ps_setup_save                       |
| sys    | ps_setup_show_disabled              |
| sys    | ps_setup_show_disabled_consumers    |
| sys    | ps_setup_show_disabled_instruments  |
| sys    | ps_setup_show_enabled               |
| sys    | ps_setup_show_enabled_consumers     |
| sys    | ps_setup_show_enabled_instruments   |
| sys    | ps_statement_avg_latency_histogram  |
| sys    | ps_trace_statement_digest           |
| sys    | ps_trace_thread                     |
| sys    | ps_truncate_all_tables              |
| sys    | statement_performance_analyzer      |
| sys    | table_exists                        |
| tarena | say48                               |
+--------+-------------------------------------+
28 rows in set (0.00 sec)
mysql> 
//查看指定存储过程功能代码
mysql> select  db , name ,body from mysql.proc where name="dep_pro" \G
*************************** 1. row ***************************
  db: mydb    # 库名
name: dep_pro #存储过程名
body: begin
insert into departments values (1,"人事部"),(2,"财务部"); #功能代码
end
1 row in set (0.00 sec)
mysql> 
//执行存储过程
mysql> call dep_pro() ;
Query OK, 2 rows affected (0.00 sec)
//查看表记录
mysql> select * from departments ;
+---------+-----------+
| dept_id | dept_name |
+---------+-----------+
|       1 | 人事部    |
|       2 | 财务部    |
+---------+-----------+
2 rows in set (0.00 sec)
//删除存储过程
mysql> drop procedure mydb.dep_pro;
Query OK, 0 rows affected (0.00 sec)
//查看不到存储过程了
mysql> select  db , name ,body from mysql.proc where name="dep_pro" \G
Empty set (0.00 sec)
mysql> 
```
# 3. 存储过程进阶管理
## 3.1 问题
具体如下：
- 练习系统变量的查看与赋值
- 练习用户变量的查看与赋值
- 练习局部变量的使用
- 练习存储过程参数的使用

## 3.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：练习系统变量的查看与赋值**
```sql
mysql> show global variables;   # 查看所有全局变量mysql> show session variables;  # 查看所有会话变量
//查看满足条件的部分变量(不指定global的话，默认为会话变量)
mysql> show global variables like '%char%'; 
#查看某个系统变量 变量结构为@@变量名、@@global.变量名、@@session.变量名mysql> select @@tx_isolation;   # 默认为会话变量+-----------------+| @@tx_isolation  |+-----------------+| REPEATABLE-READ |+-----------------+1 row in set (0.00 sec)​mysql> select @@global.character_set_system;+-------------------------------+| @@global.character_set_system |+-------------------------------+| utf8                          |+-------------------------------+1 row in set (0.00 sec)​​mysql> select @@session.tx_isolation;+------------------------+| @@session.tx_isolation |+------------------------+| REPEATABLE-READ        |+------------------------+1 row in set (0.00 sec)
mysql> set @@global.autocommit=0;    #全局变量
Query OK, 0 rows affected (0.00 sec)
mysql> select @@global.autocommit; #全局变量
+---------------------+
| @@global.autocommit |
+---------------------+
|                   0 |
+---------------------+
1 row in set (0.00 sec)
mysql> show session variables like "%buffer%"; //查看会话变量
mysql> set session sort_buffer_size = 40000;  //修改会话变量值
```
**步骤二：练习用户变量的查看与赋值**
```sql
mysql> set @user='tom';
Query OK, 0 rows affected (0.00 sec)
mysql> select count(*) from employees into @count;
Query OK, 1 row affected (0.00 sec)
mysql> select @user;
+-------+
| @user |
+-------+
| tom   |
+-------+
1 row in set (0.00 sec)
mysql> select @count;
+--------+
| @count |
+--------+
|    133 |
+--------+
1 row in set (0.00 sec)
```
**步骤三：练习局部变量的使用**
作用域:仅在定义它的GEGIN/END中有效
定义变量
DECLARE 变量 类型
DECLARE 变量 类型 DEFAULT 值

示例代码
```sql
//创建存储过程
Mysql> use  tarena;
mysql> delimiter  //
mysql> create procedure say48()
     begin
     declare name char(10);
     declare age int default 21;
     set name = "plj";
     select  name , age;
     end
     //
mysql> delimiter  ;
//调用存储过程 ，可以输出变量的值
mysql> call say48();
+------+------+
| name | age  |
+------+------+
| plj  |   21 |
+------+------+
1 row in set (0.00 sec)
Query OK, 0 rows affected (0.00 sec)
mysql> 
//调用存储过程后，无法输出变量的值
mysql> select name ,age ;
ERROR 1054 (42S22): Unknown column 'name' in 'field list'  #报错
mysql> 
mysql> select @name ,@age ;  #没有定义
+-------+------+
| @name | @age |
+-------+------+
| NULL  | NULL |
+-------+------+
1 row in set (0.00 sec)
mysql> 
```
**步骤四：练习存储过程参数的使用**

语法：
```sql
CREATE PROCEDURE 存储过程名(参数列表)BEGIN    一组合法的sql语句;END
```
参数列表包含三部分：

参数模式
IN：需要调用者传值，与Python函数的参数作用类似
OUT：该参数可以作为输入。与Python函数的返回值类似
INOUT：既可以作为输入又可以作为输出

参数名： 存储数据的变量名
参数类型： MySQL服务支持的数据类型即可

1. 使用IN参数
```sql
mysql> use tarena;
mysql> delimiter //
mysql> create procedure empcount_pro(IN dept_no int)
    begin
       select dept_id, count(*) from employees
       where dept_id=dept_no
       group by dept_id;
    end //
Query OK, 0 rows affected (0.00 sec)
mysql> delimiter ;
#统计编号1 的部门人数个数
mysql> call empcount_pro(1); 
+---------+----------+
| dept_id | count(*) |
+---------+----------+
|       1 |        8 |
+---------+----------+
1 row in set (0.00 sec)
Query OK, 0 rows affected (0.00 sec)
#统计编号2 的部门人数个数
mysql> call empcount_pro(2);
+---------+----------+
| dept_id | count(*) |
+---------+----------+
|       2 |        5 |
+---------+----------+
1 row in set (0.00 sec)
Query OK, 0 rows affected (0.00 sec)
mysql> 
```
2. 使用OUT参数
```sql
mysql> use tarena;
mysql> delimiter //
mysql> create procedure empemail_pro(IN emp_name varchar(10), OUT mail varchar(25))
     begin
       select email into mail
       from employees
       where name=emp_name;
     end //
Query OK, 0 rows affected (0.00 sec)
mysql> delimiter ;
    /添加做验证的用户
mysql> insert into employees(name,email) values("john","john@163.com"),("jerry","jerry@tedu.cn");
Query OK, 2 rows affected (0.02 sec)
Records: 2  Duplicates: 0  Warnings: 0
//调用存储过程
mysql> call empemail_pro('john',@m);  
Query OK, 1 row affected (0.00 sec)
//查看变量的值
mysql> select @m;
+--------------+
| @m           |
+--------------+
| john@163.com |
+--------------+
1 row in set (0.00 sec)
//调用存储过程
mysql> call empemail_pro('jerry',@m);
Query OK, 1 row affected (0.00 sec)
//查看变量的值
mysql> select @m;
+---------------+
| @m            |
+---------------+
| jerry@tedu.cn |
+---------------+
1 row in set (0.00 sec)
mysql> 
```
3. 使用INOUT参数
```sql
mysql> delimiter //
mysql> create procedure myadd(INOUT i int)
     begin
       set i=i+100;
     end //
Query OK, 0 rows affected (0.00 sec)
mysql> delimiter ;
mysql> set @n=8;
Query OK, 0 rows affected (0.00 sec)
mysql> call myadd(@n);
Query OK, 0 rows affected (0.00 sec)
mysql> select @n;
+------+
| @n   |
+------+
|  108 |
+------+
1 row in set (0.00 sec)
```
# 4. 流程控制
## 4.1 问题
具体如下：
- 练习顺序结构
- 练习分支结构
- 练习循环结构与流程控制语句

## 4.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：练习顺序结构**

if语句语法
```sql
IF 条件 TEHN
  语句;
END IF;
IF 条件 TEHN
  语句1;
ELSE
  语句2;
END IF;
IF 条件1 TEHN
  语句1;
ELSEIF 条件2 TEHN
  语句2;
ELSE
  语句3;
END IF;
```
示例
```sql
mysql> use tarena;
mysql> delimiter //
mysql> create procedure deptype_pro(IN no int, OUT dept_type varchar(5))
     begin
       declare type varchar(5);
       select dept_name into type from departments
       where dept_id=no;
       if type='运维部' then
         set dept_type='技术部';
       elseif type='开发部' then
         set dept_type='技术部';
       elseif type='测试部' then
         set dept_type='技术部';
       else
         set dept_type='非技术部';
       end if;
     end //
Query OK, 0 rows affected (0.00 sec)
mysql> delimiter ;
   
mysql> call deptype_pro(1, @t);
Query OK, 1 row affected (0.00 sec)
mysql> select @t;
+--------------+
| @t           |
+--------------+
| 非技术部     |
+--------------+
1 row in set (0.00 sec)
mysql> call deptype_pro(3, @t1);
Query OK, 1 row affected (0.00 sec)
mysql> select @t1;
+-----------+
| @t1       |
+-----------+
| 技术部    |
+-----------+
1 row in set (0.00 sec)
```
**步骤二：练习分支结构**
```sql
Case语句语法

CASE 变量|表达多|字段
WHEN 判断的值1 THEN 返回值1;
WHEN 判断的值2 THEN 返回值2;
... ...
ELSE 返回值n;
END CASE;
```
示例
```sql
mysql> delimiter //
mysql> create procedure deptype_pro2(IN no int, OUT dept_type varchar(5))
    -> begin
    ->   declare type varchar(5);
    ->   select dept_name into type from departments
    ->   where dept_id=no;
    ->   case type
    ->   when '运维部' then set dept_type='技术部';
    ->   when '开发部' then set dept_type='技术部';
    ->   when '测试部' then set dept_type='技术部';
    ->   else set dept_type='非技术部';
    ->   end case;
    -> end//
mysql> call deptype_pro2(1, @tt)//
Query OK, 1 row affected (0.00 sec)
mysql> select @tt//
+--------------+
| @tt          |
+--------------+
| 非技术部     |
+--------------+
1 row in set (0.00 sec)
mysql> call deptype_pro2(3, @tt2)//
Query OK, 1 row affected (0.00 sec)
mysql> select @tt2//
+-----------+
| @tt2      |
+-----------+
| 技术部    |
+-----------+
1 row in set (0.00 sec)
mysql> delimiter ;
```
**步骤三：练习循环结构与流程控制语句**
循环语句语法
```sql
[标签:]WHILE 循环条件 DO
  循环体;
END WHILE [标签];
```
示例
```sql
mysql> delimiter //
mysql> create procedure while_pro(IN i int)
     begin
       declare j int default 1;
       while j<i do
         insert into departments(dept_name) values('hr');
         set j=j+1;
       end while;
     end //
Query OK, 0 rows affected (0.00 sec)
mysql> delimiter ;
mysql> call while_pro(3);
Query OK, 1 row affected (0.00 sec)
```
2. 使用LEAVE结束循环。此处LEAVE相当于其他语言的break
```sql
mysql> delimiter //
mysql> create procedure while_pro2(IN i int)
    begin
      declare j int default 1;
       a:while j<i do
         insert into departments(dept_name) values('hr');
         if j>=2 then leave a;
         end if;
        set j=j+1;
       end while a;
     end //
Query OK, 0 rows affected (0.00 sec)
mysql> delimiter ;
mysql> call while_pro2(3);
Query OK, 1 row affected (0.07 sec)
mysql> select  * from departments;
+---------+-----------+
| dept_id | dept_name |
+---------+-----------+
|       1 | 人事部    |
|       2 | 财务部    |
|       3 | 运维部    |
|       4 | 开发部    |
|       5 | 测试部    |
|       6 | 市场部    |
|       7 | 销售部    |
|       8 | 法务部    |
|       9 | hr        |
|      10 | hr        |
+---------+-----------+
11 rows in set (0.00 sec)
mysql> 
```
3. 使用ITERATE跳过本次循环。此处的ITERATE相当于其他整语言的continue
```sql
mysql> delimiter //
mysql> create procedure while_pro3(IN i int)
    begin
    declare j int default 0;
    a:while j<i do
    set j=j+1;
    if mod(j, 2)=0 then iterate a;
    end if;
    insert into departments(dept_name) values(concat('hr', j));
    end while a;
    end //
Query OK, 0 rows affected (0.00 sec)
mysql> delimiter ;
mysql> call while_pro3(3);
Query OK, 1 row affected (0.03 sec)
mysql> select  * from departments;
+---------+-----------+
| dept_id | dept_name |
+---------+-----------+
|       1 | 人事部    |
|       2 | 财务部    |
|       3 | 运维部    |
|       4 | 开发部    |
|       5 | 测试部    |
|       6 | 市场部    |
|       7 | 销售部    |
|       8 | 法务部    |
|       9 | hr        |
|      10 | hr        |
|      11 | hr1       | 
|      12 | hr3       |
+---------+-----------+
10 rows in set (0.00 sec)
```
4. loop循环:没有条件的死循环
语法
```sql
[标签:]LOOP
  循环体;
END LOOP [标签]
```
示例
```sql
//死循环
mysql> delimiter //
mysql> create procedure p1() 
begin 
declare age int default 29;  #变量要在循环体外定义 
loop select age; 
end loop ; 
end//
mysql> delimiter ;
Mysql>  call  p1()  #无限输出 按ctrl +c  结束
//指定循环结束条件
mysql> delimiter //
mysql> create procedure loop_pro()
     begin
       declare i int default 0;
       a:loop
         set i=i+1;
         if i>5 then leave a;
         end if;
         insert into departments(dept_name) values(concat('hr1', i));
       end loop a;
     end //
Query OK, 0 rows affected (0.00 sec)
mysql> delimiter ;
mysql> call loop_pro();
Query OK, 1 row affected (0.00 sec)
```
5）repeat循环:至少循环一次
语法
```sql
[标签:]REPEAT
  循环体;
UNTILE 循环结束条件
END REPEAT [标签]
```
示例
```sql
mysql> delimiter //
mysql> create procedure repeat_pro(IN i int)
    begin
    declare j int default 1;
       a:repeat
        set j=j+1;
         insert into departments(dept_name) values('sales');
       until j>i
       end repeat a;
     end //
Query OK, 0 rows affected (0.00 sec)
mysql> delimiter ;
mysql> call repeat_pro(3);
Query OK, 1 row affected (0.08 sec)
mysql> select * from departments;
```

# Exercise
## 1 简述读取日志内容恢复数据格式
```sql
mysqlbinlog  [选项]  /目录名/binlog日志文件名 |  mysql  -uroot  -p密码 
```
## 2 简述查看日志内容选项。
```sql
--start-position=数字  起始偏移量
--stop-position=数字  结束偏移量
--start-datetime=”yyyy/mm/dd  hh:mm:ss” 起始时间
--stop-datetime=”yyyy/mm/dd  hh:mm:ss” 结束时间
```

> 如有侵权，请联系作者删除
