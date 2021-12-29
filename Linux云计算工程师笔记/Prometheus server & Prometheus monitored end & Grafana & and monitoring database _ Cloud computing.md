@[TOC]( Prometheus server & Prometheus monitored end & Grafana & and monitoring database | Cloud computing )

---
# 1. Prometheus监控服务器
## 1.1 问题
本案例要求部署prometheus监控服务器，完成以下任务：

1. 安装监控服务器
2. 修改配置文件
3. 编写service文件，管理服务
4. 查看监控数据

## 1.2 方案
实验需要2台虚拟机，主机信息如表-1所示。

所有主机系统均为CentOS7，提前配置IP、主机名、系统YUM源。

表-1 实验拓扑结构（网卡名称仅供参考，不能照抄）
![在这里插入图片描述](https://img-blog.csdnimg.cn/a8267e5dabbe4e369f7b0e29221e4a94.png)


实验拓扑如图-1所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/ec49d87cb5d74b0a9334b71c9abd3134.png)
图-1

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：安装监控软件（192.168.4.10主机操作）**

1）安装软件（软件包在第二阶段素材prometheus_soft.tar.gz中有提供）。

需要提前将软件拷贝到虚拟机。解压即可使用。
```shell
[root@prometheus ~]# tar -xf prometheus_soft.tar.gz
[root@prometheus ~]# cd prometheus_soft
[root@prometheus prometheus_soft]# tar -xf prometheus-2.17.2.linux-386.tar.gz
[root@prometheus prometheus_soft]# ls
[root@prometheus prometheus_soft]# mv prometheus-2.17.2.linux-386 /usr/local/prometheus
[root@prometheus prometheus_soft]# ls /usr/local/prometheus/
```
2）修改prometheus配置文件。
```shell
[root@prometheus ~]# vim /usr/local/prometheus/prometheus.yml
static_configs:
    - targets: ['192.168.4.10:9090']      
#修改最后一行，将IP地址改为本机IP
[root@prometheus ~]# /usr/local/prometheus/promtool check config \
/usr/local/prometheus/prometheus.yml
#检查配置配置文件是否有语法错误
```
3）编写服务service文件，使用systemd管理服务。
```shell
[root@prometheus ~]# vim /usr/lib/systemd/system/prometheus.service
[Unit]
Description=Prometheus Monitoring System
After=network.target
[Service]
ExecStart=/usr/local/prometheus/prometheus \
  --config.file=/usr/local/prometheus/prometheus.yml \
  --storage.tsdb.path=/usr/local/prometheus/data/
[Install]
WantedBy=multi-user.target
#备注：
#--config.file和--storage.tsdb.path都是prometheus这个程序的参数
#可以通过prometheus -h查看这个程序支持哪些参数
#--config.file参数后面指定该程序使用哪个配置文件启动服务
#--storage.tsdb.path参数后面指定该程序将数据存储在哪个目录下
[root@prometheus ~]# systemctl  enable prometheus.service --now
#设置服务器开机自启动服务，并立刻启动该服务
```
3）设置防火墙、SELinux（如果已经关闭则可以忽略此步骤）。
```shell
[root@prometheus ~]#firewall-cmd --set-default-zone=trusted
[root@prometheus ~]#setenforce 0
[root@prometheus ~]#sed -i '/SELINUX/s/enforcing/permissive/' /etc/selinux/config
```
**步骤二：查看监控控制台**

1）查看监控主机、监控数据。

使用浏览器firefox或者google-chrome访问http://192.168.4.10:9090。

查看监控主机，点击《Status》--《Targets》查看主机，效果如图-2所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/8b615ced0be44e5686e440d1a4463610.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-2

查看具体监控数据，点击《Graph》，选择监控数据，如go_memstats_alloc_bytes，点击《Execute》效果如图-3所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/ede14f17ca9647bf8863a92d54f4d954.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_15,color_FFFFFF,t_70,g_se,x_16)
图-3

查看监控数据对应的监控图形，效果如图-4所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/3e2b700afc724c96a6671e1421140cb0.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-4

# 2. Prometheus被监控端
## 2.1 问题
本案例要求配置Prometheus被监控端主机，主要完成以下任务：

1. 安装被监控端软件
2. 编写service文件
3. 修改监控服务器配置文件
4. 查看监控数据

## 2.2 步骤
实现此案例需要按照如下步骤进行。

步骤一：部署被控制端export

1）安装软件（192.168.4.11主机操作）。

安装软件，软件在第二阶段素材prometheus_soft.tar.gz中有提供。

提前将软件拷贝到虚拟机中。
```shell
[root@node1 ~]# tar -xf prometheus_soft.tar.gz
[root@node1 ~]# cd prometheus_soft
[root@node1 prometheus_soft]# tar -xf node_exporter-1.0.0-rc.0.linux-amd64.tar.gz
[root@node1 prometheus_soft]# ls
[root@node1 prometheus_soft]# mv node_exporter-1.0.0-rc.0.linux-amd64 /usr/local/node_exporter
[root@node1 prometheus_soft]# ls /usr/local/node_exporter  
```
2) 编写服务service文件（192.168.4.11主机操作）。
```shell
[root@node1 ~]# vim /usr/lib/systemd/system/node_exporter.service
[Unit]
Description=node_exporter
After=network.target
[Service]
Type=simple
ExecStart=/usr/local/node_exporter/node_exporter
[Install]
WantedBy=multi-user.target
[root@node1 ~]# systemctl  enable node_exporter --now
```
3）设置防火墙、SELinux（如果已经关闭则可以忽略此步骤）。
```shell
[root@node1 ~]#firewall-cmd --set-default-zone=trusted
[root@node1 ~]#setenforce 0
[root@node1 ~]#sed -i '/SELINUX/s/enforcing/permissive/' /etc/selinux/config
```
4) 修改监控服务器配置文件（192.168.4.10主机操作）。

参考配置文件最后的模板，在文件末尾添加3行新内容，具体内容如下：
```shell
[root@prometheus ~]# vim /usr/local/prometheus/prometheus.yml
scrape_configs:
  - job_name: 'prometheus'
    static_configs:
    - targets: ['192.168.4.10:9090']
  - job_name: 'node1'                    #监控任务取任意名称
    static_configs:
    - targets: ['192.168.4.11:9100']    #被监控端主机和端口
[root@prometheus ~]# systemctl  restart prometheus.service
```
5) 查看监控主机、监控数据。

使用浏览器访问http://192.168.4.10:9090。

查看监控主机列表，如图-5所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/397dccf9ab274c88888757ce815480b4.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-5

查看主机CPU监控数据，如图-6所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/12a38b9e7d634fec961dab569595834a.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-6

# 3. grafana可视化监控数据
## 3.1 问题
本案例要求配置grafana实现数据可视化效果，完成以下任务：

1. 安装Grafana
2. 修改grafana配置
3. 导入可视化模板
4. 查看监控图表

## 3.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：安装部署grafana（192.168.4.10主机操作）**

1）安装软件（软件在第二阶段素材prometheus_soft.tar.gz中有提供）
```shell
[root@prometheus ~]# cd prometheus_soft/
[root@prometheus prometheus_soft]# yum -y install grafana-6.7.3-1.x86_64.rpm
[root@prometheus prometheus_soft]# systemctl enable grafana-server.service --now
#设置grafana服务为开机自启动服务，并立刻启动该服务
```
提示：grafana默认启动的是3000端口。

2）重置登录密码

浏览器访问Grafana控制台，http://192.168.4.10:3000

默认用户名和密码都是：admin。

重置密码效果如图-7所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/859e61dd4b6a44d9a2bbaabbdc0a26aa.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-7

附加知识：

有些浏览器问题，可能无法重置密码，如果无法重置密码，则可以设置grafana允许匿名登录，具体操作如下（非必要，不要执行如下操作）：
```shell
[root@prometheus ~]# vim /etc/grafana/grafana.ini
[auth.anonymous]
enabled = true
org_role = Admin
[root@prometheus ~]# systemctl restart grafana-server.service
```
**步骤二：配置Grafana**

浏览器访问Grafana控制台，http://192.168.4.10:3000

1）添加数据源

Grafana可以将数据图形化，那么数据从哪里来呢？

点击《Add data source》，选择从Prometheus获取数据。

![在这里插入图片描述](https://img-blog.csdnimg.cn/abef82552b4a45b8a76473705d522ce4.png)
图-8

填写Prometheus基本信息，效果如图-9所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/71488ae4c5604650a9e0616018fe6379.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图-9

2）导入可视化模板

使用不同的可视化模板就可以将不同的数据进行图形化展示，下面导入prometheus图形化模板，效果如图-10、图-11所示，选择《Prometheus 2.0 Stats》。

![在这里插入图片描述](https://img-blog.csdnimg.cn/cf023eafd0ee4eff82e377d5e0bf9736.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-10

![在这里插入图片描述](https://img-blog.csdnimg.cn/3a4a74cfa47745dbb83eb3e28d815fc5.png)
图-11

查看监控效果如图-12所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/65d26f0d33f0431481900f07c33c6e41.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-12

**步骤二：查看被监控主机的系统信息**

1）导入主机监控的可视化模板（node_exporter模板）

模板文件在在第二阶段素材prometheus_soft.tar.gz中有提供。添加效果如图-13所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/702c1b5f08d5413188728f7c77bf9822.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-13

2）选择数据源

导入监控主机的可视化模板后，我们就可以查看主机的监控图形了，但是这个图形的数据从哪里获取呢，需要设置prometheus为数据源，效果如图-14所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/c12cbc9fe4bf4a1ba1c31ce2c4ea0659.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-14

返回Grafana首页，查看监控图形，效果如图-15、图-16所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/3803bac8ceb5444c9c233d37006c8d3e.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-15

![在这里插入图片描述](https://img-blog.csdnimg.cn/fa20a080d595492fa57c7833345723c5.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-16

# 4. 监控数据库
## 4.1 问题
本案例要求使用prometheus监控MariaDB数据库，完成以下任务：

1. 安装数据库
2. 安装数据库exporter
3. 配置数据库账户和密码
4. 导入监控模板

## 4.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：安装MariaDB（被监控主机192.168.4.11操作）**

1）安装软件,启动服务
```shell
[root@node1~]# yum -y install mariadb-server
[root@node1~]# systemctl enable  mariadb --now
```
2）创建数据库账户，配置密码

监控数据库，需要创建一个对数据库有权限的账户并配置密码。
```shell
[root@node1~]# mysql
> grant all on *.* to 'jerry'@'127.0.0.1' identified by '123';
> exit
```
备注：创建用户jerry，该用户可以从本机127.0.0.1登录服务器，该用户的密码为123。

**步骤二：安装配置导出器(exporter)**

（软件在第二阶段素材prometheus_soft.tar.gz中有提供）

1）安装mysqld_exporter导出器（被监控主机192.168.4.11操作）。
```shell
[root@node1 prometheus_soft]# tar -xf mysqld_exporter-0.12.1.linux-amd64.tar.gz
[root@node1 prometheus_soft]# mv mysqld_exporter-0.12.1.linux-amd64 /usr/local/mysqld_exporter
[root@node1 prometheus_soft]# vim /usr/local/mysqld_exporter/.my.cnf
[client]
host=127.0.0.1
port=3306
user=jerry
password=123
```
备注：创建数据库配置文件.my.cnf，到时mysqld_exporter自动读取配置文件，使用配置文件用的账户和密码信息访问数据库，获取数据库监控信息。

2）编写服务service文件，默认端口为9104（被监控主机192.168.4.11操作）。
```shell
[root@node1~]# vim /usr/lib/systemd/system/mysqld_exporter.service
[Unit]
Description=node_exporter
After=network.target
[Service]
ExecStart=/usr/local/mysqld_exporter/mysqld_exporter \
--config.my-cnf=/usr/local/mysqld_exporter/.my.cnf
[Install]
WantedBy=multi-user.target
#备注：
#--config.my-cnf是mysqld_exporter程序的参数，该参数后面指定数据库的配置文件
#可以使用mysqld_exporter -h查看该程序支持哪些参数
[root@node1~]# systemctl enable mysqld_exporter --now 
```
3)修改监控服务器配置文件（192.168.4.10主机操作）。

参考原文的配置模板，最文件最后手动添加如下3行内容，修改后重启服务。
```shell
[root@prometheus ~]# vim /usr/local/prometheus/prometheus.yml
scrape_configs:
… …
  - job_name: 'mysql'                    #监控任务的名称
    static_configs:
    - targets: ['192.168.4.11:9104']    #被监控主机IP和端口
[root@prometheus ~]# systemctl restart prometheus.service
```
**步骤三：配置Grafana可视化**

1）查看监控主机（浏览器访问http://192.168.4.10:9090）。

查看prometheus是否已经识别到MariaDB数据库主机，效果如图-17所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/9f3e7b925550490f966523d10811bb51.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-17

2）访问Grafana导入数据库可视化模板（浏览器访问http://192.168.4.10:3000）。

导入数据库可视化模板，效果如图-18所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/7a823c45427840e290f9d4b42be0d4d5.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-18

设置数据源，数据来源于Prometheus，效果如图-19所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/a589c169527f4726ad77a444eb3d9ad8.png)
图-19

如果离开监控图形时提示保存监控图形，可以任意输入名称即可，如图-20所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/ff1f2d4ca080404ea78a8ae4f9d67c66.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图-20


# Exercise
## 1 Prometheus默认的数据库是什么类型的数据库

时序数据库（带时间标记的数据库）

## 2 Prometheus默认端口是多少？

9090端口。

## 3 Grafana支持哪些数据源？

Graphite，InfluxDB，OpenTSDB，Prometheus，Elasticsearch，CloudWatch和KairosDB等。

## 4 MySQL默认的配置文件名？

my.cnf

> 如有侵权，请联系作者删除
