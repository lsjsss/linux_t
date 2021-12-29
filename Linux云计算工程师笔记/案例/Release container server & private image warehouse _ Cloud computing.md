@[TOC]( Container image technology reveal & release container server & private image warehouse | Cloud computing )

---

# 1. 创建自定义镜像

## 1.1 问题

本案例要求使用两种方法创建自定义镜像，具体要求如下：

1. 使用 centos镜像 启动容器
2. 在容器中配置 yum 源
3. 安装软件 bash-completion net-tools iproute psmisc vim-enhanced
4. 创建自定义镜像 myos:latest
5. 验证自定义镜像

## 1.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：自定义镜像（可以在docker-0001或者docker-0002主机操作）**

1）使用commit方法创建自定义镜像。

使用现有镜像启动容器，在该容器基础上修改，使用commit制作新镜像

```shell
[root@docker-0001 ~]# docker run -it centos:latest
[root@02fd1719c038 ~]# rm -f /etc/yum.repos.d/*.repo
[root@02fd1719c038 ~]# curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.myhuaweicloud.com/repo/CentOS-Base-7.repo
[root@02fd1719c038 ~]# yum install -y net-tools vim-enhanced tree bash-completion iproute psmisc && yum clean all
[root@02fd1719c038 ~]# exit
[root@docker-0001 ~]# docker commit 02fd1719c038 myos:latest
```

2）通过Dockerfile创建自定义镜像。

通过docker build命令可以根据 Dockerfile 里的内容生成镜像


编写Dockerfile的语法格式如下：
FROM: 基础镜像
RUN: 制作镜像时执行的命令，可以有多个
ADD: 复制文件到镜像，自动解压
COPY: 复制文件到镜像，不解压
EXPOSE: 声明开放的端口
ENV: 设置容器启动后的环境变量
WORKDIR: 定义容器默认工作目录（等于cd）
CMD: 容器启动时执行的命令，仅可以有一条CMD

具体操作流程如下：
创建目录 mkdir mybuild
在目录中编写 Dockerfile



生成镜像
docker build -t 镜像名称:标签 Dockerfile所在目录



# 2. 创建apache服务镜像
## 2.1 问题

本案例要求使用Dockerfile创建apache服务镜像myos:httpd，实现以下目标：

1. 添加默认网站
2. 设置默认的工作目录/var/www/html

## 2.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：查看帮助，熟悉命令格式（可以在docker-0001或者docker-0002操作）**

```shell
[root@docker-0001 ~]# mkdir apache; cd apache
[root@docker-0001 apache]# vim Dockerfile
FROM myos:latest
RUN  yum install -y httpd php
ENV  LANG=C
ADD  webhome.tar.gz  /var/www/html/
WORKDIR /var/www/html/
EXPOSE 80
CMD ["/usr/sbin/httpd", "-DFOREGROUND"]
# 拷贝 webhome.tar.gz 到当前目录中
[root@docker-0001 apache]# docker build -t myos:httpd .
# 验证
[root@localhost web]# docker run -itd myos:httpd    
#因为是后台服务，所以要使用-d参数
```



# 3. 创建nginx/php服务镜像

本案例要求使用Dockerfile创建nginx/php服务镜像：

## 3.1 步骤

**步骤一：制作 php 镜像**

```shell
[root@docker-0001 ~]# mkdir php; cd php
[root@docker-0001 php]# vim Dockerfile
FROM myos:latest
RUN  yum install -y php-fpm
EXPOSE 9000
CMD ["/usr/sbin/php-fpm", "--nodaemonize"]
[root@docker-0001 php]# docker build -t myos:php-fpm .
# 验证服务
[root@docker-0001 ~]# docker run -itd myos:php-fpm
deb37734e52651161015e9ce7771381ee6734d1d36bb51acb176b936ab1b3196
[root@docker-0001 ~]# docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS
deb37734e526        myos:php-fpm        "/usr/sbin/php-fpm -…"   17 seconds ago      Up 15 seconds       
[root@docker-0001 ~]# docker exec -it deb37734e526 /bin/bash
[root@deb37734e526 ~]# ss -ltun
Netid  State      Recv-Q     Send-Q        Local Address:Port         Peer Address:Port              
tcp    LISTEN     0          128                    *:9000                  *:*                  
[root@deb37734e526 ~]#
```

**步骤二：制作 nginx 镜像**

```shell
# 编译软件包
[root@docker-0001 ~]# yum install -y gcc make pcre-devel openssl-devel
[root@docker-0001 ~]# useradd nginx
[root@docker-0001 ~]# tar -zxvf nginx-1.12.2.tar.gz
[root@docker-0001 ~]# cd nginx-1.12.2
[root@docker-0001 nginx-1.12.2]# ./configure --prefix=/usr/local/nginx --user=nginx --group=nginx --with-http_ssl_module
[root@docker-0001 nginx-1.12.2]# make && make install
[root@docker-0001 nginx-1.12.2]# # 拷贝 docker-images/info.html和info.php 到 nginx/html 目录下
[root@docker-0001 nginx-1.12.2]# cd /usr/local/
[root@docker-0001 local]# tar czf nginx.tar.gz nginx
# 制作镜像
[root@docker-0001 local]# mkdir /root/nginx ;cd /root/nginx
[root@docker-0001 nginx]# cp /usr/local/nginx.tar.gz ./
[root@docker-0001 nginx]# vim Dockerfile 
FROM myos:latest
RUN  yum install -y pcre openssl && useradd nginx
ADD  nginx.tar.gz /usr/local/
EXPOSE 80
WORKDIR /usr/local/nginx/html
CMD  ["/usr/local/nginx/sbin/nginx", "-g", "daemon off;"]
[root@docker-0001 nginx]# docker build -t myos:nginx .
[root@docker-0001 nginx]#
# 验证服务
[root@docker-0001 ~]# docker rm -f $(docker ps -aq)
deb37734e526
[root@docker-0001 ~]# docker run -itd myos:nginx
e440b53a860a93cc2b82ad0367172c344c7207def94c4c438027c60859e94883
[root@docker-0001 ~]# curl http://172.17.0.2/info.html
<html>
  <marquee  behavior="alternate">
      <font size="12px" color=#00ff00>Hello World</font>
  </marquee>
</html>
[root@docker-0001 ~]#
```



# 4. 发布容器服务

## 4.1 问题

本案例练习测试docker的端口绑定和主机卷映射服务，分别实现以下目标：

1. 通过映射端口对外发布服务
2. 创建 /var/webroot、 /var/webconf
3. 映射配置文件到容器内，对外发布服务
4. 共享网络命名空间，配置 nginx + php 容器服务

## 4.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：通过映射端口发布服务（可以在docker-0001或者docker-0002操作）**

我们使用-p参数把容器端口和宿主机端口绑定，

一个宿主机端口只能绑定一个容器服务。

例如:把宿主机变成 apache

```shell
# 把 docker-0001 变成 apache 服务
[root@docker-0001 ~]# docker run -itd -p 80:80 myos:httpd
# 把 docker-0001 变成 nginx 服务，首先必须停止 apache
[root@docker-0001 ~]# docker stop $(docker ps -q)
[root@docker-0001 ~]# docker run -itd -p 80:80 myos:nginx
```

**步骤二：容器共享卷**

Docker容器不适合保存任何数据，数据文件与配置文件频繁更改，修改多个容器中的数据非常困难，多容器之间有数据共享、同步需求，重要数据在容器内不方便管理易丢失，解决这些问题请使用主机卷映射功能。

Docker可以映射宿主机文件或目录到容器中：

- 目标对象不存在就自动创建
- 目标对象存在就直接覆盖掉
- 多个容器可以映射同一个目标对象来达到数据共享的目的
- 启动容器时，使用 -v 映射参数（可有多个）

语法格式如下：

docker run -itd -v 宿主机对象:容器内对象 myos:latest

apache使用宿主机中的配置文件和网页家目录

```shell
[root@docker-0001 ~]# mkdir /var/webconf
[root@docker-0001 ~]# cp /usr/local/nginx/conf/nginx.conf /var/webconf/
[root@docker-0001 ~]# vim /var/webconf/nginx.conf
        location ~ \.php$ {
            root           html;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            include        fastcgi.conf;
        }
[root@docker-0001 ~]# docker run -itd -p 80:80 --name nginx \
      -v /var/webconf/nginx.conf:/usr/local/nginx/conf/nginx.conf myos:nginx
# 查看验证
[root@docker-0001 ~]# docker exec -it nginx /bin/bash
[root@e440b53a860a html]# cat /usr/local/nginx/conf/nginx.conf
[root@e440b53a860a html]# # 查看 php 相关配置是否被映射到容器内
```



# 5. 微服务案例

## 5.1 问题

本案例要求自作镜像实现 nginx+php-fpm服务，主要完成内容：

1. 启动容器并测试

## 5.2 步骤

实现此案例需要按照如下步骤进行。

FastCGI工作原理，如图-1所示。

![img](https://img-blog.csdnimg.cn/img_convert/9d3efa10a155a015de3ab641af461bda.png)

图-1

**步骤一：运行容器（在docker-0001操作）**

在真机上面提前准备好所有需要的网页文件，然后通过共享卷将真机的文件映射到nginx和php-fpm容器中，实现数据共享。

1）在真机提前准备网页文件

所有网页文件已经提前共享到云盘，在第四阶段的kubernetes/docker-images/目录下。

```shell
[root@docker-0001 ~]# mkdir -p /var/{webroot,webconf}
[root@docker-0001 ~]# cd kubernetes/docker-images
[root@docker-0001 ~]# cp info.php info.html /var/webroot/
[root@docker-0001 ~]# cp /usr/local/nginx/conf/nginx.conf /var/webconf/
[root@docker-0001 ~]# vim /var/webconf/nginx.conf
        location ~ \.php$ {
            root           html;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            include        fastcgi.conf;
        }
# 启动前端 nginx 服务，并映射共享目录和配置文件
[root@docker-0001 ~]# docker run -itd --name nginx -p 80:80 \
      -v /var/webconf/nginx.conf:/usr/local/nginx/conf/nginx.conf \
      -v /var/webroot:/usr/local/nginx/html myos:nginx
# 启动后端 php 服务，并映射共享目录
[root@docker-0001 ~]# docker run -itd --network=container:nginx \
      -v /var/webroot:/usr/local/nginx/html myos:php-fpm
# 验证服务
[root@docker-0001 ~]# curl http://docker-0001/info.html
<html>
  <marquee  behavior="alternate">
      <font size="12px" color=#00ff00>Hello World</font>
  </marquee>
</html>
[root@docker-0001 ~]# curl http://docker-0001/info.php
<pre>
Array
(
    [REMOTE_ADDR] => 172.17.0.1
    [REQUEST_METHOD] => GET
    [HTTP_USER_AGENT] => curl/7.29.0
    [REQUEST_URI] => /info.php
)
php_host:     f705f89b45f9
1229
```



# 6. 搭建私有镜像仓库

## 6.1 问题

本案例要求搭建私有镜像仓库，具体要求如下：

1. 在192.168.1.100上搭建私有镜像仓库
2. 所有 node 节点配置私有仓库地址

## 6.2 方案

完成后续课程的学习需要提前准备实验用的虚拟机，实验虚拟机列表如表-1所示。

所有主机的主机名和IP必须与列表相同!!!

否则后续所有试验都无法顺利完成！！！

表-1

## 6.3 步骤

实现此案例需要按照如下步骤进行。

Docker镜像参考拓扑图如图-2所示。

![img](https://img-blog.csdnimg.cn/img_convert/7519bf26773e5a9803568565d034e6bf.png)

图-2

**步骤一：搭建私有仓库服务器（在192.168.1.100服务器操作）**

1）安装软件并启动服务

```shell
[root@localhost ~]# yum install docker-distribution
[root@localhost ~]# systemctl start docker-distribution
[root@localhost ~]# systemctl enable docker-distribution
```

2）查看配置文件（不需要修改）

```shell
[root@localhost ~]# cat /etc/docker-distribution/registry/config.yml
配置文件中定义存放镜像的路径为/var/lib/registry
配置文件中默认端口号为5000
```

3）使用curl测试

```shell
[root@localhost ~]# curl http://仓库ip:5000/v2/_catalog
```

**步骤二：搭建私有仓库服务器**

注意：在所有node主机都需要操作，下面以192.168.1.31为例！！！

修改docker配置文件，改配置文件默认连接的仓库为国外官网的仓库，我们需要修改为自己定义的192.168.1.100服务器。

```shell
[root@localhost ~]# vim  /etc/docker/daemon.json     # 默认没有该文件，需要新建
{
    "exec-opts": ["native.cgroupdriver=systemd"],
    "registry-mirrors": ["https://hub-mirror.c.163.com"],
    "insecure-registries":["192.168.1.100:5000", "registry:5000"]
}
# insecure-registries后面根私有仓库的服务器IP和端口
[root@localhost ~]# docker rm -f $(docker ps -aq)
[root@localhost ~]# systemctl restart docker
# 注意：重启docker服务前要停止所有容器
```



# 7. 上传镜像到私有仓库

## 7.1 问题

本案例要求上传镜像到私有仓库，具体要求如下：

1. 在 192.168.1.100 上搭建私有镜像仓库
2. 从 docker-0001 上传镜像到仓库主机
3. 在 docker-0002 上使用远程仓库下载镜像、启动容器

## 7.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：上传镜像（在docker-0001主机操作）**

1）修改docker配置文件，指定192.168.1.100为私有仓库服务器

```shell
[root@docker-0001 ~]# vim  /etc/docker/daemon.json     # 默认没有该文件，需要新建
{
    "exec-opts": ["native.cgroupdriver=systemd"],
    "registry-mirrors": ["https://hub-mirror.c.163.com"],
    "insecure-registries":["192.168.1.100:5000", "registry:5000"]
}
[root@docker-0001 ~]# docker rm -f $(docker ps -aq)
[root@docker-0001 ~]# systemctl restart docker
# 注意：重启docker服务前要停止所有容器
```

2）上传镜像

```shell
[root@docker-0001 ~]# docker tag \
docker.io/busybox:latest  192.168.1.100:5000/busybox:latest
# 修改镜像的标签
[root@ docker-0001 ~]# docker images
# 查看镜像标签修改的效果
[root@docker-0001 ~]# docker push 192.168.1.100:5000/busybox:latest
# 上传镜像到192.168.1.100服务器（前面已经搭建好了私有仓库服务器）
The push refers to a repository [192.168.1.100:5000/busybox]
a6d503001157: Pushed 
latest: digest: sha256:43d5f7 ... ... ccd7a7cec79464 size: 527
```

3）使用curl查看刚刚上传的镜像

```shell
[root@docker-0001 ~]# curl http://192.168.1.100:5000/v2/_catalog
{"repositories":["busybox","myos"]}
[root@docker-0001 ~]# curl http://192.168.1.100:5000/v2/myos/tags/list
{"name":"myos","tags":["httpd","latest","nginx","php-fpm"]}
```

**步骤二：下载镜像（在docker-0002主机操作）**

1）修改docker配置文件，指定192.168.1.100为私有仓库服务器

```shell
[root@docker-0002 ~]# vim  /etc/docker/daemon.json     # 默认没有该文件，需要新建
{
    "exec-opts": ["native.cgroupdriver=systemd"],
    "registry-mirrors": ["https://hub-mirror.c.163.com"],
    "insecure-registries":["192.168.1.100:5000", "registry:5000"]
}
[root@docker-0002 ~]# docker rm -f $(docker ps -aq)
[root@docker-0002 ~]# systemctl restart docker
# 注意：重启docker服务前要停止所有容器
```

2）从私有仓库下载镜像

在一个没有任何镜像的机器上启动容器

语法格式：

docker run -it 仓库IP:5000/镜像的名称:镜像的标签

```shell
[root@docker-0002 ~]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
# 查看默认没有镜像
[root@docker-0002 ~]# docker run -it 192.168.1.100:5000/myos:latest
Unable to find image '192.168.1.100:5000/myos:latest' locally
Trying to pull repository 192.168.1.100:5000/myos ... 
latest: Pulling from 192.168.1.100:5000/myos
b1300879af4c: Pull complete 
[root@09845adc59fb /]# 
```


> 如有侵权，请联系作者删除
