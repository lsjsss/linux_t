@[TOC]( Basic Web applications & BASIC NFS services & triggering mount | Cloud computing )

---
# 1 案例1：独立Web站点的快速部署
## 1.1 问题
本例要求为 http://server0.example.com 配置Web站点，要求如下：

1. 建立一个主页文件，将其重命名为 index.html
2. 将此文件拷贝到站点的 DocumentRoot 目录下
3. 使用 elinks 或firefox 浏览上述Web站点

## 1.2 方案
Web网站服务端：软件包httpd、系统服务httpd
Web网站浏览器：软件包elinks或fireox
传输协议及端口：TCP 80

Web网站服务端配置文件：
- /etc/httpd/conf/httpd.conf
- /etc/httpd/conf.d/*.conf

默认首页文件：index.html
httpd网站文档的默认根目录:/var/www/html

URL（Uniform Resource Locator，统一资源定位器）网址的基本组成：
```shell
http://服务器地址[:端口号]/目录/文件名
```

对于需要验证的FTP资源，还需要指定用户名密码信息：
```shell
ftp://用户名:密码@服务器地址[:端口号]/目录/文件名
```

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：构建及部署网站服务器**

1）安装软件包httpd
```shell
[root@localhost ~]# setenforce 0
[root@localhost ~]# firewall-cmd --set-default-zone=trusted
[root@server0 ~]# yum  -y  install  httpd
.. ..
```
2）部署网页
```shell
[root@server0 ~]# cd  /var/www/html/                       //进入网页目录
[root@server0 html]#echo ‘Default Site.’ >  index.html                          
[root@server0 html]# cat  index.html                      //检查网页文件
Default Site.
```
3）启动系统服务httpd，并设置开机自启
```shell
[root@server0 html]# systemctl  restart  httpd
[root@server0 html]# systemctl  enable  httpd
ln -s '/usr/lib/systemd/system/httpd.service' '/etc/systemd/system/multi-user.target.wants/httpd.service'
```
**步骤二：访问网站服务器**

1）使用elinks浏览器查看

Elinks浏览器可以在命令行模式显示出网页文本，经常用来测试网站的可用性。
```shell
[root@localhost ~]# setenforce 0
[root@localhost ~]# firewall-cmd --set-default-zone=trusted
[root@desktop0 ~]# vim  /etc/hosts
.. ..
192.168.4.7 server0.example.com
[root@desktop0 ~]# yum  -y  install  elinks                      //安装elinks
.. ..
[root@desktop0 ~]# elinks  -dump  http://server0.example.com/     //访问指定网址
   Default Site.
   ```
2）使用firefox浏览器查看

Firefox浏览器支持更多网页特性，是访问复杂网页、网址的优秀工具。

在桌面终端直接运行“firefox http://server0.examle.com/”，或者通过菜单快捷方式打开Firefox浏览器再输入对应网址，都可以看到目标网页（如图-1所示）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/5aeb9d64ce0b4ce0b904afbed49c3e5b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-1

# 2. 虚拟Web主机的部署
## 2.1 问题
本例要求为虚拟机A扩展Web站点，新建虚拟主机 http://www0.example.com，具体要求如下：

1. 设置 DocumentRoot 为 /var/www/virtual
2. 建立主页文件，并重命名为 index.html
3. 将文件 index.html其放到此虚拟主机的 DocumentRoot 目录下
4. 确保站点 http://server0.example.com 仍然可用

## 2.2 方案
单一网站平台（比如172.25.0.11）：

- 多个域名 ---> 相同的网页内容
- 配置文件：/etc/httpd/conf/httpd.conf
- 网页目录定义：DocumentRoot /var/www/html

虚拟主机平台（比如172.25.0.11）：
- 在同一套httpd平台上跑很多个网站
- 多个域名 ---> 不同的网页内容
- 网页目录由<VirtualHost ...>区段配置定义

多个虚拟主机站点的典型设置（/etc/httpd/conf.d/*.conf）：
```shell
<VirtualHost *:80>
       ServerName  网站1的FQDN
       DocumentRoot  网站1的网页根目录
</VirtualHost>
<VirtualHost *:80>
       ServerName  网站2的FQDN
       DocumentRoot   网站2的网页根目录
</VirtualHost>
.. ..
```

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：部署网页文档**

1）建立网页目录
```shell
[root@localhost ~]# setenforce 0
[root@localhost ~]# firewall-cmd --set-default-zone=trusted
[root@server0 ~]# mkdir  /var/www/virtual
```
2）部署网页文件
```shell
[root@server0 ~]# cd  /var/www/virtual/
[root@server0 virtual]# echo ‘Virtual Site.’  >  index.html
[root@server0 virtual]# cat  index.html                  //检查网页文件
Virtual Site.
```
**步骤二：配置虚拟主机 http://www0.example.com/**

1）为新站点创建独立的配置文件
```shell
[root@server0 virtual]# vim  /etc/httpd/conf.d/01-www0.conf
<VirtualHost  *:80>
        ServerName  www0.example.com
        DocumentRoot  /var/www/virtual
</VirtualHost>
[root@server0 virtual]# httpd  -t                              //确保语法检查OK
Syntax OK
```
2）重启系统服务httpd
```shell
[root@server0 virtual]# systemctl  restart  httpd
```
**步骤三：访问虚拟主机 http://www0.example.com/**

访问此虚拟站点，可以看到预期的网页内容：
```shell
[root@localhost ~]# setenforce 0
[root@localhost ~]# firewall-cmd --set-default-zone=trusted
[root@desktop0 ~]# vim  /etc/hosts
.. ..
192.168.4.7 server0.example.com   www0.example.com
[root@desktop0 ~]# elinks  -dump  http://www0.example.com/
   Virtual Site.
   ```

**步骤四：完善原始站点 http://server0.example.com/**

需要注意的是，原始的独立站点可能出现异常，访问时并不是原始的网页：
```shell
[root@desktop0 ~]# elinks  -dump  http://server0.example.com/
   Virtual Site.
   ```
原因是一旦启用虚拟站点机制以后：

外部的 DocumentRoot、ServerName 会被忽略
- 第1个虚拟站点被视为默认站点，若客户机请求的URL不属于任何已知站点，则由第1个站点响应
- 若要解决此异常，需要将原始站点转换为第一个虚拟主机，启用顺序的设置可以通过文件名开头的数字来实现。

1）为原始站点建立虚拟主机配置
```shell
[root@server0 ~]# vim  /etc/httpd/conf.d/00-default.conf
<VirtualHost  *:80>
        ServerName  server0.example.com
        DocumentRoot  /var/www/html
</VirtualHost>
```
2）重启系统服务httpd
```shell
[root@server0 virtual]# systemctl  restart  httpd
```
3）访问两个虚拟站点，确保各自的网页内容正确
```shell
[root@desktop0 ~]# elinks  -dump  http://server0.example.com/
   Default Site.
[root@desktop0 ~]# elinks  -dump  http://www0.example.com/
   Virtual Site.
   ```

# 3. 普通NFS共享的实现
## 3.1 问题
本例要求在虚拟机A上配置NFS服务，完成以下任务：
1. 只读的方式共享目录 /public

然后在虚拟机 B上访问NFS共享目录
1. 将虚拟机A的 /public 挂到本地 /mnt/nfsmount
2. 这些文件系统在系统启动时自动挂载

## 3.2 方案
对于普通NFS共享来说：
- 服务端首先运行rpcbind服务，然后运行 nfs-server服务
- 客户端不需要运行特定的系统服务

配置NFS共享目录的记录格式：
```shell
文件夹绝对路径        客户地址1(ro或rw等控制参数)  客户地址2(ro或rw等控制参数) .. ..
```

## 3.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：在虚拟机A上发布NFS共享目录**

1）准备需要共享的文件夹
```shell
[root@localhost ~]# setenforce 0
[root@localhost ~]# firewall-cmd --set-default-zone=trusted
[root@server0 ~]# mkdir  /public
```

2）建立NFS共享配置
```shell
[root@server0 ~]# vim  /etc/exports
/public         *(ro)
```

3）启动系统服务nfs-server，并设置开机自启
```shell
[root@server0 ~]# systemctl  restart  rpcbind
[root@server0 ~]# systemctl  restart  nfs-server
[root@server0 ~]# systemctl  enable  nfs-server
ln -s '/usr/lib/systemd/system/nfs-server.service' '/etc/systemd/system/nfs.target.wants/nfs-server.service'
```

**步骤二：在虚拟机B上挂载NFS共享目录/public**

1）创建挂载点
```shell
[root@localhost ~]# setenforce 0
[root@localhost ~]# firewall-cmd --set-default-zone=trusted
[root@desktop0 ~]# mkdir  /mnt/nfsmount
```
2）配置开机挂载虚拟机A的NFS共享目录/public
```shell
[root@desktop0 ~]# vim  /etc/fstab
.. ..
192.168.4.7:/public     /mnt/nfsmount   nfs     defaults,_netdev   0  0
```
3）测试挂载配置
```shell
[root@desktop0 ~]# mount  -a
[root@desktop0 ~]# df  -hT  /mnt/nfsmount/
Filesystem                  Type  Size  Used Avail Use% Mounted on
server0.example.com:/public nfs4   10G  3.2G  6.8G  32% /mnt/nfsmount
```

# 4. autofs触发挂载
## 4.1 问题
1. 在虚拟机A上配置NFS服务
2. 只读的方式共享目录 /tedu，只能被192.168.4.0/24的系统访问
3. 在虚拟机B上访问NFS共享目录
4. 将虚拟机A 的 /tedu 完成触发挂载到本地 /mnt/nfsauto

## 4.2 方案
autofs触发挂载是一个服务，要想使用这个服务，要确保系统安装了此服务和开启此服务。autofs之所以可以达到触发挂载，原因是它具有两个配置文件：
- 主配置文件 /etc/auto.master，记录“监控点目录、挂载配置文件的路径”
- 挂载配置文件，比如 /etc/auto.misc，记录“挂载点子目录 -挂载参数 :设备名”

更改配置文件后需重启autofs服务生效。

## 4.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：虚拟机A配置NFS服务**

命令操作如下所示：

1）准备需要共享的文件夹
```shell
[root@localhost ~]# setenforce 0
[root@localhost ~]# firewall-cmd --set-default-zone=trusted
[root@server0 ~]# mkdir  /tedu
```
2）建立NFS共享配置
```shell
[root@server0 ~]# vim  /etc/exports
/public         *(ro)
/tedu          192.168.4.0/24(ro)
```
3）启动系统服务nfs-server，并设置开机自启
```shell
[root@server0 ~]# systemctl  restart  rpcbind
[root@server0 ~]# systemctl  restart  nfs-server
[root@server0 ~]# systemctl  enable  nfs-server
ln -s '/usr/lib/systemd/system/nfs-server.service' '/etc/systemd/system/nfs.target.wants/nfs-server.service'
```
**步骤二：虚拟机B配置一个触发挂载服务：**

在/etc/auto.master主配置文件

命令操作如下所示：
```shell
[root@localhost ~]# setenforce 0
[root@localhost ~]# firewall-cmd --set-default-zone=trusted
[root@localhost /]# vim /etc/auto.master
/misc   /etc/auto.misc         //此句话原本已存在无需更改
/mnt    /etc/myauto
[root@localhost /]#
```
在/etc/myauto挂载配置文件中，定义挂载设备、参数、挂载点。挂载设备为/dev/sdb5

命令操作如下所示：
```shell
[root@localhost /]# vim /etc/myauto
[root@localhost /]# grep tools /etc/auto.misc 
nfsauto           -fstype=nfs    192.168.4.7:/tedu
[root@localhost /]# service autofs restart     //重启autofs服务
[root@localhost /]# ls /mnt/
[root@localhost /]# ls /mnt/nfsauto              //访问触发挂载点
lost+found
[root@localhost /]# mount | grep nfsauto          //查看结果
```

# Exercise
## 1 简述HTTP、HTML的含义及作用

HTTP指的是Hyper Text Transfer Protocol，超文本传输协议，主要为网站服务器程序与浏览器之间传输网页定义相关的标准。

HTML指的是Hyper Text Markup Language，超文本标记语言，是静态网页文件的标记规范。

## 2 已知Web站点server0的网页目录位于/var/www/html，那么对应与网址http://server0/private/的服务端文件是什么

URL网址的/对应Web服务端上DocumentRoot指定的网页目录，其后的URL路径也对应到服务端网页目录下的子目录；当未指定网页文件名时，默认首页为index.html。

因此，此题对应的服务端文件应该是/var/www/html/private/index.html。

## 3 简述实现基于域名的多个虚拟Web主机时基本的配置内容
```shell
[root@server0 ~]# /etc/httpd/conf.d/httpd.conf
.. ..
<VirtualHost  IP地址:端口>
       ServerName  站点1的DNS名称
       DocumentRoot  站点1的网页根目录
</VirtualHost>
<VirtualHost  IP地址:端口>
       ServerName  站点2的DNS名称
       DocumentRoot  站点2的网页根目录
</VirtualHost>
.. ..
```

## 4 在服务器server0上通过NFS共享/usr/src目录，允许任何人访问
```shell
[root@server0 ~]# vim  /etc/exports 
/usr/src        *(ro)
.. ..
[root@server0 ~]# systemctl  restart  nfs-server
```

## 5 在启用SELinux保护的情况下，如何允许httpd开启8909端口
```shell
[root@server0 ~]# semanage  port  -a  -t  http_port_t  -p tcp  8909
.. ..
[root@server0 ~]# semanage  port  -l  |  grep  http_port          //确认结果
http_port_t     tcp      8909,80, 81, 443, 488, 8008, 8009, 8443, 9000 
.. ..
```

> 如有侵权，请联系作者删除
