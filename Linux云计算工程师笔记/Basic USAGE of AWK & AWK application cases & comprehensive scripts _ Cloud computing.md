@[TOC]( Basic USAGE of AWK & AWK application cases & comprehensive scripts | Cloud computing )

---
# 1 案例1：使用awk提取文本
## 1.1 问题
本案例要求使用awk工具完成下列过滤任务：

- 练习awk工具的基本用法
- 提取本机的网卡流量、根分区剩余容量、获取SSH远程失败的IP地址
- 格式化输出/etc/passwd文件中的用户名、UID、宿主目录信息

## 1.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：awk文本过滤的基本用法**

1）基本操作方法

格式：awk [选项] '[条件]{指令}' 文件

其中，print 是最常用的编辑指令；若有多条编辑指令，可用分号分隔。

Awk过滤数据时支持仅打印某一列，如第2列、第5列等。

处理文本时，若未指定分隔符，则默认将空格、制表符等作为分隔符。

直接过滤文件内容：
```shell
[root@svr5 ~]# cat test.txt 
hello the world
welcome to beijing
[root@svr5 ~]# awk '{print $1,$3}' test.txt        //打印文档第1列和第3列
hello world
welcome beijing
```
结合管道过滤命令输出：
```shell
[root@svr5 ~]# df -h | awk '{print $4}'        //打印磁盘的剩余空间
```
2）选项 -F 可指定分隔符

输出passwd文件中以分号分隔的第1、7个字段，显示的不同字段之间以逗号隔开，操作如下：
```shell
[root@svr5 ~]# awk -F: '{print $1,$7}' /etc/passwd
root /bin/bash
bin /sbin/nologin
daemon /sbin/nologin
adm /sbin/nologin
lp /sbin/nologin
… …
```
awk还识别多种单个的字符，比如以“:”或“/”分隔，输出第1、10个字段：
```shell
[root@svr5 ~]# awk -F [:/] '{print $1,$10}' /etc/passwd
root bash
bin nologin
daemon nologin
adm sbin
… …
```
awk常用内置变量：
$0 文本当前行的全部内容
$1 文本的第1列
$2 文件的第2列
$3 文件的第3列，依此类推
NR 文件当前行的行号
NF 文件当前行的列数（有几列）

输出每次处理行的行号，以及当前行以“:”分隔的字段个数（有几列）：
```shell
[root@svr5 ~]# awk -F: '{print NR,NF}' passwd.txt
1 7
2 7
3 7
.. ..
```
2）awk的print指令不仅可以打印变量，还可以打印常量
```shell
[root@svr5 ~]# awk -F: '{print $1,"的解释器:",$7}' /etc/passwd
root 的解释器: /bin/bash
bin 的解释器: /sbin/nologin
… …
```
**步骤二：利用awk提取本机的网络流量、根分区剩余容量、获取远程失败的IP地址**

1）提取IP地址

分步实现的思路及操作参考如下——

通过ifconfig eth0查看网卡信息，其中包括网卡流量：
```shell
[root@svr5 ~]# ifconfig eth0
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.4.21  netmask 255.255.255.0  broadcast 192.168.4.255
        inet6 fe80::fa64:c143:ad6a:5159  prefixlen 64  scopeid 0x20<link>
        ether 52:54:00:b3:11:11  txqueuelen 1000  (Ethernet)
        RX packets 313982  bytes 319665556 (304.8 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 51809  bytes 40788621 (38.8 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
RX为接收的数据量，TX为发送的数据量。packets以数据包的数量为单位，bytes以字节为单位：
```shell
[root@svr5 ~]# ifconfig eth0 | awk '/RX p/{print $5}'    //过滤接收数据的流量
319663094
[root@svr5 ~]# ifconfig eth0 | awk '/TX p/{print $5}'     //过滤发送数据的流量
40791683
```
2）提取根分区剩余容量

分步实现的思路及操作参考如下——

通过df命令查看根分区的使用情况，其中包括剩余容量：
```shell
[root@svr5 ~]# df -h /
文件系统             容量     已用     可用     已用%     挂载点
/dev/sda2         19G         7.2G     11G         40%         /
```
输出上述结果中最后一行的第4列：
```shell
[root@svr5 ~]# df -h / | tail -1 | awk '{print $4}'
11G
```
或者直接在awk中使用正则：
```shell
[root@svr5 ~]# df -h | awk '/\/$/{print $4}'
11G
```
3）根据/var/log/secure日志文件，过滤远程连接密码失败的IP地址
```shell
[root@svr5 ~]# awk '/Failed/{print $11}' /var/log/secure
192.168.2.254
192.168.2.100
... ...
```
**步骤三：格式化输出/etc/passwd文件**

1）awk处理的时机

awk会逐行处理文本，支持在处理第一行之前做一些准备工作，以及在处理完最后一行之后做一些总结性质的工作。在命令格式上分别体现如下：
```shell
awk  [选项]  '[条件]{指令}'  文件
awk  [选项]  ' BEGIN{指令} {指令} END{指令}'  文件
```
- BEGIN{ } 行前处理，读取文件内容前执行，指令执行1次
- { } 逐行处理，读取文件过程中执行，指令执行n次
- END{ } 行后处理，读取文件结束后执行，指令执行1次
只做预处理的时候，可以没有操作文件，比如：
```shell
[root@svr5 ~]# awk 'BEGIN{A=24;print A*2}'
[root@svr5 ~]# awk 'BEGIN{print x+1}'           #x可以不定义，直接用，默认值位0
[root@svr5 ~]# awk 'BEGIN{print 3.2+3.5}'
```

举个例子（统计系统中使用bash作为登录Shell的用户总个数）：

a.预处理时赋值变量x=0
b.然后逐行读入/etc/passwd文件，如果发现登录Shell是/bin/bash则x加1
c.全部处理完毕后，输出x的值即可。相关操作及结果如下：
```shell
[root@svr5 ~]# awk 'BEGIN{x=0}/bash$/{x++} END{print x}' /etc/passwd
29
```
2）格式化输出/etc/passwd文件

要求: 格式化输出passwd文件内容时，要求第一行为列表标题，中间打印用户的名称、UID、家目录信息，最后一行提示一共已处理文本的总行数，如图-1所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/31ec411a20184419a379693b0e166dcf.png)
图-1

3）根据实现思路编写、验证awk过滤语句

输出信息时，可以使用“\t”显示Tab制表位：
```shell
[root@svr5 ~]# awk -F: 'BEGIN{print "User\tUID\tHome"} \
                                {print $1 "\t"  $3  "\t"  $6}     \
                             END{print "Total",NR,"lines."}' /etc/passwd
User    UID     Home
root    0       /root
bin     1       /bin
daemon  2       /sbin
adm     3       /var/adm
lp      4       /var/spool/lpd
sync    5       /sbin
.. ..
Total 67 lines.
```
# 2. awk处理条件
## 2.1 问题
本案例要求使用awk工具完成下列过滤任务，注意awk处理条件的设置：

- 列出UID间于1~1000的用户详细信息
- 输出/etc/hosts文件内以127或192开头的记录
- 列出100以内整数中7的倍数或是含7的数

## 2.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：认识awk处理条件的设置**

1）使用正则设置条件

输出其中以bash结尾的完整记录：
```shell
[root@svr5 ~]# awk -F: '/bash$/{print}' /etc/passwd
root:x:0:0:root:/root:/bin/bash
```
输出包含root的行数据：
```shell
[root@svr5 ~]# awk -F: '/root/' /etc/passwd
```
输出root或adm账户的用户名和UID信息：
```shell
[root@svr5 ~]# awk -F: '/^(root|adm)/{print $1,$3}' /etc/passwd
root 0
adm 3
```
输出账户名称包含root的基本信息（第1列包含root）：
```shell
[root@svr5 ~]# awk -F: '$1~/root/' /etc/passwd
```
输出其中登录Shell不以nologin结尾（对第7个字段做!~反向匹配）的用户名、登录Shell信息：
```shell
[root@svr5 ~]# awk -F: '$7!~/nologin$/{print $1,$7}' /etc/passwd
root /bin/bash
sync /bin/sync
shutdown /sbin/shutdown
```
2）使用数值/字符串比较设置条件

比较符号：==(等于) !=（不等于） >（大于）
\>=（大于等于） <（小于） <=（小于等于）

输出第3行（行号NR等于3）的用户记录：
```shell
[root@svr5 ~]# awk -F: 'NR==3{print}' /etc/passwd
```
输出账户UID大于等于1000的账户名称和UID信息：
```shell
[root@svr5 ~]# awk -F: '$3>=1000{print $1,$3}' /etc/passwd
tom 1000
jerry 1001
```
输出账户UID小于10的账户名称和UID信息：
```shell
[root@svr5 ~]# awk -F: '$3<10{print $1,$3}' /etc/passwd
root 0
bin 1
daemon 2
adm 3
lp 4
sync 5
shutdown 6
halt 7
mail 8
```
输出用户名为“root”的行：
```shell
[root@svr5 ~]# awk -F: '$1=="root"' /etc/passwd
root:x:0:0:root:/root:/bin/bash
```
3）逻辑测试条件

输出账户UID大于10并且小于20的账户信息：
```shell
[root@svr5 ~]# awk -F: '$3>10 && $3<20' /etc/passwd
operator:x:11:0:operator:/root:/sbin/nologin
games:x:12:100:games:/usr/games:/sbin/nologin
ftp:x:14:50:FTP User:/var/ftp:/sbin/nologin
```
输出账户UID大于1000或者账户UID小于10的账户信息：
```shell
[root@svr5 ~]# awk -F: '$3>1000 || $3<10' /etc/passwd
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/spool/mail:/sbin/nologin
varnish:x:1001:1001::/home/varnish:/sbin/nologin
nginx:x:1002:1002::/home/nginx:/sbin/nologin
```
4）数学运算
```shell
[root@svr5 ~]# awk 'BEGIN{x++;print x}'
1
[root@svr5 ~]# awk 'BEGIN{x=8;print x+=2}'
10
[root@svr5 ~]# awk 'BEGIN{x=8;x--;print x}'
7
[root@svr5 ~]# awk 'BEGIN{print 2+3}'
5
[root@svr5 ~]# awk 'BEGIN{print 2*3}'
6
[root@svr5 ~]# awk 'BEGIN{print 2*3}'
6
[root@svr5 ~]# awk 'BEGIN{ print 23%8}'
7
[root@svr5 ~]# seq  200 | awk  '$1%3==0'       //找200以内3的倍数
… …
```
**步骤二：完成任务要求的awk过滤操作**

1）列出UID间于1~1000的用户详细信息：
```shell
[root@svr5 ~]# awk -F: '$3>=1 && $3<=1000' /etc/passwd
```
2）输出/etc/hosts映射文件内以127或者192开头的记录：
```shell
[root@svr5 ~]# awk  '/^(127|192)/' /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
192.168.4.5  svr5.tarena.com svr5
```
3）列出100以内整数中7的倍数或是含7的数：
```shell
[root@svr5 ~]# seq 100 | awk '$1%7==0||$1~/7/'
7
14
17
21
27
28
35
37
42
47
.. ..
```
# 3. awk数组
## 3.1 问题
本案例要求了解awk数组的使用

**步骤一：awk数组**

1）数组的语法格式

数组是一个可以存储多个值的变量，具体使用的格式如下：
定义数组的格式：数组名[下标]=元素值
调用数组的格式：数组名[下标]
遍历数组的用法：for(变量 in 数组名){print 数组名[变量]}。
```shell
[root@svr5 ~]# awk 'BEGIN{a[0]=11;a[1]=88;print a[1],a[0]}'
88 11
[root@svr5 ~]# awk 'BEGIN{a++;print a}'
1
[root@svr5 ~]# awk 'BEGIN{a0++;print a0}'
1
[root@svr5 ~]# awk 'BEGIN{a[0]++;print a[0]}'
1
[root@svr5 ~]# awk 'BEGIN{a[0]=0;a[1]=11;a[2]=22; for(i in a){print i,a[i]}}'
0 0
1 11
2 22
```
注意，awk数组的下标除了可以使用数字，也可以使用字符串，字符串需要使用双引号：
```shell
[root@svr5 ~]# awk 'BEGIN{a["hehe"]=11;print a["hehe"]}'
11
```
# 4 案例4：awk扩展应用
## 4.1 问题
本案例要求使用awk工具完成下列两个任务：

分析Web日志的访问量排名，要求获得客户机的地址、访问次数，并且按照访问次数排名

## 4.2 方案
1）awk统计Web访问排名

在分析Web日志文件时，每条访问记录的第一列就是客户机的IP地址，其中会有很多重复的IP地址。因此只用awk提取出这一列是不够的，还需要统计重复记录的数量并且进行排序。

通过awk提取信息时，利用IP地址作为数组下标，每遇到一个重复值就将此数组元素递增1，最终就获得了这个IP地址出现的次数。

针对文本排序输出可以采用sort命令，相关的常见选项为-r、-n、-k。其中-n表示按数字顺序升序排列，而-r表示反序，-k可以指定按第几个字段来排序。

## 4.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：统计Web访问量排名**

分步测试、验证效果如下所述。

1）提取IP地址及访问量
```shell
[root@svr5 ~]# awk '{ip[$1]++} \
>  END{for(i in ip) {print ip[i],i }}' /var/log/httpd/access_log
4  127.0.0.1
17 192.168.4.5
13 192.168.4.110
.. ..
```
2）对第1）步的结果根据访问量排名
```shell
[root@svr5 ~]# awk  '{ip[$1]++} END{for(i in ip) {print i,ip[i]}}' /var/log/httpd/access_log | sort -nr
17 192.168.4.5
13 192.168.4.110
4 127.0.0.1
.. ..
```

# 5. 编写监控脚本
## 5.1 问题
本案例要求编写脚本，实现计算机各个性能数据监控的功能，具体监控项目要求如下：

> CPU负载
网卡流量
内存剩余容量
磁盘剩余容量
计算机账户数量
当前登录账户数量
计算机当前开启的进程数量
本机已安装的软件包数量

## 5.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：准备工作**

1）查看性能数据的命令
```shell
[root@svr5 ~]# uptime                            //查看CPU负载
[root@svr5 ~]# ifconfig eth0                    //查看网卡流量
[root@svr5 ~]# free                            //查看内存信息
[root@svr5 ~]# df                                //查看磁盘空间
[root@svr5 ~]# wc -l /etc/passwd                //查看计算机账户数量
[root@svr5 ~]# who |wc -l                        //查看登录账户数量
[root@svr5 ~]# rpm -qa |wc -l                    //查看已安装软件包数量
```
**步骤二：编写参考脚本**

1）脚本内容如下：
```shell
[root@svr5 ~]# vim test.sh
#!/bin/bash
ip=`ifconfig eth0 | awk '/inet /{print $2}'`
echo "本地IP地址是:"$ip
cpu=`uptime | awk '{print $NF}'`            
#awk中NF为当前行的列数，$NF是最后一列
echo "本机CPU最近15分钟的负载是:"$cpu
net_in=`ifconfig eth0 | awk '/RX p/{print $5}'`
echo "入站网卡流量为:"$net_in
net_out=`ifconfig eth0 | awk '/TX p/{print $5}'`
echo "出站网卡流量为:"$net_out
mem=`free | awk '/Mem/{print $4}'`
echo "内存剩余容量为:"$mem
disk=`df | awk '/\/$/{print $4}'`
echo "根分区剩余容量为:"$disk
user=`cat /etc/passwd |wc -l`
echo "本地账户数量为:"$user
login=`who | wc -l`
echo "当前登陆计算机的账户数量为:"$login
process=`ps aux | wc -l`
echo "当前计算机启动的进程数量为:"$process
soft=`rpm -qa | wc -l`
echo "当前计算机已安装的软件数量为:"$soft
```

# 6. 编写安全检测脚本
## 6.1 问题
本案例要求编写脚本，防止远程ssh暴力破解密码，具体监控项目要求如下：

检测ssh登录日志，如果远程登陆账号名错误3次，则屏蔽远程主机的IP

检测ssh登录日志，如果远程登陆密码错误3次，则屏蔽远程主机的IP

## 6.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：准备工作**

1）过滤帐户名失败的命令(登陆日志文件为/var/log/secure)
```shell
[root@svr5 ~]# awk '/Invalid user/{print $10}' /var/log/secure
```
2）过滤密码失败的命令
```shell
[root@svr5 ~]# awk '/Failed password/{print $11}' /var/log/secure
```
**步骤二：编写参考脚本**

1）脚本内容如下：
```shell
[root@svr5 ~]# vim test.sh
#!/bin/bash
awk '/Failed password/{print $11}' /var/log/secure  | awk '{ip[$1]++}END{for(i in ip){print ip[i],i}}' | awk '$1>3{print $2}'
awk '/Invalid user/{print $10}' /var/log/secure  | awk '{ip[$1]++}END{for(i in ip){print ip[i],i}}' | awk '$1>3{print $2}'
```


# Exercise
## 1 简述awk工具的基本语法格式。

- 格式1： awk [选项] ‘[条件]{处理动作}’ 文件列表
- 格式2： 命令 | awk [选项] ‘[条件]{处理动作}’

## 2 简述awk工具常用的内置变量、各自的作用。
- $n：即$1、$2、$3……，表示指定分隔的第几个字段
- $0：保存当前读入的整行文本内容
- NF：记录当前处理行的字段个数（列数）
- NR：记录当前已读入行的数量（行数）
## 3 awk处理文本时，读文件前、读取文件内容中、读文件后后这三个环节是如何表示的？
- BEGIN{ } 文件前处理：awk没有读入行之前 要执行的动作； 一般对数据作初始化操作，可以单独使用。
- { } 行处理：对awk读入的每一行进行处理，可以单独使用。
- END{ }文件后处理：awk 把所有的行都处理完后要执行的动作，一般输出数据处理的结果。可以单独使用。
## 4 提取当前eth0网卡的IPv4地址及掩码信息。

查看测试文本：
```shell
[root@svr5 ~]# ip add list eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 00:0c:29:64:88:8e brd ff:ff:ff:ff:ff:ff
    inet 192.168.4.55/24 brd 192.168.4.255 scope global eth0
    inet 192.168.4.5/24 brd 192.168.4.255 scope global secondary eth0
    inet6 fe80::20c:29ff:fe64:888e/64 scope link 
       valid_lft forever preferred_lft forever
```
提取IPv4地址及掩码信息的操作及效果：
```shell
[root@svr5 ~]# ip add list eth0 | awk '/\<inet\>/{print $2}'
192.168.4.55/24
192.168.4.5/24
```
## 5 找出UID位于10~20之间的用户，输出用户名及对应的UID。
```shell
[root@svr5 ~]# awk -F: '$3>=10 && $3<=20{print $1":"$3}' /etc/passwd
uucp:10
operator:11
games:12
gopher:13
ftp:14 
```
## 6 利用awk工具统计使用bash作为解释器的用户数量。
使用NF内置变量找最后一列的内容，匹配bash即可让x+1：
```shell
[root@svr5 ~]# awk -F/ '$NF=="bash"{x++}END{print x}' /etc/passwd
```
## 7 在awk中是否可以使用数组，分别以什么构成？

可以使用数组，分别以 数组名、下标、值 三个部分构成

## 8 在linux中对文本的排序如何实现？

使用sort命令，比如abc.txt文本

另外还可以使用选项-n按数字升序排列 -k：针对指定的列进行排序 -r：反向排序
```shell
[root@svr5 ~]# sort –n abc.txt
```

> 如有侵权，请联系作者删除
