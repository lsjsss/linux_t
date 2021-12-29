@[TOC]( NAT & VRRP | Cloud computing )

---
# 1. 配置静态NAT
## 1.1 问题
按照图-1拓扑图所示，在R1上配置静态NAT使192.168.2.1转换为100.0.0.2,192.168.2.2转换为100.0.0.3，实现外部网络访问

![在这里插入图片描述](https://img-blog.csdnimg.cn/a72d21bf39f24fbaa330e6913d870e5c.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图-1

## 1.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：配置静态NAT**
pc3无需配置网关
```shell
[Huawei]interface GigabitEthernet 0/0/0
[Huawei-GigabitEthernet0/0/0] ip address  100.0.0.1 8
[Huawei-GigabitEthernet0/0/0]nat static global 100.0.0.2 inside 192.168.2.1
[Huawei-GigabitEthernet0/0/0]nat static global 100.0.0.3 inside 192.168.2.2
```
# 2. Easy IP
## 2.1 问题
按照图-2所示的拓扑结构，在R1上配置Easy IP使企业内网192.168.2.0/24利用g0/0/0端口的ip，实现外部网络的访问

![在这里插入图片描述](https://img-blog.csdnimg.cn/9fbd64d2fc624c86a49724d7b7e8bf61.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图-2

## 2.2 步骤
实现此案例需要按照如下步骤进行

**步骤一：配置静态NAT**

注：以下命令需要在路由器配置好ip的基础上完成
```shell
[Huawei]acl 2000    
[Huawei-acl-basic-2000]rule permit source any     //使用acl定义任何内部地址
[Huawei]interface g0/0/0
[Huawei-GigabitEthernet0/0/0]nat outbound 2000    //可以利用g0/0/0的ip访问外网
```

# 3. 三层交换配置VRRP
## 3.1 问题
按照图-3所示拓扑结构，在三层交换机配置热备份路由协议使组内两个出口设备共享一个虚拟ip地址192.168.1.254为内网主机的网关

![在这里插入图片描述](https://img-blog.csdnimg.cn/3f9b2cb8033f4b22be1d5d291d7461bd.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-3

## 3.2 步骤
本实验暂不考虑NAT问题

**步骤一：pc配置ip**

pc设备配置ip与网关，192.168.1.1的网关为192.168.1.254
192.168.4.1的网关为192.168.4.254

**步骤二：路由器配置**

路由器配置
```shell
<Huawei>system-view 
[Huawei]interface GigabitEthernet 0/0/0
[Huawei-GigabitEthernet0/0/0]ip address 192.168.2.1 24
[Huawei]interface GigabitEthernet 0/0/1
[Huawei-GigabitEthernet0/0/1]ip address 192.168.3.1 24
[Huawei]interface GigabitEthernet 0/0/2
[Huawei-GigabitEthernet0/0/2]ip address 192.168.4.254 24
[Huawei]ospf    
[Huawei-ospf-1]area 0
[Huawei-ospf-1-area-0.0.0.0]network 192.168.2.0 0.0.0.255
[Huawei-ospf-1-area-0.0.0.0]network 192.168.3.0 0.0.0.255
[Huawei-ospf-1-area-0.0.0.0]network 192.168.4.0 0.0.0.255
```
**步骤三：交换机配置**

1）MS1
```shell
<Huawei>system-view
[Huawei]interface Vlanif 1
[Huawei-Vlanif1]ip add 192.168.1.252 24
[Huawei]vlan 2
[Huawei-vlan2]quit
[Huawei]interface Vlanif 2
[Huawei-Vlanif2]ip address 192.168.2.2 24
[Huawei-Vlanif2]quit
[Huawei]interface GigabitEthernet 0/0/2
[Huawei-GigabitEthernet0/0/2]port link-type access 
[Huawei-GigabitEthernet0/0/2]port default vlan 2
[Huawei]ospf    
[Huawei-ospf-1]area 0
[Huawei-ospf-1-area-0.0.0.0]network 192.168.1.0 0.0.0.255
[Huawei-ospf-1-area-0.0.0.0]network 192.168.2.0 0.0.0.255
[Huawei]interface Vlanif 1
[Huawei-Vlanif1]vrrp vrid 1 virtual-ip 192.168.1.254
```
2）MS2
```shell
<Huawei>system-view
[Huawei]interface Vlanif 1
[Huawei-Vlanif1]ip add 192.168.1.253 24
[Huawei]vlan 3
[Huawei-vlan3]quit
[Huawei]interface Vlanif 3
[Huawei-Vlanif3]ip address 192.168.3.2 24
[Huawei-Vlanif3]quit
[Huawei]interface GigabitEthernet 0/0/2
[Huawei-GigabitEthernet0/0/2]port link-type access 
[Huawei-GigabitEthernet0/0/2]port default vlan 3
[Huawei]ospf    
[Huawei-ospf-1]area 0
[Huawei-ospf-1-area-0.0.0.0]network 192.168.1.0 0.0.0.255
[Huawei-ospf-1-area-0.0.0.0]network 192.168.3.0 0.0.0.255
[Huawei]interface Vlanif 1
[Huawei-Vlanif1]vrrp vrid 1 virtual-ip 192.168.1.254
```

# 4. 网络负载均衡
## 4.1 问题
按照图-4所示拓扑结构，配置MS1为vlan10的主路由器、vlan20的备份路由器，MS2为vlan10的备份路由器、vlan20的主路由器，实现负载均衡的效果

![在这里插入图片描述](https://img-blog.csdnimg.cn/4e64ddd96fa848c2bcc581acef512f64.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-4

## 4.2 步骤
实现此案例需要按照如下步骤进行

**步骤一：配置交换机**

1）MS1
```shell
[Huawei]interface Vlanif 10
[Huawei-Vlanif10]ip address 192.168.10.252 24
[Huawei-Vlanif10]vrrp vrid 1 virtual-ip 192.168.10.254
[Huawei-Vlanif10]vrrp vrid 1 priority 110
[Huawei]interface Vlanif 20
[Huawei-Vlanif20]ip address 192.168.20.252 24
[Huawei-Vlanif20]vrrp vrid 2 virtual-ip 192.168.20.254
```
1）MS2
```shell
[Huawei]interface Vlanif 10
[Huawei-Vlanif10]ip address 192.168.10.253 24
[Huawei-Vlanif10]vrrp vrid 1 virtual-ip 192.168.10.254
[Huawei]interface Vlanif 20
[Huawei-Vlanif20]ip address 192.168.20.253 24
[Huawei-Vlanif20]vrrp vrid 2 virtual-ip 192.168.20.254
[Huawei-Vlanif20]vrrp vrid 2 priority 110
```

# Exercise
## 1 VRRP的作用是什么？

网关的冗余备份，可以保障网关设备出现故障的情况下不会对网络造成重大影响。

## 2 VRRP中路由器身份有哪些？

主路由器，备份路由器，虚拟路由器

## 3 NAT的作用是什么？

通过将内部网络的私有IP地址翻译成全球唯一的公网IP地址，使内部网络可以连接到互联网等外部网络上。

## 4 私有IP地址分类有哪些？

A类 10.0.0.0~10.255.255.255

B类 172.16.0.0~172.31.255.255

C类 192.168.0.0~192.168.255.255

## 5 NAT常用实现方式有哪些？

静态转换

Easy IP

> 如有侵权，请联系作者删除
