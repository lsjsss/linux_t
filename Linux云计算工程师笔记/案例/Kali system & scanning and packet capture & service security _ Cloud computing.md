@[TOC]( Kali system & scanning and packet capture & SSH basic protection & service security | Cloud computing )

---
# 1. 扫描与抓包分析
## 1.1 问题
本案例要求熟悉Linux主机环境下的常用安全工具，完成以下任务操作：

1. 使用nmap扫描来获取指定主机/网段的相关信息
2. 使用nmap执行脚本扫描
3. 使用tcpdump分析FTP访问中的明文交换信息

## 1.2 方案
Kali是基于Debian的Linux发行版，Kali Linux包含上百个安全相关工具

如：渗透测试、安全检测、密码安全、反向工程等，官网：kali.org。

准备实验环境，在真机执行命令命令初始化虚拟机。

**重要提示：kali虚拟机用户名为kali，密码为kali。**
```shell
#kali reset                    #初始化虚拟机
#virt-manager                  #打开kvm虚拟机管理器
```
修改网卡配置，《网络源》选择《private1：隔离网络》如图-1所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/06c86cc901a144d98aeeec6b2b7fdd81.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-1

给kali虚拟机配置IP地址：
```shell
$ ip  a  s                      #查看网卡设备名称（设备名）
$ nmcli  connection  show     #查看网络连接名称（网卡名）
#注意：仔细区分网卡名和设备名称，两个名称有可能不一致(正常情况),配置IP时注意！！！
$ sudo nmcli connection modify "Wired connection 1" \
ipv4.method manual \
ipv4.addr 192.168.4.40/24 \
autoconnect yes
#配置IP地址，autoconnect设置网卡开机自动激活
#\代表换行符
$ sudo nmcli connection up "Wired connection 1" 
```
## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：使用NMAP扫描来获取指定主机/网段的相关信息**

1）基本用法
```shell
基本用法：
# nmap  [扫描类型]  [选项]  <扫描目标 ...>
#常用的扫描类型
# -sS，TCP SYN扫描（半开）
# -sT，TCP 连接扫描（全开）
# -sU，UDP扫描
# -sP，ICMP扫描
# -A，目标系统全面分析
```
下面的实验请根据自己的实际情况进行测试，每个人的IP地址可能不一样！

2）检查192.168.4.5主机是否可以ping通（这里假设有192.168.4.5主机）
```shell
[kali@kali ~]$ sudo nmap  -sP  192.168.4.5
Starting Nmap 6.40 ( http://nmap.org ) at 2028-06-06 21:59 CST
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for host3 (192.168.4.5)
Host is up (0.00036s latency).
MAC Address: 52:54:00:71:07:76 (QEMU Virtual NIC)
Nmap done: 1 IP address (1 host up) scanned in 0.02 seconds
```
使用-n选项可以不执行DNS解析
```shell
[kali@kali ~]$ sudo nmap -n -sP  192.168.4.5
Starting Nmap 6.40 ( http://nmap.org ) at 2028-06-06 22:00 CST
Nmap scan report for 192.168.4.5
Host is up (0.00046s latency).
MAC Address: 52:54:00:71:07:76 (QEMU Virtual NIC)
Nmap done: 1 IP address (1 host up) scanned in 0.03 seconds
```
3）检查192.168.4.0/24网段内哪些主机可以ping通

[kali@kali ~]$ sudo nmap  -n  -sP  192.168.4.0/24
Starting Nmap 5.51 ( http://nmap.org ) at 2027-05-17 18:01 CST
Nmap scan report for 192.168.4.5
Host is up.
Nmap scan report for 192.168.4.7
Host is up.
Nmap scan report for 192.168.4.120
Host is up (0.00027s latency).
MAC Address: 00:0C:29:74:BE:21 (VMware)
Nmap scan report for 192.168.4.110
Host is up (0.00016s latency).
MAC Address: 00:50:56:C0:00:01 (VMware)
Nmap scan report for 192.168.4.120
Host is up (0.00046s latency).
MAC Address: 00:0C:29:DB:84:46 (VMware)
Nmap done: 256 IP addresses (5 hosts up) scanned in 3.57 seconds
```
4）检查目标主机所开启的TCP服务
```shell
[kali@kali ~]$ sudo nmap -sT 192.168.4.254
Starting Nmap 5.51 ( http://nmap.org ) at 2028-05-17 17:55 CST
Nmap scan report for 192.168.4.254
Host is up (0.00028s latency).
Not shown: 990 closed ports
PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
25/tcp  open  smtp
80/tcp  open  http
110/tcp open  pop3
111/tcp open  rpcbind
143/tcp open  imap
443/tcp open  https
993/tcp open  imaps
995/tcp open  pop3s
MAC Address: 00:0C:29:74:BE:21 (VMware)
Nmap done: 1 IP address (1 host up) scanned in 1.31 seconds
```
5）检查192.168.4.0/24网段内哪些主机开启了FTP、SSH服务
```shell
[kali@kali ~]$ sudo nmap -p 21-22 192.168.4.0/24
Starting Nmap 5.51 ( http://nmap.org ) at 2027-05-17 18:00 CST
Nmap scan report for 192.168.4.5
Host is up (0.000025s latency).
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
Nmap scan report for 192.168.4.7
Host is up.
PORT   STATE    SERVICE
21/tcp filtered ftp
22/tcp filtered ssh
Nmap scan report for 192.168.4.120
Host is up (0.00052s latency).
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
MAC Address: 00:0C:29:74:BE:21 (VMware)
Nmap scan report for pc110.tarena.com (192.168.4.110)
Host is up (0.00038s latency).
PORT   STATE  SERVICE
21/tcp closed ftp
22/tcp closed ssh
MAC Address: 00:50:56:C0:00:01 (VMware)
Nmap scan report for 192.168.4.120
Host is up (0.00051s latency).
PORT   STATE  SERVICE
21/tcp closed ftp
22/tcp closed ssh
MAC Address: 00:0C:29:DB:84:46 (VMware)
Nmap done: 256 IP addresses (5 hosts up) scanned in 4.88 seconds
```
6）检查目标主机所开启的UDP服务
```shell
[kali@kali ~]$ sudo nmap   -sU  192.168.4.5                #指定-sU扫描UDP
53/udp   open          domain
111/udp  open          rpcbind
```
7）全面分析目标主机192.168.4.100和192.168.4.5的操作系统信息
```shell
[kali@kali ~]$ sudo nmap -A 192.168.4.100,5
Starting Nmap 5.51 ( http://nmap.org ) at 2017-05-17 18:03 CST
Nmap scan report for 192.168.4.100                      #主机mail的扫描报告
Host is up (0.0016s latency).
Not shown: 990 closed ports
PORT    STATE SERVICE  VERSION
21/tcp  open  ftp      vsftpd 2.2.2
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rw-r--r--    1 0        0            1719 Aug 17 13:33 UserB.pub
| -rw-r--r--    1 0        0             122 Aug 13 05:27 dl.txt
| drwxr-xr-x    2 14       0            4096 Aug 13 09:07 pub
| -rw-rw-r--    1 505      505           170 Aug 17 13:18 tools-1.2.3.tar.gz
|_-rw-rw-r--    1 505      505           287 Aug 17 13:22 tools-1.2.3.tar.gz.sig
22/tcp  open  ssh      OpenSSH 5.3 (protocol 2.0)
| ssh-hostkey: 1024 86:be:d6:89:c1:2d:d9:1f:57:2f:66:d1:af:a8:d3:c6 (DSA)
|_2048 16:0a:15:01:fa:bb:91:1d:cc:ab:68:17:58:f9:49:4f (RSA)
25/tcp  open  smtp     Postfix smtpd
80/tcp  open  http     Apache httpd 2.4.10 ((Red Hat))
|_http-methods: No Allow or Public header in OPTIONS response (status code 302)
| http-title: 302 Found
|_Did not follow redirect to https://192.168.4.100//
110/tcp open  pop3     Dovecot pop3d
|_pop3-capabilities: USER CAPA UIDL TOP OK(K) RESP-CODES PIPELINING STLS SASL(PLAIN)
111/tcp open  rpcbind
MAC Address: 00:0C:29:74:BE:21 (VMware)
No exact OS matches for host (If you know what OS is running on it, see http://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=5.51%D=8/19%OT=21%CT=1%CU=34804%PV=Y%DS=1%DC=D%G=Y%M=000C29%TM=52
OS:11ED90%P=x86_64-redhat-linux-gnu)SEQ(SP=106%GCD=1%ISR=10B%TI=Z%CI=Z%II=I
OS:%TS=A)OPS(O1=M5B4ST11NW6%O2=M5B4ST11NW6%O3=M5B4NNT11NW6%O4=M5B4ST11NW6%O
OS:5=M5B4ST11NW6%O6=M5B4ST11)WIN(W1=3890%W2=3890%W3=3890%W4=3890%W5=3890%W6
OS:=3890)ECN(R=Y%DF=Y%T=40%W=3908%O=M5B4NNSNW6%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O
OS:%A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=
OS:0%Q=)T5(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0%
OS:S=A%A=Z%F=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(
OS:R=Y%DF=N%T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=
OS:N%T=40%CD=S)
Network Distance: 1 hop
Service Info: Host:  mail.tarena.com; OS: Unix
TRACEROUTE
HOP RTT     ADDRESS
1   1.55 ms 192.168.4.100
```
**步骤二：使用nmap执行脚本扫描**

1）准备一台Vsftpd服务器（192.168.4.5主机操作）
```shell
[root@proxy ~]# yum -y install vsftpd
[root@proxy ~]# systemctl restart vsftpd
[root@proxy ~]# useradd  tom
[root@proxy ~]# echo 123 | passwd --stdin tom
```
2）FTP相关扫描脚本（在kali主机操作）

相关脚本存放目录：/usr/share/nmap/scripts/。
```shell
[kali@kali ~]$ sudo nmap  --script=ftp-anon.nse  192.168.4.5  -p 21
#匿名访问扫描
[kali@kali ~]$ sudo nmap  --script=ftp-syst.nse  192.168.4.5  -p  21
#扫描ftp软件相关信息（如版本号，是否有带宽限制，超时时间等）
[kali@kali ~]$ sudo nmap  --script=ftp-vsftpd-backdoor.nse 192.168.4.5  -p 21
#后门扫描
[kali@kali ~]$ sudo nmap  --script=ftp-brute.nse  192.168.4.5  -p 21
#暴力破解密码
```
3）SSH相关扫描（在kali主机操作）
```shell
[kali@kali ~]$ sudo nmap  --script=ssh-brute.nse 192.168.4.5 -p 22
#暴力破解ssh密码
[kali@kali ~]$ sudo vi /tmp/users.lst                  #新建文件，存储账户信息
root
tom
[kali@kali ~]$ sudo vi /tmp/pass.lst                   #新建文件，存储密码信息
123456
654321
[kali@kali ~]$ sudo nmap  --script=ssh-brute.nse \
--script-args userdb=/tmp/users.lst,passdb=/tmp/pass.lst  192.168.4.5 -p 22
#使用自己创建的账户和密码本暴力破解ssh密码
```
在192.168.4.5主机可以查看日志
```shell
[root@proxy ~]# tail  /var/log/secure                   #查看日志
```
4）HTTP相关扫描（kali主机操作）

这里假设192.168.4.5有http服务。
```shell
[kali@kali ~]$ sudo nmap  --script=http-methods.nse  192.168.4.5  -p 80
#请求方法扫描（如get，post，header等）
[kali@kali ~]$ sudo nmap  --script=http-sql-injection.nse 192.168.4.5  -p  80
#SQL注入扫描
```
备注：SQL注入是指web应用程序对用户输入数据的合法性没有判断或过滤不严，攻击者可以在web应用程序中事先定义好的查询语句的结尾上添加额外的SQL语句，在管理员不知情的情况下实现非法操作，以此来实现欺骗数据库服务器执行非授权的任意查询，从而进一步得到相应的数据信息。

SQL注入是将Web页面的原URL、表单域或数据包输入的参数，修改拼接成SQL语句，传递给Web服务器，进而传给数据库服务器以执行数据库命令。

5）SMB相关扫描（kali主机操作）

这里假设有一台windows主机192.168.137.4。
```shell
[kali@kali ~]$ sudo nmap --script=smb-brute.nse 192.168.137.4
[kali@kali ~]$ sudo nmap --script=smb-brute.nse  \
--script-args=userdb=/密码本,passdb=/密码本  192.168.137.4  
```
6）暴力破解密码（kali主机操作）
```shell
$ sudo   john  --single  /etc/shadow              #破解傻瓜式密码
$ sudo   john   /etc/shadow                       #字典暴力破解（随时ctrl+c终止）
$ sudo   john  --wordlist=密码本   /etc/shadow   #使用自定义密码本破解
$ sudo   john  --show  /etc/shadow                #显示破解的密码
```
**步骤三：使用tcpdump分析FTP访问中的明文交换信息**

1）启用tcpdump命令行抓包（kali虚拟机操作）

执行tcpdump命令行，添加适当的过滤条件，只抓取访问主机192.168.4.5的21端口的数据通信 ，并转换为ASCII码格式的易读文本。

这里假设，192.168.4.5主机有vsftpd服务，如果没有需要提前安装并启动服务！！！

警告：案例中所有抓包命令都没有指定网卡，每位同学需要根据实际情况指定抓包网卡的名称。
```shell
[kali@kali ~]$ sudo tcpdump -i 网卡名称 -A host 192.168.4.5 and tcp port 21
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
.. ..                                            #进入等待捕获数据包的状态
#监控选项如下：
# -i，指定监控的网络接口（默认监听第一个网卡）
# -A，转换为 ACSII 码，以方便阅读
# -w，将数据包信息保存到指定文件
# -r，从指定文件读取数据包信息
#tcpdump的过滤条件：
# 类型：host（主机）、net（网段）、port（端口）、portrange（端口范围）
# 方向：src（源地址）、dst（目标地址）
# 协议：tcp、udp、ip、wlan、arp、……
# 多个条件组合：and、or、not
```
3）执行FTP访问，并观察tcpdump抓包结果

从kali主机访问主机192.168.4.5的vsftpd服务。
```shell
[kali@kali ~]$ ftp 192.168.4.5
Connected to 192.168.4.5 (192.168.4.5).
220 (vsFTPd 3.0.2)
Name (192.168.4.5:root): tom       #输入用户名
331 Please specify the password.
Password:                              #输入密码
530 Login incorrect.
Login failed.
ftp>quit                               #退出
```
观察抓包的结果（在kali主机观察tcpdump抓包的结果）：
```shell
[kali@kali ~]$
... …
18:47:27.960530 IP 192.168.2.100.novation > 192.168.4.5.ftp: Flags [P.], seq 1:14, ack 21, win 65515, length 13
E..5..@.@......x...d.*..G.\c.1BvP.......USER tom
18:47:29.657364 IP 192.168.2.100.novation > 192.168.4.5.ftp: Flags [P.], seq 14:27, ack 55, win 65481, length 13
E..5..@.@......x...d.*..G.\p.1B.P.......PASS 123
```
4)再次使用tcpdump抓包，使用-w选项可以将抓取的数据包另存为文件，方便后期慢慢分析。
```shell
[kali@kali ~]$ sudo tcpdump  -i 网卡名称  -A  -w  ftp.cap  \
host 192.168.4.5  and  tcp  port  21                            #抓包并保存
```
tcpdump命令的-r选项，可以去读之前抓取的历史数据文件
```shell
[kali@kali ~]$ sudo tcpdump  -A  -r  ftp.cap | egrep  '(USER|PASS)'    #分析数据包
.. ..
E..(..@.@.. ...x...d.*..G.\c.1BbP.............
18:47:25.967592 IP 192.168.2.5.ftp > 192.168.2.100.novation: Flags [P.], seq 1:21, ack 1, win 229, length 20
E..<FJ@.@.jE...d...x...*.1BbG.\cP...V...220 (vsFTPd 2.2.2)
… …
18:47:27.960530 IP 192.168.2.100.novation > 192.168.2.5.ftp: Flags [P.], seq 1:14, ack 21, win 65515, length 13
E..5..@.@......x...d.*..G.\c.1BvP.......USER tom
… …
18:47:27.960783 IP 192.168.2.5.ftp > 192.168.2.100.novation: Flags [P.], seq 21:55, ack 14, win 229, length 34
E..JFL@.@.j5...d...x...*.1BvG.\pP...i~..331 Please specify the password.
… …
18:47:29.657364 IP 192.168.2.5.ftp > 192.168.2.100.novation: Flags [P.], seq 14:27, ack 55, win 65481, length 13
E..5..@.@......x...d.*..G.\p.1B.P.......PASS 123
… …
18:47:29.702671 IP 192.168.2.100.novation > 192.168.2.5.ftp: Flags [P.], seq 55:78, ack 27, win 229, length 23
E..?FN@.@.j>...d...x...*.1B.G.\}P.......230 Login successful.
```
# 2. 加固常见服务的安全
## 2.1 问题
本案例要求优化提升常见网络服务的安全性，主要完成以下任务操作：

1. 优化Nginx服务的安全配置
## 2.2 方案
Nginx安全优化包括：修改版本信息、限制并发、拒绝非法请求、防止buffer溢出。

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：优化Nginx服务的安全配置**

1） 修改版本信息，并隐藏具体的版本号

默认Nginx会显示版本信息以及具体的版本号，这些信息给攻击者带来了便利性，便于他们找到具体版本的漏洞。

如果需要屏蔽版本号信息，执行如下操作，可以隐藏版本号。
```shell
[root@proxy ~]# vim /usr/local/nginx/conf/nginx.conf
… …
http{
     server_tokens off;                            #在http下面手动添加这么一行
     … …
}
[root@proxy ~]# /usr/local/nginx/sbin/nginx -s reload
[root@proxy ~]# curl -I http://192.168.4.5          #查看服务器响应的头部信息
```
2） 限制并发量

DDOS攻击者会发送大量的并发连接，占用服务器资源（包括连接数、带宽等），这样会导致正常用户处于等待或无法访问服务器的状态。

Nginx提供了一个ngx_http_limit_req_module模块，可以有效降低DDOS攻击的风险，操作方法如下：
```shell
[root@proxy ~]# vim /usr/local/nginx/conf/nginx.conf
… …
http{
… …
limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;
    server {
        listen 80;
        server_name localhost;
        limit_req zone=one burst=5;
            }
}
#备注说明：
#limit_req_zone语法格式如下：
#limit_req_zone key zone=name:size rate=rate;
#上面案例中是将客户端IP信息存储名称为one的共享内存，内存空间为10M
#1M可以存储8千个IP信息，10M可以存储8万个主机连接的状态，容量可以根据需要任意调整
#每秒中仅接受1个请求，多余的放入漏斗
#漏斗超过5个则报错
[root@proxy ~]# /usr/local/nginx/sbin/nginx -s reload
```
客户端使用ab测试软件测试效果：
```shell
[root@client ~]# ab -c 100 -n 100  http://192.168.4.5/
```
3） 拒绝非法的请求

网站使用的是HTTP协议，该协议中定义了很多方法，可以让用户连接服务器，获得需要的资源。但实际应用中一般仅需要get和post。

具体HTTP请求方法的含义如表-1所示。

表-1 HTTP请求方法及含义
![在这里插入图片描述](https://img-blog.csdnimg.cn/01c9918361ec4893bf54bb10281d2911.png)
未修改服务器配置前，客户端使用不同请求方法测试：
```shell
[root@client ~]# curl -i -X GET  http://192.168.4.5            #正常
[root@client ~]# curl -i -X HEAD http://192.168.4.5            #正常
#curl命令选项说明：
#-i选项：访问服务器页面时，显示HTTP的头部信息
#-X选项：指定请求服务器的方法
```
通过如下设置可以让Nginx拒绝非法的请求方法：
```shell
[root@proxy ~]# vim /usr/local/nginx/conf/nginx.conf
http{
       server {
                 listen 80;
#这里，!符号表示对正则取反，~符号是正则匹配符号
#如果用户使用非GET或POST方法访问网站，则retrun返回错误信息
              if ($request_method !~ ^(GET|POST)$ ) {
                     return 444;
               }    
        }
}
[root@proxy ~]# /usr/local/nginx/sbin/nginx -s reload
```
修改服务器配置后，客户端使用不同请求方法测试：
```shell
[root@client ~]# curl -i -X GET  http://192.168.4.5            #正常
[root@client ~]# curl -i -X HEAD http://192.168.4.5            #报错
```
4） 防止buffer溢出

当客户端连接服务器时，服务器会启用各种缓存，用来存放连接的状态信息。

如果攻击者发送大量的连接请求，而服务器不对缓存做限制的话，内存数据就有可能溢出（空间不足）。

修改Nginx配置文件，调整各种buffer参数，可以有效降低溢出风险。
```shell
[root@proxy ~]# vim /usr/local/nginx/conf/nginx.conf
http{
client_body_buffer_size  1k;
client_header_buffer_size 1k;
client_max_body_size 1k;
large_client_header_buffers 2 1k;
 … …
}
[root@proxy ~]# /usr/local/nginx/sbin/nginx -s reload
```
# 3. Linux基本防护措施
## 3.1 问题
本案例要求练习Linux系统的基本防护措施，完成以下任务：

1. 修改用户zhangsan的账号属性，设置为2019-12-31日失效（禁止登录）
2. 临时锁定用户lisi的账户，使其无法登录，验证效果后解除锁定
3. 修改tty终端提示，使得登录前看到的第一行文本为“Windows Server 2012 Enterprise R2”，第二行文本为“NT 6.2 Hybrid”
4. 锁定文件/etc/resolv.conf、/etc/hosts，以防止其内容被无意中修改
5. 关闭不需要的服务

## 3.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：修改用户zhangsan的账户属性，设置为2019-12-31日失效（禁止登录）**

1）正常情况下，未过期的账号可以正常登录，使用chage可以修改账户有效期。
```shell
chage命令的语法格式：
chage -l    账户名称                #查看账户信息
chage -E 时间 账户名称                #修改账户有效期
```
2）失效的用户将无法登录

使用chage命令将用户zhangsan的账户设为当前已失效（比如已经过去的某个时间）：
```shell
[root@proxy ~]# useradd zhangsan        #创建账户
[root@proxy ~]# passwd zhangsan        #设置密码
[root@proxy ~]# chage -E 2017-12-31 zhangsan    #设置账户过期时间
```
尝试以用户zhangsan重新登录，输入正确的用户名、密码后直接闪退，返回登录页，说明此帐号已失效。

3）重设用户zhangsan的属性，将失效时间设为2019-12-31
```shell
[root@proxy ~]# chage -E 2019-12-31 zhangsan              #修改失效日期
[root@proxy ~]# chage -l zhangsan                        #查看账户年龄信息
Last password change                     : May 15, 2017
Password expires                       : never
Password inactive                       : never
Account expires                          : Dec 31, 2019
Minimum number of days between password change          : 0
Maximum number of days between password change           : 99999
Number of days of warning before password expires         : 7
```
4）重设用户zhangsan的属性，将失效时间设为永不过期
```shell
[root@proxy ~]# chage -E -1 zhangsan               #设置账户永不过期
```
5）定义默认有效期（扩展知识）

/etc/login.defs这个配置文件，决定了账户密码的默认有效期。
```shell
[root@proxy ~]# cat /etc/login.defs
PASS_MAX_DAYS    99999                        #密码最长有效期
PASS_MIN_DAYS    0                            #密码最短有效期
PASS_MIN_LEN    5                            #密码最短长度
PASS_WARN_AGE    7                            #密码过期前几天提示警告信息
UID_MIN                  1000                #UID最小值
UID_MAX                  60000                #UID最大值
```
**步骤二：临时锁定用户zhangsan的账户，使其无法登录，验证效果后解除锁定**

1）锁定用户账号

使用passwd或usermod命令将用户zhangsan的账户锁定。
```shell
[root@proxy ~]# passwd -l zhangsan           #锁定用户账号（lock）
锁定用户 zhangsan 的密码。
passwd: 操作成功
[root@proxy ~]# passwd -S zhangsan          #查看状态（status）
zhangsan LK 2018-02-22 0 99999 7 -1 (密码已被锁定。)
```
2）验证用户zhangsan已无法登录，说明锁定生效

输入正确的用户名、密码，始终提示“Login incorrect”，无法登录。

3）解除对用户zhangsan的锁定
```shell
[root@proxy ~]# passwd -u zhangsan           #解锁用户账号（unlock）
解锁用户 zhangsan 的密码 。
passwd: 操作成功
[root@proxy ~]# passwd -S zhangsan          #查看状态
zhangsan PS 2018-08-14 0 99999 7 -1 (密码已设置，使用 SHA512 加密。)
```
**步骤三：修改tty登录的提示信息，隐藏系统版本**

1）账户在登录Linux系统时，默认会显示登陆信息（包括操作系统内核信息）

/etc/issue这个配置文件里保存的就是这些登陆信息，修改该文件防止内核信息泄露。
```shell
[root@proxy ~]# cat /etc/issue                      #确认原始文件
Red Hat Enterprise Linux Server release 7.5
Kernel \r on an \m
[root@proxy ~]# cp /etc/issue /etc/issue.origin      #备份文件
[root@proxy ~]# vim /etc/issue                      #修改文件内容
Windows Server 2012 Enterprise R2
NT 6.2 Hybrid
```
2）测试版本伪装效果

退出已登录的tty终端，或者重启Linux系统，刷新后的终端提示信息会变成自定义的文本内容，如图-1所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/621171ebb7c84fd0a490233b8ab1f531.png)
图-1

**步骤四：锁定文件/etc/resolv.conf、/etc/hosts**

1）语法格式：
```shell
# chattr +i  文件名            #锁定文件（无法修改、删除、追加等）
# chattr -i  文件名            #解锁文件
# chattr +a  文件名            #锁定后文件仅可追加
# chattr -a  文件名            #解锁文件
# lsattr 文件名                #查看文件特殊属性
···
2) 使用+i锁定文件，使用lsattr查看属性
```shell
[root@proxy ~]# chattr +i /etc/resolv.conf 
[root@proxy ~]# lsattr /etc/resolv.conf 
----i---------- /etc/resolv.conf
```
3）使用+a锁定文件(仅可追加)，使用lsattr查看属性
```shell
[root@proxy ~]# chattr +a /etc/hosts
[root@proxy ~]# lsattr /etc/hosts
-----a---------- /etc/hosts
```
4）测试文件锁定效果
```shell
[root@proxy ~]# rm -rf /etc/resolv.conf
rm: 无法删除"/etc/resolv.conf": 不允许的操作
[root@proxy ~]# echo xyz > /etc/resolv.conf
-bash: resolv.conf: 权限不够
[root@proxy ~]# rm -rf  /etc/hosts                         #失败
[root@proxy ~]# echo "192.168.4.1  xyz" > /etc/hosts     #失败
[root@proxy ~]# echo "192.168.4.1  xyz" >> /etc/hosts    #成功
```
5）恢复这两个文件原有的属性（避免对后续实验造成影响）
```shell
[root@proxy ~]# chattr -i /etc/resolv.conf 
[root@proxy ~]# chattr -i /etc/hosts
[root@proxy ~]# lsattr /etc/resolv.conf /etc/hosts
--------------- /etc/resolv.conf
--------------- /etc/hosts
```
附加思维导图，如图-5所示：

![在这里插入图片描述](https://img-blog.csdnimg.cn/09fd193b7f484d00943698916c174895.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-5


# Exercise
## 1 阅读下列nmap扫描操作，根据注释的功能要求在括号中补全命令选项
> ```shell
> [root@svr7 ~]# nmap  -（  ）  svr7.tarena.com              //扫描开启的UDP服务
> 53/udp   open          domain
> [root@svr7 ~]# nmap  -（  ）  （    ）  192.168.4.0/24      //扫描哪些主机开放FTP、SSH
> [root@svr7 ~]# nmap  -（    ）  192.168.4.110               //扫描操作系统类型
> ```

```shell
[root@svr7 ~]# nmap   -（sU）  svr7.tarena.com              //扫描开启的UDP服务
53/udp   open          domain
[root@svr7 ~]# nmap  -（p）  （21-22）  192.168.4.0/24      //扫描哪些主机开放FTP、SSH
[root@svr7 ~]# nmap  -（A）  192.168.4.110               //扫描操作系统类型
```
## 2 简述ngx_http_limit_req_module模块的用法？
```shell
limit_req_zone $binary_remote_addr  zone=one:10m rate=1r/s;
limit_req zone=one burst=5;
语法：limit_req_zone key zone=name:size rate=rate;
将客户端IP信息存储名称为one的共享内存，空间为10M
1M可以存储8千个IP的信息，10M存8万个主机状态
每秒中仅接受1个请求，多余的放入漏斗
漏斗超过5个则报错
```
## 3 配置新建用户时的属性限制
对于新创建的用户，要求其密码最长使用时间为60天，密码最短使用时间为1天，在密码过期前7天内发出警告。
```shell
[root@svr5 ~]# vim /etc/login.defs
PASS_MAX_DAYS   60
PASS_MIN_DAYS   1
PASS_WARN_AGE   7
```

## 4 如何锁定解锁Linux用户的密码
```shell
[root@svr5 ~]# passwd -l  用户名
[root@svr5 ~]# passwd -u  用户名
```
> 如有侵权，请联系作者删除
