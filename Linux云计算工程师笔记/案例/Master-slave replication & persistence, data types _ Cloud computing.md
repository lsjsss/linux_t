@[TOC]( Master-slave replication & persistence, data types | Cloud computing )

---
# 1. redis主从复制
## 1.1 问题
具体要求如下：
- 将主机192.168.4.51配置为主服务器
- 将主机192.168.4.52配置为192.168.4.51的从服务器
- 测试配置

## 1.2 方案
部署redis一主一从复制结构，主机角色，如图-1所示：

![在这里插入图片描述](https://img-blog.csdnimg.cn/2af8c6ce9dcf40b49ae84fca275a86c4.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图－1

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：将主机192.168.4.51配置为主服务器**

1） 每台redis服务器，默认都是主服务器;所以主服务器不需要配置。
```shell
[root@redisA ~]# redis-cli -h 192.168.4.51 –p 6351 
192.168.4.51:6351> info replication        //查看复制信息
# Replication
role:master            //是master 服务器  
connected_slaves:0    //从服务器个数零台
master_replid:eaa14478158a71c41f947eaea036658c2087e8f2
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:0
second_repl_offset:-1
repl_backlog_active:0
repl_backlog_size:1048576
repl_backlog_first_byte_offset:0
repl_backlog_histlen:0
192.168.4.51:6351>
```
**步骤二：将主机192.168.4.52配置为192.168.4.51的从服务器**

1）命令行配置（马上生效）
```shell
[root@redisB ~]# redis-cli -h 192.168.4.52 –p 6352    
192.168.4.52:6352> slaveof  192.168.4.51  6351  //指定主服务器ip地址与端口
OK
192.168.4.52:6352> info replication   //查看复制信息
# Replication
role:slave  //从服务器
master_host:192.168.4.51        //主服务器ip地址
master_port:6351 //主服务器端口
master_link_status:up //连接状态开启
master_last_io_seconds_ago:3
master_sync_in_progress:0
```
2）永久配置（重新redis服务后，依然有效）
```shell
[root@redisB ~]# vim /etc/redis/6379.conf    
slaveof  192.168.4.51  6351    //在文件末尾添加或在原有配置项上修改都可以
:wq
```
3）在主服务器查看复制信息
```shell
[root@redisA ~]# redis-cli -h 192.168.4.51 –p 6351
192.168.4.51:6351> info replication  //查看复制信息
# Replication
role:master
connected_slaves:1 //从服务器个数 1台
slave0:ip=192.168.4.52,port=6352,state=online,offset=14,lag=1    //从服务器信息
master_replid:db7932eb0ea4302bddbebd395efa174fb079319f
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:14
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:14
192.168.4.51:6351>
```
**步骤三：测试配置**

1）客户端连接主服务器存储数据
```shell
[root@client50 ~]# redis-cli -h 192.168.4.51 –p 6351    
192.168.4.51:6351> set x  9
OK
192.168.4.51:6351> set y  8
OK
192.168.4.51:6351> set z  7
OK
192.168.4.51:6351>
```
2）在从服务器本机登录，查看数据（与主服务器数据一致）
```shell
[root@redisB ~]#     redis-cli -h 192.168.4.52 –p 6352
192.168.4.52:6352> keys  *
1）“x”
2）“y”
3）“z”
192.168.4.52:6352>
```
# 2. 配置带验证的主从复制
## 2.1 问题
- 具体要求如下：
- 基于案例1的配置
- 设置主服务器192.168.4.51 设置连接密码123456
- 配置从服务器192.168.4.52

## 2.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：设置主服务器192.168.4.51 设置连接密码123456**

1） 修改主服务器的配置文件，设置密码。
```shell
[root@redisA ~]# vim +501 /etc/redis/6379.conf 
requirepass  123456   //设置密码
:wq
[root@redisA ~]# vim +43  /etc/init.d/redis_6379  //修改脚本
$CLIEXEC -h 192.168.4.51 -p 6351 -a 123456  shutdown //添加密码
:wq
[root@redisA ~]# /etc/init.d/redis_6379 stop //停止服务
[root@redisA ~]# /etc/init.d/redis_6379  start //启动服务
Starting Redis server...
[root@redisA ~]# 
[root@redisA ~]# netstat -utnlp  | grep  :6351  //查看端口
tcp        0      0 192.168.4.51:6351       0.0.0.0:*               LISTEN      11523/redis-server
```
**步骤二：配置从服务器192.168.4.52**

1） 修改配置文件，设置主服务器连接密码。
```shell
[root@redisB ~]# /etc/init.d/redis_6379 stop //停止服务
[root@redisB ~]# vim +289 /etc/redis/6379.conf 
masterauth  123456   //设置密码
:wq
[root@redisA ~]# /etc/init.d/redis_6379  start //启动服务
Starting Redis server...
[root@redisA ~]# 
[root@redisA ~]# netstat -utnlp  | grep  :6351  //查看端口
tcp        0      0 192.168.4.51:6351       0.0.0.0:*               LISTEN      11523/redis-server
```
2） 在从服务器本机连接服务，查看复制信息
```shell
[root@redisB ~]# redis-cli -h 192.168.4.52 –p 6352    
192.168.4.52:6352> info replication   //查看复制信息
# Replication
role:slave  //从服务器
master_host:192.168.4.51        //主服务器ip地址
master_port:6351 //主服务器端口
master_link_status:up //连接状态开启
master_last_io_seconds_ago:3
master_sync_in_progress:0
……
……
192.168.4.52:6352>
```
# 3. 哨兵服务
## 3.1 问题
- 具体要求如下：
- 基于案例2配置
- 配置哨兵服务
- 测试配置

## 3.2 方案
角色规划如图-1所示：
![在这里插入图片描述](https://img-blog.csdnimg.cn/198c6fa7a7524d95ba7d531735279250.png)
图－1

## 3.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：配置哨兵服务（192.168.4.57）**

1） 安装源码软件redis ，无需做初始化配置。
```shell
[root@redis57 redis]# yum -y install gcc 
[root@redis57 redis]# tar -zxf redis-4.0.8.tar.gz
[root@redis57 redis]# cd redis-4.0.8/
[root@redis1 redis-4.0.8]# make
[root@redis1 redis-4.0.8]# make install
```
2）编辑主配置文件
```shell
[root@redis57 redis]# vim  /etc/sentinel.conf  //创建主配置文件
sentinel   monitor   server51   192.168.4.51   6351   1 //监视主服务器
bind  0.0.0.0    //哨兵服务地址（表示本机所有网络接口）
sentinel auth-pass  server51   123456   //主服务器密码
:wq
```
3）启动哨兵服务
```shell
[root@redis57 redis]# redis-sentinel /etc/sentinel.conf    //启动哨兵服务
25371:X 28 Sep 11:16:54.993 # +sdown master redis51 192.168.4.51 6351
25371:X 28 Sep 11:16:54.993 # +odown master redis51 192.168.4.51 6351 #quorum 1/1
25371:X 28 Sep 11:16:54.993 # +new-epoch 3
25371:X 28 Sep 11:16:54.993 # +try-failover master redis51 192.168.4.51 6351
25371:X 28 Sep 11:16:54.994 # +vote-for-leader be035801d4d48eb63d8420a72796f52fc5cec047 3
...
25371:X 28 Sep 11:16:55.287 * +slave slave 192.168.4.51:6351 192.168.4.51 6351 @ redis51 192.168.4.52 6351
25371:X 28 Sep 11:17:25.316 # +sdown slave 192.168.4.51:6379 192.168.4.51 6379 @ redis51 192.168.4.52 6352
```
**步骤二：测试配置**

1）停止主服务器51的redis服务
```shell
[root@redisA ~]#     /etc/init.d/redis_6379 stop
Stopping ...
Waiting for Redis to shutdown ...
Redis stopped
[root@redisA ~]#
```
2）在服务器52主机，查看复制信息
```shell
 [root@redisB ~]# redis-cli -h 192.168.4.52 -p 6352
192.168.4.52:6352> info replication
# Replication
role:master  //角色是master
connected_slaves:0
……
……
```
# 4. 使用RDB文件恢复数据
## 4.1 问题
- 要求如下：
- 启用RDB
- 设置存盘间隔为120秒且10个key改变数据自动存盘
- 备份RDB文件
- 删除数据
- 使用RDB文件恢复数据

## 4.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：使用RDB文件恢复数据**

RDB介绍：
Redis数据库文件，全称Reids DataBase
数据持久化方式之一
在指定时间间隔内，将内存中的数据集快照写入硬盘
术语叫Snapshot快照
恢复时，将快照文件直接读到内存里

相关配置参数
文件名
dbfilename “dump.rdb” 文件名

数据从内存保存到硬盘的频率
save 900 1 900秒内且有1个key改变
save 300 10 300秒内且有10个key改变
save 60 10000 60秒内且有10000个key改变
```shell
[root@redisA ~]# vim /etc/redis/6379.conf
dbfilename dump.rdb
save 900 1        
#save 300 10 //注释原有设置
save 120 10 //时间修改为 120秒
save 60 10000
：wq
[root@redisA ~]#     /etc/init.d/redis_6379 stop  //停止服务
Stopping ...
Waiting for Redis to shutdown ...
Redis stopped
[root@redisA ~]#
[root@redisA ~]# rm –rf  /var/lib/redis/6379/* //清空数据库目录
[root@redisA ~]# /etc/init.d/redis_6379 start //启动服务
Starting Redis server...
[root@redisA ~]#
[root@redisA ~]# ls /var/lib/redis/6379  //此时，查看数据库目录下没有dump.rdb文件
[root@redisA ~]# 
[root@redisA ~]# redis-cli -h 192.168.4.51  -p 6351  -a 123456  //连接服务，在200秒内存储10个变量，就会自动在数据库目录下创建dump.rdb 文件
192.168.4.51:6351> set v1 k1
OK
192.168.4.51:6351> set v2 k1
OK
192.168.4.51:6351> set v3 k1
OK
192.168.4.51:6351> set v4 k1
OK
192.168.4.51:6351> set v45 k1
OK
192.168.4.51:6351> set v46 k1
OK
192.168.4.51:6351> set v7 k1
OK
192.168.4.51:6351> set v8 k1
OK
192.168.4.51:6351> set v9 k1
OK
192.168.4.51:6351> set v10 k1
OK
192.168.4.51:6351> keys *
 1) "v2"
 2) "v9"
 3) "v10"
 4) "v45"
 5) "v4"
 6) "v1"
 7) "v46"
 8) "v8"
 9) "v7"
10) "v3"
192.168.4.51:6351>exit
[root@redisA ~]# ls /var/lib/redis/6379  //此时，查看数据库目录下有dump.rdb文件
dump.rdb
[root@redisA ~]#
```
备份数据
```shell
[root@redisA ~]# cd /var/lib/redis/6379/
[root@redisA 6379]# ls
dump.rdb  
[root@redisA 6379]# cp dump.rdb  /tmp/dump.rdb    //备份dump.rdb文件
[root@redisA 6379]# scp  /tmp/dump.rdb  root@192.168.4.56:/root/ //传递备份文件给目标主机
```
删除数据 （56主机模拟误删除数据）
```shell
[root@redis56 ~]# redis-cli -h 192.168.4.56 –p 6356        //连接服务
192.168.4.56:6356> flushall
OK
192.168.4.51:6379> keys *        //已经没有数据
(empty list or set)
192.168.4.56:6356> exit
[root@redis56 ~]#
```
恢复数据(56主机使用备份文件恢复数据)
```shell
[root@redis56 ~]# /etc/init.d/redis_6379 stop  //停止服务
Stopping ...
Waiting for Redis to shutdown ...
Redis stopped
[root@redis56 ~]# 
[root@redis56 ~]# rm  -rf  /var/lib/redis/6379/*  //清空数据库目录
[root@redis56 ~]# cp  /tmp/dump.rdb   /var/lib/redis/6379/ //拷贝备份文件到数据库目录下
[root@redis56 ~]# /etc/init.d/redis_6379  start  //    启动服务
Starting Redis server...
[root@redis56 ~]# redis-cli -h 192.168.4.56 –p 6356 //访问服务
192.168.4.56:6356> keys *  //查看数据
 1) "v7"
 2) "v46"
 3) "v45"
 4) "v8"
 5) "v4"
 6) "v2"
 7) "v1"
 8) "v3"
 9) "v9"
10) "v10"
192.168.4.56:6356>
```
# 5. 使用AOF文件恢复数据
## 5.1 问题
- 具体要求如下：
- 启用AOF
- 备份AOF文件
- 删除数据
- 使用AOF文件恢复数据

## 5.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：使用AOF文件恢复数据**

1）修改配置文件
```shell
[root@redisA ~]# redis-cli -h 192.168.4.51 –p 6351 -a 123456 //连接服务
192.168.4.51:6351>config  set   appendonly yes     //启用aof，默认no
192.168.4.51:6351> config  rewrite //写进配置文件
192.168.4.51:6351> save
192.168.4.51:6351> exit
[root@redisA ~]# ls  /var/lib/redis/6379/   //会出现appendonly.aof文件
appendonly.aof  dump.rdb  
[root@redisA ~ ]# 
```
2）备份AOF文件
```shell
[root@redisA ~]# cd /var/lib/redis/6379/
[root@redisA 6379]# cp appendonly.aof /tmp/appendonly.aof
[root@redisA 6379]# scp /tmp/appendonly.aof  root@192.168.4.57:/root/  //传递备份文件给目标主机
```
3）删除数据（在57主机 默认数据误删除）
```shell
[root@redis57 ~]# redis-cli -h 192.168.4.57 -p 6357  //连接服务
192.168.4.57:6357> flushall  //清除数据
OK
192.168.4.57:6357> keys * //查看数据
(empty list or set)
192.168.4.57:6357> exit
[root@redis57  ~ ]# 
```
4) 使用AOF文件恢复数据
```shell
[root@redis57 ~]# vim +673 /etc/redis/6379.conf
appendonly  yes  //启用AOF
:wq
[root@redis57 ~]#
[root@redis57 ~]# /etc/init.d/redis_6379 stop  //停止服务
Stopping ...
Waiting for Redis to shutdown ...
Redis stopped
[root@redis57 ~]# 
[root@redis57 ~]#  /etc/init.d/redis_6379  start //启动服务
Starting Redis server...
[root@redis57 ~]# 
[root@redis57 ~]# rm  -rf  /var/lib/redis/6379/* //删除没有数据的文件
[root@redis57 ~]# cp  /root/appendolny.aof /var/lib/redis/6379/  //拷贝文件
[root@redis57 ~]# /etc/init.d/redis_6379  start  //启动服务
Starting Redis server...
[root@redis57 ~]# redis-cli -h 192.168.4.57 -p 6357 //连接服务
192.168.4.57:6357> keys *  //查看数据
 1) "v9"
 2) "v5"
 3) "v8"
 4) "v2"
 5) "v1"
 6) "v4"
 7) "v10"
 8) "v6"
 9) "v7"
10) "v3"
192.168.4.57:6357>
```
# 6. 字符类型
## 6.1 问题
1. 练习命令的使用，具体命令如下：
set getrange strlen append setbit bitcount
decr decrby incr incrby incrbyfloat

## 6.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：string 字符串**

设置key及值，过期时间可以使用秒或毫秒为单位

setrange key offset value
```shell
192.168.4.56:6356> set  x 9 ex 10 //单位秒
OK
192.168.4.56:6356> 
192.168.4.56:6356> set  y 29 px 10 //单位毫秒
OK
192.168.4.56:6356> 
192.168.4.56:6356> set  y 39 NX //不存在赋值
OK
192.168.4.56:6356> get y //变量值没变
"39"
192.168.4.56:6356> 
192.168.4.56:6356> set  y 49 xx //变量存在赋值
OK
192.168.4.56:6356> get y //变量变了
"49"
192.168.4.56:6356>
```
2) 从偏移量开始复写key的特定位的值
```shell
192.168.4.51:6351> set  first  "hello world"
OK
192.168.4.51:6351> setrange  first  6  "Redis"     //改写为hello Redis
(integer) 11
192.168.4.51:6351> get first
"hello Redis"
```
3) strlen key，统计字串长度
```shell
192.168.4.51:6379> strlen first
(integer) 11
```
4) append key value 存在则追加，不存在则创建key及value，返回key长度
```shell
192.168.4.51:6379> append myname jacob
(integer) 5
```
5) setbit key offset value 对key所存储字串，设置或清除特定偏移量上的位(bit)，value值可以为1或0，offset为0~2^32之间，key不存在，则创建新key
```shell
192.168.4.51:6379> setbit  bit  0  1          //设置bit第0位为1
(integer) 0
192.168.4.51:6379> setbit  bit  1  0          //设置bit第1位为0 
(integer) 0
```
6) bitcount key 统计字串中被设置为1的比特位数量
```shell
192.168.4.51:6379> setbit  bits 0 1        //0001
(integer) 0
192.168.4.51:6379> setbit  bits 3 1        //1001
(integer) 0
192.168.4.51:6379> bitcount  bits            //结果为2
(integer) 2
```
记录网站用户上线频率，如用户A上线了多少天等类似的数据，如用户在某天上线，则使用setbit，以用户名为key，将网站上线日为offset，并在该offset上设置1，最后计算用户总上线次数时，使用bitcount用户名即可，这样即使网站运行10年，每个用户仅占用10*365比特位即456字节
```shell
192.168.4.51:6379> setbit  peter  100  1        //网站上线100天用户登录了一次
(integer) 0
192.168.4.51:6379> setbit  peter  105  1        //网站上线105天用户登录了一次
(integer) 0
192.168.4.51:6379> bitcount  peter
(integer) 2
```
7) decr key 将key中的值减1，key不存在则先初始化为0，再减1
```shell
192.168.4.51:6379> set z 10
OK
192.168.4.51:6379> decr z
(integer) 9
192.168.4.51:6379> decr z
(integer) 8
192.168.4.51:6379> decr bb
(integer) -1
192.168.4.51:6379> decr bb
(integer) -2
```
8) decrby key decrement 将key中的值，减去decrement
```shell
192.168.4.51:6379> set count 100
OK
192.168.4.51:6379> DECRBY cc 20    //定义每次减少20（步长）
(integer) -20
192.168.4.51:6379> DECRBY cc 20
(integer) -40
```
9) getrange key start end 返回字串值中的子字串，截取范围为start和end，负数偏移量表示从末尾开始计数，-1表示最后一个字符，-2表示倒数第二个字符
```shell
192.168.4.51:6379> set x 123456789
OK
192.168.4.51:6379> getrange x -5 -1
"56789"
192.168.4.51:6379> getrange x 0 4
"12345"
```
10) incr key 将key的值加1，如果key不存在，则初始为0后再加1，主要应用为计数器
```shell
192.168.4.51:6379> set page 20
OK
192.168.4.51:6379> incr page
(integer) 21
```
11) incrby key increment 将key的值增加increment
```shell
192.168.4.51:6379> set x 10
OK
192.168.4.51:6379> incr x
(integer) 11
192.168.4.51:6379> incr x
(integer) 12
```
12) incrbyfloat key increment 为key中所储存的值加上浮点数增量 increment
```shell
192.168.4.51:6379> set num 16.1
OK
192.168.4.51:6379> incrbyfloat num 1.1
"17.2"
```
13）字符类型实践

Redis 对于键的命名并没有强制的要求，但比较好的实践是用“对象类型:对象ID:对象属性”来命名一个键，如使用键【user:1:friends】来存储ID为1的用户的好友列表。

例：如果你正在编写一个博客网站，博客的一个常见的功能是统计文章的访问量，我们可以为每篇文章使用一个名为【post:文章ID:page.view】的键来记录文章的访问量，每次访问文章的时候使用INCR命令使相应的键值递增。
```shell
# 有用户访问文章ID号为42的博文，则将其访问计数加1
127.0.0.1:6379> INCR post:42:page.view
(integer) 1
127.0.0.1:6379> GET post:42:page.view
"1"
127.0.0.1:6379> INCR post:42:page.view
(integer) 2
127.0.0.1:6379> GET post:42:page.view
"2"
```
# 7. list 列表
## 7.1 问题
练习命令使用，具体如下：
lpush llen lrange lpop
lindex lset rpush rpop

## 7.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：list 列表**

1) lpush key value [value…] 将一个或多个值value插入到列表key的表头，Key不存在，则创建key
```shell
192.168.4.51:6379> lpush list a b c        //list值依次为c b a
(integer) 3
```
2) lrange key start stop 从开始位置读取key的值到stop结束
```shell
192.168.4.51:6379> lrange list 0 2        //从0位开始，读到2位为止
1) "c"
2) "b"
3) "a"
192.168.4.51:6379> lrange list 0 -1    //从开始读到结束为止
1) "c"
2) "b"
3) "a"
192.168.4.51:6379> lrange list 0 -2        //从开始读到倒数第2位值
1) "c"
2) "b"
```
3) lpop key 移除并返回列表头元素数据，key不存在则返回nil
```shell
192.168.4.51:6379> lpop list        //删除表头元素，可以多次执行
"c"
192.168.4.51:6379>  LPOP list
"b"
```
4) llen key 返回列表key的长度
```shell
192.168.4.51:6379>  llen list
(integer) 1
```
5) lindex key index 返回列表中第index个值
```shell
192.168.4.51:6379> lindex  list  1
"c"
```
6) lset key index value 将key中index位置的值修改为value
```shell
192.168.4.51:6379> lpush list a b c d 
(integer) 5
192.168.4.51:6379> lset list 3 test        //将list中第3个值修改为test
OK
```
7) rpush key value [value…] 将value插入到key的末尾
```shell
192.168.4.51:6379> rpush list3  a b c    //list3值为a b c
(integer) 3
192.168.4.51:6379> rpush list3 d    //末尾插入d
(integer) 4
```
8) rpop key 删除并返回key末尾的值
```shell
192.168.4.51:6379> RPOP list3 
"d"
```
9）列表类型实践 记录最新的10篇博文
```shell
127.0.0.1:6379> LPUSH posts:list 11 12 13
(integer) 3
127.0.0.1:6379> LRANGE posts:list 0 -1
1) "13"
2) "12"
3) "11"
```
# 8. 散列类型
## 8.1 问题
练习命令使用，具体如下：
hset hmset hgetall hkeys hvals
hget hmget hdel

## 8.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：hash表**

1）hset key field value 将hash表中field值设置为value
```shell
192.168.4.51:6379> hset site google 'www.g.cn'
(integer) 1
192.168.4.51:6379> hset site baidu 'www.baidu.com'
(integer) 1
```
2) hget key filed 获取hash表中field的值
```shell
192.168.4.51:6379> hget site google
"www.g.cn"
```
3) hmset key field value [field value…] 同时给hash表中的多个field赋值
```shell
192.168.4.51:6379> hmset site google www.g.cn  baidu www.baidu.com
OK
```
4) hmget key field [field…] 返回hash表中多个field的值
```shell
192.168.4.51:6379> hmget site google baidu
1) "www.g.cn"
2) "www.baidu.com"
```
5) hkeys key 返回hash表中所有field名称
```shell
192.168.4.51:6379> hmset site google www.g.cn baidu www.baidu.com
OK
192.168.4.51:6379> hkeys  site
1) "google"
2) "baidu"
```
6) hgetall key 返回hash表中所有key名和对应的值列表
```shell
192.168.4.51:6379> hgetall site
1) "google"
2) "www.g.cn"
3) "baidu"
4) "www.baidu.com"
```
7) hvals key 返回hash表中所有key的值
```shell
192.168.4.51:6379> hvals site
1) "www.g.cn"
2) "www.baidu.com"
```
8) hdel key field [field…] 删除hash表中多个field的值，不存在则忽略
```shell
192.168.4.51:6379> hdel  site  google  baidu
(integer) 2
```
9）散列类型实践

将文章ID号为10的文章以散列类型存储在Redis中
```shell
127.0.0.1:6379> HSET post:10 title 例解Python
(integer) 1
127.0.0.1:6379> HGETALL post:10
1) "title"
2) "\xe4\xbe\x8b\xe8\xa7\xa3Python"
127.0.0.1:6379> HSET post:10 author ZhangZhiGang
(integer) 1
127.0.0.1:6379> HMSET post:10 date 2021-05-01 summary 'Python Programming'
OK
127.0.0.1:6379> HGETALL post:10
1) "title"
2) "\xe4\xbe\x8b\xe8\xa7\xa3Python"
3) "author"
4) "ZhangZhiGang"
5) "date"
6) "2021-05-01"
7) "summary"
```
# 9. 集合类型
## 9.1 问题
## 9.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：练习无序集合类型命令**
```shell
127.0.0.1:6379> SADD letters a b c(integer) 3​127.0.0.1:6379> SADD letters b c d(integer) 1​127.0.0.1:6379> SMEMBERS letters1) "d"2) "b"3) "a"4) "c"​127.0.0.1:6379> SREM letters a c(integer) 2​127.0.0.1:6379> SMEMBERS letters1) "d"2) "b"
127.0.0.1:6379> SISMEMBER letters a(integer) 0​127.0.0.1:6379> SISMEMBER letters b(integer) 1
127.0.0.1:6379> SADD s1 a b c(integer) 3​127.0.0.1:6379> SADD s2 b c d(integer) 3​127.0.0.1:6379> SINTER s1 s21) "b"2) "c"​127.0.0.1:6379> SUNION s1 s21) "a"2) "c"3) "b"4) "d"​127.0.0.1:6379> SDIFF s1 s21) "a"
127.0.0.1:6379> SCARD letters(integer) 2
# 在集合s1中随机取出两个不同元素。127.0.0.1:6379> SRANDMEMBER s1 21) "b"2) "c"​# 在集合s1中随机取出两个有可能相同元素。127.0.0.1:6379> SRANDMEMBER s1 -21) "c"2) "c"​127.0.0.1:6379> SRANDMEMBER s1 -21) "a"2) "b"
127.0.0.1:6379> SPOP s1"a"​127.0.0.1:6379> SMEMBERS s11) "b"2) "c"
127.0.0.1:6379> SADD post:10:tags python redis nginx(integer) 3​127.0.0.1:6379> SMEMBERS post:10:tags1) "python"2) "nginx"3) "redis"
···
**步骤二：练习有序集合类型命令**

说明:
```shell
127.0.0.1:6379> ZADD scores 88 tom 90 jerry 75 bob 92 alice(integer) 4​127.0.0.1:6379> ZRANGE scores 0 -11) "bob"2) "tom"3) "jerry"4) "alice"​127.0.0.1:6379> ZRANGE scores 0 -1 WITHSCORES1) "bob"2) "75"3) "tom"4) "88"5) "jerry"6) "90"7) "alice"8) "92"​127.0.0.1:6379> ZADD scores 85 jerry(integer) 0​127.0.0.1:6379> ZRANGE scores 0 -1 WITHSCORES1) "bob"2) "75"3) "jerry"4) "85"5) "tom"6) "88"7) "alice"8) "92"
127.0.0.1:6379> ZSCORE scores tom"88"
127.0.0.1:6379> ZRANGEBYSCORE scores 80 90 WITHSCORES1) "jerry"2) "85"3) "tom"4) "88"
127.0.0.1:6379> ZINCRBY scores 3 bob"78"​127.0.0.1:6379> ZSCORE scores bob"78"
127.0.0.1:6379> ZCARD scores(integer) 4
127.0.0.1:6379> ZCOUNT scores 80 90(integer) 2
127.0.0.1:6379> ZREM scores bob(integer) 1
127.0.0.1:6379> ZRANK scores tom   # 获取tom的排名(integer) 1   # 升序排列，从0开始计数​127.0.0.1:6379> ZREVRANK scores alice   # 获取alice的排名(integer) 0   # 降序排列，从0开始计数
127.0.0.1:6379> ZADD posts:page.view 0 post:10:page.view(integer) 1​127.0.0.1:6379> ZINCRBY posts:page.view 1 post:10:page.view"1"​127.0.0.1:6379> ZRANGE posts:page.view 0 -1 WITHSCORES1) "post:10:page.view"2) "1"
···

# Exercise
## 1 简述redis主从复制工作原理
1）slave向master发送sync命令
2）master启动后台存盘进程，并收集所有修改数据命令
3）master完成后台存盘后，传送整个数据文件到slave
4）slave接收数据文件，加载到内存中完成首次完全同步
5） 后续有新数据产生时，master继续将新的数据收集到的修改命令依次传给slave，完成同步

## 2 简述redis支持的持久化方式
1）RDB（默认）
2）AOF

RDB介绍:
Redis数据库文件，全称 Redis DataBase
数据持久化方式之一
按照指定时间间隔，将内存中的数据集快照写入硬盘

AOF介绍：
Append Only File
记录redis服务所有写操作
不断的将新的写操作，追加到文件的末尾
使用cat命令可以查看文件内容

## 3 简述RDB持久化的默认存盘设置
save 900 1 //15分钟内且有1个key改变自动存盘
save 300 10 //5分钟内且有10个key改变自动存盘
save 60 10000 //1分钟内且有10000个key改变自动存盘

## 4 简述AOF文件记录写操作的方式
appendfsync always //时时记录，并完成磁盘同步
appendfsync everysec //每秒记录一次，并完成磁盘同步
appendfsync no //写入aof ，不执行磁盘同步

## 5 简述redis的数据类型。
Redis常用数据类型：
string字符
list列表
hash表

> 如有侵权，请联系作者删除
