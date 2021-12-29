@[TOC]( Private cloud Overview & private cloud configuration management & cloud host management | Cloud computing )

---

# 1. 登录Openstack

## 1.1 问题

本案例要求启动Openstack集群环境，具体要求如下：

- 导入教学环境，并启动Openstack集群
- 通过浏览器访问 192.168.1.10
- 登录 Openstack

## 1.2 方案

openstack 实验架构图例拓扑如图-1所示。

![img](https://img-blog.csdnimg.cn/img_convert/1f08c7aac8ae2b68f797a4b0c49036c0.png)

图-1

openstack初始化环境要求如表-1所示：

表-1

## 1.3 步骤

实现此案例需要按照如下步骤进行。

**步骤一：导入系统**

1）如果是windows系统

导入教学环境镜像到 E:\下

配置网卡连接 vmnet8、配置系统光盘路径

启动三台虚拟机 openstack、nova01、nova02

2）如果是linux系统

**步骤二：登录 openstack**

1）Web页面登录：

浏览器访问 http://192.168.1.10/

2）命令行登录：

3）总结：



# 2. 配置云主机类型并上传镜像

## 2.1 问题

本案例要求配置云主机类型，上传镜像：

- 创建一个项目 tedu
- 分配一个用户管理该项目 uu
- 自定义云主机类型 （ 2cpu， 512m 内存）
- 上传课件里面的镜像 small.img

## 2.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：创建项目**

1）创建tedu项目，如图-2所示：

![img](https://img-blog.csdnimg.cn/img_convert/10e3a443f1dab1cb775fc1fd0d427f44.png)

图-2

2）创建uu用户，如图-3所示：

![img](https://img-blog.csdnimg.cn/img_convert/5e52a9c6c0f673cbbbe132896f14aafa.png)

图-3

**步骤二：新建云主机类型**

1）通过Horizon创建云主机类型，如图-4所示：

![img](https://img-blog.csdnimg.cn/img_convert/ebb4a52b385f5f7e72f0faa56d3d1c45.png)

图-4

2）上传镜像，效果如图-5所示。

![img](https://img-blog.csdnimg.cn/img_convert/59a5c84a32f7fe19416207996f204788.png)

图-5



# 3. 配置公有网络

## 3.1 问题

本案例要求：

- 创建一个外部网络，分配给项目
- 创建一个内部网络
- 创建一个路由，把内部网络和外部网络连接起来

## 3.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：创建网络**

1）登陆admin用户，创建外网public，如图-6所示：

![img](https://img-blog.csdnimg.cn/img_convert/b4b4551dc9d232507609fa350a95273e.png)

图-6

2）退出admin用户 ，登陆uu用户，创建public的子网wan，如图-7所示：

![img](https://img-blog.csdnimg.cn/img_convert/6697a4a6783b36e20047e207ee55202b.png)

图-7

3）public外网不需要激活DHCP，如图-8所示：

![img](https://img-blog.csdnimg.cn/img_convert/1039a0af47af9739768b1ab3337a2abb.png)

图-8

4）创建内网lan，如图-9所示：

![img](https://img-blog.csdnimg.cn/img_convert/93b13d3931d1ab2bfc52ce94c0f8ae7c.png)

图-9

5）创建lan的子网，如图-10所示：

![img](https://img-blog.csdnimg.cn/img_convert/f035689e31cf0106e3fd4d11018ebd33.png)

图-10

7）给内网分配地址池，如图-11所示：

![img](https://img-blog.csdnimg.cn/img_convert/7e540a3a1d78ba55a537aa4d86ff75d2.png)

图-11

8）新建路由，如图-12所示：

![img](https://img-blog.csdnimg.cn/img_convert/7eb5537f8cfe2772f68fa1075fabb84a.png)

图-12

9）选择路由子网，如图-13所示：

![img](https://img-blog.csdnimg.cn/img_convert/870406713430646b2f4bf383b0c24da5.png)

图-13



# 4. 配置私有网络及路由

## 4.1 问题

本案例要求：

- 为项目 tedu 设置一个私有网络
- 网络名称 tedu_lan
- 定义子网 tedu_lan_subnet
- 子网IP范围: 10.10.10.101,10.10.10.200
- 启用DHCP
- 设置DNS：192.168.1.254
- 设置路由 tedu_route
- 路由要求联通内网和外网
- 路由私有网络地址为 10.10.10.254

### 4.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：创建私有网络**

创建私有网络如图-14所示。

![img](https://img-blog.csdnimg.cn/img_convert/824f703b79f5862101546d2708edc234.png)

图-14

创建子网如图-15和图-16所示。

![img](https://img-blog.csdnimg.cn/img_convert/68ce4c2b51946cf7367517c554bae0e4.png)

图-15

![img](https://img-blog.csdnimg.cn/img_convert/220c2f68aba35229332e716d5f2f5bf0.png)

图-16

**步骤二：创建路由**

创建路由如图-17所示。

![img](https://img-blog.csdnimg.cn/img_convert/4bbc29715ff1f3cecb4e76b2f8a2cf2e.png)

图-17

添加路由接口如图-18所示。

![img](https://img-blog.csdnimg.cn/img_convert/cfec83a31bc9f011ca6ae3a850bbfb45.png)

图18



# 5. 创建云主机

## 5.1 问题

本案例要求：

- 通过 web 页面创建云主机
- 并通过 web console 登录云主机

## 5.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：创建云主机**

1）创建云主机，如图-19所示：

![img](https://img-blog.csdnimg.cn/img_convert/a79e13e8d446340d294463f9c0e89e96.png)

图-19

![img](https://img-blog.csdnimg.cn/img_convert/ba94cff9c27ed5d33b457e25936e2258.png)

图-20

4）云主机类型，如图-21所示：

![img](https://img-blog.csdnimg.cn/img_convert/962e1432ea54dd95c099dd5d24bd4c74.png)

图-21

5）云主机网络，如图-22所示：

![img](https://img-blog.csdnimg.cn/img_convert/cacec3f4bc907732cef23e5b5f24cb02.png)

图-22

5）web页面访问云主机，如图-23所示：

![img](https://img-blog.csdnimg.cn/img_convert/516c6db6a164f7064edf44dc03d794b6.png)

图-23



# 6. 配置浮动IP与安全组

## 6.1 问题

本案例要求：

- 为刚刚创建的云主机设置外部访问
- 设置浮动 ip
- 配置安全组，允许外部主机 ping 云主机
- 配置安全组，允许外部主机通过 ssh 管理云主机

## 6.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：创建浮动IP**

![img](https://img-blog.csdnimg.cn/img_convert/c3cc078a488fd0a137172802e44d5a42.png)

图-24

![img](https://img-blog.csdnimg.cn/img_convert/95afc044ce87f8089beddb3d6d9a976a.png)

图-25

**步骤二：建立安全组**

1）新建一个安全组，允许SSH访问，如图-26：

![img](https://img-blog.csdnimg.cn/img_convert/35650e49f7fa0240e2c72e9dcb1c7be7.png)

图26

2）允许ssh访问，如图-27

![img](https://img-blog.csdnimg.cn/img_convert/7769fc8b23f7c63d00302c041694b00f.png)

图-27

3）允许HTTPS访问，如图-28所示：

![img](https://img-blog.csdnimg.cn/img_convert/6d76f8e3335c5900a716e3b2ca61381f.png)

图-28

**步骤三：设置安全组规则，允许外界ping通云主机**

1）添加规则，如图-29所示：

![img](https://img-blog.csdnimg.cn/img_convert/10c97cdaf775afec04ad6246bd1fa869.png)

图-29

2）增加ping规则，如图-30所示

![img](https://img-blog.csdnimg.cn/img_convert/2649f18ddfe3d3ca77cc6ddf7c567f0a.png)

图-30

7）进入控制台，配置dns的ip为192.168.1.254，这里不再重复，通过浮动ip可以ssh连接，如图-31所示：

![img](https://img-blog.csdnimg.cn/img_convert/6604634908ed725a7b880d426cd0a798.png)

图-31



# 7. 练习

## 7.1 问题

本案例要求增加一个nova计算节点：

- 把nova02虚拟机加入openstack集群
- 创建云主机，实现自动调度分配

## 7.2 步骤

实现此案例需要按照如下步骤进行。

**步骤一：安装计算节点**

1）更改answer.ini文件

```shell
[root@openstack ~]# vim answer.ini        //在openstack上面操作
98 CONFIG_COMPUTE_HOSTS=192.168.1.11,192.168.1.12    
102 CONFIG_NETWORK_HOSTS=192.168.1.10,192.168.1.11,192.168.1.12 
[root@openstack ~]# packstack --answer-file answer.ini
**** Installation completed successfully ******
```

2）这时浏览器访问时不出现页面，15-horizon_vhost.conf文件被还原，需要重新修改这个文件

```shell
[root@openstack ~]# cd /etc/httpd/conf.d/
[root@openstack conf.d]# vi 15-horizon_vhost.conf
     35   WSGIProcessGroup apache
     36   WSGIApplicationGroup %{GLOBAL}     //添加这一行
[root@openstack conf.d]# apachectl  graceful  //重新载入配置文件
```

3）浏览器访问，出现页面

```shell
[root@openstack conf.d]# firefox 192.168.1.10
[root@localhost conf.d]# cd
[root@localhost ~]# ls
answer.ini   keystonerc_admin   
[root@openstack ~]# cat keystonerc_admin   
unset OS_SERVICE_TOKEN
    export OS_USERNAME=admin
    export OS_PASSWORD=1bb4c987345c45ba
```

4）安装后的节点状态，如图-32所示：

![img](https://img-blog.csdnimg.cn/img_convert/bd8830a704faf2d434a330c7c410bfba.png)

图-32

openstack错误分析：

1）进入控制台不显示内容，如图-33所示：

![img](https://img-blog.csdnimg.cn/img_convert/08dd8283dddf1f94a9825c4dba8ff48a.png)

图-33

解决办法：可以重新启动一下openstack-nova-console

2）若出现云主机处于错误状态，如图-34所示：

![img](https://img-blog.csdnimg.cn/img_convert/eb8a449ec309386b66535ec90625d427.png)

图-34

解决办法：

可能是主机down掉

可能是内存不足

可能是内网出现了问题，检查内网，或者把内网删除（不会建立的可以参考案例4），重新建立，之后重新启动openstack

```shell
[root@openstack ~]# systemctl restart openstack-nova-compute
```
> 如有侵权，请联系作者删除
