@[TOC](Linux 操作系统命令 | Linux)

---

# Linux 操作系统命令

## 目录说明

​	根目录 **/** :Linux系统起点
​	**/dev** ：存放设备（键盘、鼠标、显示器、硬盘）
​	**/dev/hda** ：第一块IDE设备
​	**/dev/sda** ： 第一块SCSI设备
​	![Alt](https://img-blog.csdnimg.cn/img_convert/9443f1de6401cbeb91d4f060ebf055a5.png)

​	绝对路径：以根（**/**）开始的路径
​	相对路径：不以根（**/**）开始的路径



## 用户

### 用户标志

root 标志：**#**
普通用户标志：**$**


### 用户类型

普通用户
系统管理员用户
超级用户（root）



### 账号控制（ID）

#### 用户

**UID**：用户ID

> root 的 UID 为：**0**
>
> 普通用户的 UID **$\geqslant$ 1000** （用户UID之间若有跳跃，则创建新用户时UID默认延续用户中UID最大值）



#### 组

**GID**：组ID

> 组账号类型：
>
> ​	基本组（私有组）
>
> ​	附加组（从属组）



### 用户操作

#### 添加用户

```shell
useradd [选项]... 用户名
```

> 常用命令选项：
>
> **-u**：指定 UID
>
> **-d**：指定要创建用户的家目录，不使用则默认用户的家目录为 **/home/创建的用户名**
>
> **-G**：指定用户的附加组（从属组）
>
> **-s**：指定用户的shell解释器



#### 修改用户属性（usermod）

```shell
usermod [选项]... 用户名
```

> 常用命令选项：
>
> **-l**：更改用户帐号的登录名称
>
> **-u**：更改用户id
>
> **-d**：更改用户家目录路径
>
> **-s**：更改用户登录解释器
>
> **-G**：更改用户附加组



#### 查看已存在的用户

```shell
grep 要查找的用户 /etc/passwd
```

> 查找用户的结果格式：**用户名 : 密码占位符 : UID : GID(基本组) : 用户描述 : 用户家目录(宿主目录) : 用户所使用的shell解释器程序**

> 用户相关文件说明：
>
> ​	**/etc/passwd**：存放用户账户信息文件
>
> ​	**/etc/shadow**：存放用户密码文件



#### 删除用户

```shell
userdel 用户名	#删除用户（不删除用户的家目录）
userdel -r 用户名	#删除用户及用户的家目录
```

```shell
userdel -r admin	#删除用户root及用户root的家目录
```



### 组操作

#### 创建组

```shell
groupadd [-g GID组ID] 组名
```

> 记录组账号的基本信息文件： **/etc/group**



#### 组查看

记录组的基本信息文件：**/etc/group**

```shell
grep 要查找的组 /etc/group
```

> 组基本信息文件**/etc/group**格式：**组账号名称  : 密码占位符x : 组的GID号 : 本组的成员用户列表**


记录组的管理信息文件：**/etc/gshadow**

> 组管理信息**/etc/gshadow**文件格式：**组账号名称 : 加密后的密码字符串 : 组的管理员列表 : 组成员列表 **


#### 组成员管理

```shell
gpasswd [选项]... 要操作的用户 组名
```

命令常用选项：

> **gpasswd -A**：定义组管理员列表
>
> **gpasswd -M **：定义组成员用户列表，可设置多个（用逗号分隔）
>
> **gpasswd -a 要添加的用户 组名**：添加组成员，每次只能加一个
>
> **gpasswd -d 要删除的用户 组名**：删除组成员，每次只能删一个


```shell
gpasswd -A nsd01 stugrp	#定义stugrp管理员列表是nsd01
gpasswd -M nsd04,nsd05,nsd01 stugrp	#定义组成员列表为nsd04,nsd05,nsd01
gpasswd -a nsd02 stugrp	#将nsd02用户加入到stugrp组里
gpasswd -d nsd03 stugrp	#将nsd03用户从stugrp组里移除
```

#### 删除组

```shell
groupdel 要删除的组名
```



## 基本目录操作命令

### 目录的查看、切换

`pwd`：查看当前工作目录
`cd`：切换工作目录

> ```shell
> cd ～user	#用户的家目录
> cd /root	#管理员用户的家目录
> cd /home	#普通用户的家目录
> ```



`ls`：显示当前目录的内容

> **青色**：快捷方式
> **蓝色**：目录
> **黑色**：文本文件
> **绿色**：可执行程序

> ```shell
> ls -l /目录	#查看详细属性信息
> ls -A /目录	#查看所有文件
> ls -a /目录	#显示所有文件
> ls -ld /目录	#显示目录本身属性信息
> ls -lh /目录	#提供易读的容量单位
> ls -R /目录	#递归显示内容
> ```



### 目录及文件的创建、移动、复制、删除

#### 目录的创建

```shell
mkdir /要创建的目录	#创建目录
mkdir -p /要创建的目录	#连同父目录一起创建
mkdir -m 要创建的目录    #创建文件夹时直接设置权限，默认权限umask值为022，创建文件夹时的权限为777-022=755
```



#### 目录及文件的移动

```shell
mv /源目录 /要移动到的目录	#移动，路径不变的情况下通目录内移动的同时可修改文件名称
```



#### 目录及文件的复制

```shell
cp /源目录 ...n个 /要复制到的目录	#复制
cp -r /源目录 ...n个 /要复制到的目录	#递归复制（复制的同时可修改名称）
```



#### 目录及文件的删除

```shell
rm -rf /要删除的目录	#强制删除
rm -r /要删除的目录	#递归删除（删除目录是必须加 -r，删除文件时可不加）
```



### 目录的查找

```shell
find /要查找的目录 -type f	#查找目录中的文本文件
find /要查找的目录 -type d	#查找目录中的目录
find /要查找的目录 -type l	#查找目录中的快捷方式
```

>  查找文件格式与要查找的文件类型可使用 `-a`（且） 或 `-o`（或） 表示（不加默认为使用-a）

```shell
find /要查找的目录 -name ”v*”	#查找目录及子目录中的以v开头的文件或目录

find /要查找的目录 -size -10M	#查找小于10M的文件或目录
find /要查找的目录 -size +10M	#查找大于10M的文件或目录

find /要查找的目录 -user 指定用户名	#查找指定用户所有权下的文件或文件夹

find /要查找的目录 -mtime -10	#查看10天内修改的文件
find /要查找的目录 -mtime +10	#查看10天前修改的文件

find /要查找的目录 -exec 	#执行后续操作
```



#### 使用find命令的 -exec（额外）操作

```shell
find /要查找的目录 条件 -exec 处理命令 {} \;	#根据条件查找并处理结果
```

> **{}**：替代每一个查找结果
> **\;** ： 处理操作结束



#### find 的高级使用

```shell
wc /要查看的目录	#显示文件夹属性
wc -l /要查看的文件	#查看文件行数

find /etc/ -name "*.conf" | wc -l	#统计以.conf结尾的行

find /opt/ -name "nsd*" -a -type f	#查找以nsd开头的文件
find /opt/ -name "nsd*" -o -type f	#查找以nsd开头的文件或/opt中的文本文件
```



## 文本文件操作

```shell
cat /要查看的文件	#查看文本文件内容
```

>  less分屏阅读工具（支持上下键翻页）
>
>  创建文本文件 `touch /要创建的文件位置`



### 查找文本内容

```shell
grep -v '要查找的文本'	#取反匹配
grep -i '要查找的文本'	#忽略大小写
grep '^root'	#查找以root为首的行
grep 'root$'	#查找以root为尾的行
grep 'root'	#查找含有root的行
grep '^$'	#查找空行

grep root /etc/passwd	#过滤 /etc/passwd 文件含root的行
```



## 格式化手册阅读工具 man （可查看所有命令的手册）

```shell
man hier	#查看目录结构描述
```



## 历史命令

```shell
history	#查看历史命令（默认1000条）
history -c	#清空历史命令
```



## 统计文件占用空间

```shell
du	#统计文件的占用空间
du -s	#只统计一个目录的占用空间
du -sh	#统计文件占用空间（带单位显示）
```



## 系统信息查看

```shell
hostname	#查看主机名
uname -r	#查看内核版本
lscpu	#查看cpu信息
cat /proc/meminfo	#查看内存
cat /etc/redhat-release	#查看系统信息
```



## 系统配置修改

```shell
hostname 要设置的主机名	#修改主机名 
ifconfig	#查看ip
ifconfig ens33 192.168.1.41/34	#修改网卡ens33的IP地址
date	#查看系统日期时间
```

```shell
date +%F	#查看年月日
date +%Y	#只显示年
date +%m	#只显示月份
date +%d	#只显示日期
date -s ”yyyy-mm-dd HH:MM:SS”	#设置系统时间（自定义）
hwclock -s	#重置系统时间（当前时间）
```



## 解释器

> 默认解释器： **/bin/bash**

```shell
cat /etc/shells	#查看系统中所有解释器
```



## 快捷键

**Tab**：自动补全 --- 1下 自动补齐；2下 自动查找
**Ctrl**+**c** ：中止/废弃当前命令行
**Ctrl**+**l** ：清屏
**Ctrl**+**u** ：清空至行首
**Ctrl**+**w** ：往回删除一个单词，以空格为界
**Esc**+**.** / **Alt**+**.** ：粘贴上一个命令的参数
**.** ：当前目录
**..** ：父目录（上一层目录）




## 通配符

**？** ：单个字符
**\*** ：任意多个字符
**{a,b}** ：匹配a,b两个中的其中一个
**[a,c]** ：匹配a～c范围中的任意一个



## 别名

```shell
alias	#查看已设置的别名
alias hn='ls'	#为命令ls设置别名hn （临时）
unalias hn	#取消已设置的别名hn
vim /etc/bashrc	#为所有用户添加别名（永久）
vim ~/.bashrc	#为当前用户添加别名（永久）
```



## vim编辑器

![Alt](https://img-blog.csdnimg.cn/img_convert/ca493c7bcf4cf6a789555d16f4e1e333.png)

​	：o为另起一行插入



### 命令模式操作

#### 命令模式下光标操作

**0** 或 **^** 或 **Home键** ：到当前行行首
**End键** 或 **$** ：到当前行行尾

**Page Up键** ：向上翻页
**Page Down键** ：向下翻页

**1G** 或 **gg** ：到文件首行
**G** ：到文件末行

#### 命令模式下复制删除操作

**yy** / **#yy** ：复制光标处的一行/整行
**P** ：粘贴到光标之前
**p** ：粘贴到光标之后
**x** 或 **Delete** ：删除光标处的单个字符
**dd** / **#dd** ：删除光标处的一行/整行
**d^** ：从光标处之前删除至行首
**d$** ：从光标处删除至行尾

#### 命令模式下撤销编辑操作

**u** ：撤销最近的一次操作
**U** ：撤销对当前行的所有修改
**Ctrl** + **r** ：取消前一次的撤销操作

#### 命令模式下保存退出操作

**zz** ：保存修改并退出

#### 命令模式下查找功能

**/word** ：向后查找字符串”word”
**N** ：跳至前一个结果
**n** ：跳至后一个结果

### 末行模式操作

#### 文件操作

**:w /root/newfile** ：另存为其他文件（ /root/newfile ）
**:r /etc/filesystems** ：读取其他文件内容（ /etc/filesystems ）

### 字符串替换

#### 行内替换

**: s /old/new** ：使用new替换当前行的第一个old
**: s /old/new/g** ：使用new替换当前行所有的old

#### 区域内替换

**:n,m s/old/new/g** ：使用new替换n～m行中所有的old
**:% s/old/new/g** ：使用new替换文件内所有的old

#### 存盘及退出

**:w** ：保存当前文件
**:q!** ：放弃已有更改后强制退出
**:wq** 或 **:x** ：保存已有修改后退出

### 开关参数的控制

#### 编辑器设置

**:set nu** ：显示行号
**:set nonu** ：不显示行号
**:set ai** ：启用自动缩进
**:set noai** ：关闭自动缩进

## 重定向

定义：将屏幕显示的信息保存到文件中
**>** ：多次重定向到一个文件将被覆盖原来的内容
**>>** ：多次重定向可实现追加信息

示例：

```shell
ls --help > /opt/help.txt	#将帮助信息保存到文件中
echo 123 > /opt/a.txt	#将数字123写入到文件中
echo 123 >> /opt/a.txt	#将数字123追加写入到文件中
```



## 管道

定义：将前一条命令的标准输出后交给下一条命令处理
**|** ：管道符

示例：

```shell
ifconfig ens33 | head -2	#显示上一个命令结果的前两行
cat -n /etc/passwd | head -12 | tail -5	#显示5～12行内容
```



## 软连接（快捷方式）

```shell
ln -s /原始文件或目录 /软连接文件(快捷方式路径)	#创建软连接（快捷方式），快捷方式与原始文件可不在同一分区（删除原始文件后快捷方式不可用）
```



## 硬连接

```shell
ln /原始文件或目录 /硬连接文件(快捷方式路径)	#创建硬连接（快捷方式），快捷方式与原始文件必须在同一分区（删除原始文件后快捷方式仍然可用）
```



## 压缩包的创建及解压

### 创建压缩包

```shell
tar -tf /压缩包文件	#查看压缩文件
tar -zcf /压缩后的文件.tar.gz /要压缩的文件路径	#通过.gz格式进行打包归档（压缩）
tar -jcf /压缩后的文件.tar.bz2 /要压缩的文件路径	#通过.bz2格式进行打包归档（压缩）
tar -Jcf /压缩后的文件.tar.xz /要压缩的文件路径	#通过.xz格式进行归档（压缩）

zip -r /压缩后的文件.zip /要压缩的文件路径	#通过.zip格式进行压缩（跨平台）
```



### 解压缩

```shell
tar -xf /压缩文件	#解压缩到当前目录
tar -xf /压缩文件 -C /要解压到的位置	#解压缩到指定目录

unzip -r /压缩文件.zip	#解压缩到当前目录
unzip /压缩文件.zip -d /要解压到的位置	#解压缩到指定目录
```




## 设备挂载及卸载

### 设备的挂载

```shell
mount /设备路径(/dev/cdrom) /挂载点目录(/dvd)	#挂载光驱设备（一个设备可有多个挂载点目录，但不允许一个挂载点有多个设备）
```



### 设备的卸载

```shell
unmount /挂载点目录	#卸载设备
```



## 软件包管理 RPM

```shell
rpm -q 软件名称	#查询已安装的RPM软件包的版本信息
rpm -qa	#列出已安装的所有软件包
rpm -qpi 软件包.rpm	#查看指定软件的详细信息
rpm -qpl 软件包.rpm	#查看指定软件的文件安装清单（目录）
rpm -ivh 需要安装的软件包	#安装软件包
rpm --import 签名文件	3导入签名认证
rpm -e 软件名称	#卸载软件
```



###  yum命令工具

> yum：自动解决依赖关系

```shell
yum list firefox  #查看软件列表

yum search ftp	#查找包含ftp和ftp相关的包
yum info firefox #查看firefox软件的描述信息
yum probides /etc/passwd	#查看/etc/passwd文件是由哪个软件产生的
```



#### 安装/卸载软件包

```shell
yum [-y] 指令 [软件名]

yum [-y] install	#安装指定软件包 类似于rpm -i
yum [-y] remove	#卸载指定软件包

yum install https	#安装https软件包
yum install -y gcc	#自动安装
```



#### 清空本地 yum 缓存

```shell
yum clean all
```



## 计划任务（周期性任务）

### cron 任务

> 用途：按照设置的时间间隔为用户反复执行某一项固定的系统任务
>
> 软件包：cronie、crontabs
>
> * 系统服务：crond
>
> * 日志文件：/var/log/cron

```shell
tail /var/log/cron    # 了解cron执行消息
crontab -e -u root #为root用户添加日志文件
crontab -r #清空当前用户计划任务
```
> 编辑：crontab -e [-u 用户名]
>
> 查看：crontab -l [-u 用户名]
>
> 清除：crontab -r [-u 用户名]



### 编写crontab任务记录

>  **/etc/crontab**文件：任务记录文件

任务命令行（绝对路径）：  分时日月周
**\***：匹配范围内任意时间 例如 * * * * * 
**,**：分隔多个不连续的时间点
**-**：指定连续时间范围
**/n**：指定时间频率，每n...


## 权限
### 访问权限

访问权限由读取、写入、可执行共同决定

> 读取：允许查看内容 `r`ead，涉及操作：cat，less，head，tail等
>
> 写入：允许修改内容 `w`rite，涉及操作：vim，>>，> 
>
> 可执行：允许运行和切换 e`x`cute，涉及操作：shell脚本编写时可以赋予，默认文本文件有可执行权限


### 权限归属关系

> 所有者：拥有此文件/目录的用户 `u`ser
>
> 所属组：拥有此文件/目录的组 `g`roup
>
> 其他用户：除所有者、所属组以外的用户 `o`ther


### 权限查看

#### 查看文件/目录权限：

```shell
ls -l 要查看的目录	#查看指定目录中的目录及文件权限
ls -ld 要查看的目录	#查看指定目录的权限
```

#### 权限查看结果字段
##### 文件类型位（首位）：

> **-**：文件
>
> **d**：文件夹
>
> **l**：快捷方式

##### 权限位：

**rw- r-- r--**

> 所有者权限 所属组权限 其他用户权限
> 420 400 401
>
> rwx=7
>
> rx=5
>
>`7:rwx`    `6:rw-`    `5:r-x`    `4:r--`    `3:-wx`    `2:-w-`    `1:--x`    `0:---`


##### 用户在不同权限下的访问情况：
`r--`：用户无法进行任何操作
`rw-`：
`rwx`：用户可执行任何操作
`-w-`：只能创建文件，无法进行移动操作
`-wx`：
`--x`：用户只可进入目录，无法查看到目录下的文件及其他操作
`r-x`：



##### 权限信息字段：
```shell
lrwxrwxrwx. 1 root root 3 4月   7 10:04 /dev/cdrom -> sr0
```

> 文件类型 所有者权限 所属组权限 其他用户权限. 硬链接数 所有者 所属组 大小 最后修改时间 文件名称


### 设置基本权限
```shell
chmod [ugoa][+-=], ... 要设置权限的文件夹
```

选项说明：
> **-R**：递归修改权限（修改目录及其子目录）


参数说明：
> **u**：修改所有者权限
> 
> **g**：修改所属组权限
> 
> **o**：其他用户
> 
> 
> **+**：赋予权限
>
> **-**：删除权限
>
> **=**：直接指定所有权限


#### 用户文件权限设置示例：
```shell
chmod u-w /nsd01	#取消所有者w(写)权限
chmod u+w /nsd01	#所有者添加w权限
chmod g=r /nsd01	#设置所属组权限为只读
chmod o=--- /nsd01	#设置其他用户的权限为无任何权限

chmod u=rwx,g=w,o=rx /nsd01	#同时为用户设置权限
chmod 725 /nsd01

chmod -R o=--- /opt/aa/	#递归修改权限，目录本身及此目录中的权限都会发生变化
```

### 修改默认权限

```shell
umask    #查看默认权限值
umask 022    #修改默认权限值为022（创建文件夹时的权限为777-022=755，创建文件时的权限为644）
```

### 设置归属关系

```shell
chown 属主[:属组] 文件
```

选项说明：
> **-R**：递归修该归属关系

#### 文件归属关系设置示例：

```shell
chown a:root /opt	#为opt文件夹设置所属用户a，所属组root
```

### 权限优先级

1. 判断用户的身份	所有者>所属组>其他人
2. 查看对应身份的权限


### 附加权限

#### Set GID

> 1. 占用属组的x位（`g+x`，`g-x`）
> 
> 2. 显示为s或S，取决于属组是否有x权限（s：有x执行权限，S：没有x执行权限）
> 
> 3. 对目录有效
> 
> 4. 在一个具有SGID权限的目录下，新建的文档会自动继承此目录的属组身份


#### Set UID（适用于攻击方）

> 1. 占用属主（User）的x位（`u+x`，`u-x`）
> 
> 2. 显示为s或S，取决于属组是否有x权限（s：有x执行权限，S：没有x执行权限）
> 
> 3. 对对可执行的程序有意义
> 
> 4. 在一个具有SUID标记的程序下，具有此程序属主的身份和相应的权限



#### Sticky Bit 粘滞位（t权限，如公共目录 /tmp）

> 占用其他人权限（Other）的x位（`o+t`，`o-t`）
> 
> 显示为t或T，取决于其他人是否有x权限
> 
> 适用于目录，用来限制用户滥用写入权
> 
> 在设置了粘滞位的文件夹下，即使用户有写入权限，也不能删除或改名其他用户文档



### ACL策略管理

#### ACL访问策略

> 能够对个别用户、个别组设置独立的权限
> 大多数挂载的ECT3/4、XFS文件系统默认已支持


#### 设置ACL权限

```shell
setfacl -m u:要设置的用户:要给此用户的权限rwx 要设置的目录或文件
setfacl -m g:要设置的用组:要给此组的权限rwx 要设置的目录或文件
```

常用命令选项：
> **-m**：定义一条ACL策略
>
> **-x**：清除指定的ACL策略
>
> **-b**：清除**所有**已设置的ACL策略
>
> **-R**：递归设置ACL策略

##### 设置ACL权限示例

```shell
setfacl -m u:root:4 /a    #在a目录下为root用户设置读权限

setfacl -m u:root:--- /a    #设置拒绝权限
```


#### 查看ACL权限

```shell
getfacl 要查看的目录或文件
```



---

---

# 练习题目



## grep 命令的使用

1. 利用grep显示/etc/fstab文件中以UUID开头的信息

	```shell
	grep '^UUID' /etc/fstab
	```

2. 利用grep显示/etc/passwd以bash结尾的行

	```shell
	grep 'bash$' /etc/passwd
	```

3. 利用grep显示/etc/login.defs 以#开头的行

	```shell
	grep '^#' /etc/login.defs
	```

4. 利用grep显示/etc/login.defs 有效配置的行

	```shell
	grep -v '^$' /etc/login.defs | grep -v '^#'
	```

   

## vim 命令的使用

5. 在根目录下创建一个子目录 c

	```shell
	mkdir /c
	```

6. 利用vim建立文件/tedu/stu.txt并写入内容“I Love Goddess”

   ```shell
   vim /tedu/stu.txt
   	I Love Goddess
   :wq
   ```

  

## 复制、删除、移动命令的使用

 1. 在目录/opt下创建一个子目录 nsd 

    ```shell
    mkdir -p /opt/nsd
    ```

 2. 在目录/opt/nsd/创建文件readme.txt,利用vim写入内容 I Love Linux

    ```shell
    vim /opt/nsd/readme.txt
    ```

 3. 将/etc/passwd 和 /etc/resolv.conf同时拷贝到/opt/nsd目录下

    ```shell
    cp /etc/passwd  /etc/resolv.conf /opt/nsd
    ```

 4. 将文件 /etc/redhat-release复制到 /root/ 下，同时改名为 version.txt 

    ```shell
    cp /etc/redhat-release /root/version.txt
    ```

 5. 将文件 /root/version.txt 移动到/opt/nsd/目录下 

    ```shell
    mv /root/version.txt /opt/nsd/
    ```

 6. 将/home目录复制到/opt/nsd/目录下 

    ```shell
    cp -r /home /opt/nsd/
    ```


1. 新建目录结构/student/test/nsd

	```shell
	mkdir -p /student/test/nsd
	cd /student/test/nsd
	```

2. 将文件夹/boot/grub2/复制到目录/student/test/nsd下

	```shell
	cp /boot/grub2 /student/test/nsd
	```

3. 在目录/student/test/nsd创建文件testa.txt并写入内容 NSD  Student（利用echo方式）

	```shell
	echo "NSD Student" > testa.txt
	```

4. 将/student/test/nsd/testa.txt文件复制到/root目录下，同时 改名为 tedu.txt

	```shell
	cp /student/test/nsd/testa.txt /root/tedu.txt
	```

5. 将/etc/passwd 、/etc/resolv.conf、/etc/hosts 同时拷贝到/student/test/nsd目录下

	```shell
	cp /etc/passwd /etc/resolv.conf /etc/hosts /student/test/nsd
	```

6. 将文件/root/tedu.txt移动到/student/test/nsd目录下

	```shell
	mv /root/tedu.txt /student/test/nsd
	```

7. 将文件 student/test/nsd 重改名为 hs.txt

	```shell
	mv /student/test/nsd /student/test/hs.txt
	```

8. 删除/student/test/nsd目录下的grub2子目录

	```shell
	rm -rf /student/test/nsd/grup2
	```



## 别名的使用

1. 为虚拟机定义一个别名，执行byebye可以实现关闭系统

	```shell
	alias byebye='poweroff'
	```

## 创建命令的使用

1. 一条命令创建文件夹/protected/project/tts10

	```shell
	mkdir -p /protected/project/tts10
	```

2. 请在/opt创建三个文本文件分别为1.txt、a.txt、nsd.txt（至少写出2种方法）

	```shell
	touch /opt/1.txt /opt/a.txt /opt/nsd.txt
	touch {1,a,nsd}.txt
	```

3. 利用vim文本编辑器修改/opt/nsd.txt内容写入"I LOVE Linux"

	```shell
	vim /opt/nsd.txt
		I LOVE Linux
	:wq
	```



## 重定向和管道命令的使用

1. 显示ifconfig命令的前2行内容

	```shell
	ifconfig | head -2
	```

2. 显示/etc/passwd第九行内容

	```shell
	cat -n /etc/passwd | head -9 | tail -1
	```

3. 将hostname命令的输出内容，覆盖写入到/opt/hn.txt

	```shell
	hostname > /opt/hn.txt
	```

4. 利用echo命令，将”abc“ 内容追加写入到/opt/hn.txt

	```shell
	echo abc >> /opt/hn.txt
	```

  

## 系统网络参数的配置

1. 设置主机名为t.a.cn

	```shell
	hostname t.a.cn
	```

2. 配置静态IP地址为192.168.4.0/24

	```shell
	ifconfig ens33 192.168.4.0/24
	```

  

## 查找并提取文件内容

1. 在文件 /usr/share/dict/words 中查找到所有包含字符串 seismic 的行,将输出信息,写入到/opt/nsd1.txt

	```shell
	grep 'seismic' /use/share/dict/words > /opt/nsd1.txt
	```

2. 查看内核版本，将显示结果重定向到/root/version.txt

	```shell
	uname -r > /root/version.txt
	```

3. 查看红帽系统版本，将显示结果追加到/root/version.txt

	```shell
	cat /red hat-release > /root/version.txt
	```

4. 查看主机名将显示结果追加到/root/version.txt

	```shell
	hostname > /root/version.txt
	```

5. 将/etc/fstab文件中以UUID开头的信息，写入到/root/fstab.txt

	```shell
	grep ‘^UUID’ /etc/fstab > /root/fastab.txt
	```

6. 提取/etc/passwd以bash结尾的行，将其信息写入/opt/pass.txt

	```shell
	grep ‘bash$’/etc/passwd  > /opt/pass.txt
	```

7. 复制/etc/login.defs文件到当前目录下，改名为init.txt

	```shell
	cp /etc/login.defs ./init.txt
	```

8. 提取init.txt文件里的有效配置（去除以#号开头，去除空行），保存为init2.txt

	```shell
	grep -v '^#' init.txt | grep -v '^$' > init2.txt
	```



## rpm 命令的使用

1. 列出当前主机已安装的所有RPM软件

	```shell
	rpm -qa | wc -l
	```

2. 查看firefox软件包的安装清单

	```shell
	rpm -ql firefox
	```

3. 查看firefox软件包的用途

	```shell
	rpm -qi firefox`
	```

4. 查询光盘中的lynx软件包的用途，安装清单
	```shell
	rpm -pi firefox
	```

5. 利用rpm安装vsftpd这个软件包

	```shell
	rpm -ihv /mnt/Packages/vsftpd-3.0.2-22.el7.x86_64.rpm
	rpm -q vsftpd
	```

6. 删除vim、vi、hostname命令程序

	```shell
	which vim vi hostname
	rm- rf /usr/bin/vim /usr/bin/hostname /
	```

7. 修复vim、vi、hostname
  
	```shell
	rpm -ivh --force /mnt/Packages/vim-enhanced-7.4.160-4.el7.x86_64.rpm
	rpm -qf /usr/bin/vim
	```

8. 安装bind-chroot包，体验依赖关系

	```shell
	rpm -ivh --force /mnt/Packages/bind-9.9.4-61.el7.x86_64.rpm
	```

10. 卸载vsftpd软件

	```shell
	rpm -e vsftpd
	rpm -q vsftpd
	```

## yum练习

1. 将光盘文件挂载到/mnt目录下，查看/mnt下内容

	```shell
	mount /dev/cdrom /mnt
	ls /mnt
	```

1. 搭建本地yum仓库

	```shell
	vim /etc/yum.repos.d/mnt.repo
	
		[mnt] 			# 源名称
		name=Centos7.5		# 操作系统版本
		baseurl=file:///mnt		# 包路径，光盘挂载路径，要与挂在路径相同
		enabled=1
		gpgcheck=0		
	
	ls /etc/yum.repos.d/
	mkdir /etc/yum.repos.d/bind
	mv /etc/yum.repos.d/bind
	mv /etc/yum.repos.d/CentOS-* /etc/yum.repos.d/bind
	ls /etc/yum.repos.d/
	yum repolist	#验证包
	```

## 综合练习 3.31
### 案例1：添加用户帐号

1. 创建一个名为tedu01的用户帐号 

	```shell
	useradd tedu01
	grep tedu01 /etc/passwd
	id tedu01
	```

2. 检查/etc/passwd文件的最后一行

	```shell
	tail -1 /etc/passwd
	```

3. 检查/home新增的宿主目录

	```shell
	ls /home/
	```

4. 新建用户tedu02,宿主目录位于/opt/tedu02

	```shell
	useradd -d /opt/tedu02 tedu02
	grep tedu02 /etc/passwd
	```

5. 新建系统账号system01，将UID设为1234，登录shell设为/sbin/nologin

	```shell
	useradd -u 1234 -s /sbin/nologin system0
	grep system01 /etc/passwd
	```

6. 新建用户admin，附加组设为adm，root

	```shell
	useradd -G adm,root admin
	id admin
	```

7. 更改用户tedu 01密码（root用户）

	```shell
	passwd tedu01
	```

8. 修改当前用户密码

	```shell
	passwd
	```

9. 直接为用户tedu02设置密码123（非交互式）

	```shell
	echo 123 | passwd --stdin tedu02
	```

### 案例2：设置用户密码

1. 为用户tedu01设置一个密码：123456

	```shell
	echo 123456 | passwd --stdin tedu01
	```

2. 过滤/etc/shadow文件中包含tedu01的内容

	```shell
	grep tedu01 /etc/shadow
	```

3. 为用户system01设置密码，并测试是否能够登录

	```shell
	echo a | passwd --stdin system01
	```
	`无法登陆`
	
4. 非交互式给用户tedu02设置密码123456

	```shell
	echo 123456 | passwd --stdin tedu02
	```

5. 交互式给用户admin设置密码redhat

	```shell
	passwd admin
	redhat
	```

---

## 综合练习 4.2
### 案例1:指定yum软件源

1. 将此配置为虚拟机默认软件仓库

	```shell
	mkdir /dvd
	mount /dev/cdrom /dvd
	```

2. 确认可用的仓库列表

	```shell
	ls /mnt
	```

3. 利用yum仓库安装httpd与vsftpd

	```shell
	vim /etc/yum.repos.d/mnt.repo
	    [mnt]
	    name=Centos
	    baseurl=file:///mnt
	    enabled=1
	    gpgcheck=0
	:wq
	rm -rf /etc/yum.repos.d/Centos-*
	ls /etc/yum.repos.d/
	yum repolist
	rm -rf /var/run/yum.pid
	
	cat /etc/yum.repos.d/mnt.repo
	yum install -y httpd vsftpd
	```

4. 利用rpm命令检测是否安装成功

	```shell
	rpm -q httpd vsftpd
	```

### 案例2:查找并处理文件

1. 创建目录/root/findfiles/

	```shell
	mkdir /root/findfiles
	ls /root/
	```

 2. 利用find查找所有用户 lisi 拥有的必须是文件,把它们拷贝到 /root/findfiles/ 文件夹中

	```shell
	find / -user lisi -a -type f -exec cp {} /root/findfiles/ \;
	```

	`-user`：按照文件的所有者来查找

 3. 利用find查找/boot目录下大于10M并且必须是文件，拷贝到/opt

	```shell
	find /boot -size +10M -type f -exec cp {} /opt/ \;
	```

 4. 将目录 /boot内容中以 vm 开头的数据, 复制到/boot/kernel目录下

	```shell
	mkdir /boot/kernel
	find /boot/ -name "vm*" -exec cp {} /boot/kernel/ \;
	ls /boot/kernel/
	```

 5. 利用find查找/boot/ 目录下为快捷方式

	```shell
	find /boot/ -type l
	```

 6. 利用find查找/etc 目录下，以 tab 作为结尾的 必须是文件，将其拷贝到/opt/tab/文件夹下

	```shell
	ls /opt/
	rm -rf /opt/tab
	mkdir /opt/tab
	find /etc/ -name "*tab" -type f -exec cp {} /opt/tab/ \;
	```

### 案例3:查找并提取文件内容

1. 在文件 /usr/share/dict/words 中查找到所有包含字符串 seismic 的行,将输出信息,写入到/opt/nsd18.txt

	```shell
	grep "seismic" /usr/share/dict/words >> /opt/nsd18.txt
	cat /opt/nsd18.txt
	```

2. 查看内核版本，将显示结果重定向到/root/version.txt

	```shell
	uname -r > /root/version.txt
	cat /root/version.txt
	```

3. 查看红帽系统版本，将显示结果追加到/root/version.txt

	```shell
	cat /etc/red hat-release > /root/version.txt
	cat /root/version.txt
	```

4. 查看主机名将显示结果追加到/root/version.txt

	```shell
	hostname >> /root/version.txt
	```

5. 将/etc/fstab文件中以UUID开头的信息，写入到/root/fstab.txt

	```shell
	grep '^UUID' /etc/fstab > /root/fastab.txt
	cat /root/fastab.txt
	```

6. 提取/etc/passwd以bash结尾的行，将其信息写入/opt/pass.txt

	```shell
	grep 'bash$' /etc/passwd  > /opt/pass.txt
	cat /opt/pass.txt
	```

7. 复制/etc/login.defs文件到当前目录下，改名为init.txt

	```shell
	cp -r /etc/login.defs ./init.txt
	```

8. 提取init.txt文件里的有效配置（去除以#号开头，去除空行），保存为init2.txt

	```shell
	grep -v '^#' init.txt | grep -v '^$' > init2.txt
	```

### 案例4:tar制作/释放归档压缩包（zcf、ztf、zxf、jcf、jtf、jxf、cf、tf）
0. 首先创建/root/boothome/与/root/usrsbin/目录
	
	```shell
	mkdir /root/boothome/ /root/usrsbin/
	```

1. 备份/boot、/home这两个文件夹，保存为boothome.tar.gz文件

	```shell
	tar -zcf /boothome.tar.gz /boot /home
	```

2. 查看boothome.tar.gz文件内包含哪些内容 

	```shell
	tar -tf /boothome.tar.gz
	```

3. 将boothome.tar.gz释放到文件夹/root/boothome/下

	```shell
	tar -xf /boothome.tar.gz -C /root/boothome/
	```

4. 备份/usr/sbin目录，保存为usrsbin.tar.bz2文件

	```shell
	tar -jcf /usrsbin.tar.bz2 /usr/sbin
	```

5. 查看usrsbin.tar.bz2文件内包含哪些内容

	```shell
	tar -xf /usrsbin.tar.bz2
	```

6. 将usrsbin.tar.bz2释放到/root/usrsbin/文件夹下

	```shell
	tar -xf /usrsbin.tar.gz2 /root/usrsbin
	```

7. 创建一个名为 /root/backup.tar.bz2 的归档文件，其中包含 /usr/local 目录中的内容，tar 归档必须使用 bzip2 进行压缩

	```shell
	tar -jcf /root/backup.tar.bz2 /usr/local/
	tar -xf /root/backup.tar.bz2
	```

### 案例5：usermod修改用户

1. 新建一个用户nsd03，将宿主目录设为/opt/home03，并设置密码为redhat

	```shell
	useradd -d /opt/nsd03 nsd03
	id nsd03
	ls /opt
	grep nsd03 /etc/passwd
	echo redhat | passwd --stdin nsd03
	```

2. 将用户nsd03的宿主目录改为/home/nsd03

	```shell
	usermod -d /home/nsd03 nsd03
	grep nsd03 /etc/passwd
	ls /home
	```

3. 将用户sys01的登录Shell改为/bin/bash

	```shell
	useradd  -s /sbin/nologin sys01
	usermod -s /bin/bash sys01
	grep sys01 /etc/passwd
	```

### 案例6：创建用户

1. 创建一个名为alex的用户，用户ID是 3456。密码是flectrag

	```shell
	useradd -u 3456 alex
	grep alex /etc/passwd
	echo flectrag | passwd --stdin alex
	id alex
	```
	
### 案例7：创建用户和组

1. 一个名为adminuser的组

	```shell
	groupadd adminuser
	grep adminuser /etc/group
	```

2. 一个名为natasha的用户，其属于adminuser，这个组是该用户的从属组

	```shell
	useradd -G adminuser natasha
	grep natasha /etc/group
	```

3. 一个名为harry的用户，属于adminuser，这个组是该用户的从属组

	```shell
	useradd -G adminuser harry
	grep harryr /etc/group
	```

4. 一个名为sarah的用户，其在系统中没有可交互的shell，并且不是adminuser组的成员用户

	```shell
	useradd -s /sbin/nologin sarah
	grep sarah /etc/group
	```

5. natasha、harry、和sarah的密码都要设置为flectrag

	```shell
	echo flectrag | passwd --stdin natasha
	echo flectrag | passwd --stdin harry
	echo flectrag | passwd --stdin sarah
	```

### 案例8：配置一个cron任务

1. 为用户 natasha 配置一个定时任务

	```shell
	su natasha
	crontab -e
	```

	```shell
	crontab -e -u natasha
	```

2. 每天在本地时间 23:30 执行
3. 需要完成的任务操作为 /bin/echo  hiya

	```shell
	30 23 * * * /bin/echo hiya
	```

### 案例9：设置别名

1. 为root用户永久设置别名为hn='hostname'

	```shell
	su root
	vim ~/.bashrc
		alias hn='hostname'
	```

	```shell
	vim /root/.bashrc
		alias hn='hostname'
	```
	


2. 为所有用户设置别名为 qstat='/bin/ps -Ao pid,tt,user,fname,rsz' 

	```shell
	vim /etc/bashrc
		qstat='/bin/ps -Ao pid,tt,user,fname,rsz'
	```


## 练习 4.7
### 案例3：配置用户和组账号
1. 新建用户alex，其用户ID 为3456，密码是flectrag

	```shell
	useradd -u 3456 alex
	grep alex /etc/passwd
	echo flectrag | passwd --stdin alex
	```

2. 创建下列用户、组及组成员的关系：
    2.1 一个名为adminuser的组

	```shell
	groupadd adminuser
	grep adminuser /etc/group
	```
	
	2.2 一个名为natasha的用户，其属于adminuser组，这个组是该用户的从属组
	
	```shell

	```shell
	useradd -G adminuser natasha
	id natasha
	```


    2.3 一个名为harry的用户，其属于adminuser组，这个组是该用户的从属组

	```shell
	useradd -G adminuser harry
	id harry
	```

    2.4 一个名为sarah的用户，其在系统中没有可交互的Shell，并且不是adminuser组的成员

	```shell
	useradd -s /sbin/nologin sarah
	grep sarah /etc/passwd
	```

    2.5 natasha、harry、sarah的密码都要设置为flectrag

	```shell
	echo flectrag | passwd --stdin natasha
	echo flectrag | passwd --stdin harry
	echo flectrag | passwd --stdin sarah
	```

### 练习4.8
#### 案例2：文件/目录的默认权限
1. 以root用户登录，测试umask掩码值
    1.1. 查看当前umask值

    ```shell
    umask
    ```

    1.2. 新建目录udir1，文件ufile1，查看默认权限

    ```shell
    mkdir /udir1 /ufile1
    ls -ld /udir1
    ls -ld /ufile1
    ```
    
    1.3. 将umask设为077，再新建目录udir2、文件ufile2,查看默认权限

    ```shell
    umask 077
    umask
    mkdir /udir2 /ufile2
    ls -l /udir2
    ls -l /ufile2
    ```

    1.4. umask值重新设置为022

    ```shell
    umask 022
    umask
    ```

2. 以用户zhangsan登入，查看当前的umask值

    ```shell
    useradd zhangsan
    su zhangsan
    umask
    ```


## 练习4.8 
### 案例3：设置归属关系

0. 新建/tarena1目录，并进一步完成下列操作

    ```shell
    mkdir /tarena1
    ls -ld /tarena1
    ```

1. 将属主设为gelin01，属主设为tarena组

    ```shell
    id gelin01
    grep tarena
    
    useradd gelin01
    groupadd tarena
    chown gelin01:tarena /tarena1/
    ```

2. 使用户gelin01对此目录具有rwx权限，其他人对此目录无任何权限

    ```shell
    ls -ld /tarena1/
    chmod o=/tarena1/
    ```

3. 使用户gelin02能进入，查看此目录

    ```shell
    id gelin02
    useradd gelin02
    
    gpasswd -a gelin02 tarena
    su gelin02
    ls -ld /tarena1/
    ```

4. 将gelin01加入tarena组，将tarena1目录的权限设为450，再测试gelin01童虎能否进入此目录

    ```shell
    gpasswd -a gelin01 tarena
    chmod 450 /tarena1/
    ls -ld /tarena1/
    
    su - gelin01
    cd /tarena1/
    ```

    `否`



## 练习4.9 
### 案例：SGID练习

1. 创建/nsdpublic目录，将属组改为tarena，进一步完成下列操作：

    ```shell
    mkdir /nsdpublic
    ls -ld /nsdpublic
    groupadd tarena
    chown :tarena /nsdpublic
    ```

2. 新建子目录nsd01，子文件test01.txt，查看两者的权限及归属

    ```shell
    mkdir /nsdpublic/nsd01
    touch /nsdpublic/nsd01/test01.txt
    ```

3. 为此目录添加SGID权限，再新建子目录nsd02，子文件test02.txt

    ```shell
    chmod g+s /nsdpublic
    ls -ld /nsdpublic/
    
    mkdir /nsdpublic/nsd02
    touch /nsdpublic/nsd02/test02.txt
    ```

4. 查看上述子目录及文件的权限及归属

    ```shell
    ls -ld /nsdpublic/nsd02
    ls -ld /nsdpublic/nsd02/test02.txt
    ```




> 如有侵权，请联系作者删除