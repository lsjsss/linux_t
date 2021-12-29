@[TOC]( User authorization & full backup, incremental backup | Cloud computing )

---
# 1. 常用函数
## 1.1 问题
- 练习字符函数
- 练习数学函数
- 练习日期函数
- 练习聚集函数
- 练习数学函数
- 练习if函数
- 练习case函数
## 1.2 步骤
在主机192.168.4.50主机用tarena库下的表，做如下练习。
练习的表结构说明如图-1、图-2、图-3所示

![在这里插入图片描述](https://img-blog.csdnimg.cn/a4c7ce0e93a048709de9d3ef014fbe54.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-1

![在这里插入图片描述](https://img-blog.csdnimg.cn/7bd92de24091461988c45b4eb5d3e92d.png)
图-2

![在这里插入图片描述](https://img-blog.csdnimg.cn/3d4fe5c1dac84313ac1acdf06ef5f770.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-3

**步骤一：练习字符函数**
LENGTH(str)：返字符串长度，以字节为单位
```sql
mysql> select length('abc');+---------------+| length('abc') |+---------------+|             3 |+---------------+1 row in set (0.00 sec)​​mysql> select length('你好');+------------------+| length('你好')   |+------------------+|                6 |+------------------+1 row in set (0.00 sec)​​mysql> select name, email, length(email) from employees where name='李平';+--------+----------------+---------------+| name   | email          | length(email) |+--------+----------------+---------------+| 李平   | liping@tedu.cn |            14 |+--------+----------------+---------------+1 row in set (0.00 sec)
```
CHAR_LENGTH(str): 返回字符串长度，以字符为单位
```sql
mysql> select char_length('abc');+--------------------+| char_length('abc') |+--------------------+|                  3 |+--------------------+1 row in set (0.00 sec)​​mysql> select char_length('你好');+-----------------------+| char_length('你好')   |+-----------------------+|                     2 |+-----------------------+1 row in set (0.00 sec)
```
CONCAT(s1,s2，...): 返回连接参数产生的字符串，一个或多个待拼接的内容，任意一个为NULL则返回值为NULL
```sql
# 拼接字符串mysql> select concat(dept_id, '-', dept_name) from departments;+---------------------------------+| concat(dept_id, '-', dept_name) |+---------------------------------+| 1-人事部                        || 2-财务部                        || 3-运维部                        || 4-开发部                        || 5-测试部                        || 6-市场部                        || 7-销售部                        || 8-法务部                        |+---------------------------------+8 rows in set (0.00 sec)
```
UPPER(str)和UCASE(str): 将字符串中的字母全部转换成大写
```sql
mysql> select name, upper(email) from employees where name like '李%';+-----------+----------------------+| name      | upper(email)         |+-----------+----------------------+| 李玉英    | LIYUYING@TEDU.CN     || 李平      | LIPING@TEDU.CN       || 李建华    | LIJIANHUA@TARENA.COM || 李莹      | LIYING@TEDU.CN       || 李柳      | LILIU@TARENA.COM     || 李慧      | LIHUI@TARENA.COM     || 李静      | LIJING@TARENA.COM    || 李瑞      | LIRUI@TARENA.COM     |+-----------+----------------------+8 rows in set (0.00 sec)
```
LOWER(str)和LCASE(str):将str中的字母全部转换成小写
```sql
# 转小写mysql> select lower('HelloWorld');+---------------------+| lower('HelloWorld') |+---------------------+| helloworld          |+---------------------+1 row in set (0.00 sec)
```
SUBSTR(s, start, length): 从子符串s的start位置开始，取出length长度的子串，位置从1开始计算
```sql
mysql> select substr('hello world', 7);+--------------------------+| substr('hello world', 7) |+--------------------------+| world                    |+--------------------------+1 row in set (0.00 sec)​​# 取子串，下标从7开始取出3个mysql> select substr('hello world', 7, 3);+-----------------------------+| substr('hello world', 7, 3) |+-----------------------------+| wor                         |+-----------------------------+1 row in set (0.00 sec)
```
INSTR(str,str1)：返回str1参数，在str参数内的位置
```sql
# 子串在字符串中的位置mysql> select instr('hello world', 'or');+----------------------------+| instr('hello world', 'or') |+----------------------------+|                          8 |+----------------------------+1 row in set (0.00 sec)​​mysql> select instr('hello world', 'ol');+----------------------------+| instr('hello world', 'ol') |+----------------------------+|                          0 |+----------------------------+1 row in set (0.00 sec)
```
TRIM(s): 返回字符串s删除了两边空格之后的字符串
```sql
mysql> select trim('  hello world.  ');+--------------------------+| trim('  hello world.  ') |+--------------------------+| hello world.             |+--------------------------+1 row in set (0.00 sec)
```
**步骤二：练习数学函数**
ABS(x)：返回x的绝对值
```sql
mysql> select abs(-10);+----------+| abs(-10) |+----------+|       10 |+----------+1 row in set (0.00 sec)
```
PI(): 返回圆周率π，默认显示6位小数
```sql
mysql> select pi();+----------+| pi()     |+----------+| 3.141593 |+----------+1 row in set (0.00 sec)
```
MOD(x,y): 返回x被y除后的余数
```sql
mysql> select mod(10, 3);+------------+| mod(10, 3) |+------------+|          1 |+------------+1 row in set (0.00 sec)
```
CEIL(x)、CEILING(x): 返回不小于x的最小整数
```sql
mysql> select ceil(10.1);+------------+| ceil(10.1) |+------------+|         11 |+------------+1 row in set (0.00 sec)
```
FLOOR(x): 返回不大于x的最大整数
```sql
mysql> select floor(10.9);+-------------+| floor(10.9) |+-------------+|          10 |+-------------+1 row in set (0.00 sec)
```
ROUND(x)、ROUND(x,y): 前者返回最接近于x的整数，即对x进行四舍五入；后者返回最接近x的数，其值保留到小数点后面y位，若y为负值，则将保留到x到小数点左边y位
```sql
mysql> select round(10.6666);+----------------+| round(10.6666) |+----------------+|             11 |+----------------+1 row in set (0.00 sec)mysql> select round(10.6666, 2);+-------------------+| round(10.6666, 2) |+-------------------+|             10.67 |+-------------------+1 row in set (0.00 sec)
```
**步骤三：练习日期函数**
CURDATE()、CURRENT_DATE(): 将当前日期按照"YYYY-MM-DD"或者"YYYYMMDD"格式的值返回，具体格式根据函数用在字符串或是数字语境中而定
```sql
mysql> select curdate();+------------+| curdate()  |+------------+| 2021-03-09 |+------------+1 row in set (0.00 sec)mysql> select curdate() + 0;+---------------+| curdate() + 0 |+---------------+|      20210309 |+---------------+1 row in set (0.00 sec)
```
NOW(): 返回当前日期和时间值，格式为"YYYY_MM-DD HH:MM:SS"或"YYYYMMDDHHMMSS"，具体格式根据函数用在字符串或数字语境中而定
```sql
mysql> select now();+---------------------+| now()               |+---------------------+| 2021-03-09 02:28:26 |+---------------------+1 row in set (0.00 sec)mysql> select now() + 0;+----------------+| now() + 0      |+----------------+| 20210309022848 |+----------------+1 row in set (0.00 sec)
```
MONTH(date)和MONTHNAME(date):前者返回指定日期中的月份，后者返回指定日期中的月份的名称
```sql
mysql> select month('20211001120000');+-------------------------+| month('20211001120000') |+-------------------------+|                      10 |+-------------------------+1 row in set (0.00 sec)mysql> select monthname('20211001120000');+-----------------------------+| monthname('20211001120000') |+-----------------------------+| October                     |+-----------------------------+1 row in set (0.00 sec)
```
DAYNAME(d)、DAYOFWEEK(d)、WEEKDAY(d): DAYNAME(d)返回d对应的工作日的英文名称，如Sunday、Monday等；DAYOFWEEK(d)返回的对应一周中的索引，1表示周日、2表示周一；WEEKDAY(d)表示d对应的工作日索引，0表示周一，1表示周二
```sql
mysql> select dayname('20211001120000');+---------------------------+| dayname('20211001120000') |+---------------------------+| Friday                    |+---------------------------+1 row in set (0.00 sec)mysql> select dayname('20211001');+---------------------+| dayname('20211001') |+---------------------+| Friday              |+---------------------+1 row in set (0.00 sec)
```
WEEK(d): 计算日期d是一年中的第几周
```sql
mysql> select week('20211001');+------------------+| week('20211001') |+------------------+|               39 |+------------------+1 row in set (0.00 sec)
```
DAYOFYEAR(d)、DAYOFMONTH(d)： 前者返回d是一年中的第几天，后者返回d是一月中的第几天
```sql
mysql> select dayofyear('20211001');+-----------------------+| dayofyear('20211001') |+-----------------------+|                   274 |+-----------------------+1 row in set (0.00 sec)
```
YEAR(date)、QUARTER(date)、MINUTE(time)、SECOND(time): YEAR(date)返回指定日期对应的年份，范围是1970到2069；QUARTER(date)返回date对应一年中的季度，范围是1到4；MINUTE(time)返回time对应的分钟数，范围是0~59；SECOND(time)返回制定时间的秒值
```sql
mysql> select year('20211001');+------------------+| year('20211001') |+------------------+|             2021 |+------------------+1 row in set (0.00 sec)mysql> select quarter('20211001');+---------------------+| quarter('20211001') |+---------------------+|                   4 |+---------------------+1 row in set (0.00 sec)
```
**步骤四：练习聚集函数**
sum() ：求和
```sql
mysql> select employee_id, sum(basic+bonus) from salary where employee_id=10 and year(date)=2018;+-------------+------------------+| employee_id | sum(basic+bonus) |+-------------+------------------+|          10 |           116389 |+-------------+------------------+1 row in set (0.00 sec)
```
avg() ：求平均值
```sql
mysql> select employee_id, avg(basic+bonus) from salary where employee_id=10 and year(date)=2018;+-------------+------------------+| employee_id | avg(basic+bonus) |+-------------+------------------+|          10 |       29097.2500 |+-------------+------------------+1 row in set (0.00 sec)
```
max() ：求最大值
```sql
mysql> select employee_id, max(basic+bonus) from salary where employee_id=10 and year(date)=2018;+-------------+------------------+| employee_id | max(basic+bonus) |+-------------+------------------+|          10 |            31837 |+-------------+------------------+1 row in set (0.00 sec)
```
min() ：求最小值
```sql
mysql> select employee_id, min(basic+bonus) from salary where employee_id=10 and year(date)=2018;+-------------+------------------+| employee_id | min(basic+bonus) |+-------------+------------------+|          10 |            24837 |+-------------+------------------+1 row in set (0.00 sec)
```
count() ：计算个数
```sql
mysql> select count(*) from departments;+----------+| count(*) |+----------+|        9 |+----------+1 row in set (0.00 sec)
```
**步骤五：练习数学计算**

加法计算： 给user表里前5行用户对uid 号分别 加1
```sql
//修改前查看
mysql> select id , name , uid from tarena.user where id <= 5 ;
+----+--------+------+
| id | name   | uid  |
+----+--------+------+
|  1 | root   |    0 |
|  2 | bin    |    1 |
|  3 | daemon |    2 |
|  4 | adm    |    3 |
|  5 | lp     |    4 |
+----+--------+------+
5 rows in set (0.00 sec)
//修改
mysql> update tarena.user set uid = uid +1  where id <= 5;
Query OK, 5 rows affected (0.03 sec)
Rows matched: 5  Changed: 5  Warnings: 0
mysql> 
//修改后查看
mysql> select id , name , uid from tarena.user where id <= 5 ;
+----+--------+------+
| id | name   | uid  |
+----+--------+------+
|  1 | root   |    1 |
|  2 | bin    |    2 |
|  3 | daemon |    3 |
|  4 | adm    |    4 |
|  5 | lp     |    5 |
+----+--------+------+
5 rows in set (0.00 sec)
mysql> 
```
减法计算：把编号8的员工 2020年12 月的减去500
```sql
//修改前查看
mysql> select employee_id , bonus  from  tarena.salary where employee_id =8 and year(date)=2020 and month(date)=12;
+-------------+-------+
| employee_id | bonus |
+-------------+-------+
|           8 |  2000 |
+-------------+-------+
1 row in set (0.00 sec)
mysql> 
//修改
mysql> update tarena.salary set bonus = bonus - 500  where employee_id =8 and year(date)=2020 and month(date)=12;
Query OK, 1 row affected (0.03 sec)
Rows matched: 1  Changed: 1  Warnings: 0
//修改后查看
mysql> select employee_id , bonus  from  tarena.salary where employee_id =8 and year(date)=2020 and month(date)=12;
+-------------+-------+
| employee_id | bonus |
+-------------+-------+
|           8 |  1500 |
+-------------+-------+
1 row in set (0.00 sec)
```
乘法计算: 把编号8的员工 2020年12 月的工资改为源工资的5倍
```sql
//修改前查看
mysql> select employee_id , basic  from  tarena.salary where employee_id =8 and year(date)=2020 and month(date)=12;
+-------------+-------+
| employee_id | basic |
+-------------+-------+
|           8 | 25459 |
+-------------+-------+
1 row in set (0.00 sec)
mysql>
//修改
mysql> update tarena.salary set basic=basic*5 where employee_id =8 and year(date)=2020 and month(date)=12;
Query OK, 1 row affected (0.03 sec)
Rows matched: 1  Changed: 1  Warnings: 0
//修改后查看
mysql> select employee_id , basic  from  tarena.salary where employee_id =8 and year(date)=2020 and month(date)=12;
+-------------+--------+
| employee_id | basic  |
+-------------+--------+
|           8 | 127295 |
+-------------+--------+
1 row in set (0.00 sec)
mysql> 
```
除法计算：查看平均工资
```sql
mysql> select employee_id , basic , bonus , (basic+bonus)/2  As 平均工资 from  tarena.salary where employee_id =8 and year(date)=2020 and month(date)=8;
+-------------+-------+-------+--------------+
| employee_id | basic | bonus | 平均工资     |
+-------------+-------+-------+--------------+
|           8 | 24247 |  4000 |   14123.5000 |
+-------------+-------+-------+--------------+
1 row in set (0.00 sec)
```
取余计算：显示偶数行
```sql
mysql> select  * from tarena.user where id % 2  =  0 ;
+----+-----------------+----------+-------+-------+----------------------------+--------------------+---------------+
| id | name            | password | uid   | gid   | comment                    | homedir            | shell         |
+----+-----------------+----------+-------+-------+----------------------------+--------------------+---------------+
|  2 | bin             | x        |     1 |     1 | bin                        | /bin               | /sbin/nologin |
|  4 | adm             | x        |     3 |     4 | adm                        | /var/adm           | /sbin/nologin |
|  6 | sync            | x        |     5 |     0 | sync                       | /sbin              | /bin/sync     |
|  8 | halt            | x        |     7 |     0 | halt                       | /sbin              | /sbin/halt    |
| 10 | operator        | x        |    11 |     0 | operator                   | /root              | /sbin/nologin |
| 12 | ftp             | x        |    14 |    50 | FTP User                   | /var/ftp           | /sbin/nologin |
| 14 | systemd-network | x        |   192 |   192 | systemd Network Management | /                  | /sbin/nologin |
| 16 | polkitd         | x        |   999 |   998 | User for polkitd           | /                  | /sbin/nologin |
| 18 | postfix         | x        |    89 |    89 |                            | /var/spool/postfix | /sbin/nologin |
| 20 | rpc             | x        |    32 |    32 | Rpcbind Daemon             | /var/lib/rpcbind   | /sbin/nologin |
| 22 | nfsnobody       | x        | 65534 | 65534 | Anonymous NFS User         | /var/lib/nfs       | /sbin/nologin |
+----+-----------------+----------+-------+-------+----------------------------+--------------------+---------------+
11 rows in set (0.00 sec)
mysql> 
```
**步骤六: 练习流程控制函数**
IF(expr,v1,v2): 如果expr是TRUE则返回v1，否则返回v2
```sql
mysql> select if(3>0, 'yes', 'no');+----------------------+| if(3>0, 'yes', 'no') |+----------------------+| yes                  |+----------------------+1 row in set (0.00 sec)mysql> select name, dept_id, if(dept_id=1, '人事部', '非人事部')  from employees where name='张亮';+--------+---------+--------------------------------------------+| name   | dept_id | if(dept_id=1, '人事部', '非人事部')        |+--------+---------+--------------------------------------------+| 张亮   |       7 | 非人事部                                   |+--------+---------+--------------------------------------------+1 row in set (0.00 sec)
```
IFNULL(v1,v2): 如果v1不为NULL，则返回v1，否则返回v2
```sql
mysql> select dept_id, dept_name, ifnull(dept_name, '未设置') from departments;+---------+-----------+--------------------------------+| dept_id | dept_name | ifnull(dept_name, '未设置')    |+---------+-----------+--------------------------------+|       1 | 人事部    | 人事部                         ||       2 | 财务部    | 财务部                         ||       3 | 运维部    | 运维部                         ||       4 | 开发部    | 开发部                         ||       5 | 测试部    | 测试部                         ||       6 | 市场部    | 市场部                         ||       7 | 销售部    | 销售部                         ||       8 | 法务部    | 法务部                         |+---------+-----------+--------------------------------+8 rows in set (0.00 sec)mysql> insert into departments(dept_id) values(9);mysql> select dept_id, dept_name, ifnull(dept_name, '未设置') from departments; +---------+-----------+--------------------------------+| dept_id | dept_name | ifnull(dept_name, '未设置')    |+---------+-----------+--------------------------------+|       1 | 人事部    | 人事部                         ||       2 | 财务部    | 财务部                         ||       3 | 运维部    | 运维部                         ||       4 | 开发部    | 开发部                         ||       5 | 测试部    | 测试部                         ||       6 | 市场部    | 市场部                         ||       7 | 销售部    | 销售部                         ||       8 | 法务部    | 法务部                         ||       9 | NULL      | 未设置                         |+---------+-----------+--------------------------------+9 rows in set (0.00 sec)
```
CASE expr WHEN v1 THEN r1 [WHEN v2 THEN v2] [ELSE rn] END: 如果expr等于某个vn，则返回对应位置THEN后面的结果，如果与所有值都不想等，则返回ELSE后面的rn
```sql
mysql> select dept_id, dept_name,    -> case dept_name    -> when '运维部' then '技术部门'    -> when '开发部' then '技术部门'    -> when '测试部' then '技术部门'    -> when null then '未设置'    -> else '非技术部门'    -> end as '部门类型'    -> from departments;+---------+-----------+-----------------+| dept_id | dept_name | 部门类型        |+---------+-----------+-----------------+|       1 | 人事部    | 非技术部门      ||       2 | 财务部    | 非技术部门      ||       3 | 运维部    | 技术部门        ||       4 | 开发部    | 技术部门        ||       5 | 测试部    | 技术部门        ||       6 | 市场部    | 非技术部门      ||       7 | 销售部    | 非技术部门      ||       8 | 法务部    | 非技术部门      ||       9 | NULL      | 非技术部门      |+---------+-----------+-----------------+9 rows in set (0.00 sec)mysql> select dept_id, dept_name,    -> case     -> when dept_name='运维部' then '技术部门'    -> when dept_name='开发部' then '技术部门'    -> when dept_name='测试部' then '技术部门'    -> when dept_name is null then '未设置'    -> else '非技术部门'    -> end as '部门类型'    -> from departments;+---------+-----------+-----------------+| dept_id | dept_name | 部门类型        |+---------+-----------+-----------------+|       1 | 人事部    | 非技术部门      ||       2 | 财务部    | 非技术部门      ||       3 | 运维部    | 技术部门        ||       4 | 开发部    | 技术部门        ||       5 | 测试部    | 技术部门        ||       6 | 市场部    | 非技术部门      ||       7 | 销售部    | 非技术部门      ||       8 | 法务部    | 非技术部门      ||       9 | NULL      | 未设置          |+---------+-----------+-----------------+9 rows in set (0.00 sec)
```
# 2. 查询结果处理
## 2.1 问题：具体要求如下
- 分组练习
- 排序练习
- 过滤练习
- 分页练习

## 2.2 步骤
**步骤一：分组练习**

查询每个部门的人数
```sql
mysql> select dept_id, count(*) from employees group by dept_id;+---------+----------+| dept_id | count(*) |+---------+----------+|       1 |        8 ||       2 |        5 ||       3 |        6 ||       4 |       55 ||       5 |       12 ||       6 |        9 ||       7 |       35 ||       8 |        3 |+---------+----------+8 rows in set (0.00 sec)
```
查询每个部门中年龄最大的员工
```sql
mysql> select dept_id, min(birth_date) from employees group by dept_id;+---------+-----------------+| dept_id | min(birth_date) |+---------+-----------------+|       1 | 1971-08-19      ||       2 | 1971-11-02      ||       3 | 1971-09-09      ||       4 | 1972-01-31      ||       5 | 1971-08-14      ||       6 | 1973-04-14      ||       7 | 1971-12-10      ||       8 | 1989-05-19      |+---------+-----------------+8 rows in set (0.00 sec)
```
查询每个部门入职最晚员工的入职时间
```sql
mysql> select dept_id, max(hire_date) from employees group by dept_id;+---------+----------------+| dept_id | max(hire_date) |+---------+----------------+|       1 | 2018-11-21     ||       2 | 2018-09-03     ||       3 | 2019-07-04     ||       4 | 2021-02-04     ||       5 | 2019-06-08     ||       6 | 2017-10-07     ||       7 | 2020-08-21     ||       8 | 2019-11-14     |+---------+----------------+8 rows in set (0.00 sec)
```
统计各部门使用tedu.cn邮箱的员工人数
```sql
mysql> select dept_id, count(*) from employees 
where email like '%@tedu.cn' group by dept_id;+---------+----------+| dept_id | count(*) |+---------+----------+|       1 |        5 ||       2 |        2 ||       3 |        4 ||       4 |       32 ||       5 |        7 ||       6 |        5 ||       7 |       15 ||       8 |        1 |+---------+----------+8 rows in set (0.00 sec)
```
**步骤二：排序练习**
查看员工2018年工资总收入，按总收入进行降序排列
```sql
mysql> select employee_id, sum(basic+bonus) as total from salary where year(date)=2018 group by employee_id order by total desc;
```
默认升序
```sql
//查出符合条件的用户
mysql> select name, birth_date from employees where birth_date>'19980101';
+-----------+------------+
| name      | birth_date |
+-----------+------------+
| 姚琳      | 1998-05-20 |
| 吴雪      | 1998-06-13 |
| 薄刚      | 2000-05-17 |
| 张玉英    | 1998-06-22 |
| 刘倩      | 1998-10-27 |
| 申峰      | 1999-01-13 |
| 陈勇      | 1998-02-04 |
| 厉秀云    | 1999-09-08 |
| 张桂英    | 1999-05-31 |
| 赵峰      | 1998-03-06 |
| 蒙梅      | 2000-09-01 |
| 陈欢      | 1998-07-01 |
| 马磊      | 2000-08-07 |
| 赵秀梅    | 1998-09-25 |
+-----------+------------+
14 rows in set (0.00 sec)
//默认升序排序
mysql> select name, birth_date from employees 
where birth_date>'19980101' order by birth_date;
+-----------+------------+
| name      | birth_date |
+-----------+------------+
| 陈勇      | 1998-02-04 |
| 赵峰      | 1998-03-06 |
| 姚琳      | 1998-05-20 |
| 吴雪      | 1998-06-13 |
| 张玉英    | 1998-06-22 |
| 陈欢      | 1998-07-01 |
| 赵秀梅    | 1998-09-25 |
| 刘倩      | 1998-10-27 |
| 申峰      | 1999-01-13 |
| 张桂英    | 1999-05-31 |
| 厉秀云    | 1999-09-08 |
| 薄刚      | 2000-05-17 |
| 马磊      | 2000-08-07 |
| 蒙梅      | 2000-09-01 |
+-----------+------------+
14 rows in set (0.00 sec)
//降序排序
mysql> select name, birth_date from employees where birth_date>'19980101'
 order by birth_date desc;
+-----------+------------+
| name      | birth_date |
+-----------+------------+
| 蒙梅      | 2000-09-01 |
| 马磊      | 2000-08-07 |
| 薄刚      | 2000-05-17 |
| 厉秀云    | 1999-09-08 |
| 张桂英    | 1999-05-31 |
| 申峰      | 1999-01-13 |
| 刘倩      | 1998-10-27 |
| 赵秀梅    | 1998-09-25 |
| 陈欢      | 1998-07-01 |
| 张玉英    | 1998-06-22 |
| 吴雪      | 1998-06-13 |
| 姚琳      | 1998-05-20 |
| 赵峰      | 1998-03-06 |
| 陈勇      | 1998-02-04 |
+-----------+------------+
14 rows in set (0.00 sec)
# 查询2015年1月10号员工工资情况
mysql> select date, employee_id, basic, bonus from salary where date='20150110';
# 查询2015年1月10号员工工资情况，以基本工资进行降序排列；如果基本工资相同，再以奖金升序排列
mysql> select date, employee_id, basic, bonus from salary where date='20150110' order by basic desc, bonus;
# 查询2015年1月10号员工工资情况，以工资总额为排序条件
mysql> select date, employee_id, basic, bonus, basic+bonus as total from salary where date='20150110' order by total;
```
**步骤三：过滤练习**
查询部门人数少于5人
```sql
mysql> select dept_id, count(*) from employees group by dept_id having count(*)<10;+---------+----------+| dept_id | count(*) |+---------+----------+|       1 |        8 ||       2 |        5 ||       3 |        6 ||       6 |        9 ||       8 |        3 |+---------+----------+5 rows in set (0.00 sec)
```
**步骤四：分页练习**
使用SELECT查询时，如果结果集数据量很大，比如几万行数据，放在一个页面显示的话数据量太大，不如分页显示,比如每次只显示100条

要实现分页功能，实际上就是从结果集中显示第1至100条记录作为第1页，显示第101至200条记录作为第2页，以此类推
```sql
# 按employee_id排序，取出前5位员姓名
mysql> select employee_id, name from employees
    -> order by employee_id
    -> limit 0, 5;
+-------------+-----------+
| employee_id | name      |
+-------------+-----------+
|           1 | 梁伟      |
|           2 | 郭岩      |
|           3 | 李玉英    |
|           4 | 张健      |
|           5 | 郑静      |
+-------------+-----------+
5 rows in set (0.00 sec)
# 按employee_id排序，取出前15至20号员姓名
mysql> select employee_id, name from employees
    -> order by employee_id
    -> limit 15, 5;
+-------------+--------+
| employee_id | name   |
+-------------+--------+
|          16 | 聂想   |
|          17 | 陈阳   |
|          18 | 戴璐   |
|          19 | 陈斌   |
|          20 | 蒋红   |
+-------------+--------+
5 rows in set (0.00 sec)
//查询uid号最大的用户名和uid号
mysql> select  name , uid  from user order by uid desc limit 1;
+-----------+-------+
| name      | uid   |
+-----------+-------+
| nfsnobody | 65534 |
+-----------+-------+
1 row in set (0.00 sec)
mysql> 
```
# 3. 连接查询
## 3.1 问题，具体如下：
- 练习内连接查询
- 练习外连接查询
- 练习全连接查询
- 练习交叉连接查询
- 练习子查询
- 练习多表更新与删除

## 3.2 步骤
练习使用的表说明：三张表的关系 如图-1所示

部门表departments与员工表employees之间有外键约束关系，employees表的的dept_id字段必须出现在departments表中

员工表employees和工资表salary表之间有外键约束关系，salary表的employee_id必须出现在employees表中

![在这里插入图片描述](https://img-blog.csdnimg.cn/ff104c51ee15439fadc751ea9fc602ce.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-1

**步骤一：练习内连接查询**

查询每个员工所在的部门名
```sql
mysql> select name, dept_name    -> from employees    -> inner join departments    -> on employees.dept_id=departments.dept_id;
```
查询每个员工所在的部门名，使用别名
```sql
mysql> select name, dept_name    -> from employees as e    -> inner join departments as d    -> on e.dept_id=d.dept_id;
```
查询每个员工所在的部门名，使用别名。两个表中的同名字段，必须指定表名
```sql
mysql> select name, d.dept_id, dept_name    -> from employees as e    -> inner join departments as d    -> on e.dept_id=d.dept_id;
```
查询11号员工的名字及2018年每个月工资
```sql
mysql> select name, date, basic+bonus as total    -> from employees as e    -> inner join salary as s    -> on e.employee_id=s.employee_id    -> where year(s.date)=2018 and e.employee_id=11;
```
查询2018年每个员工的总工资
```sql
mysql> select name, sum(basic+bonus) from employees    -> inner join salary    -> on employees.employee_id=salary.employee_id    -> where year(s.date)=2018    -> group by name;
```
查询2018年每个员工的总工资，按工资升序排列
```sql
mysql> select name, sum(basic+bonus) as total from employees as e    -> inner join salary as s    -> on e.employee_id=s.employee_id    -> where year(s.date)=2018    -> group by name    -> order by total;
```
查询2018年总工资大于30万的员工，按工资降序排列
```sql
 mysql> select name, sum(basic+bonus) as total from employees as e    -> inner join salary as s    -> on e.employee_id=s.employee_id    -> where year(s.date)=2018    -> group by name    -> having total>300000    -> order by total desc;
```
非等值连接：使用不相等做为连接筛选条件

准备工作：创建工资级别表：
id：主键。仅作为表的行号
grade：工资级别，共ABCDE五类
low：该级别最低工资
high：该级别最高工资

```sql
mysql> use tarena;mysql> create table wage_grade    -> (    -> id int,    -> grade char(1),    -> low int,    -> high int,    -> primary key (id)
);
```
向wage_grade表中插入五行数据：
```sql
mysql> insert into wage_grade values    -> (1, 'A', 5000, 8000),    -> (2, 'B', 8001, 10000),    -> (3, 'C', 10001, 15000),    -> (4, 'D', 15001, 20000),    -> (5, 'E', 20001, 1000000);
```
查询2018年12月员工基本工资级别
```sql
mysql> select employee_id, date, basic, grade    -> from salary as s    -> inner join wage_grade as g    -> on s.basic between g.low and g.high    -> where year(date)=2018 and month(date)=12;
```
查询2018年12月员工各基本工资级别的人数
```sql
mysql> select grade, count(*)    -> from salary as s    -> inner join wage_grade as g    -> on s.basic between g.low and g.high    -> where year(date)=2018 and month(date)=12    -> group by grade;+-------+----------+| grade | count(*) |+-------+----------+| A     |       13 || B     |       12 || C     |       30 || D     |       32 || E     |       33 |+-------+----------+5 rows in set (0.00 sec)
```
查询2018年12月员工基本工资级别，员工需要显示姓名
```sql
mysql> select name, date, basic, grade    -> from employees as e    -> inner join salary as s    -> on e.employee_id=s.employee_id    -> inner join wage_grade as g    -> on s.basic between g.low and g.high    -> where year(date)=2018 and month(date)=12;
```
自连接：自己连接自己，将一张表作为两张使用，每张表起一个别名

查看哪些员的生日月份与入职月份相同
```sql
mysql> select e.name, e.hire_date, em.birth_date    -> from employees as e    -> inner join employees as em    -> on month(e.hire_date)=month(em.birth_date)    -> and e.employee_id=em.employee_id;+-----------+------------+------------+| name      | hire_date  | birth_date |+-----------+------------+------------+| 李玉英    | 2012-01-19 | 1974-01-25 || 郑静      | 2018-02-03 | 1997-02-14 || 林刚      | 2007-09-19 | 1990-09-23 || 刘桂兰    | 2003-10-14 | 1982-10-11 || 张亮      | 2015-08-10 | 1996-08-25 || 许欣      | 2011-09-09 | 1982-09-25 || 王荣      | 2019-11-14 | 1999-11-22 |+-----------+------------+------------+7 rows in set (0.00 sec)
```
**步骤二：练习外连接查询**

外连接
常用于查询一个表中有，另一个表中没有的记录
如果从表中有和它匹配的，则显示匹配的值
如j要从表中没有和它匹配的，则显示NULL
外连接查询结果=内连接查询结果+主表中有而从表中没有的记录
左外连接中，left join左边的是主表
右外连接中，right join右边的是主表
左外连接和右外连接可互换，实现相同的目标
查询所有部门的人员以及没有员工的部门
```sql
mysql> select d.*, e.name    -> from departments as d    -> left  join employees as e    -> on d.dept_id=e.dept_id;
```
右连接(也称右外连接）示例
查询所有部门的人员以及没有员工的部门
```sql
mysql> select d.*, e.name    -> from employees as e    -> right  join departments as d    -> on d.dept_id=e.dept_id;
```
**步骤三：练习交叉连接查询**
交叉连接：返回笛卡尔积
查询员工表和部门表的笛卡尔积
```sql
mysql> select name, dept_name    -> from employees    -> cross join departments;
```
**步骤四：练习联合查询**
联合查询UNION
作用：将多条select语句的结果，合并到一起，称之为联合操作。

语法：( ) UNION ( )

要求查询时，多个select语句的检索到的字段数量必须一致
每一条记录的各字段类型和顺序最好是一致的

UNION关键字默认去重，可以使用UNION ALL包含重复项
```sql
mysql> (select 'yes') union (select 'yes');
+-----+
| yes |
+-----+
| yes |
+-----+
1 row in set (0.00 sec)
mysql> (select 'yes') union all (select 'yes');
+-----+
| yes |
+-----+
| yes |
| yes |
+-----+
2 rows in set (0.00 sec)
```
查询1972年或2000年后出生的员工
```sql
# 普通方法
mysql> select name, birth_date from employees
    -> where year(birth_date)<1972 or year(birth_date)>2000;
+-----------+------------+
| name      | birth_date |
+-----------+------------+
| 梁伟      | 1971-08-19 |
| 张建平    | 1971-11-02 |
| 窦红梅    | 1971-09-09 |
| 温兰英    | 1971-08-14 |
| 朱文      | 1971-08-15 |
| 和林      | 1971-12-10 |
+-----------+------------+
6 rows in set (0.01 sec)
# 联合查询的方法
mysql> (
    -> select name, birth_date from employees
    ->   where year(birth_date)<1972
    -> )
    -> union
    -> (
    ->   select name, birth_date from employees
    ->   where year(birth_date)>2000
    -> );
+-----------+------------+
| name      | birth_date |
+-----------+------------+
| 梁伟      | 1971-08-19 |
| 张建平    | 1971-11-02 |
| 窦红梅    | 1971-09-09 |
| 温兰英    | 1971-08-14 |
| 朱文      | 1971-08-15 |
| 和林      | 1971-12-10 |
+-----------+------------+
6 rows in set (0.00 sec)
//一起输出user表中uid号最小和uid号最大的用户信息
mysql> select * from user where uid = (select min(uid) from user) union select * from user where uid = (select max(uid) from user);
+----+-----------+----------+-------+-------+--------------------+--------------+---------------+
| id | name      | password | uid   | gid   | comment            | homedir      | shell         |
+----+-----------+----------+-------+-------+--------------------+--------------+---------------+
|  1 | root      | x        |     1 |     0 | root               | /root        | /bin/bash     |
| 22 | nfsnobody | x        | 65534 | 65534 | Anonymous NFS User | /var/lib/nfs | /sbin/nologin |
+----+-----------+----------+-------+-------+--------------------+--------------+---------------+
2 rows in set (0.00 sec)
mysql> 
```
**步骤五：练习子查询**
查询运维部所有员工信息
```sql
//首先从departments表中查出运维部的编号
mysql> select dept_id from departments where dept_name='运维部';+---------+| dept_id |+---------+|       3 |+---------+1 row in set (0.00 sec)
//再从employees表中查找该部门编号和运维部编号相同的员工
mysql> select *    -> from employees    -> where dept_id=(    ->   select dept_id from departments where dept_name='运维部'    -> );
```
查询2018年12月所有比100号员工基本工资高的工资信息
```sql
//首先查到2018年12月100号员工的基本工资
mysql> select basic from salary    -> where year(date)=2018 and month(date)=12 and employee_id=100;+-------+| basic |+-------+| 14585 |+-------+1 row in set (0.00 sec)
//再查询2018年12月所有比100号员工基本工资高的工资信息
mysql> select * from salary    -> where year(date)=2018 and month(date)=12 and basic>(    ->   select basic from salary    ->   where year(date)=2018 and month(date)=12 and employee_id=100    -> );
```
查询部门员工人数比开发部人数少的部门
```sql
//查询开发部部门编号
mysql> select dept_id from departments where dept_name='开发部';+---------+| dept_id |+---------+|       4 |+---------+1 row in set (0.00 sec)
//查询开发部人数
mysql> select count(*) from employees    -> where dept_id=(    ->   select dept_id from departments where dept_name='开发部'    -> );+----------+| count(*) |+----------+|       55 |+----------+1 row in set (0.00 sec)
//分组查询各部门人数
mysql> select count(*), dept_id from employees group by dept_id;+----------+---------+| count(*) | dept_id |+----------+---------+|        8 |       1 ||        5 |       2 ||        6 |       3 ||       55 |       4 ||       12 |       5 ||        9 |       6 ||       35 |       7 ||        3 |       8 |+----------+---------+8 rows in set (0.01 sec)
//查询部门员工人数比开发部人数少的部门
mysql> select count(*), dept_id from employees group by dept_id    -> having count(*)<(    ->   select count(*) from employees    ->   where dept_id=(    ->     select dept_id from departments where dept_name='开发部'    ->   )    -> );+----------+---------+| count(*) | dept_id |+----------+---------+|        8 |       1 ||        5 |       2 ||        6 |       3 ||       12 |       5 ||        9 |       6 ||       35 |       7 ||        3 |       8 |+----------+---------+7 rows in set (0.00 sec)
```
查询每个部门的人数
```sql
//查询所有部门的信息
mysql> select d.* from departments as d;+---------+-----------+| dept_id | dept_name |+---------+-----------+|       1 | 人事部    ||       2 | 财务部    ||       3 | 运维部    ||       4 | 开发部    ||       5 | 测试部    ||       6 | 市场部    ||       7 | 销售部    ||       8 | 法务部    ||       9 | NULL      |+---------+-----------+9 rows in set (0.00 sec
//查询每个部门的人数
mysql> select d.*, (    ->  select count(*) from employees as e    ->   where d.dept_id=e.dept_id    -> ) as amount    -> from departments as d;+---------+-----------+--------+| dept_id | dept_name | amount |+---------+-----------+--------+|       1 | 人事部    |      8 ||       2 | 财务部    |      5 ||       3 | 运维部    |      6 ||       4 | 开发部    |     55 ||       5 | 测试部    |     12 ||       6 | 市场部    |      9 ||       7 | 销售部    |     35 ||       8 | 法务部    |      3 ||       9 | NULL      |      0 |+---------+-----------+--------+9 rows in set (0.00 sec)
```
查询人事部和财务部员工信息
```sql
//查询人事部和财务部编号
mysql> select dept_id from departments    -> where dept_name in ('人事部', '财务部');+---------+| dept_id |+---------+|       1 ||       2 |+---------+2 rows in set (0.00 sec)
//查询部门编号是两个部门编号的员工信息
mysql> select * from employees    -> where dept_id in (    ->   select dept_id from departments    ->   where dept_name in ('人事部', '财务部')    -> );
```
查询人事部2018年12月所有员工工资
```sql
//查询人事部部门编号
mysql> select dept_id from departments where dept_name='人事部';+---------+| dept_id |+---------+|       1 |+---------+1 row in set (0.00 sec)
//查询人事部员的编号
mysql> select employee_id from employees    -> where dept_id=(    ->   select dept_id from departments where dept_name='人事部'    -> );+-------------+| employee_id |+-------------+|           1 ||           2 ||           3 ||           4 ||           5 ||           6 ||           7 ||           8 |+-------------+8 rows in set (0.00 sec)
//查询2018年12月人事部所有员工工资
mysql> select * from salary    -> where year(date)=2018 and month(date)=12 and employee_id in (    ->   select employee_id from employees    ->   where dept_id=(    ->     select dept_id from departments where dept_name='人事部'    ->   )    -> );+------+------------+-------------+-------+-------+| id   | date       | employee_id | basic | bonus |+------+------------+-------------+-------+-------+| 6252 | 2018-12-10 |           1 | 17016 |  7000 || 6253 | 2018-12-10 |           2 | 20662 |  9000 || 6254 | 2018-12-10 |           3 |  9724 |  8000 || 6255 | 2018-12-10 |           4 | 17016 |  2000 || 6256 | 2018-12-10 |           5 | 17016 |  3000 || 6257 | 2018-12-10 |           6 | 17016 |  1000 || 6258 | 2018-12-10 |           7 | 23093 |  4000 || 6259 | 2018-12-10 |           8 | 23093 |  2000 |+------+------------+-------------+-------+-------+8 rows in set (0.00 sec)
```
查找2018年12月基本工资和奖金都是最高的工资信息
```sql
//查询2018年12月最高的基本工资
mysql> select max(basic) from salary    -> where year(date)=2018 and month(date)=12;+------------+| max(basic) |+------------+|      25524 |+------------+1 row in set (0.00 sec)
//查询2018年12月最高的奖金
mysql> select max(bonus) from salary    -> where year(date)=2018 and month(date)=12;+------------+| max(bonus) |+------------+|      11000 |+------------+1 row in set (0.00 sec)
//查询
mysql> select * from salary    -> where year(date)=2018 and month(date)=12 and basic=(    ->   select max(basic) from salary    ->   where year(date)=2018 and month(date)=12    -> ) and bonus=(    ->   select max(bonus) from salary    ->   where year(date)=2018 and month(date)=12    -> );+------+------------+-------------+-------+-------+| id   | date       | employee_id | basic | bonus |+------+------------+-------------+-------+-------+| 6368 | 2018-12-10 |         117 | 25524 | 11000 |+------+------------+-------------+-------+-------+1 row in set (0.01 sec)
```
查询3号部门及其部门内员工的编号、名字和email
```sql
//查询3号部门和员工的所有信息
mysql> select d.dept_name, e.*    -> from departments as d    -> inner join employees as e    -> on d.dept_id=e.dept_id;
//将上述结果当成一张临时表，必须为其起别名。再从该临时表中查询
mysql> select dept_id, dept_name, employee_id, name, email    -> from (    ->   select d.dept_name, e.*    ->   from departments as d    ->   inner join employees as e    ->   on d.dept_id=e.dept_id    -> ) as tmp_table    -> where dept_id=3;+---------+-----------+-------------+-----------+--------------------+| dept_id | dept_name | employee_id | name      | email              |+---------+-----------+-------------+-----------+--------------------+|       3 | 运维部    |          14 | 廖娜      | liaona@tarena.com  ||       3 | 运维部    |          15 | 窦红梅    | douhongmei@tedu.cn ||       3 | 运维部    |          16 | 聂想      | niexiang@tedu.cn   ||       3 | 运维部    |          17 | 陈阳      | chenyang@tedu.cn   ||       3 | 运维部    |          18 | 戴璐      | dailu@tedu.cn      ||       3 | 运维部    |          19 | 陈斌      | chenbin@tarena.com |+---------+-----------+-------------+-----------+--------------------+6 rows in set (0.00 sec)
```
**步骤六：练习多表更新与删除**
```sql
mysql> use tarena;
Database changed
mysql> 
//创建t1表
mysql> create table t1 select uid , name  from user limit 3 ;
Query OK, 3 rows affected (0.04 sec)
Records: 3  Duplicates: 0  Warnings: 0
//创建t2表
mysql> create table t2 select uid , homedir,shell  from user limit 6 ;
Query OK, 6 rows affected (0.02 sec)
Records: 6  Duplicates: 0  Warnings: 0
mysql> select  * from t1;
+------+--------+
| uid  | name   |
+------+--------+
|    0 | root   |
|    1 | bin    |
|    2 | daemon |
+------+--------+
3 rows in set (0.00 sec)
mysql> select  * from t2;
+------+----------------+---------------+
| uid  | homedir        | shell         |
+------+----------------+---------------+
|    0 | /root          | /bin/bash     |
|    1 | /bin           | /sbin/nologin |
|    2 | /sbin          | /sbin/nologin |
|    3 | /var/adm       | /sbin/nologin |
|    4 | /var/spool/lpd | /sbin/nologin |
|    5 | /sbin          | /bin/sync     |
+------+----------------+---------------+
6 rows in set (0.00 sec)
//连接查询
mysql> select * from t1 inner join t2 on  t1.uid = t2.uid ;
+------+--------+------+---------+---------------+
| uid  | name   | uid  | homedir | shell         |
+------+--------+------+---------+---------------+
|    0 | root   |    0 | /root   | /bin/bash     |
|    1 | bin    |    1 | /bin    | /sbin/nologin |
|    2 | daemon |    2 | /sbin   | /sbin/nologin |
+------+--------+------+---------+---------------+
3 rows in set (0.00 sec)
mysql>
//多表修改
mysql> update t1 inner join t2 on  t1.uid = t2.uid  set shell=NULL , t1.uid=101 , t2.uid=102 where t1.uid=0 ;
Query OK, 2 rows affected (0.01 sec)
Rows matched: 2  Changed: 2  Warnings: 0
mysql>
//查看修改
mysql> select  * from t1;
+------+--------+
| uid  | name   |
+------+--------+
|  101 | root   |     # uid = 101
|    1 | bin    |
|    2 | daemon |
+------+--------+
3 rows in set (0.00 sec)
mysql> select  * from t2;
+------+----------------+---------------+
| uid  | homedir        | shell         |
+------+----------------+---------------+
|  102 | /root          | NULL          |    #shell=null  uid=102
|    1 | /bin           | /sbin/nologin |
|    2 | /sbin          | /sbin/nologin |
|    3 | /var/adm       | /sbin/nologin |
|    4 | /var/spool/lpd | /sbin/nologin |
|    5 | /sbin          | /bin/sync     |
+------+----------------+---------------+
6 rows in set (0.01 sec)
mysql>
//连接查询
mysql> select * from t1 inner join t2 on  t1.uid = t2.uid;
+------+--------+------+---------+---------------+
| uid  | name   | uid  | homedir | shell         |
+------+--------+------+---------+---------------+
|    1 | bin    |    1 | /bin    | /sbin/nologin |
|    2 | daemon |    2 | /sbin   | /sbin/nologin |
+------+--------+------+---------+---------------+
2 rows in set (0.00 sec)
//多表删除
mysql> delete t1,t2  from t1 inner join t2 on  t1.uid = t2.uid;
Query OK, 4 rows affected (0.00 sec)
mysql>
//查看表记录
mysql> select  * from t1;  #uid=1和 uid=2 的记录被删除了
+------+------+
| uid  | name |
+------+------+
|  101 | root |
+------+------+
1 row in set (0.00 sec)
mysql> select  * from t2; #uid=1和 uid=2 的记录被删除了
+------+----------------+---------------+
| uid  | homedir        | shell         |
+------+----------------+---------------+
|  102 | /root          | NULL          |
|    3 | /var/adm       | /sbin/nologin |
|    4 | /var/spool/lpd | /sbin/nologin |
|    5 | /sbin          | /bin/sync     |
+------+----------------+---------------+
4 rows in set (0.00 sec)
mysql>
```

# Exercise
## 1 简述用户授权命令的语法格式。
```sql
GRANT  权限列表  ON  库名.表名  TO  用户名@'客户端地址'   [ IDENTIFIED BY '密码' ]  [ WITH GRANT OPTION ];
```
## 2 数据库授权综合练习，按题目要求写出对应的授权命令。
> 1. 查看当前数据库服务器有哪些授权用户?
> 2. 授权管理员用户可以在网络中的任意主机登录，对所有库和表有完全权限且有授权的权限登陆密码123456
> 3. 授权webadmin用户可以从网络中的所有主机登录，对bbsdb库拥有完全权限，且有授权权限，登录密码为 123456
> 4. 不允许数据库管理员在数据库服务器本机登录。

```sql
1.select user from mysql.user;
2.grant all on *.*  to  root@“%” identified  by “123456” with grant option;
3.grant all  on  bbsdb.*  to   webadmin@“%” identified  by “123456” with grant option; grant insert  on  mysql.user to  webadmin@“%”;
4.delete from mysql.user where host in (“::1”,”127.0.0.1”,”localhost”,”stu.tedu.cn”) and user=”host”;flush privileges;
```

## 3 简述撤销用户授权命令的语法格式。
```sql
revoke  权限列表  on  数据库名  from  用户名@”客户端地址”；
```
## 4 简述binlog日志格式。
```sql
statement 、  row  、  mixed
```
## 5 简述备份策略的类型。

完全备份：备份所有数据。
差异备份：备份自完全备份后所有新产生的数据。
增量备份：备份上次备份后所有新产生的数据。

> 如有侵权，请联系作者删除
