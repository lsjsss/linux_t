@[TOC]( Tomcat server & Tomcat application cases & Maven application cases | Cloud computing )

---
# 1. 安装部署Tomcat服务器
## 1.1 问题
本案例要求部署Tomcat服务器，具体要求如下：

- 安装部署JDK基础环境
- 安装部署Tomcat服务器
- 创建JSP测试页面，文件名为test.jsp，显示服务器当前时间

然后客户机访问此Web服务器验证效果：
- 使用火狐浏览器访问Tomcat服务器的8080端口，浏览默认首页
- 使用火狐浏览器访问Tomcat服务器的8080端口，浏览默认测试页面

## 1.2 方案
使用2台RHEL7虚拟机，其中一台作为Tomcat服务器（192.168.2.100）、另外一台作为测试用的Linux客户机（192.168.2.5），如图-1所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/0b6a24d3af0042d9bd4a80f2d8c8e80e.png)
图-1

使用RPM安装JDK基础环境

使用源码安装部署Tomcat服务器

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：部署Tomcat服务器软件(192.168.2.100/24)**

1）使用RPM安装JDK环境
```shell
[root@web1 ~]# yum -y install  java-1.8.0-openjdk                //安装JDK
[root@web1 ~]# yum -y install java-1.8.0-openjdk-headless        //安装JDK
[root@web1 ~]# java -version                                    //查看JAVA版本
```

2）安装Tomcat（apache-tomcat-8.0.30.tar.gz软件包，在lnmp_soft中有提供）
```shell
[root@web1 ~]# tar -xf  apache-tomcat-8.0.30.tar.gz
[root@web1 ~]# mv apache-tomcat-8.0.30  /usr/local/tomcat
[root@web1 ~]# ls /usr/local/tomcat
bin/                                            //主程序目录
lib/                                            //库文件目录
logs/                                          //日志目录  
temp/                                         //临时目录
work/                                        //自动编译目录jsp代码转换servlet
conf/                                        //配置文件目录
webapps/                                        //页面目录
```
3）启动服务
```shell
[root@web1 ~]# /usr/local/tomcat/bin/startup.sh
```
4）服务器验证端口信息
```shell
[root@web1 ~]# ss -nutlp |grep java        //查看java监听的端口
tcp        0      0 :::8080              :::*                LISTEN      2778/java 
tcp        0      0 :::8009              :::*                LISTEN      2778/java                     
tcp        0      0 ::ffff:127.0.0.1:8005     :::*         LISTEN       2778/java
```
提示：如果检查端口时，8005端口启动非常慢，默认tomcat启动需要从/dev/random读取大量的随机数据，默认该设备生成随机数据的速度很慢，可用使用下面的命令用urandom替换random（非必须操作）。
```shell
[root@web1 ~]# mv /dev/random  /dev/random.bak
[root@web1 ~]# ln -s /dev/urandom  /dev/random
```
另外，还可以使用方案二解决：
```shell
[root@web1 ~]# yum install rng-tools
[root@web1 ~]# systemctl start rngd
[root@web1 ~]# systemctl enable rngd
```
5）客户端浏览测试页面(proxy作为客户端)
```shell
[root@proxy ~]# firefox http://192.168.2.100:8080
```
**步骤二：修改Tomcat配置文件**

1）创建测试JSP页面
```shell
[root@web1 ~]# vim  /usr/local/tomcat/webapps/ROOT/test.jsp
<html>
<body>
<center>
Now time is: <%=new java.util.Date()%>            //显示服务器当前时间
</center>
</body>
</html>
```

**步骤三：验证测试**

1）客户端浏览测试页面(proxy充当客户端角色)
```shell
[root@proxy ~]# firefox http://192.168.2.100:8080
[root@proxy ~]# firefox http://192.168.2.100:8080/test.jsp
```

# 2. 使用Tomcat部署虚拟主机
## 2.1 问题
沿用练习二，使用Tomcat部署加密虚拟主机，实现以下要求：

- 实现两个基于域名的虚拟主机，域名分别为：www.a.com和 www.b.com
- 使用www.a.com域名访问的页面根路径为/usr/local/tomcat/a/ROOT
- 使用www.b.com域名访问的页面根路径为/usr/local/tomcat/b/base
- 访问www.a.com/test时，页面自动跳转到/var/www/html目录下的页面
- 访问页面时支持SSL加密通讯
- 私钥、证书存储路径为/usr/local/tomcat/conf/cert
- 每个虚拟主机都拥有独立的访问日志文件
- 配置tomcat集群环境

## 2.2 方案
修改server.xml配置文件，创建两个域名的虚拟主机，修改如下两个参数块：
```shell
# cat /usr/local/tomcat/conf/server.xml
<Server>
   <Service>
     <Connector port=8080 />
     <Connector port=8009 />
     <Engine name="Catalina" defaultHost="localhost">
<Host name="www.a.com" appBase="a" unpackWARS="true" autoDeploy="true">
</Host>
<Host name="www.b.com" appBase="b" unpackWARS="true" autoDeploy="true">
</Host>
… …
```

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：配置服务器虚拟主机**

1）修改server.xml配置文件，创建虚拟主机
```shell
[root@web1 ~]# vim /usr/local/tomcat/conf/server.xml
… …
<Host name="www.a.com" appBase="a" unpackWARS="true" autoDeploy="true">
</Host>
<Host name="www.b.com" appBase="b" unpackWARS="true" autoDeploy="true">
</Host>
```
2）创建虚拟主机对应的页面根路径
```shell
[root@web1 ~]# mkdir -p  /usr/local/tomcat/{a,b}/ROOT
[root@web1 ~]# echo "AAA"   > /usr/local/tomcat/a/ROOT/index.html
[root@web1 ~]# echo "BBB" > /usr/local/tomcat/b/ROOT/index.html
```
3）重启Tomcat服务器
```shell
[root@web1 ~]# /usr/local/tomcat/bin/shutdown.sh
[root@web1 ~]# /usr/local/tomcat/bin/startup.sh
```
4）客户端设置host文件，并浏览测试页面进行测试(proxy充当客户端角色)

注意：ssh远程连接时使用使用-X参数才可以！！！
```shell
[root@proxy ~]# vim /etc/hosts
… …
192.168.2.100      www.a.com  www.b.com
[root@proxy ~]# firefox http://www.a.com:8080/        //注意访问的端口为8080
[root@proxy ~]# firefox http://www.b.com:8080/
```
**步骤二：修改www.b.com网站的首页目录为base**

1）使用docBase参数可以修改默认网站首页路径
```shell
[root@web1 ~]# vim /usr/local/tomcat/conf/server.xml
… …
<Host name="www.a.com" appBase="a" unpackWARS="true" autoDeploy="true">
</Host>
<Host name="www.b.com" appBase="b" unpackWARS="true" autoDeploy="true">
<Context path="" docBase="base"/>
</Host>
… …
[root@web1 ~]# mkdir  /usr/local/tomcat/b/base
[root@web1 ~]# echo "BASE" > /usr/local/tomcat/b/base/index.html
[root@web1 ~]# /usr/local/tomcat/bin/shutdown.sh
[root@web1 ~]# /usr/local/tomcat/bin/startup.sh
```
2）测试查看页面是否正确(proxy充当客户端角色)
```shell
[root@proxy ~]# firefox http://www.b.com:8080/        //结果为base目录下的页面内容
```
**步骤三：跳转**

1）当用户访问http://www.a.com/test打开/var/www/html目录下的页面
```shell
[root@web1 ~]# vim /usr/local/tomcat/conf/server.xml
… …
<Host name="www.a.com" appBase="a" unpackWARS="true" autoDeploy="true">
<Context path="/test" docBase="/var/www/html/" />
</Host>
<Host name="www.b.com" appBase="b" unpackWARS="true" autoDeploy="true">
<Context path="" docBase="base" />
</Host>
… …
[root@web1 ~]# echo "Test" > /var/www/html/index.html
[root@web1 ~]# /usr/local/tomcat/bin/shutdown.sh
[root@web1 ~]# /usr/local/tomcat/bin/startup.sh
```
2）测试查看页面是否正确(proxy充当客户端角色)
```shell
[root@proxy ~]# firefox http://www.a.com:8080/test    
//返回/var/www/html/index.html的内容
//注意，访问的端口为8080
```
**步骤四：配置Tomcat支持SSL加密网站**

1）创建加密用的私钥和证书文件
```shell
[root@web1 ~]# keytool -genkeypair -alias tomcat -keyalg RSA -keystore /usr/local/tomcat/keystore                //提示输入密码为:123456
//-genkeypair     生成密钥对
//-alias tomcat     密钥别名
//-keyalg RSA     定义密钥算法为RSA算法
//-keystore         定义密钥文件存储在:/usr/local/tomcat/keystore
```
2)再次修改server.xml配置文件，创建支持加密连接的Connector
```shell
[root@web1 ~]# vim /usr/local/tomcat/conf/server.xml
… …
<Connector port="8443" protocol="org.apache.coyote.http11.Http11NioProtocol"
maxThreads="150" SSLEnabled="true" scheme="https" secure="true"
keystoreFile="/usr/local/tomcat/keystore" keystorePass="123456" clientAuth="false" sslProtocol="TLS" />
//备注，默认这段Connector被注释掉了，打开注释，添加密钥信息即可
```
3）重启Tomcat服务器
```shell
[root@web1 ~]# /usr/local/tomcat/bin/shutdown.sh
[root@web1 ~]# /usr/local/tomcat/bin/startup.sh
```
4）客户端设置host文件，并浏览测试页面进行测试(proxy充当客户端角色)
```shell
[root@proxy ~]# vim /etc/hosts
… …
192.168.2.100      www.a.com  www.b.com
[root@proxy ~]# firefox https://www.a.com:8443/
[root@proxy ~]# firefox https://www.b.com:8443/
[root@proxy ~]# firefox https://192.168.2.100:8443/
```
**步骤五：配置Tomcat日志**

1)为每个虚拟主机设置不同的日志文件
```shell
[root@web1 ~]# vim /usr/local/tomcat/conf/server.xml
.. ..
<Host name="www.a.com" appBase="a" unpackWARS="true" autoDeploy="true">
<Context path="/test" docBase="/var/www/html/" />
#从默认localhost虚拟主机中把Valve这段复制过来，适当修改下即可
<Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"
               prefix="a_access" suffix=".txt"
               pattern="%h %l %u %t &quot;%r&quot; %s %b" />
</Host>
<Host name="www.b.com" appBase="b" unpackWARS="true" autoDeploy="true">
<Context path="" docBase="base" />
<Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"
               prefix="b_access" suffix=".txt"
               pattern="%h %l %u %t &quot;%r&quot; %s %b" />
</Host>
.. ..
```
2）重启Tomcat服务器
```shell
[root@web1 ~]# /usr/local/tomcat/bin/shutdown.sh
[root@web1 ~]# /usr/local/tomcat/bin/startup.sh
```
3）查看服务器日志文件
```shell
[root@web1 ~]# ls /usr/local/tomcat/logs/
```
**步骤六：扩展实验(配置Tomcat集群)**

1) 在192.168.4.5主机上配置Nginx调度器（具体安装步骤参考前面的章节）
```shell
[root@proxy ~]# vim  /usr/local/nginx/conf/nginx.conf
http{
    upstream toms {
        server 192.168.2.100:8080;
        server 192.168.2.200:8080;
    }
    server  {
        listen 80;
        server_name localhost;
        location / {
            proxy_pass  http://toms;
        }
    }
}  
```
2) 在192.168.2.100和192.168.2.200主机上配置Tomcat调度器

以下以Web1为例：
```shell
[root@web1 ~]# yum -y install  java-1.8.0-openjdk                //安装JDK
[root@web1 ~]# yum -y install java-1.8.0-openjdk-headless        //安装JDK
[root@web1 ~]# tar -xzf  apache-tomcat-8.0.30.tar.gz
[root@web1 ~]# mv apache-tomcat-8.0.30  /usr/local/tomcat
```
3）启动服务
```shell
[root@web1 ~]# /usr/local/tomcat/bin/startup.sh
```
4）客户端验证

为了防止有数据缓存，可以使用真实主机的google-chrome访问代理服务器，输入Ctrl+F5刷新页面。

# 3. 使用Maven部署网站系统
## 3.1 问题
通过安装配置Maven，实现如下目标：
- 查询Maven版本
- 配置镜像地址
- 打包并上线网站项目
## 3.2 方案
通过tar包安装Maven
- 释放tar包，拷贝到/usr/local目录
- 安装并运行数据库
- 打包网站项目，之后利用tomcat上线该网站

## 3.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：安装maven工具，以及java环境**

1）释放tar包，并拷贝到指定目录
```shell
[root@web1 ~]# tar -xf apache-maven-3.6.3-bin.tar.gz
[root@web1 ~]# mv apache-maven-3.6.3 /usr/local/maven
```
2）安装java依赖包
```shell
[root@web1 ~]# yum -y install java-1.8.0-openjdk
[root@web1 ~]# yum -y install java-devel
[root@web1 ~]# /usr/local/maven/bin/mvn -v
```
3）修改镜像地址，在第158行下添加
```shell
[root@web1 ~]# vim /usr/local/maven/conf/settings.xml  
<mirror>
          <id>nexus-aliyun</id>
          <mirrorOf>*</mirrorOf>
          <name>Nexus aliyun</name>
          <url>http://maven.aliyun.com/nexus/content/groups/public</url> 
</mirror>
```
**步骤二：配置数据库并打包项目**

1）配置数据库
```shell
[root@web1 ~]# yum install -y mariadb-server
[root@web1 ~]# systemctl start mariadb
[root@web1 ~]# cd CMS/
[root@web1 CMS]# cp src/main/resources/shishuocms.properties .
[root@web1 CMS]# mysql -uroot < sql/install.sql
[root@web1 CMS]# mysqladmin password
```
2）打包项目
```shell
[root@web1 CMS]# /usr/local/maven/bin/mvn clean package
```
**步骤三：上线测试**

1）备份原有网站页面
```shell
[root@web1 CMS]# mv /usr/local/tomcat/webapps/ROOT /opt/tomcat_ROOT
```
2）将war包拷贝到tomcat网站页面目录
```shell
[root@web1 CMS]#cp target/shishuocms-2.0.1.war /usr/local/tomcat/webapps/ROOT.war
[root@web1 CMS]#/usr/local/tomcat/bin/startup.sh
```

# Exercise
## 1 哪些参数影响了Tomcat部署网站时的路径
appBase，docBase，path。

## 2 使用keytool生成密钥文件的命令是什么？
```shell
[root@localhost ~]keytool -genkeypair -alias tomcat -keyalg RSA \
> -keystore /usr/local/tomcat/keystore
```
## 3 Tomcat配置虚拟主机的关键词是什么？
首先以<Host ......> 开头
......
然后以</Host>结尾，中间包含的 . 的内容是虚拟主机的各种参数配置

## 4 Maven的功能是什么？
是一个软件项目管理工具

> 如有侵权，请联系作者删除
