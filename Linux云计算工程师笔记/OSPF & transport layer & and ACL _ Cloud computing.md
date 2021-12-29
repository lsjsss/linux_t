@[TOC]( OSPF & transport layer & and ACL | Cloud computing )

---
# 1. 动态路由
## 1.1 问题
通过配置静态路由协议ospf实现全网互通，按照图-1拓扑图所示

![在这里插入图片描述](https://img-blog.csdnimg.cn/7aec552222fb4851885e529fe4b4e314.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-1

## 1.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：配置交换机**

1）S3700交换机配置
```shell
[Huawei]vlan batch 2 3            //创建VLAN2、3
[Huawei]interface Ethernet0/0/2
[Huawei-Ethernet0/0/2]port default vlan 2
[Huawei]interface Ethernet0/0/3
[Huawei-Ethernet0/0/3]port default vlan 3
[Huawei]interface Ethernet0/0/4  （该接口连接了三层交换机S5700）
[Huawei-Ethernet0/0/4]port link-type trunk
[Huawei-Ethernet0/0/4]port trunk allow-pass vlan all
```
2）S5700交换机配置
```shell
[Huawei]vlan batch 2 3 4            //创建VLAN2、3、4
[Huawei]interface Vlanif 1
[Huawei-Vlanif4]ip address  192.168.1.254 24
[Huawei]interface Vlanif 2
[Huawei-Vlanif4]ip address  192.168.2.254 24
[Huawei]interface Vlanif 3
[Huawei-Vlanif4]ip address  192.168.3.254 24
[Huawei]interface Vlanif 4
[Huawei-Vlanif4]ip address  192.168.4.1 24
[Huawei]interface GigabitEthernet 0/0/1   （该接口连接了S3700交换机）
[Huawei-GigabitEthernet0/0/1] port link-type trunk
[Huawei-GigabitEthernet0/0/1] port trunk allow-pass vlan all
[Huawei]interface GigabitEthernet 0/0/2   （该接口连接了路由器）
[Huawei-GigabitEthernet0/0/2] port link-type access
[Huawei-GigabitEthernet0/0/2] port default vlan 4
[Huawei]ospf 1
[Huawei-ospf-1]area 0
[Huawei-ospf-1-area-0.0.0.0]network 192.168.1.0 0.0.0.255
[Huawei-ospf-1-area-0.0.0.0]network 192.168.2.0 0.0.0.255
[Huawei-ospf-1-area-0.0.0.0]network 192.168.3.0 0.0.0.255
[Huawei-ospf-1-area-0.0.0.0]network 192.168.4.0 0.0.0.255
[Huawei]ip route-static 0.0.0.0 0.0.0.0 192.168.4.2
```
**步骤二：配置路由器**

AR2220路由器配置如下
```shell
[Huawei]interface GigabitEthernet 0/0/0
[Huawei-GigabitEthernet0/0/0] ip address  192.168.4.2 24
[Huawei]interface GigabitEthernet 0/0/1
[Huawei-GigabitEthernet0/0/0] ip address  192.168.5.254 24
[Huawei]ospf 1
[Huawei-ospf-1]area 0
[Huawei-ospf-1-area-0.0.0.0]network 192.168.4.0 0.0.0.255
```

# 2. 基本ACL的配置（1）
## 2.1 问题
按照图-2所示拓扑结构，禁止主机pc2与pc1通信，而允许所有其他流量

![在这里插入图片描述](https://img-blog.csdnimg.cn/03809e5a419d4b3e84703b21400812d2.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-2

## 2.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：配置IP**

为路由器g0/0/0接口配置ip 192.168.1.254，为路由器g0/0/1接口配置ip 192.168.2.254
```shell
[Huawei]interface GigabitEthernet 0/0/0
[Huawei-GigabitEthernet0/0/0] ip address  192.168.1.254 24
[Huawei]acl 2000
[Huawei-acl-basic-2000]rule deny source 192.168.2.1 0
[Huawei]interface GigabitEthernet 0/0/1
[Huawei-GigabitEthernet0/0/1]ip address  192.168.2.254 24
[Huawei-GigabitEthernet0/0/1]traffic-filter inbound acl 2000
```

# 3. 基本ACL的配置（2）
## 3.1 问题
按照图-3所示拓扑结构，允许主机pc2与pc1互通，而禁止其他设备访问pc1

![在这里插入图片描述](https://img-blog.csdnimg.cn/89ab9930578e497ab5c33cffa1d84077.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-3

## 3.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：放行192.168.2.1，拒绝其他设备**

此步骤需要在上一实验基础上进行
```shell
[Huawei]acl 2001
[Huawei-acl-basic-2001]rule permit source 192.168.2.1 0
[Huawei-acl-basic-2001]rule deny source any
[Huawei]interface GigabitEthernet 0/0/1
[Huawei-GigabitEthernet0/0/1]undo traffic-filter inbound acl 2000
[Huawei-GigabitEthernet0/0/1] traffic-filter inbound acl 2001
```

# 4. 高级ACL
## 4.1 问题
按照图-4所示拓扑结构，禁止pc2访问pc1的ftp服务，禁止pc3访问pc1的www服务，所有主机的其他服务不受限制

![在这里插入图片描述](https://img-blog.csdnimg.cn/2a694fc65e464f9b850dcedbcd6ab365.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-4

## 4.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：根据协议所用端口进行封堵**

此步骤需要在上一实验基础上进行
```shell
[Huawei]acl 3000
[Huawei-acl-adv-3000]rule deny tcp source 192.168.2.1 0 destination 192.168.1.1 
0 destination-port eq 21
[Huawei-acl-adv-3000]rule deny tcp source 192.168.2.2 0 destination 192.168.1.1 
0 destination-port eq 80
[Huawei]interface g0/0/1
[Huawei-GigabitEthernet0/0/1]traffic-filter inbound acl 3000      //在接口中应用acl
```

# Exercise
## 1 传输层有哪些协议，各有什么特点？

TCP（Transmission Control Protocol）
传输控制协议
可靠的、面向连接的协议
传输效率低

UDP（User Datagram Protocol）
用户数据报协议
不可靠的、无连接的服务
传输效率高

## 2 描述TCP三次握手以及四次断开的过程

三次握手

/

四次断开

/

## 3 SMTP、DNS、Telnet、TFTP、NTP分别是什么协议，使用了什么端口？

SMTP 简单邮件传输协议 端口号25
DNS 域名系统 端口号53
Telnet 远程登录 端口号23
TFTP 简单文件传输协议 端口号69
NTP 网络时间协议 端口号123

## 4 ACL常见类型有哪些，各有什么区别？

基本ACL
基于源IP地址过滤数据包
基本访问控制列表的列表号是2000~2999

高级ACL
基于源IP地址、目的IP地址、指定协议、端口来过滤数据包
高级访问控制列表的列表号是3000~3999



> 如有侵权，请联系作者删除
