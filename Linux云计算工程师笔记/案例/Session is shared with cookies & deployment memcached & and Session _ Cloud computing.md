@[TOC]( Session is shared with cookies & deployment memcached & and Session | Cloud computing )

---
# 1 案例1：PHP的本地Session信息
## 1.1 问题
通过Nginx调度器负载后端两台Web服务器，实现以下目标：

1. 部署Nginx为前台调度服务器
2. 调度算法设置为轮询
3. 后端为两台LNMP服务器
4. 部署测试页面，查看PHP本地的Session信息

## 1.2 方案
概念：

Session：存储在服务器端，保存用户名、登陆状态等信息。
Cookies：由服务器下发给客户端，保存在客户端的一个文件里。
保存的内容主要包括：SessionID。

实验拓扑环境：
使用4台RHEL7虚拟机，其中一台作为Nginx前端调度器服务器（eth0:192.168.4.5,eth1:192.168.2.5）、两台虚拟机部署为LNMP服务器，分别为Web1服务器（192.168.2.100）和Web2服务器（192.168.2.200），另外一台作为测试用的Linux客户机（192.168.4.10），拓扑如图-2所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/e4b744b647a3430e8d4afdd57606ea01.png)
图-2

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：部署后端LNMP服务器相关软件**

**注意:以下部署LNMP服务器的操作，需要在两台后端服务器做相同的操作，下面我们以一台Web2服务器（192.168.2.200）为例，对Web1服务器执行相同操作即可。**

1）使用yum安装基础依赖包
```shell
[root@web2 ~]# yum -y install gcc openssl-devel pcre-devel
.. ..
```
2）源码安装Nginx
```shell
[root@web2 ~]# tar -xf nginx-1.12.2.tar.gz
[root@web2 ~]# cd nginx-1.12.2
[root@web2 nginx-1.12.2]#  ./configure   \
> --with-http_ssl_module 
[root@web2 nginx-1.12.2]# make && make install
```
3）安装MariaDB数据库
```shell
[root@web2 ~]# yum -y install  mariadb  mariadb-server  mariadb-devel
```
4）安装PHP
```shell
[root@web2 ~]# yum -y install  php  php-mysql
[root@web2 ~]# yum -y install  php-fpm
```
5）修改Nginx配置文件（修改默认首页与动静分离）
```shell
[root@web2 ~]# vim /usr/local/nginx/conf/nginx.conf
location / {
            root   html;
            index  index.php  index.html   index.htm;
        }
 location  ~  \.php$  {
            root           html;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
           # fastcgi_param   SCRIPT_FILENAME  $document_root$fastcgi_script_name;
            include        fastcgi.conf;
        }
```
**步骤二：启动LNMP服务器相关的服务**

1）启动Nginx服务

这里需要注意的是，如果服务器上已经启动了其他监听80端口的服务软件（如httpd），则需要先关闭该服务，否则会出现冲突。
```shell
[root@web2 ~]# systemctl stop  httpd                //如果该服务存在，则关闭该服务
[root@web2 ~]# /usr/local/nginx/sbin/nginx
[root@web2 ~]# ss -utnlp | grep :80
tcp    0    0 0.0.0.0:80        0.0.0.0:*        LISTEN        32428/nginx         
```
2）启动MySQL服务
```shell
[root@web2 ~]# systemctl start mariadb
[root@web2 ~]# systemctl status mariadb
```
3）启动PHP-FPM服务
```shell
[root@web2 ~]# systemctl start  php-fpm
[root@web2 ~]# systemctl status php-fpm
```
**步骤三：部署前端Nginx调度服务器**

1）使用源码安装nginx软件（如果Nginx软件包已安装可以忽略此步骤）
```shell
[root@proxy ~]# yum  -y  install   gcc pcre-devel openssl-devel
[root@proxy ~]# tar -xf nginx-1.12.2.tar.gz
[root@proxy ~]# cd nginx-1.12.2
[root@proxy nginx-1.12.2]# ./configure
[root@proxy nginx-1.12.2]# make && make install
```
2）修改Nginx配置文件，实现代理服务器

Nginx配置文件中，通过upstream定义后端服务器地址池，默认调度策略为轮询，使用proxy_pass调用upstream定义的服务器地址池：
```shell
[root@proxy ~]# vim /usr/local/nginx/conf/nginx.conf
.. ..
upstream webs  {
        server 192.168.2.100:80;
        server 192.168.2.200:80;
  }
 server  {
          listen       80;
          server_name  localhost;
          location  /  {
              proxy_pass http://webs;
            root   html;
            index  index.php index.html index.htm;
          }
}
```
3）重新加载配置文件
```shell
[root@proxy ~]# /usr/local/nginx/sbin/nginx -s reload
#请先确保nginx是启动状态，否则运行该命令会报错,报错信息如下：
[error] open() "/usr/local/nginx/logs/nginx.pid" failed (2: No such file or directory)
```
**步骤四：测试环境是否配置成功**

1）浏览器访问测试页面验证。
```shell
[root@client ~]# curl  http://192.168.4.5                //查看是否有数据
```
**步骤五：部署测试页面**

1）部署测试页面(Web1服务器）。

测试页面可以参考lnmp_soft/php_scripts/php-memcached-demo.tar.gz。
```shell
[root@web1 ~]# cd lnmp_soft/php_scripts/
[root@web1 php_scripts]# tar -xf php-memcached-demo.tar.gz
[root@web1 php_scripts]# cd php-memcached-demo
[root@web1 php-memcached-demo]# cp -r  *  /usr/local/nginx/html/
```
2）浏览器直接访问后端服务器的测试页面（Web1服务器）。
```shell
[root@web1 ~]# firefox http://192.168.2.100    /index.php        //填写账户信息
[root@web1 ~]# cd /var/lib/php/session/            //查看服务器本地的Session信息
[root@web1 ~]# ls
sess_ahilcq9bguot0vqsjtd84k7244                        //注意这里的ID是随机的
[root@web1 ~]# cat sess_ahilcq9bguot0vqsjtd84k7244
```
注意：可用修改index.php和home.php两个文件的内容，添加页面颜色属性，以区别后端两台不同的服务器:<body bgcolor=blue>。

3）部署测试页面(Web2服务器）。

测试页面可以参考lnmp_soft/php_scripts/php-memcached-demo.tar.gz。
```shell
[root@web2 ~]# cd lnmp_soft/php_scripts/
[root@web2 php_scripts]# tar -xf php-memcached-demo.tar.gz
[root@web2 php_scripts]# cd php-memcached-demo
[root@web2 php-memcached-demo]# cp -r  *  /usr/local/nginx/html/
```
4）浏览器直接访问后端服务器的测试页面（Web2服务器）。
```shell
[root@web2 ~]# firefox http://192.168.2.100    /index.php         //填写账户信息
[root@web2 ~]# cd /var/lib/php/session/            //查看服务器本地的Session信息
[root@web2 ~]# ls
sess_qqek1tmel07br8f63d6v9ch401                        //注意这里的ID是随机的
[root@web2 ~]# cat sess_qqek1tmel07br8f63d6v9ch401    
```
注意：可用修改index.php和home.php两个文件的内容，添加页面颜色属性，以区别后端两台不同的服务器:<body bgcolor=green>。

5）浏览器访问前端调度器测试（不同后端服务器Session不一致）。

真实主机使用google浏览器测试。
```shell
[root@room9pc01 ~]# google-chrome http://192.168.4.5/index.php
//填写注册信息后，刷新，还需要再次注册，说明两台计算机使用的是本地Session
//第二台主机并不知道你再第一台主机已经登录，第一台主机的登录信息也没有传递给第二台主机
```
# 2. 构建memcached服务
## 2.1 问题
本案例要求先快速搭建好一台memcached服务器，并对memcached进行简单的增、删、改、查操作：

- 安装memcached软件，并启动服务
- 使用telnet测试memcached服务
- 对memcached进行增、删、改、查等操作

## 2.2 方案
使用1台RHEL7虚拟机作为memcached服务器（192.168.4.5）。

在RHEL7系统光盘中包含有memcached，因此需要提前配置yum源，即可直接使用yum安装，客户端测试时需要提前安装telnet远程工具。

验证时需要客户端主机安装telnet，远程memcached来验证服务器的功能：

- add name 0 180 10 //变量不存在则添加
- set name 0 180 10 //添加或替换变量
- replace name 0 180 10 //替换
- get name //读取变量
- delete name //删除变量
- flush_all //清空所有
- 提示：0表示不压缩，180为数据缓存时间，10为需要存储的数据字节数量。

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：构建memcached服务**

1）使用yum安装软件包memcached
```shell
[root@proxy ~]# yum -y  install   memcached   telnet
[root@proxy ~]# rpm -qa memcached
memcached-1.4.15-10.el7_3.1.x86_64
```
2) memcached配置文件（查看即可，不需要修改）
```shell
[root@proxy ~]# vim /usr/lib/systemd/system/memcached.service
ExecStart=/usr/bin/memcached -u $USER -p $PORT -m $CACHESIZE -c $MAXCONN $OPTIONS
[root@proxy ~]# vim /etc/sysconfig/memcached
PORT="11211"
USER="memcached"
MAXCONN="1024"
CACHESIZE="64"
OPTIONS=""
```
3）启动服务并查看网络连接状态验证是否开启成功：

ss命令可以查看系统中启动的端口信息，该命令常用选项如下：
-a显示所有端口的信息
-n以数字格式显示端口号
-t显示TCP连接的端口
-u显示UDP连接的端口
-l显示服务正在监听的端口信息，如httpd启动后，会一直监听80端口
-p显示监听端口的服务名称是什么（也就是程序名称）

注意：在RHEL7系统中，使用ss命令可以替代netstat，功能与选项一样。
```shell
[root@proxy ~]# systemctl  start  memcached
[root@proxy ~]# systemctl  status  memcached
[root@proxy ~]# ss  -anptu  |  grep Memcached
udp  UNCONN  0 0    *:11211   *:*      users:(("memcached",pid=12068,fd=28))
udp  UNCONN  0 0    :::11211  :::*     users:(("memcached",pid=12068,fd=29))
tcp  LISTEN  0 128  *:11211   *:*      users:(("memcached",pid=12068,fd=26))
tcp  LISTEN  0 128  :::11211  :::*     users:(("memcached",pid=12068,fd=27))
```
**步骤二：使用telnet访问memcached服务器**

1)使用telnet连接服务器测试memcached服务器功能，包括增、删、改、查等操作。
```shell
[root@proxy ~]# telnet  192.168.4.5  11211
Trying 192.168.4.5...
……
##提示：0表示不压缩，180为数据缓存时间，3为需要存储的数据字节数量。
set name 0 180 3                //定义变量，变量名称为name
plj                            //输入变量的值，值为plj                
STORED
get name                        //获取变量的值
VALUE name 0 3                 //输出结果
plj
END
##提示：0表示不压缩，180为数据缓存时间，3为需要存储的数据字节数量。
add myname 0 180 10            //新建，myname不存在则添加，存在则报错
set myname 0 180 10            //添加或替换变量
replace myname 0 180 10        //替换，如果myname不存在则报错
get myname                    //读取变量
delete myname                    //删除变量
flush_all                        //清空所有
quit                            //退出登录                                  
```

# 3. PHP实现session共享
## 3.1 问题
沿用练习三，通过修改PHP-FPM配置文件，实现session会话共享：

配置PHP使用memcached服务器共享Session信息
客户端访问两台不同的后端Web服务器时，Session 信息一致
## 3.2 方案
在练习三拓扑的基础上，Nginx服务器除了承担调度器外，还需要担任memcached数据库的角色，并在两台后端LNMP服务器上实现PHP的session会话共享。拓扑结构如图-4所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/1cc8d13ddac6458d80f00ceabfb3a5b0.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-4

## 3.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：为Web服务器安装PHP扩展**

1）为web1主机的PHP添加memcache扩展
```shell
[root@web1 ~]# yum -y install  php-pecl-memcache
[root@web1 ~]# systemctl restart php-fpm
···
2）为web2主机的PHP添加memcache扩展
```shell
[root@web2 ~]# yum -y install  php-pecl-memcache
[root@web2 ~]# systemctl restart php-fpm
```
**步骤二：在后端LNMP服务器上部署Session共享**

注意：这些操作在两台后端Web服务器上均需要执行，以下操作以Web1（192.168.2.100）服务器为例。

1）修改PHP-FPM配置文件，并重启服务

注意，因为后端两台web服务器(web1,web2)都需要修改配置文件(下面也web1为例)。
```shell
[root@web1 ~]# vim  /etc/php-fpm.d/www.conf            //修改该配置文件的两个参数
//文件的最后2行
修改前效果如下:
php_value[session.save_handler] = files
php_value[session.save_path] = /var/lib/php/session
//原始文件，默认定义Sessoin会话信息本地计算机（默认在/var/lib/php/session）
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
修改后效果如下:
php_value[session.save_handler] = memcache
php_value[session.save_path] = "tcp://192.168.2.5:11211"
//定义Session信息存储在公共的memcached服务器上，主机参数中为memcache（没有d）
//通过path参数定义公共的memcached服务器在哪（服务器的IP和端口）
[root@web1 ~]# systemctl  restart  php-fpm
```
**步骤三：客户端测试**

客户端使用浏览器访问两台不同的Web服务器。

操作步骤参考练习一，最终可以获得相关的Session ID信息。


# Exercise
## 1 简述什么是memcached

- memcached是高性能的分布式缓存服务器，是一个跨平台的、开源的实现分布式缓存服务的软件
- 用来集中缓存数据库查询结果，减少数据库访问次数，以提高动态Web应用的响应速度
- memcached支持许多平台：Linux、FreeBSD、Solaris (memcached 1.2.5以上版本)、Mac OS X、Windows

## 2 PHP的Session会话共享
> 要求：PHP通过memcached实现Session会话共享，修改哪儿文件如何修改？

```shell
vim  /etc/php-fpm.d/www.conf
修改前:
php_value[session.save_handler] = files
php_value[session.save_path] = /var/lib/php/session
修改后
php_value[session.save_handler] = memcache
php_value[session.save_path] = "tcp://192.168.2.5:11211" 
```

> 如有侵权，请联系作者删除
