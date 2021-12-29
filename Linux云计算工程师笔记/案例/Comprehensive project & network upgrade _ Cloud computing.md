@[TOC]( Comprehensive project & network upgrade | Cloud computing )

---
# 1 案例：综合网络搭建
## 1.1 问题
现有网络问题分析：
- 接入层交换机只与同一个三层交换机相连，存在单点故障而影响网络通信。
- 互联网连接单一服务商

现有网络需求：
- 随着企业发展，为了保证网络的高可用性，需要使用很多的冗余技术
- 保证局域网络不会因为线路故障而导致的网络故障
- 保证客户端机器不会因为使用单一网关而出现的单点失败
- 保证到互联网的高可用接入使用冗余互联网连接
## 1.2 方案
基于项目的需求，需要用到如下技术：

- OSPF路由协议：实现网络路径的自动学习
- VRRP：实现网关冗余

重新规划后的网络拓扑如图-1：

![在这里插入图片描述](https://img-blog.csdnimg.cn/c24b30db9ac04b1db7791e8cefa89a16.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-1

## 1.3 步骤
实现此案例需要按照如下步骤进行，为了配置过程中不被弹出信息干扰，可以关闭信息提示

**步骤一：S3700交换机配置**
```shell
SW1配置
<Huawei>system-view
[Huawei]vlan batch 10 20 30 40
[Huawei]port-group 1
[Huawei-port-group-1]group-member Ethernet 0/0/1 to Ethernet 0/0/2
[Huawei-port-group-1]port link-type  trunk
[Huawei-port-group-1]port trunk allow-pass vlan all
[Huawei-port-group-1]quit
[Huawei]interface Ethernet 0/0/5
[Huawei-Ethernet0/0/5] port link-type access
[Huawei-Ethernet0/0/5] port default vlan 10
SW2配置
<Huawei>system-view
[Huawei]vlan batch 10 20 30 40
[Huawei]port-group 1
[Huawei-port-group-1]group-member Ethernet 0/0/1 to Ethernet 0/0/2
[Huawei-port-group-1]port link-type  trunk
[Huawei-port-group-1]port trunk allow-pass vlan all
[Huawei-port-group-1]quit
[Huawei]interface Ethernet 0/0/5
[Huawei-Ethernet0/0/5] port link-type access
[Huawei-Ethernet0/0/5] port default vlan 20
SW3配置
<Huawei>system-view
[Huawei]vlan batch 10 20 30 40
[Huawei]port-group 1
[Huawei-port-group-1]group-member Ethernet 0/0/1 to Ethernet 0/0/2
[Huawei-port-group-1]port link-type  trunk
[Huawei-port-group-1]port trunk allow-pass vlan all
[Huawei-port-group-1]quit
[Huawei]interface Ethernet 0/0/5
[Huawei-Ethernet0/0/5] port link-type access
[Huawei-Ethernet0/0/5] port default vlan 30
SW4配置
<Huawei>system-view
[Huawei]vlan batch 10 20 30 40
[Huawei]port-group 1
[Huawei-port-group-1]group-member Ethernet 0/0/1 to Ethernet 0/0/2
[Huawei-port-group-1]port link-type  trunk
[Huawei-port-group-1]port trunk allow-pass vlan all
[Huawei-port-group-1]quit
[Huawei]interface Ethernet 0/0/5
[Huawei-Ethernet0/0/5] port link-type access
[Huawei-Ethernet0/0/5] port default vlan 40
```
**步骤二：S5700交换机配置**
```shell
MS1配置
<Huawei>system-view
[Huawei]vlan batch 10 20 30 40 50 60
[Huawei]port-group 1
[Huawei-port-group-1]group-member GigabitEthernet 0/0/1 to GigabitEthernet 0/0/5
[Huawei-port-group-1]port link-type  trunk
[Huawei-port-group-1]port trunk allow-pass vlan all
[Huawei-port-group-1]quit
[Huawei]interface Vlanif 10
[Huawei-Vlanif10]ip address 192.168.10.252 24
[Huawei-Vlanif10]vrrp vrid 1 virtual-ip 192.168.10.254
[Huawei-Vlanif10]vrrp vrid 1 priority 110
[Huawei]interface Vlanif 20
[Huawei-Vlanif20]ip address 192.168.20.252 24
[Huawei-Vlanif20]vrrp vrid 2 virtual-ip 192.168.20.254
[Huawei-Vlanif20]vrrp vrid 2 priority 110
[Huawei]interface Vlanif 30
[Huawei-Vlanif30]ip address 192.168.30.252 24
[Huawei-Vlanif30]vrrp vrid 3 virtual-ip 192.168.30.254
[Huawei]interface Vlanif 40
[Huawei-Vlanif40]ip address 192.168.40.252 24
[Huawei-Vlanif40]vrrp vrid 4 virtual-ip 192.168.40.254
[Huawei]interface Vlanif 50
[Huawei-Vlanif50]ip address 192.168.50.2 24
[Huawei]interface GigabitEthernet 0/0/23
[Huawei-GigabitEthernet0/0/23]port link-type access
[Huawei-GigabitEthernet0/0/23]port default vlan 50
[Huawei]interface Vlanif 60
[Huawei-Vlanif60]ip address 192.168.60.2 24
[Huawei]interface GigabitEthernet 0/0/24
[Huawei-GigabitEthernet0/0/24]port link-type access
[Huawei-GigabitEthernet0/0/24]port default vlan 60
[Huawei]ospf    
[Huawei-ospf-1]area 0
[Huawei-ospf-1-area-0.0.0.0]network 192.168.10.0 0.0.0.255
[Huawei-ospf-1-area-0.0.0.0]network 192.168.20.0 0.0.0.255
[Huawei-ospf-1-area-0.0.0.0]network 192.168.30.0 0.0.0.255
[Huawei-ospf-1-area-0.0.0.0]network 192.168.40.0 0.0.0.255
[Huawei-ospf-1-area-0.0.0.0]network 192.168.50.0 0.0.0.255
[Huawei-ospf-1-area-0.0.0.0]network 192.168.60.0 0.0.0.255
MS2配置
<Huawei>system-view
[Huawei]vlan batch 10 20 30 40 70 80
[Huawei]port-group 1
[Huawei-port-group-1]group-member GigabitEthernet 0/0/1 to GigabitEthernet 0/0/5
[Huawei-port-group-1]port link-type  trunk
[Huawei-port-group-1]port trunk allow-pass vlan all
[Huawei-port-group-1]quit
[Huawei]interface Vlanif 10
[Huawei-Vlanif10]ip address 192.168.10.253 24
[Huawei-Vlanif10]vrrp vrid 1 virtual-ip 192.168.10.254
[Huawei]interface Vlanif 20
[Huawei-Vlanif20]ip address 192.168.20.253 24
[Huawei-Vlanif20]vrrp vrid 2 virtual-ip 192.168.20.254
[Huawei]interface Vlanif 30
[Huawei-Vlanif30]ip address 192.168.30.253 24
[Huawei-Vlanif30]vrrp vrid 3 virtual-ip 192.168.30.254
[Huawei-Vlanif20]vrrp vrid 3 priority 110
[Huawei]interface Vlanif 40
[Huawei-Vlanif40]ip address 192.168.40.253 24
[Huawei-Vlanif40]vrrp vrid 4 virtual-ip 192.168.40.254
[Huawei-Vlanif20]vrrp vrid 4 priority 110
[Huawei]interface Vlanif 70
[Huawei-Vlanif70]ip address 192.168.70.2 24
[Huawei]interface GigabitEthernet 0/0/23
[Huawei-GigabitEthernet0/0/23]port link-type access
[Huawei-GigabitEthernet0/0/23]port default vlan 70
[Huawei]interface Vlanif 80
[Huawei-Vlanif80]ip address 192.168.80.2 24
[Huawei]interface GigabitEthernet 0/0/24
[Huawei-GigabitEthernet0/0/24]port link-type access
[Huawei-GigabitEthernet0/0/24]port default vlan 80
[Huawei]ospf    
[Huawei-ospf-1]area 0
[Huawei-ospf-1-area-0.0.0.0]network 192.168.10.0 0.0.0.255
[Huawei-ospf-1-area-0.0.0.0]network 192.168.20.0 0.0.0.255
[Huawei-ospf-1-area-0.0.0.0]network 192.168.30.0 0.0.0.255
[Huawei-ospf-1-area-0.0.0.0]network 192.168.40.0 0.0.0.255
[Huawei-ospf-1-area-0.0.0.0]network 192.168.70.0 0.0.0.255
[Huawei-ospf-1-area-0.0.0.0]network 192.168.80.0 0.0.0.255
```
然后测试目前网络是否可以达成全网互通

**步骤三：路由器配置**

按图-2为路由器与三层交换机相连的接口配置ip

注:50.1表示ip需要配置为192.168.50.1

![在这里插入图片描述](https://img-blog.csdnimg.cn/72f24969742c4ab6a4141e79c23d3e05.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_13,color_FFFFFF,t_70,g_se,x_16)
图-2

```shell
R1
<Huawei>system-view 
[Huawei]acl 2000    
[Huawei-acl-basic-2000]rule permit source any 
[Huawei]interface GigabitEthernet 0/0/0
[Huawei-GigabitEthernet0/0/0]ip address 192.168.50.1 24
[Huawei]interface GigabitEthernet 0/0/1
[Huawei-GigabitEthernet0/0/1]ip address 192.168.70.1 24
[Huawei]interface GigabitEthernet 0/0/2
[Huawei-GigabitEthernet0/0/2]ip address 100.0.0.1 8
[Huawei-GigabitEthernet0/0/2]nat outbound 2000
[Huawei-GigabitEthernet0/0/2]quit
[Huawei]ip route-static 0.0.0.0 0 100.0.0.10
[Huawei]ospf
[Huawei-ospf-1]default-route-advertise      //对外通告默认路由
[Huawei-ospf-1]area 0
[Huawei-ospf-1-area-0.0.0.0]network 192.168.50.0 0.0.0.255
[Huawei-ospf-1-area-0.0.0.0]network 192.168.70.0 0.0.0.255
R2
<Huawei>system-view 
[Huawei]acl 2000    
[Huawei-acl-basic-2000]rule permit source any 
[Huawei]interface GigabitEthernet 0/0/0
[Huawei-GigabitEthernet0/0/0]ip address 192.168.60.1 24
[Huawei]interface GigabitEthernet 0/0/1
[Huawei-GigabitEthernet0/0/1]ip address 192.168.80.1 24
[Huawei]interface GigabitEthernet 0/0/2
[Huawei-GigabitEthernet0/0/2]ip address 100.0.0.2 8
[Huawei-GigabitEthernet0/0/0]nat outbound 2000
[Huawei-GigabitEthernet0/0/2]quit
[Huawei]ip route-static 0.0.0.0 0 100.0.0.10
[Huawei]ospf
[Huawei-ospf-1]default-route-advertise 
[Huawei-ospf-1]area 0
[Huawei-ospf-1-area-0.0.0.0]network 192.168.60.0 0.0.0.255
[Huawei-ospf-1-area-0.0.0.0]network 192.168.80.0 0.0.0.255
```

三层交换机如果看不到从路由器学习来的默认路由就去检查路由器G0/2地址是否配置，之后验证从内网可以访问外网设备，ping通证明项目升级成功


# Exercise
> 如有侵权，请联系作者删除
