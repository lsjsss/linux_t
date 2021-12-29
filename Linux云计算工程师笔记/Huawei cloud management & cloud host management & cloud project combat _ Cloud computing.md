@[TOC]( Huawei cloud management & cloud host management & cloud project combat | Cloud computing )

---

# 1 案例1：创建虚拟私有云

## 1.1 问题

本案例要求：

- 创建虚拟私有云

## 1.2 步骤

实现此案例需要按照如下步骤进行。

步骤一：创建虚拟私有云，如图-1

![img](https://img-blog.csdnimg.cn/img_convert/1c68fd33ae091dace0ec324574d89008.png)
图-1

选择区域，名称等，如图-2：

![img](https://img-blog.csdnimg.cn/img_convert/ea635ad8656c508020948bc706ad8705.png)
图-2



# 2 案例2：购买云主机

## 2.1 问题

本案例要求在华为云上购买 2 台云主机实现如下操作：

- 云主机 ecs-proxy（登录方式，密码）
- 云主机 ecs-host （登录方式，密钥）

## 2.2 步骤

实现此案例需要按照如下步骤进行。

选择弹性云服务器ECS，如图-3

![img](https://img-blog.csdnimg.cn/img_convert/002c7e63b65136f05f0a262d24d7e812.png)
图-3

选择按需购买ECS，选择型号和系统后，查看价格，如图-4

![img](https://img-blog.csdnimg.cn/img_convert/7a3a8e525beb7c1eba3ad445e614a2c6.png)
![img](https://img-blog.csdnimg.cn/img_convert/12c2274b6b3cbf7a99acaf20f9c5c2a0.png)
图-4

网络配置，如图-5

![img](https://img-blog.csdnimg.cn/img_convert/9b0d2ea4ef9a56d03df262bc40eaea83.png)
图-5

设置密码，如图-6

![img](https://img-blog.csdnimg.cn/img_convert/dec1cd2f6fafdc12c4b4117bba37b900.png)
图-6

使用云主机，如图-7

![img](https://img-blog.csdnimg.cn/img_convert/f9d6921348052ee3e3c377ffdd4e9945.png)
![img](https://img-blog.csdnimg.cn/img_convert/6def085eded9c4f85e3d69fbcc6fb7c2.png)
图-7



# 3 案例3：弹性公网IP与安全组配置

## 3.1 问题

本案例要求购买弹性公网 IP 和带宽：

- 在云主机上配置华为云私网YUM源
- 安装软件测试bash-completion
- 让云主机可以访问互联网
- 配置安全组
- 允许互联网用户访问云主机服务

## 3.2 步骤

实现此案例需要按照如下步骤进行。

如何使用 华为云私网Yum源？

在文档中心搜索 "华为云 yum 源"

https://support.huaweicloud.com/ecs_faq/ecs_faq_1003.html

在云主机上配置华为云 Yum 源 (2台)

配置以后使用 yum repolist 查看

安装 bash-completion 进行测试

配置yum源，并测试

```shell
[root@localhost ~]# rm -rf /etc/yum.repos.d/*.repo
[root@localhost ~]# curl -o \ 
/etc/yum.repos.d/CentOS-Base.repo \ http://mirrors.myhuaweicloud.com/repo/CentOS-Base-7.repo
[root@localhost ~]# yum install –y bash-completion
```

购买弹性公网IP，如图-8和图-9所示。

![img](https://img-blog.csdnimg.cn/img_convert/38479cac7381d94de4706b05f328b3cb.png)
图-8

![img](https://img-blog.csdnimg.cn/img_convert/692853f297e8a2128928c992263e2ac5.png)
图-9

绑定公网IP，如图-10所示。

![img](https://img-blog.csdnimg.cn/img_convert/2f05ca5f5b4c1d75090a904503a82e9d.png)
图-10

设置安全组，如图-11、图-12、图-13所示。

![img](https://img-blog.csdnimg.cn/img_convert/770cd26446a0ccde5a001b5724ca276a.png)
图-11

![img](https://img-blog.csdnimg.cn/img_convert/ca9730ebe80d38fed30ab3d7073be447.png)
图-12

![img](https://img-blog.csdnimg.cn/img_convert/f04d059cb4ac3ec642bc15e396746382.png)
图-13

连接公网IP，如图-14。

![img](https://img-blog.csdnimg.cn/img_convert/6ad917646b7212c16b333d7ffc5f7fa5.png)
图-14



# 4 案例4：创建模板机和跳板机

## 4.1 问题

本案例要求创建模板机和跳板机：

- ecs-proxy 跳板机
- ecs-host 模板

## 4.2 步骤

实现此案例需要按照如下步骤进行。

```shell
# 配置yum源
[root@ecs-proxy ~]# rm -rf /etc/yum.repos.d/*.repo
[root@ecs-proxy ~]# curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.myhuaweicloud.com/repo/CentOS-Base-7.repo
[root@ecs-proxy ~]# yum clean all
[root@ecs-proxy ~]# yum makecache
[root@ecs-proxy ~]# yum install -y net-tools lftp rsync psmisc vim-enhanced tree vsftpd  bash-completion createrepo lrzsz iproute
[root@ecs-proxy ~]# mkdir /var/ftp/localrepo
[root@ecs-proxy ~]# cd /var/ftp/localrepo
[root@ecs-proxy ~]# createrepo  .
[root@ecs-proxy ~]# createrepo --update . # 更新
[root@ecs-proxy ~]# systemctl enable --now vsftpd
# 优化系统服务
[root@ecs-proxy ~]# systemctl stop postfix atd tuned
[root@ecs-proxy ~]# yum remove -y postfix at audit tuned kexec-tools firewalld-*
[root@ecs-proxy ~]# vim /etc/cloud/cloud.cfg
# manage_etc_hosts: localhost 注释掉这一行
[root@ecs-proxy ~]# reboot
# 安装配置ansible管理主机
[root@ecs-proxy ~]# tar zxf ansible_centos7.tar.gz
[root@ecs-proxy ~]# yum install -y ansible_centos7/*.rpm
[root@ecs-proxy ~]# ssh-keygen -t rsa -b 2048 -N '' -f /root/.ssh/id_rsa
[root@ecs-proxy ~]# chmod 0400 /root/.ssh/id_rsa
[root@ecs-proxy ~]# ssh-copy-id -i /root/.ssh/id_rsa 模板主机IP
```

2）配置模板机

```shell
[root@ecs-host ~]# rm -rf /etc/yum.repos.d/*.repo
[root@ecs-host ~]# curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.myhuaweicloud.com/repo/CentOS-Base-7.repo
[root@ecs-host ~]# vim /etc/yum.repos.d/local.repo 
[local_repo]
name=CentOS-$releasever – Localrepo
baseurl=ftp://192.168.1.252/localrepo
enabled=1
gpgcheck=0
[root@ecs-host ~]# yum clean all
[root@ecs-host ~]# yum makecache
[root@ecs-host ~]# yum repolist
[root@ecs-host ~]# yum install -y net-tools lftp rsync psmisc vim-enhanced tree lrzsz bash-completion iproute
# 优化系统服务
[root@ecs-host ~]# systemctl stop postfix atd tuned
[root@ecs-host ~]# yum remove -y postfix at audit tuned kexec-tools firewalld-*
[root@ecs-host ~]# vim /etc/cloud/cloud.cfg
# manage_etc_hosts: localhost 注释掉这一行
[root@ecs-host ~]# yum clean all 
[root@ecs-host ~]# poweroff
# 注：配置完成以后，关机，在华为云主机管理菜单中把模板主机系统硬盘做成镜像，供以后使用
```



# 5 案例5：部署网站实战

## 5.1 问题

本案例要求部署网站：

- 购买3台云主机（web服务器）
- 安装配置 web 集群（推荐playbook方式）

## 5.2 步骤

实现此案例需要按照如下步骤进行。

```shell
[root@ecs-proxy ~]# mkdir -p web-site
[root@ecs-proxy ~]# cd web-site
[root@ecs-proxy ~]# vim ansible.cfg
[defaults]
inventory         = hostlist
host_key_checking = False
[root@ecs-proxy ~]# vim hostlist
[web]
192.168.1.[11:13]
[root@ecs-proxy ~]# vim web_install.yaml
---
- name: web 集群安装
  hosts: web
  tasks:
  - name: 安装 apache 服务 
    yum:
      name: httpd,php
      state: latest
      update_cache: yes
  - name: 配置 httpd 服务 
    service:
      name: httpd
      state: started
      enabled: yes
  - name: 部署网站网页
    unarchive:
      src: files/webhome.tar.gz
      dest: /var/www/html/
      copy: yes
      owner: apache
      group: apache
[root@ecs-proxy ~]# mkdir files
# 上传 webhome.tar.gz 到 files 目录下
[root@ecs-proxy ~]# ansible-playbook web_install.yaml
```

部署完成之后，购买弹性负载均衡ELB，如图-15

![img](https://img-blog.csdnimg.cn/img_convert/78e87c85a5c0419b1f7152b8570d95b8.png)
图-15

添加监听器和后端服务器，如图-16和图-17所示。

![img](https://img-blog.csdnimg.cn/img_convert/894c82445c332bc41fbe053c61498beb.png)
图-16

![img](https://img-blog.csdnimg.cn/img_convert/85c0b347d0e9c9c4a9c1f7c58082aa30.png)
图-17

绑定公网IP，测试访问，如图-18所示。

![img](https://img-blog.csdnimg.cn/img_convert/2137e62b9f03da8e864113efba281a62.png)
图-18

> 如有侵权，请联系作者删除
