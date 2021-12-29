@[TOC]( Deploy GitLab & configure GitLab & CI/CD Overview & Deploy Jenkins | Cloud computing )

---
# 1. 部署GitLab
## 1.1 问题
本案例要求搭建一台GitLab服务器，要求如下：

- 准备环境（容器环境）
- 安装GitLab

## 1.2 方案
实验环境准备（沿用DAY01的实验环境）：

1）准备两台RHEL8虚拟机，主机名分别为develop和git。
2）develop主机的IP地址为192.168.4.10，不需要配置网关和DNS。
3）git主机的IP地址为192.168.4.20，不需要配置网关和DNS。
4）给develop和git两台主机配置可用的YUM源。

备注：跨网段走路由，相同网段不需要配置网关就可以互联互通！

实验拓扑如图-1所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/e64887bbb64440c6bb38479e88794720.png)
图-1

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：环境准备（在192.168.4.20主机操作）**

1）防火墙、SELinux。
```shell
[root@git ~]# firewall-cmd --set-default-zone=trusted
[root@git ~]# setenforce 0
[root@git ~]# sed -i '/SELINUX/s/enforcing/permissive/' /etc/selinux/config
```

2)修改sshd默认端口。

因为Git是通过SSH协议形式访问，后面需要启动GitLab容器，该容器需要占用22端口，而电脑的sshd服务也需要占用22端口（端口冲突），所以需要提前修改sshd默认端口，将端口修改为2022。

注意：修改后需要重新登录一次虚拟机（重新登录需要指定端口）。
```shell
[root@git ~]# vim /etc/ssh/sshd_config
Port 2022                                               #17行
[root@git ~]# systemctl restart sshd
[root@git ~]# exit
真机# ssh -p 2022  192.168.4.20 
```
3）准备容器环境。

提示：gitlab_zh.tar在第二阶段素材目录中，需要先将该素材拷贝到192.168.4.20主机。（比如拷贝到/root目录）
```shell
[root@git ~]# dnf  -y   install   podman
[root@git ~]# podman load < ./gitlab_zh.tar
[root@git ~]# podman images
REPOSITORY               TAG      IMAGE ID          CREATED       SIZE
localhost/gitlab_zh   latest   1f71f185271a       2 years ago   1.73 GB
```
4）创建数据目录

容器无法持久保存数据，需要将真机目录和容器目录绑定，实现数据永久保存。
```shell
[root@git ~]# mkdir -p /srv/gitlab/{config,logs,data}
```
**步骤二：启动GitLab容器(192.168.4.20操作)**

1）启动容器
```shell
[root@git ~]# touch /etc/resolv.conf                       
#如果没有该文件则创建文件，防止无法podman run启动容器
[root@git ~]# podman run -d -h gitlab --name gitlab \
-p 443:443 -p 80:80 -p 22:22 \
--restart=always \
-v /srv/gitlab/config:/etc/gitlab \
-v /srv/gitlab/logs:/var/log/gitlab \
-v /srv/gitlab/data:/var/opt/gitlab \
gitlab_zh
```
注释：
-d将容器放入后台启动。
-h设置容器的主机名为gitlab。
--name设置容器名称为gitlab。
-p进行端口映射，将git主机的443、80、22端口和git上面运行的容器端口绑定

这样以后任何人访问git主机(192.168.4.20)的22端口也就是在访问容器里面的22端口，任何人访问git主机(192.168.4.20)的80端口也就是访问容器里面的80端口。

-v将git主机上面的目录和容器里面的目录绑定，git主机的/srv/gitlab/config目录对应容器里面的/etc/gitlab/目录，其他目录同理。

`最后的gitlab_zh是镜像名称。`

2）配置systemd，实现容器开机自启动(选做实验)

生成service文件，-n是容器的名称，给gitlab容器生成service文件
```shell
[root@git ~]# cd /usr/lib/systemd/system
[root@git ~]# podman generate systemd -n gitlab --files
[root@git ~]# cd ~
```
设置开机自启动
```shell
[root@git ~]# systemctl enable container-gitlab.service
```
3）初始化登录密码（真机使用浏览器访问GitLab页面）
```shell
# firefox http://192.168.4.20
```
GitLab默认用户名为root，第一次访问需要设置密码，效果如图-2所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/c3d641098f82444ba786a70ceef9c442.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_12,color_FFFFFF,t_70,g_se,x_16)
图-2

设置密码后即可使用新设置的密码登录（密码要8位，有字母符号数字组成），效果如图-3所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/9a78cdbf827b4552bd316a53fd423b74.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_13,color_FFFFFF,t_70,g_se,x_16)
图-3

# 2. 配置GitLab
## 2.1 问题
沿用练习一，配置GitLab，具体要求如下：

- 创建GitLab用户和组
- 创建GitLab项目
- 客户端管理GitLab项目
- 上传代码

## 2.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：创建用户和组**

1）创建用户，点击GitLab页面的小扳手图标，创建用户，效果如图-4所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/ce650ecab70844bd8ffbd40b9fbce4bc.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-4

创建jerry用户，点击《编辑》设置用户的密码，效果如图-5所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/e3f9ca450e574b5ba33e52d87e4f3cd1.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-5

2）创建组

点击GitLab页面的小扳手图标，创建组，效果如图-6所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/0b50385939d8411c8b107381cea7b525.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-6

设置组名称（组名称为devops）以及可见等级（等级为公开），效果如图-7所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/bd0802f7837441cda8808a284bdf5cf0.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_15,color_FFFFFF,t_70,g_se,x_16)
图-7

3）将用户加入到组（将jerry用户加入devops组），效果如图-8所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/77aaeb5c6c944b0fa600f0f0b813e84e.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-8

**步骤二：创建GitLab项目**

1）创建项目，效果如图-9所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/468c06d8bb7f49ebb23d6922deb84af9.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-9

2）设置项目名称、组、可见等级，效果如图-10所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/c1be8df2650f46799ce17bde3a56ff31.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图-10

**步骤三：管理GitLab项目**

1）客户端使用密码管理GitLab项目（在192.168.4.10主机操作）
```shell
[root@develop ~]# git config --global user.name "Administrator"
[root@develop ~]# git config --global user.email "admin@example.com"
[root@develop ~]# git clone http://192.168.4.20/devops/myproject.git
[root@develop ~]# cd myproject
[root@develop myproject]# touch README.md
[root@develop myproject]# git add README.md
[root@develop myproject]# git commit -m "add README"
[root@develop myproject]# git push -u origin master
Username for 'http://192.168.4.20': jerry    #这里输入用户名
Password for 'http://jerry@192.168.4.20':    #这里输入密码
```
2）客户端生成SSH密钥（在192.168.4.10主机操作）
```shell
[root@develop myproject]# rm -rf /root/.ssh/known_hosts  #删除之前的ssh远程记录
[root@develop myproject]# ssh-keygen                   #生成ssh密钥文件
[root@develop myproject]# cat ~/.ssh/id_rsa.pub       #查看密钥文件
ssh-rsa 
AAAAB3NzaC1yc2EAAAADAQABAAABAQDPVwP8E7TtKha9H8Ec+CU2n19aIPo9sUa/pdM7gRaf0yG+Bcdy
Q7Hgi6pI51IhX6tat46L5tLkAY7urVeEmnPtUk/TVIUc0smJPXYKIggOCr2dDd9s1S0
```
3）使用jerry用户登录GitLab页面

jerry用户第一次登录页面需要重置一次密码，密码可以与旧密码相同。效果如图-11所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/38e34527b02f47bb87cb620883317b35.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-11

4）上传密钥

将刚刚192.168.4.10上面创建的密钥文件内容上传到GitLab。

点击右上角账户图标，点击《设置》，点击展开按钮，点击《SSH密钥》，然后将develop主机生成的密钥文件内容复制到GitLab上面。效果如图-12、图-13所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/73f1a057037844598d1f3bb59c372b72.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-12

![在这里插入图片描述](https://img-blog.csdnimg.cn/b5ec8c264f5742039fea38a42855a034.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-13

5）使用密钥管理GitLab项目

首先要查看下基于SSH连接方式的链接，如图-14所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/a9b1bb57b28048ceae052d3e86ae75ab.png)
图-14
```shell
[root@develop myproject]# git remote remove origin
[root@develop myproject]# git remote add \
origin git@192.168.4.20:devops/myproject.git
```
#重要备注:

前面的案例使用http协议访问clone了服务器的代码仓库，这里把之前的http服务器信息删除（remove：删除），然后在添加新的服务器信息(add：添加)，使用ssh协议访问服务器。
```shell
[root@develop myproject]# echo hello word >> README.md
[root@develop myproject]# git add .
[root@develop myproject]# git commit -m "modify readme"
[root@develop myproject]# git push -u origin master
```
6) 上传静态页面代码（代码在第二阶段素材lnmp_soft.tar.gz中）

需要提前将真机的网页素材scp拷贝到develop虚拟机用户的家目录，解压lnmp_soft.tar.gz，在该压缩包里面有一个www_template.zip文件。
```shell
[root@develop ~]# dnf  -y  install   unzip tar
[root@develop ~]# unzip  www_template.zip
[root@develop ~]# cp -r www_template/*   myproject/
[root@develop ~]# cd  myproject/
[root@develop myproject]# git add .
[root@develop myproject]# git commit -m  "web site"
[root@develop myproject]# git push -u origin master
[root@develop myproject]# git tag  v1
[root@develop myproject]# git push -u origin v1
```
通过tag可以给代码设置版本标签，如v1，v2，v3等等。

# 3. 部署Jenkins
## 3.1 问题
沿用练习二，部署CI/CD环境，部署Jenkins，具体要求如下：

- 准备实验环境
- 部署Jenkins、初始化Jenkins
- 管理Jenkins插件、调整系统配置

## 3.2 方案
实验环境准备：

1）5台RHEL8虚拟机，主机名分别为develop、git、jenkins、web1和web2。
2）develop主机的IP地址为192.168.4.10，不需要配置网关和DNS。
3）git主机的IP地址为192.168.4.20，不需要配置网关和DNS。
4）jenkins主机的IP地址为192.168.4.30，不需要配置网关和DNS。
5）web1和web2主机的IP地址分别为192.168.4.100和192.168.4.200，不需要配置网关和DNS。
6）所有主机都需要配置可用的系统YUM源，设置防火墙信任所有，SELinux放行所有。

备注：跨网段走路由，相同网段不需要配置网关就可以互联互通！实验拓扑如图-15所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/60ce027f22934b2f92200f5a706141d7.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-15

**步骤一：环境准备**

1）设置防火墙和SELinux（仅以一台主机为例，其他所有主机都需要操作）
```shell
[root@git ~]# firewall-cmd --set-default-zone=trusted
[root@git ~]# setenforce 0
[root@git ~]# sed -i '/SELINUX/s/enforcing/permissive/' /etc/selinux/config
```
2）安装依赖软件（git、postfix、java JDK）。

注意：仅在jenkins主机操作！
```shell
[root@jenkins ~]# dnf -y install git
[root@jenkins ~]# dnf -y install postfix
[root@jenkins ~]# dnf -y install mailx
[root@jenkins ~]# dnf -y install java-11-openjdk
[root@jenkins ~]# systemctl enable postfix --now
```
备注：Git（版本控制软件）、postfix（邮件服务器软件）、mailx（邮件客户端软件）、openjdk（Java JDK工具）。

**步骤二：部署、初始化Jenkins**

1）安装、启动Jenkins。
```shell
[root@jenkins ~]# dnf -y install ./jenkins-2.263.1-1.1.noarch.rpm
[root@jenkins ~]# systemctl enable jenkins
[root@jenkins ~]# systemctl start jenkins
#设置jenkins服务为开机自启动服务，并立刻启动该服务
```
2）初始化Jenkins

真机浏览器访问Jenkins页面（firefox http://192.168.4.30:8080）。

第一次访问会提示初始密码的位置（密码在/var/lib/Jenkins/secrets/initialAdminPassword文件中），效果如图-16所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/3e1db9d154d044a2a14f500ac62d5077.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-16

初始化时选择不安装插件，效果如图-17和图-18所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/efb4485369944d55b5299ae83faebcb5.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_16,color_FFFFFF,t_70,g_se,x_16)
图-17

![在这里插入图片描述](https://img-blog.csdnimg.cn/148c5fb55b38445b9ca9e3271224e1c5.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_17,color_FFFFFF,t_70,g_se,x_16)
图-18

使用默认的admin用户登录，完成初始化操作，效果如图-19，图-20，图-21所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/e9126dcd9c3444b4a1b13fbcbd2d427a.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图-19

![在这里插入图片描述](https://img-blog.csdnimg.cn/1380bc4a3e1c4acdaed8bdd3236101bd.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_18,color_FFFFFF,t_70,g_se,x_16)
图-20

![在这里插入图片描述](https://img-blog.csdnimg.cn/c6d961eccdd84eb59dcc6423231c5c82.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-21

**步骤三：管理Jenkins插件、系统配置**

1）重置管理员密码。

重置密码如图-22所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/98868ea72a0643dd9647579a9c0ebd6a.png)
图-22

使用新密码重新登录，如图-23所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/49221c05ace4411f87d7aa81355d30c6.png)
图-23

2）插件管理。

查看插件列表，效果如图-24、图-25所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/0884b407f8dc4160bb29020c76aebd79.png)
图-24

![在这里插入图片描述](https://img-blog.csdnimg.cn/f1a277b39f694097a96ae6cece36d4bc.png)
图-25

拷贝插件文件到Jenkins目录，Jenkins插件目录为插件目录：/var/lib/jenkins/plugins/。

Jenkins插件文件在第二阶段素材目录：jenkins_plugins.tar.gz。

插件包含：中文插件、Git插件等。

需要提前将真机素材拷贝到Jenkins虚拟机。

`警告：cp拷贝时需要-p选项保留权限!!!`

[root@jenkins ~]# tar -xf  jenkins_plugins.tar.gz
[root@jenkins ~]# cp -rp jenkins_plugins/* /var/lib/jenkins/plugins/
[root@jenkins ~]# systemctl restart jenkins
重新登录Jenkins网页控制台，如图-26所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/5b664fce86044ea0a74279be8f9f63a1.png)
图-26

再次查看插件列表，效果如图-27、图-28所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/26f09caf4e284477aa55e1199edcafc6.png)
图-27

![在这里插入图片描述](https://img-blog.csdnimg.cn/c2d1cdf5824f43e6aa35da916948f02d.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-28

3）调整系统设置，配置邮箱，效果如图-29、图-30所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/b8bb7553b97949fb9a452acd31f3ae0d.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-29

![在这里插入图片描述](https://img-blog.csdnimg.cn/4873fc9f584d4f7abb9cb4d5ead75d80.png)
图-30

附加思维导图，如图-31所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/146db67469404d50950ae73e8198b53f.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-31



# Exercise
## 1 podman从本地文件加载镜像的命令是什么?
```shell
# podman  load  < ./文件名
```
## 2 Podman实现端口映射和目录映射的选项是什么？
```shell
-p可以实现端口映射，-v可以实现目录映射
```

## 3 如何给git代码仓库创建版本标签？
```shell
# git  tag  <标签>
```

## 4 什么是CI/CD？
CI（Continuous Integration）
持续集成：开发人员的自动化流程。成功的 CI 意味着应用代码的新更改会定期构建、测试并合并到共享存储库中。

CD（Continuous Delivery）
持续交付：通常是指开发人员对应用的更改会自动进行错误测试并上传到存储库（如 GitLab 或容器注册表），然后由运维团队将其部署到实时生产环境中。

目的就是确保尽可能减少部署新代码时所需的工作量。

## 5 Jenkins默认插件目录是什么？
/var/lib/jenkins/plugins/

> 如有侵权，请联系作者删除
