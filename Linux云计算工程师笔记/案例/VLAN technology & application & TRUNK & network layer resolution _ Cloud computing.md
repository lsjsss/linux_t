@[TOC]( VLAN technology & application & TRUNK & network layer resolution | Cloud computing )

---
# 1. 划分VLAN
## 1.1 问题
在交换机上创建以下VLAN，按照拓扑图-1将端口加入到指定的VLAN并配置服务器IP地址，实现同VLAN主机的通信

![在这里插入图片描述](https://img-blog.csdnimg.cn/5a733d197b9b4bffba6bfafa7658dd63.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_16,color_FFFFFF,t_70,g_se,x_16)
图-1

## 1.2 步骤
实现此案例需要按照如下步骤进行

**步骤一：创建vlan，并将接口加入**

由于默认情况下所有接口都在VLAN1中，且VLAN1默认就存在，所以只需要配置VLAN2和VLAN3即可

```shell
<Huawei>system-view 
[Huawei]vlan batch 2 3            //创建VLAN2、3
[Huawei]port-group 1
[Huawei-port-group-1]group-member Ethernet0/0/3 Ethernet0/0/4
[Huawei-port-group-1]port link-type access 
[Huawei-port-group-1]port default vlan 2                        
[Huawei-port-group-1]quit
[Huawei]port-group 2
[Huawei-port-group-2]group-member Ethernet0/0/5 Ethernet0/0/6
[Huawei-port-group-2]port link-type access 
[Huawei-port-group-2]port default vlan 3    
```

# 2. 多交换机VLAN的划分
## 2.1 问题
通过配置交换机实现图-2中的VLAN划分

![在这里插入图片描述](https://img-blog.csdnimg.cn/831376cda2b24401af184d0e6d8af14b.png)
图-2

## 2.2 步骤
注：以下配置需要在案例1的基础上完成

**步骤一：创建vlan，并将接口加入**

1）S1配置
```shell
[Huawei]interface Ethernet0/0/7
[Huawei-Ethernet0/0/7] port link-type access
[Huawei-Ethernet0/0/7] port default vlan 3
```
2）S2配置
```shell
<Huawei>system-view 
[Huawei]vlan 3            //创建VLAN3
[Huawei]port-group 1
[Huawei-port-group-1]group-member Ethernet0/0/5 to Ethernet0/0/7
[Huawei-port-group-1]port link-type access 
[Huawei-port-group-1]port default vlan 3    
```
# 3. 配置trunk中继链路
## 3.1 问题
通过配置实现跨交换机的同VLAN通信，如图-3所示

![在这里插入图片描述](https://img-blog.csdnimg.cn/1861447b2ce240e298d34e05c68c9923.png)
图-3

## 3.2 步骤
注：以下配置需要在案例2的基础上完成

**步骤一：配置trunk，放行所有vlan**

1）S1配置
```shell
如果接口被改动过，则需要恢复默认配置
[Huawei] clear configuration interface Ethernet0/0/7
[Huawei]interface Ethernet0/0/7
[Huawei-Ethernet0/0/7]port default vlan 1
[Huawei-Ethernet0/0/7]port link-type trunk
[Huawei-Ethernet0/0/1]port trunk allow-pass vlan all
```
2）S2配置
```shell
<Huawei>system-view 
[Huawei]vlan 2         //创建VLAN2
[Huawei]port-group 1
[Huawei-port-group-1]group-member Ethernet0/0/3 Ethernet0/0/4
[Huawei-port-group-1]port link-type access 
[Huawei-port-group-1]port default vlan 2                        
[Huawei]interface Ethernet0/0/7
[Huawei-Ethernet0/0/7]port default vlan 1
[Huawei-Ethernet0/0/7]port link-type trunk
[Huawei-Ethernet0/0/1]port trunk allow-pass vlan all
```
# 4. 链路聚合配置
## 4.1 问题
参照图-4将两台交换机的f0/1-f0/2接口互联，并实现高可用

![在这里插入图片描述](https://img-blog.csdnimg.cn/8b41e741582a4592a308b7f2f0d385e7.png)
图-4

## 4.2 步骤
**步骤一：创建链路聚合接口，并捆绑物理接口**

1）S1配置
```shell
[Huawei]interface Eth-trunk 1
[Huawei- Eth-trunk1]trunkport ethernet 0/0/1  0/0/2
如果接口被改动过，则需要恢复默认配置
[Huawei] clear configuration interface Ethernet0/0/1
```
2）S2配置
```shell
[Huawei]interface Eth-trunk 1
[Huawei- Eth-trunk1]trunkport ethernet 0/0/1  0/0/2
```

# 5. 配置静态路由
## 5.1 问题
按照图-5拓扑结构配置接口ip地址并通过静态路由实现全网互通

![在这里插入图片描述](https://img-blog.csdnimg.cn/7e6997fe3bce49a9ac9bdd4380ffba33.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-5

## 5.2 步骤
**步骤一：配置ip地址，添加静态路由**

1）R1配置
```shell
<Huawei>system-view 
[Huawei]interface GigabitEthernet 0/0/0
[Huawei-GigabitEthernet0/0/1]ip address 192.168.1.254 24
[Huawei-GigabitEthernet0/0/1]quit
[Huawei]interface GigabitEthernet 0/0/1
[Huawei-GigabitEthernet0/0/1]ip address 192.168.2.1 24
[Huawei]ip route-static 192.168.3.0 24 192.168.2.2
[Huawei]ip route-static 192.168.4.0 24 192.168.2.2
```
2）R2配置
```shell
<Huawei>system-view 
[Huawei]interface GigabitEthernet 0/0/0
[Huawei-GigabitEthernet0/0/1]ip address 192.168.3.254 24
[Huawei-GigabitEthernet0/0/1]quit
[Huawei]interface GigabitEthernet 0/0/1
[Huawei-GigabitEthernet0/0/1]ip address 192.168.2.2 24
[Huawei-GigabitEthernet0/0/1]quit
[Huawei]interface GigabitEthernet 0/0/2
[Huawei-GigabitEthernet0/0/1]ip address 192.168.4.254 24
[Huawei]ip route-static 192.168.1.0 24 192.168.2.1
```

# 6. 三层交换机基本配置
## 6.1 问题
按照图-6的拓扑结构配置ip地址并通过三层交换实现VLAN间通信

![在这里插入图片描述](https://img-blog.csdnimg.cn/d06ae60bb321411d89efc1776bee14cc.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_16,color_FFFFFF,t_70,g_se,x_16)
图-6

## 6.2 步骤
**步骤一：创建vlan，并配置虚拟接口的ip**

三层交换机配置
```shell
[Huawei]vlan batch 2 3
[Huawei]interface Vlanif 1
[Huawei-Vlanif1]ip address 192.168.1.254 24
[Huawei]interface Vlanif 2
[Huawei-Vlanif1]ip address 192.168.2.254 24
[Huawei]interface Vlanif 3
[Huawei-Vlanif1]ip address 192.168.3.254 24
[Huawei]interface G0/0/2
[Huawei-GigabitEthernet0/0/2] port link-type access
[Huawei-GigabitEthernet0/0/2] port default vlan 2
[Huawei]interface G0/0/3
[Huawei-GigabitEthernet0/0/2] port link-type access
[Huawei-GigabitEthernet0/0/2] port default vlan 3
```

# Exercise
## 1 VLAN的作用是什么？

广播控制，增加安全性，提高带宽利用，降低延迟

## 2 TRUNK的作用是什么？

为数据帧打上VLAN标识，使不同VLAN数据可以用一条链路传递

## 3 链路聚合的作用是什么？

链路聚合为交换机提供了接口捆绑的技术，允许两个交换机之间通过两个或多个接口并行连接，同时传输数据，以提供更高的带宽和可靠性

## 4 网络层的功能有哪些？

定义了基于IP协议的逻辑地址
连接不同的媒介类型
选择数据通过网络的最佳路径

## 5 ping工具与哪个协议有关？
ICMP

## 6 获取路由表的方式有哪些？
直连路由、静态路由、动态路由


> 如有侵权，请联系作者删除

