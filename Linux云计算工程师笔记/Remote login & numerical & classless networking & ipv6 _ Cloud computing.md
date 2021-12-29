@[TOC]( Remote login & numerical & classless networking & ipv6 | Cloud computing )

---
# 1. 配置远程登录服务
## 1.1 问题
通过配置实现对路由器的远程管理，要求如下：

1. 创建远程登录用户为test01，密码为123

2. 在交换机上操作，使用ssh协议

## 1.2 方案
从交换机上远程管理路由器，如图-1所示

图-1

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：配置路由器**

ar2220 路由器配置
```shell
<Huawei>system-view 
Enter system view, return user view with Ctrl+Z.
[Huawei]interface GigabitEthernet 0/0/0
[Huawei-GigabitEthernet0/0/0]ip address 192.168.1.254 24
[Huawei-GigabitEthernet0/0/0]quit
[Huawei]aaa
[Huawei-aaa]local-user test01 password cipher 123    
[Huawei-aaa]local-user test01 privilege level 3
[Huawei-aaa]local-user test01 service-type ssh
[Huawei-aaa]quit
[Huawei]user-interface vty 0 4
[Huawei-ui-vty0-4]authentication-mode aaa
[Huawei-ui-vty0-4]protocol inbound ssh
[Huawei-ui-vty0-4]quit
[Huawei]stelnet server enable
```
**步骤二：配置路由器**

S3700交换机配置
```shell
<Huawei>system-view 
Enter system view, return user view with Ctrl+Z.
[Huawei]interface Vlanif 1
[Huawei-Vlanif1]ip address 192.168.1.100 24
[Huawei-Vlanif1]quit
[Huawei]ssh client first-time enable 
[Huawei]stelnet 192.168.1.254
Please input the username:test01
Trying 192.168.1.254 ...
Press CTRL+K to abort
Connected to 192.168.1.254 ...
The server is not authenticated. Continue to access it? [Y/N] :y
Save the server's public key? [Y/N] :y
The server's public key will be saved with the name 192.168.1.254. Please wait..
.
Enter password:
```

# 2. 数制转换
## 2.1 问题
1. 将下列数字转换为十进制数

	11011101、1101、101010

2. 将下列数字转换为二进制

	156、26、104

## 2.2 步骤
实现此案例需要按照如下步骤进行。

1. 将下列数字转换为十进制数
	(11011101)2=221
	(1101)2=13
	(101010)2=42

2. 将下列数字转换为二进制
	156=(10011100)2
	26=(11010)2
	104=(1101000)2

# 3. 子网划分
## 3.1 问题
将192.168.0.0/24划分为4个网段，并应用在下列拓扑中

## 3.2 方案
首先将该地址划分成4个网段，可用范围是
192.168.0.1 ~ 192.168.0.62
192.168.0.65 ~ 192.168.0.126
192.168.0.129 ~ 192.168.0.190
192.168.0.193 ~ 192.168.0.254

然后在交换机与pc应用，如图-2所示

![在这里插入图片描述](https://img-blog.csdnimg.cn/74ec2c0d6f1f48b8a2549258d1bbfdbf.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_16,color_FFFFFF,t_70,g_se,x_16)
图-2

## 3.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：在交换机进行配置**
```shell
<Huawei>system-view 
Enter system view, return user view with Ctrl+Z.
[Huawei]vlan batch 2 3 4
Info: This operation may take a few seconds. Please wait for a moment...done.
[Huawei]in vlan1
[Huawei-Vlanif1]ip add 192.168.0.62 26
[Huawei-Vlanif1]in vlan 2
[Huawei-Vlanif2]ip add 192.168.0.126 26
[Huawei-Vlanif2]in vlan 3
[Huawei-Vlanif3]ip add 192.168.0.190 26
[Huawei-Vlanif3]in vlan 4
[Huawei-Vlanif4]ip add 192.168.0.254 26
[Huawei-Vlanif4]quit
[Huawei]interface GigabitEthernet 0/0/2
[Huawei-GigabitEthernet0/0/2]port link-type access 
[Huawei-GigabitEthernet0/0/2]port default vlan 2
[Huawei-GigabitEthernet0/0/2]in g0/0/3
[Huawei-GigabitEthernet0/0/3]port link-type access
[Huawei-GigabitEthernet0/0/3]port default vlan 3
[Huawei-GigabitEthernet0/0/3]in g0/0/4
[Huawei-GigabitEthernet0/0/4]port link-type access
[Huawei-GigabitEthernet0/0/4]port default vlan 4
```
**步骤二：在各vlan所在主机配置的ip如下**

vlan1主机如图-3所示

![在这里插入图片描述](https://img-blog.csdnimg.cn/a1ed8e0767e945e9a97974cd457b9c1e.png)
图-3

vlan2主机如图-4所示

![在这里插入图片描述](https://img-blog.csdnimg.cn/b7f7966c91f84a2faf1d692f6c846cff.png)
图-4

vlan3主机如图-5所示

![在这里插入图片描述](https://img-blog.csdnimg.cn/955b0e770151436bab70c8fd414cc79e.png)
图-5

vlan4主机如图-6所示

![在这里插入图片描述](https://img-blog.csdnimg.cn/e6a6d00faff14c9489e65f6e928ab156.png)
图-6

# 4. 使用IPv6地址连接网络
## 4.1 问题
通过配置IPv6地址使下列拓扑中的设备互通，如图-7所示

![在这里插入图片描述](https://img-blog.csdnimg.cn/f4d0a1c240a44fdd920fcd5990cfcd69.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)

图-7

## 4.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：在路由器配置**

此步骤需要在上一实验基础上进行
```shell
<Huawei>system-view 
Enter system view, return user view with Ctrl+Z.
[Huawei]ipv6    
[Huawei]interface GigabitEthernet 0/0/0    
[Huawei-GigabitEthernet0/0/0]ipv6 enable     
[Huawei-GigabitEthernet0/0/0]ipv6 address 2001:2::254 64
[Huawei-GigabitEthernet0/0/0]in g0/0/1
[Huawei-GigabitEthernet0/0/1]ipv6 enable 
[Huawei-GigabitEthernet0/0/1]ipv6 address 2001:1::254 64
```
**步骤二：各主机配置的ip如下**

PC1主机如图-8所示
![在这里插入图片描述](https://img-blog.csdnimg.cn/833a095393cd41c3b0917a40442ff559.png)
图-8

PC2主机如图-9所示
![在这里插入图片描述](https://img-blog.csdnimg.cn/97e469f18c3840d3824fe694de19d01a.png)
图-9

PC3主机如图-10所示
![在这里插入图片描述](https://img-blog.csdnimg.cn/a589cb1cea4e40d098636e6e36e2c989.png)
图-10


# Exercise
## 1 远程登录协议有哪些？区别是什么?

telnet与ssh两种协议可以实现远程登录功能

区别是telnet使用明文方式传递数据，可以在内部网络等安全要求不高的场合使用，而ssh使用加密方式传递数据，可以放心用在各种环境的网络中

## 2 计算机中常用数制有哪些？

二进制、十进制、十六进制

## 3 一个4GB大小的文件，如果利用200Mb带宽的网络传递，需要多久完成？

首先使用200除以8得出该网络每秒可以传递25MB的数据

4乘以1024等于4096MB，再用4096除以25得出时间是163.84秒

大约不到3分钟即可完成传递

## 4 子网划分的原因是？

满足不同网络对IP地址的需求

节省IP地址

## 5 IPv4的与IPv6的地址长度分别是多少位？

IPv4是32位

IPv6是128位

## 6 IPv6地址在配置时通常使用几进制？
十六进制

> 如有侵权，请联系作者删除
