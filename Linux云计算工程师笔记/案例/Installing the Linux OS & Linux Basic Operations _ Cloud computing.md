

@[TOC]( Installing the Linux OS & Linux Basic Operations | Cloud computing )

---
# 1. 装机预备技能
## 1.1 问题
1. RHEL与CentOS系统有什么关联？
2. Linux系统中第三块SCSI硬盘如何表示？
## 1.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：RHEL系统与CentOS系统的渊源**

RHEL是红帽公司提供的商业版Linux系统，若要获取DVD镜像、安全更新等技术服务支持，一般需要付费订阅；不过构成RHEL系统的各种软件包都是基于GPL开源协议免费发布的。

CentOS是一个社区性质的Linux系统，相当于RHEL的一个克隆版本，它采用了构成RHEL系统的各种软件包重新组装、开发而成，并且在此过程中做了一些优化、必要的Bug修复；CentOS系统的版本会稍晚于同版本的RHEL系统发布，其构成、管理方式与同版本的RHEL系统几乎一模一样，而且能够找到大量开放的软件源，因此受到很多企业的欢迎。

目前，CentOS已经被Red Hat公司所收购，仍然可自由使用。

**步骤二：Linux系统中第三块SCSI硬盘如何表示？**

在Linux系统中，第三块SCSI硬盘如何表示利用/dev/sdc表示

# 2 案例2：安装一台LINUX虚拟机
## 2.1 问题
基于KVM虚拟机环境新安装一各LINUX操作系统，主要完成以下事项：

1. 新建一台虚拟机，硬盘30GB，内存1GB
2. 为此虚拟机安装LINUX操作系统，采取自动分区方案
3. 软件包定制

## 2.2 方案
在虚拟机环境练习装机过程——通过菜单组`应用程序`-->`系统工具`-->`虚拟系统管理器`，打开KVM虚拟化的图形管理程序（如图-1所示），添加一台虚拟机，将LINUX系统的ISO镜像文件作为此虚拟机的安装光盘。

![在这里插入图片描述](https://img-blog.csdnimg.cn/2408ee32ce0c4deab65a4fcb5e71b7b3.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_17,color_FFFFFF,t_70,g_se,x_16)
图-1

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：新建一台LINUX虚拟机**

> 1）启动“新建虚拟机”向导程序

单击虚拟系统管理器左上方的“新建”按钮，即可打开 `新建虚拟机` 向导窗口；为新建虚拟机指定名称，安装方式选择从本地ISO镜像安装（如图-2所示），单击 `前进`。

![在这里插入图片描述](https://img-blog.csdnimg.cn/0e83d38a3a174a9886820bf0d44c8c0d.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_14,color_FFFFFF,t_70,g_se,x_16,align:center)
图-2

> 2）指定ISO文件位置、系统版本

通过“浏览”找到正确的LINUX安装镜像文件的路径，操作系统类型选择 `Linux` ，版本选择 `CentOS 7.0`（如图-3所示），单击 `前进`。

![在这里插入图片描述](https://img-blog.csdnimg.cn/8df37343e1a94deab3666ada249bc93b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_16,color_FFFFFF,t_70,g_se,x_16)
图－3

> 3）指定虚拟机内存与CPU核心数

内存建议设为2048MB，CPU默认1个即可（如图-4所示），单击 `前进`。

![在这里插入图片描述](https://img-blog.csdnimg.cn/136f41fe3e1044c9bc46c560c889fb3b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_17,color_FFFFFF,t_70,g_se,x_16)
图－4

> 4）指定虚拟机的磁盘大小

此处建议选择30GB，（如图-5所示），单击 `前进`。

![在这里插入图片描述](https://img-blog.csdnimg.cn/73e55ed366ee4a49bb34d88fffe83e1c.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_14,color_FFFFFF,t_70,g_se,x_16)
图－5

> 5）确认并完成创建

查看虚拟机最终配置信息，建议展开 `高级选项`，将虚拟网络选择为 `private1`（如图-6所示），单击“完成”后将会自动运行新建的虚拟机。

![在这里插入图片描述](https://img-blog.csdnimg.cn/dd0a5ed5b07d48688dd10e5c6fc05cfb.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_15,color_FFFFFF,t_70,g_se,x_16)
图－6

**步骤二：启动虚拟机电源，安装Linux系统**

> 1）运行Linux安装程序

打开新虚拟机的电源后，会自动从光盘引导主机（因为新磁盘没有引导信息，自动找其他启动设备），进入CentOS系统的安装选择界面。按上箭头键选择第一项 `Install CentOS 7`（如图-7所示），然后按Enter键启动安装程序。

![在这里插入图片描述](https://img-blog.csdnimg.cn/adefaafb05574351934b057c1d36eece.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图－7

> 2）选择语言类型

建议初学者选择 `简体中文（中国）`以降低难度（如图-8所示），单击“继续”。

![在这里插入图片描述](https://img-blog.csdnimg.cn/3e0511dcb6734704ac071134f4add0ae.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图－8

> 3）自定义磁盘分区方案

在 `安装信息摘要` 的列表界面中，单击 `系统` --> `安装位置`（如图-9所示）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/4e820eb10b7d4ce5b49cf554b221c577.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图－9

打开 `安装目标位置` 界面以后，选择 `安装位置` 下的 `自动配置分区`  （如图-10所示），单击上方的 `完成` 按钮。

![在这里插入图片描述](https://img-blog.csdnimg.cn/e27b7303ecf14bdc8824662b9509bb88.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图-10

> 4）选择要安装的软件包

单击 `安装信息摘要` 界面中的 `软件选择` 接下来在 `基本环境` 下选取 `带GUI的服务器` （如图-11所示），单击 `完成` 按钮返回。

![在这里插入图片描述](https://img-blog.csdnimg.cn/d4352fe6e1d7413fbecf096b63990f41.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图－11

> 5）确认并开始安装

检查 `安装信息摘要界面` ，确保所有带叹号的部分都已经完成，然后单击右下方的 `开始安装` 按钮（如图-12所示），将会执行正式安装。

![在这里插入图片描述](https://img-blog.csdnimg.cn/e0da078e86d442d39ae50595738a25c8.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图－12

在安装执行期间，根据页面提示（如图-13所示）单击 `ROOT密码` 后为root用户设置一个密码（注意：若密码太简单需要按两次 `完成` 按钮！！），无需创建其他用户。

![在这里插入图片描述](https://img-blog.csdnimg.cn/6a18d2936bef49d69b96a8504e5ca73e.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图-13

设置好密码以后，只要等待安装结束就行了（如图-14所示）。根据系统性能及选取的软件包不同，安装过程一般需要5~30分钟。

![在这里插入图片描述](https://img-blog.csdnimg.cn/0a3d9c12075a4313bfc791a49aec02d6.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)图-14

**6）结束安装过程**

全部安装执行完毕后，会提示重启主机（如图-15所示），根据提示操作即可。

![在这里插入图片描述](https://img-blog.csdnimg.cn/2d0ce3959d94428aae9238937771b6d7.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图－15

**步骤三：初始化配置**

完成LINUX系统的安装过程后，第一次启动时会要求进行初始化设置。

> 1）确认许可协议,如图-16与图-17所示，点击`完成`
![在这里插入图片描述](https://img-blog.csdnimg.cn/f30d741b6f72438d9b567d07b62f3c0c.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图-16

![在这里插入图片描述](https://img-blog.csdnimg.cn/248be8dfe587485688cbf8d60ebb4697.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图-17

> 2）选择 `完成配置` （如图-18所示）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/abd9c18f529245579a4cee68ac0cedb9.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图-18

3）选择语言，如图-19所示，点击 `前进` 

![在这里插入图片描述](https://img-blog.csdnimg.cn/a3bf086feb384fbf8968fe955c0b8e9b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图-19

> 4）选择`语言输入`，建议选择`汉语pinyin`（如图-20所示）

![在这里插入图片描述](https://img-blog.csdnimg.cn/8b0d28adb1d3459d95328a7661f5608c.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)

图-20

> 5）隐私如图-21所示，点击 `前进` 

/

图-21

> 6）时区如图-22所示，选择 `上海` 

/

图-22

> 7）在线账号如图-23所示，选择 `跳过` 

/

图-23

> 8）接下来只要单击 `开始使用` 即可

![在这里插入图片描述](https://img-blog.csdnimg.cn/fe95dfd1c37a4296b4f3e31c1a02cacc.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图-24

自动登入（以后登录时需要提供密码）到桌面环境（如图-25所示）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/64a0a8f5556f4f14b5ea50da1dd28732.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)

图-25

至此，整个LINUX虚拟机系统的安装就完成了。

**3 案例3：使用LINUX图形桌面**

## 3.1 问题
本例要求熟悉新装LINUX系统的图形桌面环境，完成下列任务：

>更改桌面背景图片
打开应用程序 “Firefox Web Browser”
添加一个普通用户账号（4参考自己姓名的拼音）
注销，换新用户登录
重启此系统

## 3.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：以root用户登入到图形桌面**

将新装的LINUX系统关机、重新开机，启动完毕会看到登录界面（如图-26所示）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/2358a9fd9ede4108939a5a4da7f95eae.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_18,color_FFFFFF,t_70,g_se,x_16)
图-26

单击展示的用户列表下方的`未列出？`，然后根据提示输入管理员用户名root（如图-27所示），单击`下一步`。

![在这里插入图片描述](https://img-blog.csdnimg.cn/e878dcb37f7e4c75b37e94bdb944495b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_18,color_FFFFFF,t_70,g_se,x_16)
图-27

接下来再根据提示输入root用户的正确口令（如图-28所示），单击“登录”按钮即成功进入图形桌面环境。

![在这里插入图片描述](https://img-blog.csdnimg.cn/eab0ae949a80452dabd260dddce75b0c.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_18,color_FFFFFF,t_70,g_se,x_16)
图-28

**步骤二：完成简单的桌面操作**

> 1）更改桌面背景图片

在桌面空白处右击，选择 `更改桌面背景` ，在弹出的对话框中单击 `背景` 并选取自己所喜爱的图片即可（如图-29所示）；如果需要更改锁屏图片，可以单击旁边的 `锁屏` 去选择。

![在这里插入图片描述](https://img-blog.csdnimg.cn/ec045c61bfcd40f4ab53f68b93c771c2.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_18,color_FFFFFF,t_70,g_se,x_16)

图-29

> 2）打开Firefox网页浏览器

单击桌面菜单组`应用程序`-->`互联网`-->`Firefox Web Browser`（如图-30所示），可以打开火狐网页浏览器程序。

![在这里插入图片描述](https://img-blog.csdnimg.cn/07857dfe2c044ac582497c52d8775673.png)
图-30

> 3）添加一个普通用户账号（参考自己姓名的拼音）

单击桌面菜单组 `应用程序` --> `系统工具` --> `设置`（如图-31所示），可以打开系统设置平台。

![在这里插入图片描述](https://img-blog.csdnimg.cn/2e8754e9443944788fa318c33c0b6959.png)
图-31

点击 `详细信息`（如图-32所示）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/8ce1a749fd964dfe986b1c5d06ff7bb4.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_18,color_FFFFFF,t_70,g_se,x_16)
图-32

然后点击 `用户` 管理窗口后，可以通过右上方的按钮来添加用户账号。根据自己的姓名拟定一个用户名，添加此账号即可（如图-33所示）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/cbfabfd990234383b7f0611d82090100.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_18,color_FFFFFF,t_70,g_se,x_16)
图-33

> 4）注销，换新用户登录

单击桌面右上角的电源按钮，在弹出窗口中展开用户右侧的下拉列表，根据需要选择 `切换用户` 或者 `注销`（如图-34所示）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/167ac2f39e094593b98356d44f78bb94.png)
图-34

> 5）重启此系统

单击桌面右上角的电源按钮，在弹出窗口中再单击右下的电源标识（如图-35所示）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/b0143f10094b43439e88ae8670944b35.png)
图-35

接下来会提示操作类型，根据需要选择 `取消`、`重启`、`关机` 即可（如图-36所示）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/bf12fdd9442a41fea7d02cfe3776ab2f.png)
图-36

# 4. Linux命令行基本操作
## 4.1 问题
本例要求熟悉新装LINUX系统中命令行界面的获取方法，并通过命令行完成下列任务：

>查看内核版本、主机名、IP/MAC地址
查看CPU型号/频率、内存大小
切换到根目录，确认当前位置、列出有哪些子目录
返回到 /root 目录，确认当前位置
重启当前系统

## 4.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：获取命令行界面的不同方法**

> 1）虚拟控制台切换

LINUX系统默认提供6个虚拟控制台（tty1 ~ tty6），每个控制台可以独立登录、执行不同的任务。其中tty1默认开启图形桌面，tty2 ~ tty6只开启字符模式。

通过组合快捷键Ctrl+Alt+Fn可以在不同的虚拟控制台之间切换，这里的Fn代表F1~F6键中的某一个。例如，当处在正常的图形桌面时，按Ctrl+Alt+F3组合键可以切换到控制台tty3，登录后即进入纯字符模式的命令行界面；如果需要返回之前的图形桌面，则再按键Ctrl+Alt+F1组合键即可。

> 2）桌面右键菜单

在桌面空白处右击，或者通过资源管理器浏览文件夹时在空白处右击，可以看到右键菜单中出现“在终端中打开”项（如图-37所示）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/aa5329bdf6e043d5a0636d21a61853a9.png)
图-37

单击“在终端中打开”项即可获得以图形窗口展现的命令行终端程序（如图-38所示）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/64178a18aedd40b6a27d457973198bd0.png)
图-38

> 3）`应用程序` 相应菜单

通过桌面菜单组`应用程序`-->`工具`-->`终端`，也可以打开以图形窗口展现的命令行终端程序。

**步骤二：简单命令行操作练习**

> 1）查看内核版本、主机名、IP/MAC地址

检查红帽发行信息：
```shell
[root@svr7 桌面]# cat /etc/redhat-release 
Red Hat Enterprise Linux Server release 7.5 (Maipo)
```
列出内核版本：
```shell
[root@svr7 桌面]# uname -r
3.10.0-327.el7.x86_64
```

> 2）查看CPU型号/频率、内存大小

列出CPU处理器信息：
```shell
[root@svr7 桌面]# lscpu
Architecture:          x86_64 
CPU op-mode(s):        32-bit, 64-bit
Byte Order:            Little Endian
CPU(s):                1
On-line CPU(s) list:   0
Thread(s) per core:    1
Core(s) per socket:    1
座：                 1
NUMA 节点：         1
厂商 ID：           GenuineIntel 
CPU 系列：          6
型号：              13
型号名称：        QEMU Virtual CPU version (cpu64-rhel6)
步进：              3
CPU MHz：             2693.762
BogoMIPS：            5387.52
超管理器厂商：  KVM
虚拟化类型：     完全
L1d 缓存：          32K
L1i 缓存：          32K
L2 缓存：           4096K
NUMA 节点0 CPU：    0
```
检查内存大小、空闲情况
```shell
[root@svr7 桌面]# cat /proc/meminfo 
MemTotal:        1016904 kB
MemFree:          245364 kB
MemAvailable:     566664 kB
Buffers:            2116 kB
Cached:           417372 kB
SwapCached:            0 kB
Active:           267272 kB
Inactive:         381760 kB
.. ..
```

> 3）切换到根目录，确认当前位置、列出有哪些子目录

切换目录、确认当前位置：
```shell
[root@svr7 桌面]# cd  /
[root@svr7 /]# pwd
/
```

> 4）返回到 /root 目录，确认当前位置

```shell
[root@svr7 /]# cd  /root
[root@svr7 ~]# pwd
/root
```

> 5）重启当前系统

```shell
[root@svr7 ~]# reboot
.. ..
```


# Exercise
## 1 请列举你所知道的Linux发行版
常见的Linux发行版：
- Red Hat Enterprise Linux 5/6/7
- CentOS 5/6/7
- Suse Linux Enterprise 11
- Debian Linux 6.0
- Ubuntu Linux 13.04/13.10
- Oracle Linux 6
## 2 Linux系统的根目录、/dev目录的作用是什么
- /：linux文件系统的起点，linux所有的文件都放在其中。
- /dev：存放硬盘、键盘、鼠标、光驱等各种设备文件。
## 3 从Linux桌面环境如何快速切换到字符控制台终端
按组合键Ctrl+Alt+Fn，其中Fn为F2、F3、F4、F5、F6键中的任何一个。

## 4 如何查看当前主机的CPU处理信息

```shell
[root@svr7 ~]# lscpu
Architecture:          x86_64
CPU op-mode(s):        32-bit, 64-bit
.. ..
厂商 ID：           GenuineIntel
CPU 系列：          6
型号：              13
型号名称：        QEMU Virtual CPU version (cpu64-rhel6)
.. ..
```


> 如有侵权，请联系作者删除
