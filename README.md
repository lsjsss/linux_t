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

echo "svr7.nm.cn" > /etc/hostname	#永久修改主机名
hostname svr7.nm.cn

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


### 批量添加注释（命令模式下）

>`Ctrl`+`v`键
>
> 选中要添加注释的行
>
> `I`键
>
> #
>
> `Esc`键

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



## 分区管理

磁道：
扇区：1扇区=512字节

识别硬盘 -> 分区规划 -> 格式化 -> 挂载使用

```shell
lsblk	#查看分区详细信息，查看识别硬盘
```

### 分区规划
#### MBR分区模式

> 分区类型：主分区、扩展分区、逻辑分区

实际操作为：3个主分区+1个扩展分区+n个逻辑分区

理论最多支持4个主分区（题目正确答案）
最多支持1个扩展分区（扩展分区不可直接用来存储数据）
逻辑分区可以有无限个，建立在扩展分区之上
最大支持2.2TB容量


#### GPT分区模式（常用）

最多支持128个主分区
最大支持18EB的容量
1EB=1024*1024TB

### 分区工具

```shell
fdisk /dev/sdb	#进入分区工具
```

选项
**n**：添加一个分区
**p**：打印分区表
**q**：不保存退出



### 格式化分区

文件系统类型：
> windows：NTFS FAT32
>
> Linux：ext4 xfs


```shell
mkfs.ext4 /deb/sdb1    #将sdb1格式化为ext4文件系统类型
blkid /dev/sdb2    #查看分区文件系统类型，UUID是设备的唯一标识
mkfs.xfs /dev/sdb2    #格式化分区为xfs文件系统类型
```


### 挂载使用

```shell
mkdir /dvd/mdb
mount /dev/sdb1 /dvd
ls /dvd
mkdir /dvd/abc    #验证写入数据
mount /dev/sdb2 /mdb
mkdir /mdb/abc01    #验证写入数据
ls /mdb/
df -h /mypart1    #查看挂载设备的使用情况
```



#### 开机自动挂载
开机自动挂载配置文件：**/etc/fstab**

```shell
vim /etc/fstab
```

> 配置文件/etc/fstab 的显示格式：**设备路径**  **挂载点**  **类型**  **参数**  **备份标记**[1:备份，0:不备份]  **检测顺序**[1:检测，0:不检测]

```shell
mount -a    #作用1：检测etc/fstab下的问题，作用2：查看文件中的设备有没有挂载的会自动进行挂载
```

> 示例：实现开机自动挂载

```shell
mount /mypt1
mount /mypt2
vim /etc/fstab
	/dev/sdb3 /mytp1 ext3 defaults 0 0
	/dev/sdb7 /mytp1 xfs defaults 0 0
	/dev/cdrom /mnt iso9660 defaults 0 0    #光盘的文件类型为 iso9660
tail -2 /etc/fstab
mount -a
df -h
```


### 交换空间

> 相当于虚拟内存，
>
> 当物理内存不够用时，使用磁盘空间来模拟内存
>
> 在一定程度上缓解内存不足的问题
> 
> 交换分区：以空闲分区充当的交换空间
>
> 交换文件：以文件模拟的设备充当交换空间


#### parted常用分区指令

```shell
parted /dev/sdc

#
mktab gpt    #指定分区模式为 gpt
print    #查看分区表
mkpart    #交互式创建分区
unit GB    #以 GB 单位显示分区表
```

#### 使用交换分区做交换空间（格式化交换文件）

```shell
mkswap -f 要交换文件
```

选项
> **f**：强制执行

```shell
mkswap /dev/sdb1    #将分区 /dev/sdb1 格式化为交换分区
free -m	#查看剩余内存的使用量及交换空间的大小（单位：MB）

swapon /dev/sdb1    #启用交换分区 /dev/sdb1
swapon -s    #查看交换分区
swapoff /dev/sdb1    #停用交换分区 /dev/sdb1

vim /etc/fstab    #将交换分区设置为开机自动挂载
/dev/sdb1 swap swap defaults 0 0
/dev/sdb2 swap swap defaults 0 0
tail -2 /etc/fstab
swapon -a
swapon -s
```


#### 创建Swap文件

利用文件创建Swap空间
（生成大的文件用dd命令）

```shell
dd if=源设备 of=目标设备 bs=块大小 count=块数
```

```shell
dd if=dev/xero of=/opt/swap.db bs=1M count=2048	#示例
ls -lh /opt/swap.db
mkswap /opt/swap.txt
swapon /opt/swap.txt
swapon -s
free -m
chmod 600 /opt/swap.txt
swapoff /opt/swap.txt
vim /etc/fstab
    /opt/swap.txt swap swap defaults 0 0
swapon -a
swapon -s
```

## 逻辑卷

> 优势：
>
> 1. 可以整合分散的空间
>
> 2. 逻辑卷支持扩容（动态扩容）


### LVM快速部署及使用
#### 创建卷组
格式：vgcreate 卷组名 设备路径

工作方式：
> 零散空闲存储 -> 整合的虚拟磁盘 -> 虚拟的分区
> 物理卷（PV）        卷组（VG）        逻辑卷（LV）

| 功能 | 物理卷管理 | 卷组管理 | 逻辑卷管理 |
| -- | -- | -- | -- |
| Scan扫描 | pvscan | vgscan | lvscan |
| Create创建 | pvcreate | vgcreate | lvcreate |
| Display显示 | pvdisplay | vgdisplay | lvdisplay |
| Remove删除 | pvremove | vgremove | lvremove |
| Ectend扩展 | / | vgextend | lvextend |


```shell
pvcreate /dev/sdb1 /dev/sdb2	#创建物理卷，可以不用写，直接使用vgcreate创建也是可以的
pvs	#查看物理卷信息
vgcreate myvg /dev/sdb1 /dev/sdb2	#创建卷组
vgs	#查看卷组信息
```

#### 创建逻辑卷

格式：

```shell
lvcreate -L 逻辑卷大小 -n 逻辑卷名 卷组名
```

示例：
```shell
lvcreate -L 16G -n myvo myvg
lvs
```


#### 扩展逻辑卷
情况一：卷组有足够的剩余空间

1. 扩展逻辑卷大小

    ```shell
    vgs
    lvextend -L 18GG /dev/systemvg/vo    #扩展到18G
    df -h /vo    #查看使用情况
    lvs
    df -h
    ```

2. 扩展文件系统大小

    ```shell
    resize2fs    #扩展 ext3/ext4 文件系统类型
    xfs_growfs /dev/systemvg/vo    #扩展 xfs 文件系统类型
    df -h
    ```

情况二：卷组没有足够的剩余空间

1. 扩展卷组

    ```shell
    vgs
    vgextend systemvg /dev/sdb3	#为逻辑卷systemvg扩展空间
    ```

2. 扩展逻辑卷大小

    ```shell
    vgs
    lvextend -L 25G /dev/systemvg/vo
    lvs
    ```

3. 扩展文件系统大小

    ```shell
    xfs_growfs /dev/systemvg/vo
    df -h
    ```

#### 逻辑卷的删除

--

#### 逻辑卷的缩减

> ext4不支持逻辑卷的缩减
>
> xfs不支持逻辑卷的缩减


## RAID磁盘阵列

> 廉价冗余磁盘阵列
>
> 通过硬件/软件技术，将多个较小/低速磁盘整合成一个磁盘
>
> 阵列的价值：提升I/O效率、硬件级别的数据冗余
>
> 不同RAID级别的功能、 特性各不相同


### RAID0，条带模式
同一个文档分散存放在不同磁盘
并行写入以提高效率

### RAID1，镜像模式
一个文档**复制**成多分，分别写入不同磁盘
多份拷贝提高可靠性，效率无提升

### RAID5（至少需要三块磁盘组成）
相当于RAID0和RAID1的折中方案
需要至少一块磁盘的容量来存放校验数据（奇偶校验）

### RAID0+1（至少需要四块磁盘组成）
?整合于RAID0和RAID1的折中方案
?需要至少一块磁盘的容量来存放校验数据（奇偶校验）

### RAID1+0（至少需要四块磁盘组成）
?整合于RAID0和RAID1的折中方案
?需要至少一块磁盘的容量来存放校验数据（奇偶校验）

### RAID各级别特点对比

| 对比项 | RAID0 | RAID1 | RAID10 | RAID5 | RAID
| -- | -- | -- | -- | -- | -- |
| 磁盘数 | >=2 | >=2 | >=4 | >=3 | >=4 |
| 存储利用率 | 100% | <=50% | <=50% | n-1/n | n-2/n |
| 校验盘 | 无 | 无 | 无 | 1 | 2 |
| 容错性 | 无 | 有 | 有 | 有 | 有 |
| IO性能 | 高 | 低 | 中 | 较高 | 较高 |



### RAID阵列实现方式
#### 硬RAID
> 由RAID控制卡管理阵列（不同型号服务器配置方式不同）
>
> 主板 -> 阵列卡 -> 磁盘 -> 操作系统 -> 数据

#### 软RAID
> 由操作系统来管理阵列
>
> 主板 -> 硬盘 -> 操作系统 -> RAID软件 -> 数据


### 系统文件损坏故障
#### 故障现象：
/etc/fstab文件内容有误，系统无法正常开机

#### 解决思路：
引导进入修复模式，然后进行修复

#### 模拟故障：

```shell
vim /etc/fstab
	/dev/sdb1 /mypar1 xfs defaults 0 0
reboot
```

解决故障：
在Control-D界面处直接输入root密码，会直接进入命令行，之后修改fstab文件

```shell
vim /etc/fstab
# /dev/sdb1 /mypar1 xfs defaults 0 0
reboot
```

## 重设root密码
开机界面按e

```shell
UTF-8
rd.break console=tty0
```

`Ctrl+X`

```shell
mount -o remount,rw /sysroot
chroot /sysroot
echo redhat | passwd --stdin root

touch /.autorelabel
exit
reboot
```




---

# 云计算网络管理命令

## 配置Linux网络
### 配置静态主机名

> 配置文件/etc/hostname
>
> 固定保存的主机名，永久有效

```shell
echo "svr7.tedu.cn" > /etc/hostname
hostname svr7.tedu.cn
```

### 修改网卡命名规则

```shell
vim /etc/default/grub
    .........
    GRUB_CMDLINE_LINUX="..... quiet net.ifnames=0 biosdevname=0"
    ...........

grub2-mkconfig -o  /boot/grub2/grub.cfg #使网卡命名规则生效
reboot

ifconfig | head -2    #重启之后查看网卡名是不是eth0
```

### 配置静态IP地址

```shell
nmcli connection show   #查看网卡信息
nmcli connection delete ens33   #删除ens33网卡设备
nmcli connection show
nmcli connection delete 有线连接\ 1
nmcli connection show
nmcli connection add type ethernet ifname eth0 con-name eth0         #添加网卡设备eth0
nmcli connection show

#配置 eth0 的IP地址 （手动manual，自动auto） 为 192.168.4.10/24，网关为 192.168.4.254，开机后自动连接
nmcli connection modify eth0 ipv4.method manual ipv4.addresses 192.168.4.10/24 ipv4.gateway 192.168.4.254 connection.autoconnect yes

nmcli connection up eth0    #激活网卡
ifconfig | head -2
route -n    #查看网关
```

#### 通过修改配置文件的方式修改IP地址

```shell
vim /etc/sysconfig/network-scripts/ifcfg-eth0
    TYPE=Ethernet
    BOOTPROTO=static    #自动获取是dhcp，手动配置是static
    NAME=eth0
    DEVICE=eth0
    ONBOOT=yes
    IPADDR=192.168.4.25 #ip地址
    PREFIX=24   #子网掩码

systemctl restart network   #重启network网络服务
ifconfig | head -2
    eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
    inet 192.168.4.25  netmask 255.255.255.0  broadcast 192.168.4.255
```

### 为本机指定DNS服务器

> 配置文件   /etc/resolv.conf
>
> 关键记录：nameserver DNS服务器地址


```shell
vim /etc/resolv.conf
    # Generated by NetworkManager
    search tedu.cn
    nameserver 8.8.8.8

echo "nameserver 9.9.9.9" > /etc/resolv.conf
```

## 远程管理ssh
### SSH协议（Secure Shell）

> 为客户机提供安全的 Shell 环境
>
> 默认端口：**TCP22**


### OpenSSH 服务

> 服务名称：sshd
>
> 主程序：/use/sbin/sshd、/usr/bin/ssh
>
> 配置主件：/etc/ssh/sshd_config
>
> 	/etc/ssh/ssh_config

### SSH的基本使用

```shell
ssh root@要远程主机的ip地址	#远程指定的主机

ssh root@要使用图形界面远程主机的ip地址	#使用图形界面远程指定的主机
firefox	#测试图形界面状态下
```


## 使用scp远程复制工具
### 安全复制工具scp

```shell
scp -r 用户名@服务器:远程路径 本地路径	#将指定主机上的文件下载到本地
scp -r 本地路径 用户名@服务器:远程路径	#将本地的文件上上传至指定主机
```

```shell
scp -r root@192.168.4.207:/boot /opt/	#将远程主机.207的目录boot复制到本地opt目录下
scp -r /boot root@192.168.4.207:/opt/	#将本机的boot目录复制到远程主机.207主机的opt目录下
```


## 常用的网络工具
### 查看ip地址

```shell
ip address show
ip a s	#简写
```

### 添加ip地址

```shell
ip address add 192.168.8.1/24 dev ens33
ip aa
```

### 指定下一跳

```shell
vim /etc/rc.d/rc.local	#设置每次开机生效
	ip address add 192.168.8.1/24 dev ens33

ip route add 10.0.0.0/24 via 192.168.8.100 dev ens33	#添加路由，via是下一跳
ip route del 10.0.0.0/24	#删除路由表
ip route show	#查看路由表
```


### 查看对应的端口号
ss与netstat

选项列表：

> **-a**：显示所有端口的信息
> 
> **-n**：以数字格式显示端口号
> 
> **-t**：显示TCP连接的端口
>
> **-u**：显示UDP连接的端口
> 
> **-l**：显示服务正在监听的端口信息
> 
> **-p**：显示监听端口的服务名（程序名称）

```shell
netstat -anptu	#查看端口的详细信息
ss -antpu	#查看TCP端口号（相对全面）
netstat -anptu | grep :22	#筛选端口号为22的端口
ss -anptu | grep :22
```


### ping命令

```shell
ping -c 测试包的个数n 目标ip地址 #ping包n次
```

### Yum仓库特点
作为yum源需要准备的内容
大量的.rpm源需要准备的内容
针对这些软件包 **repodata/** 仓库档案


**repodata/**：仓库档案数据

> filelists.xml.gz	软件包的文件安装清单
>
> primary.xml.gz	软件包的基本/主要信息
>
> other.xml.gz	软件包的其他信息
>
> repomd.xml


### 结束后台进程

```shell
kill oneko	
```


### 源码编译安装的优势

主要优点

> 获得软件的最新版，及时修复bug
>
> 软件功能可按需选择/定制，有更多软件可供选择
> 
> 源码包适用于各种平台

#### 安装开发工具gcc、make

```shell
yum -y install gcc make	#安装gcc、make包
rpm -q gcc	#检查是否安装成功
rpm -q make
tar -xf /opt/tools/inotify-tools-3.13.tar.gz -C /opt/
cd /opt/inotify-tools-3.13/
./confgure --help
./confgure --help --prefix=/opt/haha	#配置时指定安装位置
make	#编译
make install	#安装
ls /opt/haha/
ls /opt/haha/bin/
```


## SELinux运行模式的切换
### SELinux的运行模式

> enforcing（强制模式）
>
> permissive（宽松模式）
>
> disabled（彻底禁用）


### 切换运行模式
#### 临时切换：

```shell
getenforce	#查看SELinux当前的运行状态

setenforce 1	#切换至强制模式 1
setenforce 0	#切换至宽松模式 0
```

#### 永久改变SELinux的运行模式

> 固定配置：/etc/selinux/config 文件

```shell
vim /etc/selinux/config	#永久改变SELinux的运行模式
    SELINUX=disabled	#彻底禁用SELinux
    SELINUX=enabled	#彻底禁用SELinux
	
reboot	#重启查看状态
```


## 服务器架构

服务器：能够为其他服务器提供服务的更高级的电脑
> 
> 机架式
> 
> 塔式
> 
> 机柜室
>
> 刀片式


### Client/Server架构

> 由服务器提供资源或某种功能
>
> 客户机使用资源或功能

### 搭建web（http）服务
#### 装包、起服务

1. 安装httpd（Apache）软件包（服务器软件）

    ```shell
    yum -y install httpd
    ```

2. 重起httpd服务

    ```shell
    systemctl start httpd
    ```

3. 访问测试，书写一个页面文件

    ```shell
    firefox http://192.168.4.10
    
    vim /var/www/html/index.html	#打开默认存放网页文件的路径进行编辑
    	<marquee><fount color=red><h1>I am king
    
    yum -y install elinks	#命令行浏览器
    
    elinks --dump http://192.168.4.10
    curl http://192.168.4.10	#命令行浏览器
    ```

##### 浏览页面

```shell
curl http://192.168.4.10	#命令行界面访问网站
elinks http://192.168.4.10	#命令行界面下的浏览器
elinks --dump http://192.168.4.10	#命令行界面直接浏览
```

### 搭建ftp服务
#### 装包、起服务
1. 安装vsftpd软件包

    ```shell
    yum -y install vsftpd
    ```

2. 启动vsftpd服务

    ```shell
    systemctl start vsftpd	#启动vsftpd服务
    systemctl restart vsftpd	#重起vsftpd服务
    ```

3. 访问测试

    ```shell
    firefox ftp://192.168.4.10
    touch /var/ftp/a.txt
    
    ls /var/ftp
    ```


## 防火墙
### Firewalld服务基础

> 系统服务：firewalld
>
> 管理工具：firewall-cmd、firewall-config


```shell
systemctl restart firewalld
firewall-config &
```


### 预设安全区域

根据所在的网络场所划分，预设保护规则集

> **public**：仅允许访问本机的sshd等少数几个服务（sshd、ping、dhcp）
>
> **trusted**：允许任何访问
>
> **block**：阻塞任何来访请求
>
> **drop**：丢弃任何来访的数据包

配置规则的位置

> 运行时（runtime）
>
> 永久（permanent）


```shell
#A机器
firewall-cmd --get-default-zone

#B机器
ping 192.168.4.10	可以ping通
curl http://192.168.4.10	#拒绝访问
curl ftp://192.168.4.10	#拒绝访问

#A机器
firewall-cmd --set-default-zone=trusted	#修改防火墙默认区域为trusted
firewall-cmd --get-default-zone

#B机器测试
ping 192.168.4.10	#可以ping通
curl http://192.168.4.10	#可以访问
curl ftp://192.168.4.10	#可以访问

#A机器
firewall-cmd --set-default-zone=block	#修改防火墙默认区域为block
firewall-cmd --get-default-zone

#B机器测试
ping 192.168.4.10	#不可以ping通，但是有回应

#A机器
firewall-cmd --set-default-zone=drop	#修改防火墙默认区域为drop
firewall-cmd --get-default-zone

#B机器测试
ping 192.168.4.10	#不可以ping通，但是有回应
```

## 互联网常见协议

| 名称 | 协议类型 | 默认端口 |
| -- | -- | -- |
| **http** | 超文本传输协议 | 80 |
| **https** | 安全的超文本传输协议 | 443 |
| **ftp** | 文件传输协议 | 21 |
| **tftp** | 简单的文件传输协议 | 69 |
| **DNS** | 域名解析协议 | 53 |
| **telent** | 远程管理协议 | 23 |
| **smtp** | 邮件协议（发送端口） | 25 |
| **pop3** | 邮件协议（接收端口） | 110 |
| **snmp** | 简单的网络管理协议 | 161 |



### 添加服务（临时）

```shell
firewall-cmd --zone=public --add-service=http	#启动http服务，设置允许http协议通过public区域（允许其他主机通过http访问）
firewall-cmd --zone=public --add-service=ftp	#启动ftp服务，设置允许ftp协议通过public区域（允许其他主机通过ftp访问）
firewall-cmd --zone=public --list-all	#查看区域策略（查看已启动的服务）

curl http://192.168.4.10	#在另一台主机上检测是否开启成功
curl ftp://192.168.4.10
```

### 添加服务（永久）
（永久设置允许ftp协议和http协议通过public区域（permanent：永久设置）开机自启）

```shell
firewall-cmd --permanent --zone=public --add-service=ftp	#永久启动ftp服务
firewall-cmd --permanent --zone=public --add-service=http	#永久启动http服务
firewall-cmd --reload    #重新加载配置文件
firewall-cmd --permanent --zone=public --list-all    #查看区域策略

netatat -anptu | grep :80    #过滤80端口
systemcli status httpd    #查看http服务状态
systemcli enable httpd    #设置http服务开机自启

curl ftp://192.168.4.10    #使用192.168.4.7主机检测，可以访问
curl http://192.168.4.10    #使用192.168.4.7主机检测，可以访问
```


### 服务的启动、重启、停止

```shell
systemcli enable httpd    #设置http服务开机自启
systemcli disable httpd    #设置http服务开机不自启

systemcli restart httpd    #重启http服务
systemcli stop httpd    #停止http服务
```

### 拒绝其他主机（指定ip，指定网络段）访问服务

```shell
firewall-cmd --zone=block --add-source=192.168.4.7    #拒绝192.168.4.7主机访问服务

curl ftp://192.168.4.10    #使用192.168.4.7主机检测，不可以访问
curl http://192.168.4.10    #使用192.168.4.7主机检测，不可以访问
```

### 恢复其他主机（移除列表中已指定ip，指定网络段）访问服务

```shell
firewall-cmd --zone=block --remove-source=192.168.4.7	#移除192.168.4.7主机，使其可以访问服务

curl ftp://192.168.4.10    #使用192.168.4.7主机检测，可以访问
curl http://192.168.4.10    #使用192.168.4.7主机检测，可以访问
```



## 部署网络 yum 源

>  服务端：利用 Web 服务或 FTP 服务共享光盘所有内容

### 利用 web（HTTP）服务共享

默认共享位置:/var/www/html/ 

> 服务端svr7操作
>
> ```shell
> yum -y install httpd
> systemctl start httpd
> systemctl status httpd #查看服务运行状态
> mkdir /var/www/html/dvd
> mount /dev/cdrom /var/www/html/dvd
> ls /var/www/html/dvd #查看是否有光盘内容
> firefox http://192.168.4.7/dvd #访问测试
> ```

>  客户端pc207操作
>
> ```shell
> vim /etc/yum.repos.d/dvd.repo
> 	[dvd]
> 	name=CentOS7.5
> 	baseurl=http://192.168.4.7/dvd
> 	enabled=1
> 	gpgcheck=0
> yum clean all
> yum repolist
> yum -y install unzip
> ```



### 利用 FTP 服务共享

默认共享位置：/var/ftp  

>  服务端svr7操作
>
> ```shell
> rpm -q vsftpd
> systemctl start vsftpd
> systemctl status vsftpd #查看服务运行状态
> mkdir /var/ftp/dvd
> mount /dev/cdrom /var/ftp/dvd
> firefox ftp://192.168.4.7/dvd #访问测试
> ```



> 客户端pc207操作
>
> ```shell
> vim /etc/yum.repos.d/dvd.repo
> 	[dvd]
> 	name=CentOS7.5
> 	baseurl=ftp://192.168.4.7/dvd
> 	enabled=1
> 	gpgcheck=0
> yum clean all
> yum repolist
> ```


## NPT（网络时间协议）时间同步
Network Time Protocol（网络时间协议）

> 用来同步网络中各个计算机的时间的协议
>
> 210.72.145.39（国家授时中心服务器IP地址）

Stratum（分层设计）

> Stratum层的总数限制在15层以内（包括15）

### 时间同步软件包

服务端（设置为时间同步服务器）：

```shell
yum -y install chrony
rpm -qc chrony	#查看配置文件（.conf结尾的文件）

vim /etc/chrony.conf
	server 0.centos.pool.ntp.org iburst	#网络标准时间服务器（快速同步）
	allow 192.168.4.0/24	#允许同步时间的主机网络段
	denv 192.168.4.1	#拒绝同步时间的主机网络段
	local statum 10	#访问层数
systemctl restart chronyd	#重启时间同步服务

setenforce 0
systemctl stop firewalld	#关闭防火墙
```

客户端（同步服务器上的时间）：

```shell
vim /etc/chrony.conf
	server 192.168.4.7 iburst	#指定要同步时间的服务器（192.168.4.7）
systemctl restart chronyd	#重启时间同步服务
chronyc sources -v	#验证时间是否同步成功
```


## Iscsi概述
### Internet SCSI，网际SCSI接口

> 一种基于C/S架构的虚拟磁盘技术
>
> 服务器提供磁盘空间，客户机连接并当成本地磁盘使用


### Iscsi磁盘的构成
backstore，后端存储
> 对应到服务端提供实际存储空间的设备，需要起一个管理名称

target，磁盘组
> 是客户端的访问目标，作为一个框架，由多个lun组成

lun，逻辑单元
> 每一个lun需要关联到某一个后端存储设备，在客户端会视为一块虚拟磁盘

### 使用targetcli建立配置（服务机svr7）

```shell
backstore/block create name=后端存储名 dev=实际设备路径	#创建后端存储
iscsi create 磁盘组的IQN名称	#IQN名称规范，创建磁盘组
iscsi/磁盘组名/tpql/luns create 后端存储路径	#创建关联
iscsi/磁盘组名/tpgl/acls create 客户机IQN标识
iscsi/磁盘组名/tpql/portals create IP地址 端口号
```

```shell
yum -y install targetcli	#安装服务软件包 targetcli
systemctl stop firewalld    #关闭防火墙
targetcli	#运行 targetcli 命令进行配置
	ls
	
	#创建后端存储
	backstores/block create dev=/dev/sdb1 name=nsd
	
	#创建磁盘组target，使用IQN名称规范
	iscsi/ create iqn.2019-09.cn.tedu:server
	
	#创建lun关联
	iscsi/iqn.2019-09.cn.tedu:server/tpg1/luns create /backstores/block/nsd
	
	#设置访问控制（acl），设置客户端的名称
	iscsi/iqn.2019-09.cn.tedu:server/tpg1/acls create iqn.2019-09.cn.tedu:client

	ls
	exit
systemctl restart target.service
```

#### IQN名称规范

`iqn.yyyy-mm.倒序域名`：自定义标识
用来识别target磁盘组，也用来识别客户机身份


### 使用targetcli建立配置（客户机pc207）

```shell
#安装客户端软件
yum -y install iscsi-initiator-utils
rpm -q iscsi-initiator-utils

#修改配置文件，指定客户端声称的名称
vim  /etc/iscsi/initiatorname.iscsi
	InitiatorName=iqn.2019-09.cn.tedu:client

#重起iscsid服务，仅仅是刷新客户端声称的名称
systemctl restart iscsid

#利用命令发现服务端共享存储
man iscsiadm	#查看iscsiadm帮助	/example按n向下匹配，按b向上匹配
iscsiadm --mode discoverydb --type sendtargets --portal 192.168.4.7 --discover

#重启iscsi服务（主服务），使用共享存储
systemctl restart iscsi
lsblk
```


## Web通信基本概念

> 基于B/S（Browser/Server）架构的网页服务
>
> 服务端提供网页
>
> 浏览器下载并显示网页

### 构建独立的web服务器

服务端

```shell
yum -y install httpd	#安装httpd软件包
echo abc > /var/www/html/index.html	#书写页面文件内容
systemctl restart httpd	#启动服务
```

客户端
```shell
curl http://192.168.4.7
```

### 提供的默认配置

> Listen：监听地址：端口80
>
> ServerName：本站点注册的DNS名称（空缺）
>
> DocumentRoot：网页根目录（/var/www/html）
>
> DirectoryIndex：起始页/首页文件名（index.html）


#### 修改http服务的默认路径
```shell
vim /etc/httpd/conf/httpd.conf	#修改监听的端口号
	/DocumentRoot
	DocumentRoot /var/www/myweb
echo abc > /var/www/myweb/index.html
systemctl restart httpd	#重启服务

#客户端测试
curl http://192.168.4.7	#成功
```

#### 修改http服务的默认端口号

```shell
vim /etc/httpd/conf/httpd.conf
	/Listen
	Listen 8080
netstate -anptu | grep httpd	#查看httpd服务的监听端口

#客户端测试
curl http://192.168.4.7	#失败
curl http://192.168.4.7:8080	#成功
```


#### 为浏览器程序提供URL网址

 `协议名://服务器地址[:端口号]/目录/文件名`

```shell
elinks -dump http://server0.example.com/
firefox http://server0.example.com/
```


### 改变网页文件存放路径

> 网络路径：浏览器中输入的路径（192.168.4.7/abc）
>
> 实际路径：服务器上网页文件存放的路径（/var/www/myweb /abc/index.html）

```shell
#服务端配置
mkdir/webapp
vim /etc/httpd/conf/httpd.conf
	DocumentRoot /webapp
echo woshiapp > /webapp/index.html
systemctl restart httpd

#客户端测试
curl http://192.168.4.7	#出现测试页面

#服务端配置
vim /etc/httpd/conf/httpd.conf
    <Directory "/webapp">	#新添加
        Require all granted	#对webapp目录设置为允许任何人访问
    <Directory>
systemctl restart httpd

#客户端测试
curl http://192.168.4.7	#出现woshiapp页面
```

### 配置文件说明
`/etc/httpd/conf/httpd.conf`	#主配置文件
`/etc/httpd/conf.d/*.conf`	#调用配置文件


### 域名解析（一台服务器使用两个域名，虚拟主机）
#### 为每个虚拟站点添加配置

```shell
vim /etc/httpd/conf.d/nsd01.conf
	<VirtualHost IP地址:端口>
		ServerName 此站点的DNS名称(www.qq.com)
		DocumentRoot 此站点的网页根目录(/var/www/qq)
	</VirtualHost>
```

#### 配置页面

服务端操作

```shell
setenforce 0
systemctl stop firewalld.services	#关闭防火墙

vim /etc/httpd/conf.d/nsd01.conf
    <VirtualHost *:80>
    	ServerName www.qq.com
    	DocumentRoot /var/www/qq
    </VirtualHost>
    <VirtualHost *:80>
    	ServerName www.baidu.com
    	DocumentRoot /var/www/baidu
    </VirtualHost>

mkdir /var/www/qq /var/www/baidu

echo "qq" > /var/www/qq/index.html
echo "baidu" > /var/www/baidu/index.html

systemctl restart httpd
```

客户端操作

```shell
vim /etc/hosts
    192.168.4.7 www.qq.com www.baidu.com

curl www.qq.com	#结果显示qq
curl www.baidu.com	#结果显示baidu
```


### 虚拟主机对web站点的影响

> 一旦启用虚拟主机之后，外部的DocumentRoot、ServerName都会被忽略
>
> 第一个虚拟站点被视为默认站点，若客户机请求的URL不属于任何已有站点，则有第一个站点响应
>
> 当独立web服务器升级为虚拟主机服务器之后，需要为原web站点建立一个虚拟站点


## NFS共享概述
Network File System，网络文件系统

> 用途：为客户机提供共享使用的文件夹
>
> 协议：NFS（TCP/UDP 2049）、RPC(TCP/UDP 111)
>
> 所需软件包：nfs-utils
>
> 系统服务：nfs-server


### exports（/etc/exports）配置文件解析

> 文件夹路径  客户端地址
>
> /test 192.168.4.0(ro)



### 实现NFS共享

服务端
```shell
rpm -q nfs-utils
yum -y install nfs-utils
mkdir /test
echo abc > /test/1.txt
vim /etc/exports
	/test 192.168.4.0(ro)

systemctl restart nfs-server
systemctl enable nfs-server
systemctl stop firewall
```

客户端

```shell
rpm -q nfs-utils
yum -y install nfs-utils
showmount -e 192.168.4.7
mkdir /abc
mount 192.168.4.7:/test /abc
df -h
ls /abc
```


### 实现开机自动挂载

> _netdev：声明网络设备，系统在网络服务配置完成后，再挂载本设备

```shell
vim /etc/fstab
192.168.4.7:/test /abc nfs defaults,_netdev 0 0
mount /abc
mount -a
df -h
```



## autofs触发挂载

由autofs提供的“按需访问”机制

> 只要访问挂载点，就会触发响应，自动挂载指定设备
>
> 闲置超过时限（默认5分钟）后，会自动卸载

```shell
yum -y install autofs
systemctl restart autofs
ls /
```

### autofs配置解析

> 主配置文件 /etc/auto.master
>
> `监控点目录` `/misc` `挂载配置文件的路径`


> 挂载配置文件，如 /etc/auto.misc
> 
> `触发点子目录` `挂载参数` `:设备名`
> 
> grep -v '^#' /etc/auto.misc
>
> `/misc /etc/auto.misc	#/misc为存放触发点的父文件夹`
> 
> `cd -fstype=iso9660,ro,nosuid,nodev :/dev/cdrom`	#cd为autofs自动建立/移除的挂载点目录名


客户端

```shell
yum -y install autofs
systemctl restart autofs
ls /	#会出现misc的目录
ls /misc/
ls -A /misc
cd /misc/aa	#失败
cd /misc/bb	#失败
cd /misc/cd	#成功
pwd
ls
df -ah
vim /etc/auto.master	#查看即可，不作任何修改
vim /etc/auto.misc	#查看即可，不作任何修改
fdisk /dev/sdb	#划分一个3G的主分区
lsblk
mkfs.xfs /dev/sdb1
blkid /dev/sdb1
ls /misc/mydev
vim /etc/suto.misc	#当触发/misc/mydev时，实现将/dev/sdb1自动挂载
	mydev -fstype=xfs :/dev/sdb1

ls /misc/mydev
df -ah
```

客户端

```shell
vim /etc/auto.master
    /haha /etc/xoxo.conf

vim /etc/xixi.conf
    abc -fstype=cfs "/dev/sdb1

systemctl restart autofs
ls /haha/abc
df -ah
```


```shell
vim /etc/auto.misc
autonfs -fstype=nfs 192.168.4.7:/public
ls /misc/autonfs
df -ah
```



### 配置DNS服务器

```shell
#服务器配置
yum -y install bind bind-chroot.x86_64
rpm -q bind bind-chroot

vim /etc/named.conf
    options {
            directory       "/var/named";
    };
    
    zone "tedu.cn" IN {
            type master;
            file "tedu.cn.zone";
    };

named-checkconf /etc/named.conf	#检查主配置文件是否存在语法问题

cp -p /var/named/named.localhost /var/named/tedu.cn.zone
vim /var/named/tedu.cn.zone
	$TTL 1D
	@       IN SOA  @ rname.invalid. (
	                                        0       ; serial
	                                        1D      ; refresh
	                                        1H      ; retry
	                                        1W      ; expire
	                                        3H )    ; minimum
	
	tedu.cn.        NS      svr7.tedu.cn.
	www.tedu.cn.    A       192.168.4.100

named-checkzone tedu.cn /var/named/tedu.cn.zone	#检查地址库文件是否存在语法问题
systemctl restart named	#重启服务

systemctl stop firewalld.service    #关闭防火墙
setenforce 0


# 客户端验证
echo "nameserver 192.168.4.7" > /etc/resolv.conf
yum -y install bind-utils
nslookup www.tedu.cn
```


#### 构建多区域的DNS（多区域DNS服务）
服务端：
```shell
#修改主配置文件，在下面新添加
vim /etc/named.conf
    options {
            directory       "/var/named";
    };
    #指定这台机器要解析的域名
    zone "tedu.cn" IN {
            type master;
            file "tedu.cn.zone";
    };
    zone "baidu.com" IN {
            type master;
            file "baidu.com.zone";
    };
    
cp -p /var/named/named.localhost /var/named/baidu.com.zone
cp -p /var/named/named.localhost /var/named/tedu.cn.zone
vim /var/named/baidu.com.zone
	$TTL 1D
	@       IN SOA  @ rname.invalid. (
	                                        0       ; serial
	                                        1D      ; refresh
	                                        1H      ; retry
	                                        1W      ; expire
	                                        3H )    ; minimum
	
	baidu.com.        NS      svr7
	svr7   A       192.168.4.7
	www    A       10.20.30.40

vim /var/named/tedu.cn.zone
	$TTL 1D
	@	IN SOA	@ rname.invalid. (
						0	; serial
						1D	; refresh
						1H	; retry
						1W	; expire
						3H )	; minimum
	tedu.cn.	NS	www.tedu.cn.
	www	A	192.168.4.7
	svr7	A	0.0.0.0

systemctl restart named	#重启服务
```

客户端操作：
```shell
yum -y install bind-utils
nslookup svr7.tedu.cn
nslookup www.baidu.com
```

#### 特殊的解析记录
基于DNS的站点负载均衡
一个域名 --> 多个不同IP地址

##### 基于解析记录的轮询（负载均衡，缓解网站服务器的压力）

服务器：
```shell
vim /var/named/baidu.com.zone
	baidu.com	NS	svr7
	svr7	A	192.168.4.7
	www	A	192.168.4.50
	www	A	192.168.4.60
	www	A	192.168.4.70
	www	A	192.168.4.80
	www	A	192.168.4.90

systemctl restart named
```


客户端：
```shell
ping www.baidu.com
ping www.baidu.com
```


##### 泛域名解析
解决用户输入错误域名时的解析结果

```shell
#服务端
vim /var/named/baidu.com.zone
	* A 10.20.30.40

systemctl restart named

#客户端测试
nslookup wwww.baidu.com
```

##### 无规律的泛域名解析（无前置域名访问）
服务端：
```shell
vim /var/named/baidu.com.zone
    ···
    baidu.com. A 50.60.70.80

systemctl restart named
```

客户端：
```shell
nslookup baidu.com
```

##### 使用内置函数生成有规律的泛域名解析

> `$GENERATE 1-100 pc$ A 192.168.10.$`

```shell
vim /var/named/baidu.com.zone
	$GENERATE 1-100 pc$ A 192.168.10.$
	#$GENERATE 要生成的整数范围 pc$ A 192.168.10.$

system restart named    #重启服务

nslookup pc1.baidu.com    #测试结果
nslookup pc2.baidu.com
nslookup pc100.baidu.com
```

##### 使用别名解析（CNAME）

```shell
vim /var/named/baidu.com.zone
	···
	tts CNAME ftp
	#别名 CNAME 要解析的域名

systemctl restart named	#重启服务
nslookup tts.baidu.com	#测试结果
```

### 主/从DNS服务器

#### 主域名服务器

特定DNS区域的官方服务器，具有唯一性

负责维护该区域内所有的“域名 <--> IP地址”记录

#### 从域名服务器

也称为`辅助域名服务器`，可以没有

其维护的“域名 <--> IP地址”记录取决于主域名服务器

#### 主/从DNS应用场景
案例环境
主DNS服务器的IP地址为 192.168.4.7/24

从DNS服务器的IP地址为192.168.4.207/24

其中任何一台都能提供对tedu.cn域的主机查询，返回相同的解析结果


#### 基本配置步骤
以区域tedu.cn为例，正常搭建好DNS服务

主服务器配置：

1. 装bind、bind-chroot软件包

2. 建立主配置文件

3. 建立区域数据文件

4. 启动named服务

5. 测试主DNS的域名解析

```shell
#主服务器配置
vim /etc/named.conf
	options {
                directory 	"/var/named";
		allow-transfer { 192.168.4.207; };
		#allow-transfer  { 从服务器的IP地址; };
	};
        zone "tedu.cn." IN {
		type master;
		file "tedu.cn.zone";
	};

cp -p /var/named/named.localhost /var/named/tedu.cn.zone
vim /var/named/tedu.cn.zone
	$TTL 1D
	@	IN SOA	@ rname.invalid. (
						0	; serial    #版本号（10位数字组成，年月日修改次数 2020010101，做数据同步使用，用于在主服务器修改地址后，同步数值只可增加不可减小）
						1D	; refresh
						1H	; retry
						1W	; expire
						3H )	; minimum    #无效记录缓存时间

	tedu.cn NS pc207
	pc207 A 192.168.4.207
	#从服务器名称（NS记录必须写在A解析记录上）

systemctl restart named	#重启服务
systemctl stop firewalld.service    #关闭防火墙
setenforce 0
```

从服务器配置：

1. 装bind、bind-chroot软件包

2. 建立主配置文件

3. 启动named服务

4. 测试主DNS的域名解析

```shell
#从服务器配置
vim /etc/named.conf
    options {
        directory	"/var/named";
    };
    
    zone "tedu.cn" IN {
      	type slave;
    	file "/var/named/slaves/tedu.cn.slave";
        masters { 192.168.4.7; };
    };

systemctl restart named	#重启服务
```

客户端测试

```shell
#客户端测试
nslookup www.tedu.cn 192.168.4.7
nslookup www.tedu.cn 192.168.4.207
vim /etc/resolv.conf
    nameserver 192.168.4.7
    nameserver 192.168.4.207

nslookup www.tedu.cn    #会首先解析到主服务器
```

### 基础邮件服务
电子邮件通信


电子邮件服务器的基本功能

> 为用户提供电子邮箱存储空间（用户名@邮件域名）
>
> 处理用户发出的邮件 -- 传递给收件服务器
>
> 处理用户收到的邮件 -- 投递到邮箱 


#### 配置邮件服务器的DNS

服务器端（svr7）构建DNS服务器

```shell
yum -y install bind bind-chroot
vim /etc/named.conf 
	options {
		directory 	"/var/named";
	};
	zone "example.com." IN {
		type master;
		file "example.com.zone";
	};

cp -p /var/named/named/named.localhost /var/named/example.com.zone
vim /var/named/example.com.zone
	$TTL 1D
	@	IN SOA	@ rname.invalid. (
						0	; serial
						1D	; refresh
						1H	; retry
						1W	; expire
						3H )	; minimum
	example.com.	NS	svr7
	example.com.	MX	10 mail    #MX邮件交互记录，10为第几台邮件服务器，数字越小优先级越高；mail：邮件服务器
	svr7	A	192.168.4.7
	mail	A	192.168.4.207

systemctl restart named
```

客户端（pc207）主机验证邮件交换记录

```shell
echo "nameserver 192.168.4.7" > /etc/resolv.conf	
yum -y install bind-utils
host -t MX example.com	#查看在example.com域中邮件服务器是谁
host mail.example.com	#查看邮件服务器解析
```


#### 构建邮件服务器

##### 邮件服务搭建

```shell
rpm -q postfix
vim /etc/postfix/main.cf
	#99行 - 去除注释
	myorigin = example.com	#默认补全的域名后缀

	#116行
	inet_interfaces = all	#修改默认监听端口为所有网卡都提供邮件功能

	#164 行
	mydestination = example.com	#判断为本域邮件的依据

systemctl restart postfix	#重启服务

#测试
useradd fajianren	#发件用户
useradd shoujianren	#收件用户
yum -y install mailx	#安装邮件收发包
```

##### 交互式mail命令

语法格式：

> mail -s '邮件标题' -r 发件人 收件人
>
> 邮件内容
>
> .	#结束邮件

```shell
mail -s "test01" -r fajianren shoujianren
	邮件内容
	.	#结束邮件

mail -u xln	#查看邮件
	1
	q
```

##### 非交互式mail命令

语法格式：

> echo "邮件内容" | mail -s '邮件标题' -r 发件人 收件人

```shell
echo abc | mail -s 'mail title' -r fajianren shoujianren	#使用非交互式命令发送邮件
mail -u shoujianren	#检查邮件
```


### 分离解析概述

#### 分离解析：

当收到客户机的DNS查询请求的时候


> 能够区分客户机的来源地址
>
> 为不同类别的客户机提供不向的解析结果（IP地址）



典型适用场景：

> 访问压力大的网站，购买CDN提供的内容分发服务
>
> 在全国各地/不同网终内部署大量镜像服务节点
>
> 针对不同的客户机就近提供服务器


#### BIND的view视图

匹配原则：由上到下

> 根据源地址集合将客户机分类
>
> 不同客户机获得不同结果(待遇有差别)

```shell
view "联通" {
	match-clients { 来源地址1; ...; }:
	zone "12306.cn" IN 
		...地址库1;
	};  };
view "铁通" {
	match-clients { 来源地址2; ...; };
	zone "12306.cn" IN {
		...地址库2;
	}; };
```


#### 分离解析实例

服务端（svr）7操作:

```shell
vim /etc/named.conf
	options {
		directory /var/named";
	}；
	view "VIP" {
		match-clients { 192.168,4.207; };
		zone "tedu.en" IN {
			type master
			file "tedu.cn.zone";
		};
	};
	view "other" {
		match-clients { any; };
		zone "tedu.cn" IN {
			type master;
			file "tedu.cn.other;
		};
	};

cp -p /var/named/named.localhost /var/named/tedu.cn.zone
vim /var/named/tedu.cn.zone
	$TTL 1D
	@	IN SOA	@ rname.invalid. (
						0	; serial
						1D	; refresh
						1H	; retry
						1W	; expire
						3H )	; minimum

	tedu.cn.	NS	svr7
	svr7	А	192.168.4.7
	www	A	192.168.4.100

cp -p /var/named/tedu.cn.zone /var/named/tedu.cn.other
vim /var/named/tedu.cn.other
	$TTL 1D
	@	IN SOA	@ rname.invalid. (
						0	; serial
						1D	; refresh
						1H	; retry
						1W	; expire
						3H )	; minimum

	tedu.cn.	NS	svr7
	svr7	А	192.168.4.7
	www	A	1.2.3.4

systemcti restart named
```

分别用pc207和虚拟机A验证

```shell
nslookup www.tedu.cn
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


### 案例10：设置基本权限

0. 新建/nsddir1/目录，在此目录下新建readme.txt文件，并进一步完成下列操作：

    ```shell
    mkdir /nsddir1/
    touch /nsddir1/readme.txt
    ```

1. 使用户zhangsan能够在此目录下创建/删除子目录

    ```shell
    useradd zhangsan
    setfacl -m u:zhangsan:rwx /nsddir1/
    ```

2. 使用户zhangsan能够修改readme.txt文件

    ```shell
    setfacl -m u:zhangsan:rw /nsddir1/readme.txt
    vim /nsddir1/readme.txt
    ```

3. 调整此目录的权限，使任何用户都不能进入，然后测试用户zhangsan是否还能修改readme.txt

    ```shell
    chmod -r /nsddir1/
    ls -ld /nsddr1/readme.txt
    vim /nsddr1/readme.txt
    ```

4. 为此目录及其下所有文档设置权限 rwxr-x---

    ```shell
    chmod -R 760 /nsddir1/
    ls -ld /nsddr1/readme.txt
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
	
	​```shell
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


## 练习 4.12
### 权限简答
1. 权限的分类是什么？

> 基本权限、附加权限、ACL权限

2. 基本权限的分类是什么？

> 读取r、写入w、可执行x

3. 归属关系都有哪些？

> 所有者、所属组、其他用户

4. 用户的分类？组账号的分类？

>用户分类：普通用户、系统用户、超级用户
>
>组账号分类：基本组，附加组

5. 唯一标识用户身份的是什么？

>UID

6. 保存用户信息的配置文件是？里面的字段值都是什么意思？

>/etc/passwd
>
> 用户名 : 密码占位符 : UID : GID(基本组) : 用户描述 : 用户家目录(宿主目录) : 用户所使用的shell解释器程序

7. 保存组账号基本信息的配置文件是？里面的字段值是什么意思？

>/etc/group
>
> 组账号名称 : 密码占位符x : 组的GID号 : 本组的成员用户列表

8. 保存组账号管理信息的配置文件是？里面的字段值是什么意思？

> /etc/gshadow
>
> 组账号名称 : 加密后的密码字符串 : 组的管理员列表 : 组成员列表


9. 如何创建用户？如何修改用户的属性？分别说出下列选项意思-d  -G  -s   -u

> Useradd
>
> usermod
>
> -d：指定要创建用户的家目录，不使用则默认用户的家目录为 /home/创建的用户名
>
> -G：指定用户的附加组（从属组）
>
> -s：指定用户的shell解释器
>
> -u：指定 UID


10. 如何修改权限？如何修改归属关系？

> chmod [ugoa][+-=], ... 要设置权限的文件夹
>
> chown 属主[:属组] 文件



11. 文件/目录默认的权限是？

> 644/755
>
> 取决于umask设置

12. 用户的初始配置文件来自于哪个模板目录

> /etc/skel


13. 如何创建组？如何删除组？如何往组里添加成员？如何删除组成员？

> groupadd [-g GID组ID] 组名
>
> groupdel 要删除的组名
>
> gpasswd -a 要添加的用户 组名
>
> gpasswd -d 要删除的用户 组名



### 案例1：创建用户和组

1. 一个名为tarena的组

    ```shell
    groupadd tarena
    grep tarena /etc/group
    ```

2. 一个名为natasha的用户，其属于tarena组，这个组是该用户的从属组

    ```shell
    useradd -G tarena natasha
    id natasha
    ```

3. 一个名为harry的用户，其属于tarena组，这个组是该用户的从属组

    ```shell
    useradd -G tarena harry
    id harry
    ```


4. 一个名为sarah的用户，其在系统中没有可交互的shell，并且不是tarena这个组的成员用户

    ```shell
    useradd -s /sbin/nologin sarah
    grep sarah /etc/passwd
    ```


5. 为natasga、harry、sarah设置密码为redhat

    ```shell
    echo redhat | passwd --stdin nataha
    echo redhat | passwd --stdin harry
    echo redhat | passwd --stdin sarah
    ```


### 案例2：配置文件/var/tmp/fstab的权限

0. 拷贝文件/etc/fstab到/var/tmp/fstab，配置文/var/tmp/fstab的权限

    ```shell
    cp /etc/fstab /var/tmp/fstab
    ```

1. 文件/var/tmp/fstab的拥有着是root用户
2. 文件/var/tmp/fstab属于root组

    ```shell
    chown root:root /var/tmp/fstab 
    ls -ld /var/tmp/fstab 
    ```

3. 文件/var/tmp/fstab对任何人都不可执行

    ```shell
    chmod -x /var/tmp/fstab
    ls -l /var/tmp/fstab
    ```

4. 用户natasha能够对文件/var/tmp/fstab执行读和写操作

    ```shell    
    setfacl -m u:natasha:rw /var/tmp/fstab
    setfacl /var/tmp/fstab
    ```

5. 用户harry对文件/var/tmp/fstab既不能读，也不能写

    ```shell
    setfacl -m u:harry:- /var/tmp/fstab
    getfacl /var/tmp/fstab
    ```

6. 所有其他用户（当前的和将来的）能够对文件/var/tmp/fstab进行读操作

    ```shell
    ls -l /var/tmp/fstab
    ```



## 4.14练习
划分3个2G的主分区，一个扩展分区，3个2G的逻辑分区
1. 利用sdb硬盘划分2个1G的逻辑分区

    ```shell
    lsblk
    fdisk /dev/sdb
    n
    p
    
    +2G
    n
    p
    
    +2G
    n
    p
    
    +2G
    n
    e
    
    
    n
    
    +2G
    n
    
    +2G
    n
    
    +2G
    ```

2. 将/dev/sdb3格式化成ext3的文件系统类型，第一个逻辑分区格式化为xfs的文件系统类型，第3个逻辑分区格式化为ext4的文件系统类型

    ```shell
    mkfs.xfs /dev/sdb5
    blkid /dev/sdb5
    ```


3. 分别查看几个分区的文件类型

    ```shell
    blkid /dev/sdb1
    blkid /dev/sdb2
    blkid /dev/sdb3
    blkid /dev/sdb4
    blkid /dev/sdb5
    blkid /dev/sdb6
    blkid /dev/sdb7
    ```

4. 将/dev/sdb3挂在到/mypt1文件夹下，第3个逻辑分区挂载到/mypt2

    ```shell
    mount /dev/sdb3 /mytp1
    df -h /mypt1
    
    mkfs.xfs /dev/sdb7
    mkdir /mypt2
    mount /dev/sdb7 /mypt2
    df -h /mypt2
    ```

> 刷新分区表

    ```shell
    partprobe /dev/sdb	#刷新分区表 或者reboot
    ```


## 练习4.15

### 案例：硬盘分区练习
添加一块10G硬盘，采用msdos（MBR）分区模式，完成如下操作
1. 划分2个2G的主分区，一个1G的主分区，2个1G的逻辑分区

    ```shell
    lsblk
    fdisk /dev/sdb
        n
        p
        1
        
        +2G
        n
        p
        2
        
        +2G
        n
        p
        3
        
        +1G
        n
        e
        
        
        n
        
        +2G
        n
        
        +2G
        p
        w
    ```


2. 将/dev/sdb3格式化为ext4的文件系统类型。将第2个逻辑分区格式化为xfs的文件系统类型

    ```shell
    mkfs.ext4 /dev/sdb3
    blkid /dev/sdb3
    
    mkfs.xfs /dev/sdb6
    blkid /dev/sdb6
    ```

3. 实现开机自动挂/dev/sdb3，挂载到/mydb1目录

    ```shell
    vim /etc/fstab
        /dev/sdb3 /mydb1 ext4 defaults 0 0
    mount -a	#检测文件语法、自动挂载
    mkdir /mydb1
    df -h
    ```


### 练习：新建一个逻辑卷
使用/dev/sdb3构建LVM存储
1. 新建一个名为systemvg的卷组

    ```shell
    vgcreate systemvg /dev/sdc{3,5}
    ```

2. 在此卷组中创建名为vo的逻辑卷，大小为180M

    ```shell
    lvcreate -L 180M -n vo systemvg 
    ```

3. 将逻辑卷vo格式化为xfs的文件系统类型

    ```shell
    mkfs.xfs /dev/systemvg/vo
    ```

4. 将逻辑卷vo挂载到/myvo目录，并在此目录下建立一个测试文件votest.txt，内容为“I AM KING”

    ```shell
    mkdir /myvo
    mount /dev/systemvg/vo /myvo
    vim /myvo/votest.txt
        "I AM KING"
    cat /myvo/votest.txt
    ```

5. 将逻辑卷实现自动开机自动挂载到/myvo目录

    ```shell
    vim /etc/fstab 
        /dev/systemvg/vo /myvo xfs defaults 0 0
    umount /myvo
    mount -a
    ```


### 4.16 案例：LVM逻辑卷练习

1. 添加一块80G硬盘，划分三个10G的主分区，2个10G的逻辑分区
   
    ```shell
    lsblk
    fdisk /dev/sdb
    vgcreate system /dev/sdc{3,5}    
    lsblk
    ```

2. 利用/dev/sdb1和/dev/sdb2创建一个名为systemvg的卷组

    ```shell
    vgcreate systemvg /dev/sdb[1-2]
    ```

3. 在此卷组中创建一个名为vo的逻辑卷，大小是16G

    ```shell
    lvcreate -L 16G -n vo systemvg1
    ```

4. 将此逻辑卷格式化为xfs文件系统类型

    ```shell
    mkfs.xfs /dev/systemvg/vo
    blkid /dev/systemvg/vo
    ```

5. 将该逻辑卷挂载到根下的vo文件夹下，并写入测试文件为test.txt，内容为"I AM KING."

    ```shell
    mkdir /vo
    mount /dev/systemvg/vo /vo

    vim /vo/test.txt
        I AM KING.
    echo "I AM KING." > /vo/test.txt

    cat /vo/test.txt 
    ```

6. 将此逻辑卷实现开机自动化挂载

    ```shell
    vim /etc/fstab 
        /dev/systemvg/vo /vo xfs defaults 0 0
    
    umount /vo
    mount -a
    lsblk
    ```

## 练习4.19
### 案例1：MBR分区模式规划分区
0. 添加一块80G的硬盘并规划分区
1. 划分2个10G的主分区；1个12G的主分区；2个10G的逻辑分区。

    ```shell
    fdisk /dev/sdb
        n
        p
        1
        
        +10G
        
        n
        p
        2
        
        +10G
        n
        p
        3
        
        +10G
        n
        e
        
        
        n
        e
        
        +10G
        n
        e
        
        +10G
    ```

### 案例2：构建LVM存储
1. 利用/dev/sdb1和/dev/sdb2新建一个名为systemvg的卷组

    ```shell
    vgcreate systemvg /dev/sdb1 /dev/sdb2
    vgs
    ```

2. 在此卷组中创建一个名为vo的逻辑卷，大小为10G

    ```shell
    lvcreate -L 10G -n vo systemvg
    ```

3. 将逻辑卷vo格式化为xfs文件系统

    ```shell
    mkfs.xfs /dev/systemvg/vo 
    blkid /dev/systemvg/vo
    ```

4. 将逻辑卷vo挂载到/vo目录，并在此目录下建立一个测试文件votest.txt，内容为“I AM KING”

    ```shell
    mkdir /vo
    mount /dev/systemvg/vo /vo
    echo "I AM KING" > /vo/votest.txt
    cat /vo/votest.txt
    ```

5. 实现逻辑卷vo开机自动挂载到/vo

    ```shell
    vim /etc/fstab
        /dev/systemvg/vo /vo xfs defaults 0 0
    umount /vo
    df -h
    mount -a
    df -h /vo
    ```

### 案例3：构建lvm存储（修改PE大小）
1. 新的逻辑卷命名为dateabase，其大小为50个PE的大小，属于datastore卷组

    ```shell
    vgcreate database /dev/sdb3
    vgs
    lvcreate -l 50 -n database datastore
    ```


2. 使用EXT4文件系统对逻辑卷database格式化，此逻辑卷应该在开机时自动挂载到/nsd/vo

    ```shell
    mkfs.ext4 /dev/database/datastore
    vim /etc/fstab
        /dev/database/datastore /nsd/vo ext4 defaults 0 0
    
    mkdir -p /nsd/vo
    mount -a
    df -h
    ```


### 案例4:扩展逻辑卷
1. 将/dev/systemvg/vo逻辑卷的大小扩展到30G

    ```shell
    vgs
    lvs
    
    vgextend systemvg /dev/sdb5 /dev/sdb6
    vgs
    lvextend -L 30G /dev/systemvg/vo
    
    df -h
    xfs_growfs /dev/systemvg/vo
    df -h /vo
    ```

## 远程管理ssh

### SSH协议（Secure Shell）

> 为客户机提供安全的 Shell 环境
>
> 默认端口：**TCP22**


### OpenSSH 服务

> 服务名称：sshd
>
> 主程序：/use/sbin/sshd、/usr/bin/ssh
>
> 配置主件：/etc/ssh/sshd_config
>
> 	/etc/ssh/ssh_config

### SSH的基本使用

```shell
ssh root@要远程主机的ip地址	#远程指定的主机

ssh root@要使用图形界面远程主机的ip地址	#使用图形界面远程指定的主机
firefox	#测试图形界面状态下
```


### 使用scp远程复制工具
#### 安全复制工具scp

```shell
scp -r 用户名@服务器:远程路径 本地路径	#将指定主机上的文件下载到本地
scp -r 本地路径 用户名@服务器:远程路径	#将本地的文件上上传至指定主机
```

```shell
scp -r root@192.168.4.207:/boot /opt/	#将远程主机.207的目录boot复制到本地opt目录下
scp -r /boot root@192.168.4.207:/opt/	#将本机的boot目录复制到远程主机.207主机的opt目录下
```

### 实现ssh无密码验证
部署公钥与私钥
生成公钥与私钥

```shell
ssh-keygen
（使用默认ssh路径）
（实现ssh无密码验证，不需要设置密码）
（确认密码）
ls /root/.ssh
cat /root/.ssh/known_hosts

ssh-copy-id root@要传输公钥目标主机（无密码登陆）的ip地址
ssh root@无密码登陆目标主机的ip地址
```

传递公钥到对方主机




## 练习 4.25

### 案例：使用ssh客户端
准备虚拟机A和虚拟机B，完成以下操作
1. 从主机A(192.168.4.7)上以root身份登入主机B(192.168.4.207)

```shell
ssh root@192.168.4.207
```

2. 在主机B上创建用户student，设置密码为redhat

```shell
useradd student
echo redhat | passwd --stdin student
```

3. 从主机A上以用户student登入主机B

```shell
ssh student@192.168.4.207
```

### 案例：使用scp远程复制工具
1. 在主机A上使用scp下载文档
a. 将主机B上的/root/anaconda-ks.cfg文件复制到/opt下

```shell
scp -r root@192.168.4.207:/root/anaconda-ks.cfg /opt/
ls /opt/
```

b. 将主机B上的/home目录复制到本地的/opt下

```shell
scp -r root@192.168.4.207:/home /opt
ls /home
```

2. 在主机A上使用scp上传文档
a. 确保主机B上有本地用户lisi

```shell
id lisi
```

b. 将本地的/root/anaconda-ks.cfg文件复制到主机B上用户lisi的家目录下，以用户lisi的密码验证

```shell
scp -r /root/anaconda-ks.cfg lisi@192.168.4.207:/home/lisi
su lisi
ls
```

## 4.26 练习
### 案例
1. 利用ip命令查看ip地址

    ```shell
    ip address show
    ```

2. 利用ip命令为本机第一张网卡添加ip地址192.168.100.10/24

    ```shell
    ip address add 192.168.100.10/24 dev ens33
    ```

3. 利用ip命令添加路由，去往200.0.0.0/24下一跳为192.168.100.10

    ```shell
    ip route add 200.0.0.0/24 via 192.168.100.10 dev ens33
    ```

4. 安装vsftpd软件包

    ```shell
    yum -y install vsftpd
    ```

5. 启动vsftpd服务（systemctl restart vsftpd）

    ```shell
    systemctl restart vsftpd
    ```
    
6. 查看vsftpd服务监听的端口号

    ```shell
    netstat -anptu | grep vsftpd
    ```


## 4.27 练习
### 实验环境准备
虚拟机A
1. 主机名配置为A.tedu.cn

    ```shell
    hostname A.tedu.cn
    echo A.tedu.cn > /etc/hostname
    ```

2. IP地址配置为192.168.4.10/24

    ```shell
    nmcli connection modify ens33 ipv4.method manual ipv4.addresses 192.168.4.10/24 connection.autoconnect yes
    nmcli connection up ens33 
    ```

3. 用真机Xshell远程到虚拟机A

    ```shell
    ssh root@192.168.4.10
    ```

4. 将tools.tar.gz包传输到虚拟机A

    ```shell
    tar xf /root/tools.tar.gz /
    ```

5. 将tools.tar.gz解压到/tools文件夹下

    ```shell
    mkdir /tools/
    tar xf /root/tools.tar.gz /tools/
    ```

6. 源码编译安装inotify-tools-3.13.tar.gz，安装位置为/opt/abc

    ```shell
    ./configure --prefix=/opt/abc
    vim /etc/yum.repos.d/mnt.repo
        [mnt]
        name=Centos7.5
        baseurl=file:///dvd
        enabled=1
        gpgcheck=0
        [mymnt]
        name=Centos7.5
        baseurl=file:///tools/tools/other
        enabled=1
        gpgcheck=0
    
    rm -rf /etc/yum.repos.d/C*
    yum clean all
    yum repolist
    
    createrepo /tools/tools/other/
    yum -y install gcc
    yum -y install make
    
    rpm -q gcc make	#检查安装情况
    
    tar -xf /tools/tools/inotify-tools-3.13.tar.gz -C /opt
    
    cd /opt/inotify-tools-3.13/
    
    make
    make install
    
    ls /opt/abc/
    ```
## 4.28 练习
### 案例

1. 在svr7安装web服务和ftp服务

    ```shell
    #前提：安装yum源
    yum -y install httpd
    systemctl start httpd
    
    yum -y install vsftpd
    systemctl start vsftpd
    ```

2. 修改防火墙默认区域，在pc207上验证

    ```shell
    firewall-cmd --set-default-zone=trusted
    
    curl http://192.168.4.7	#使用另一台主机进行验证
    curl ftp://192.168.4.7
    ```

## 4.29 练习
### 将虚拟机A，svr7，pc207开机，网络模式选为vmnet1
1. 将虚拟机A主机名设置为A.tedu.cn

    ```shell
    hostname A.tedu.cn
    echo A.tedu.cn > /etc/hostname
    ```

2. 将虚拟机A IP地址设置为192.168.4.10
   
    ```shell
    nmcli connection modify ens33 ipv4.method manual ipv4.addresses 192.168.4.10/24 connection.autoconnect yes 
    nmcli connection up ens33 
    ```

3. 在虚拟机A上构建web服务和ftp服务

    ```shell
    mount /dev/cdrom /mnt
    
    vim /etc/yum.repos.d/a.repo
        [mnt]
        name=Centos
        baseurl=file:///mnt
        gpgcheck=0
        enabled=1
        
    rm -rf /etc/yum.repos.d/C*
    yum clean all
    yum repolist 
    
    yum repolist 
    yum -y install httpd
    yum -y install vsftpd
    systemctl start vsftpd
    systemctl start httpd
    
    curl http://192.168.4.10
    curl ftp://192.168.4.10
    ```

4. 用真机xshell远程到虚拟机A，svr7，pc207

    ```shell
    ssh root@192.168.4.10
    ```

5. 关闭虚拟机A，svr7，pc207的selinux

    ```shell
    vim /etc/selinux/config 
        SELINUX=disabled
    ```

### 案例1：新建一台虚拟机，要求如下：
1. 硬盘80G，内存2G
2. 采取自动分区规划
3. 软件选择“最小安装”

### 案例2（重复）： 配置网络参数，要求如下：
1. 永久设置主机名为 A.tedu.cn

    ```shell
    echo A.tedu.cn > /etc/hostname
    hostname A.tedu.cn
    
    hostname
    ```

2. 永久配置静态IP地址为192.168.4.20/24

    ```shell
    #安装yum源
    mount /dev/cdrom /mnt/	#先连接光盘
    vi /etc/fstab
    	/dev/cdrom /mnt iso9660 defaults 0 0
    
    vi /etc/yum.repos.d/mnt.repo
    	[mnt]
    	name=Centos7.5
    	baseurl=file:///mnt
    	enable=1
    	gpgcheck=0
    
    rm -rf /etc/yum.repos.d/CentOS-*
    yum clean all
    yum repolist
    
    yum -y install vim-enhanced	#安装vim包
    yum -y install net-tools	#安装ifconfig支持包
    yum -y install bash-completion	#安装Tab键支持包
    poweroff	#重启以生效
    #调整网络适配器，开机
    
    nmcli connection modify ens33 ipv4.addresses 192.168.4.20/24 connection.autoconnect yes
    nmcli connection up ens33
    ```

3. 用真机XShell远程到虚拟机B

    ```shell
    ssh root@192.168.4.20
    ```

### 案例3：练习克隆
1. 将A机器进行克隆
2. 克隆后的机器配置要求如下：
   a. 永久设置主机名为 B.tedu.cn

    ```shell
    echo B.tedu.cn > /etc/hostname
    hostname B.tedu.cn
    
    hostname
    ```

b. 永久配置静态IP地址为192.168.4.30/24

    ```shell
    nmcli connection modify ens33 ipv4.addresses 192.168.4.30/24 connection.autoconnect yes
    nmcli connection up ens33
    ```

### 案例4（重复）：复制，拷贝，移动要求如下：
1. 新建目录结构/student/test/nsd

    ```shell
    mkdir -p /student/test/nsd
    ```

2. 在目录/student/test/nsd创建文件testa.txt并写入内容 NSD  Student


    ```shell
    echo "NSD  Student" > /student/test/nsd/testa.txt
    ```

3. 将/student/test/nsd/testa.txt文件复制到/root目录下，同时改名为 tedu.txt

    ```shell
    cp /student/test/nsd/testa.txt /root/tedu.txt
    ```

4. 将/etc/passwd 、/etc/resolv.conf、/etc/hosts 同时拷贝到/student/test/nsd目录下

    ```shell
    cp /etc/passwd /etc/resolv.conf /etc/hosts /student/test/nsd
    ```

5. 将文件 student/test/nsd 重改名为 hs.txt

    ```shell
    mv student/test/nsd student/test/hs.txt
    ```

### 案例5（重复）:查找并处理文件
1. 创建目录/root/findfiles/

    ```shell
    mkdir /root/findfiles/
    ```

2. 利用find查找所有用户 lisi 拥有的必须是文件,把它们拷贝到 /root/findfiles/ 文件夹中

    ```shell
    useradd lisi
    mkdir /root/findfiles/
    find / -user lisi -a -type f -exec cp {} /root/findfiles/ \;
    ```

3. 利用find查找/boot目录下大于10M并且必须是文件，拷贝到/opt

    ```shell
    find /boot -size +10M -type f -exec cp {} /opt \;
    ```

4. 利用find查找/boot/ 目录下以 vm 开头且必须是文件，拷贝到/opt

    ```shell
    find /boot -name "vm*" -type f -exec cp {} /opt \;
    ```

5. 利用find查找/etc 目录下，以 tab 作为结尾的 必须是文件

    ```shell
    find /etc -name "*tab" -type f -exec cp {} /opt \;
    ```

### 案例6（重复）:查找并提取文件内容
1. 在文件 /usr/share/dict/words 中查找到所有包含字符串 seismic 的行,将输出信息,写入到/opt/nsd18.txt

    ```shell
    grep seismic /usr/share/dict/words > /opt/nsd18.txt
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
    grep ‘bash$’ /etc/passwd  > /opt/pass.txt
    ```

7. 复制/etc/login.defs文件到当前目录下，改名为init.txt

    ```shell
    cp /etc/login.defs ./init.txt
    ```
    
8. 提取init.txt文件里的有效配置（去除以#号开头，去除空行），保存为init2.txt

    ```shell
    grep -v '^#' init.txt | grep -v '^$' > init2.txt
    ```

    

### 案例7（重复）: MBR分区模式规划分区
1. 添加一块80G的硬盘并规划分区：
2. 划分2个10G的主分区；1个12G的主分区;2个10G的逻辑分区。

    ```shell
    fdisk /dev/sdb
        n
        p
        1
        
        +10G
        
        n
        p
        2
        
        +10G
        n
        p
        3
        
        +10G
        n
        e
        
        
        n
        e
        
        +10G
        n
        e
        
        +10G
    ```
### 案例8（重复）:构建 LVM 存储
1. 利用/dev/sdb1和/dev/sdb2 新建一个名为 systemvg 的卷组 

    ```shell
    vgcreate systemvg /dev/sdb1 /dev/sdb2
    vgs
    ```

2. 在此卷组中创建一个名为 vo 的逻辑卷，大小为10G 

    ```shell
    lvcreate -L 10G -n vo systemvg
    ```

3. 将逻辑卷 vo 格式化为 xfs 文件系统 

    ```shell
    mkfs.xfs /dev/systemvg/vo 
    blkid /dev/systemvg/vo
    ```

4. 将逻辑卷 vo 挂载到 /vo 目录，并在此目录下建立一个测试文件 votest.txt，内容为“I AM KING.” 

    ```shell
    mkdir /vo
    mount /dev/systemvg/vo /vo
    echo "I AM KING" > /vo/votest.txt
    cat /vo/votest.txt
    ```

5. 实现逻辑卷vo开机自动挂载到/vo

    ```shell
    vim /etc/fstab
        /dev/systemvg/vo /vo xfs defaults 0 0
    umount /vo
    df -h
    mount -a
    df -h /vo
    ```




### 案例9（重复）:构建 LVM 存储(修改PE大小)
1. 新的逻辑卷命名为 database，其大小为50个PE的大小，属于 datastore 卷组 

    ```shell
    vgcreate database /dev/sdb3
    vgs
    lvcreate -l 50 -n database datastore
    ```

2. 使用 EXT4 文件系统对逻辑卷 database 格式化，此逻辑卷应该在开机时自动挂载到/nsd/vo

    ```shell
    mkfs.ext4 /dev/database/datastore
    vim /etc/fstab
        /dev/database/datastore /nsd/vo ext4 defaults 0 0
    
    mkdir -p /nsd/vo
    mount -a
    df -h
    ```


### 案例10（重复）:扩展逻辑卷
1. 将/dev/systemvg/vo逻辑卷的大小扩展到30G

    ```shell
    vgs
    lvs
    
    vgextend systemvg /dev/sdb5 /dev/sdb6
    vgs
    lvextend -L 30G /dev/systemvg/vo
    
    df -h
    xfs_growfs /dev/systemvg/vo
    df -h /vo
    ```



### 案例11（重复）：创建用户
1. 创建一个名为alex的用户，用户ID是 3456。密码是flectrag

    ```shell
    useradd -u 3456 alex
    grep alex /etc/passwd
    echo flectrag | passwd --stdin alex
    id alex
    ```

### 案例12（重复）：创建用户和组
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

### 案例13（重复）：配置文件 /var/tmp/fstab 的权限
1.  拷贝文件/etc/fstab到/var/tmp/fstab，配置文件/var/tmp/fstab的权限：

    ```shell
    cp /etc/fstab /var/tmp/fstab
    ```

2. 文件/var/tmp/fstab的拥有者是root用户
3. 文件/var/tmp/fstab属于root组

    ```shell
    chown root:root /var/tmp/fstab
    ls -ld /var/tmp/fstab 
    ```

4. 文件/var/tmp/fstab对任何人都不可执行
   
    ```shell
    chmod -x /var/tmp/fstab
    ls -l /var/tmp/fstab
    ```

5. 用户natasha 能够对文件/var/tmp/fstab执行读和写操作

    ```shell
    setfacl -m u:natasha:rw /var/tmp/fstab
    setfacl /var/tmp/fstab
    ```
    
6. 用户harry 对文件/var/tmp/fstab既不能读，也不能写

    ```shell
    setfacl -m u:harry:- /var/tmp/fstab
    getfacl /var/tmp/fstab
    ```

7. 所有其他用户（当前的和将来的）能够对文件/var/tmp/fstab进行读操作

    ```shell
    ls -l /var/tmp/fstab
    ```


### 案例14（重复）：创建一个归档
1. 创建一个名为 /root/backup.tar.bz2 的归档文件，其中包含 /usr/local 目录中的内容，tar 归档必须使用 bzip2 进行压缩

    ```shell
    tar -jcf /root/backup.tar.bz2 /usr/local/
    ```

### 案例15（重复）：配置一个cron任务
1. 为用户 natasha 配置一个定时任务

    ```shell
    su natasha
    crontab -e
    
    crontab -e -u natasha
    ```

2. 每天在本地时间 14:23 执行
3. 需要完成的任务操作为 /bin/echo  hiya

    ```shell
    23 14 * * * /bin/echo hiya
    ```


### 案例16（重复）：设置别名
1. 为root用户永久设置别名为hn=‘hostname’

    ```shell
    su root
    vim ~/.bashrc
    	alias hn='hostname'
    ```

2. 为所有用户设置别名为 qstat='/bin/ps -Ao pid,tt,user,fname,rsz' 
   
    ```shell
    vim /etc/bashrc
    	qstat='/bin/ps -Ao pid,tt,user,fname,rsz'
    ```

### 案例17：实现虚拟机B的Web服务
1. 利用httpd软件搭建Web服务，页面显示内容为 I LIKE  LINUX.

    ```shell
    yum -y install httpd
    systemctl start httpd
    
    firefox http://192.168.4.10
    
    vim /var/www/html/index.html	#打开默认存放网页文件的路径进行编辑
    	I LIKE  LINUX.
    
    yum -y install elinks	#命令行浏览器
    
    elinks --dump http://192.168.4.10
    curl http://192.168.4.10	#命令行浏览器
    ```

### 案例18：实现虚拟机A的防火墙配置
1. 修改虚拟机A防火墙配置，明确拒绝所有客户端访问(默认区域修改为block)

    ```shell
    firewall-cmd --set-default-zone=block	#修改防火墙默认区域为block
    ```

2. 在虚拟机B上测试能否访问A的Web服务

    ```shell
    curl http://192.168.4.10	#不可以访问
    ```

3. 在虚拟机 B上测试能否 ping通 虚拟机A

    ```shell
    ping 192.168.4.10	#不可以访问
    ```


### 案例19：实现虚拟机A 的防火墙配置
1. 修改虚拟机A防火墙配置，将默认区域修改为trusted

    ```shell
    firewall-cmd --set-default-zone=trusted	#修改防火墙默认区域为trusted
    ```

2. 在虚拟机B上测试能否访问A的Web服务

    ```shell
    curl http://192.168.4.10	#可以访问
    ```

3. 在虚拟机B上测试能否 ping通 虚拟机 A

    ```shell
    ping 192.168.4.10	#可以访问
    ```


### 案例20：实现虚拟机A的防火墙配置
1. 修改虚拟机A防火墙配置，将默认区域修改为public

    ```shell
    firewall-cmd  --set-default-zone=public
    ```

2. 修改虚拟机A防火墙配置，在public区域中添加http协议,实现永久配置

    ```shell
    firewall-cmd --permanent --zone=public --add-service=http	#永久启动http服务
    firewall-cmd --reload    #重新加载配置文件
    firewall-cmd --permanent --zone=public --list-all    #查看区域策略
    
    netatat -anptu | grep :80    #过滤80端口
    systemcli status httpd    #查看http服务状态
    systemcli enable httpd    #设置http服务开机自启
    ```

3. 在虚拟机B上测试能否访问A 的Web服务

    ```shell
    curl ftp://192.168.4.10    #使用B主机检测，可以访问
    curl http://192.168.4.10    #使用B主机检测，可以访问
    ```

## 5.7 练习
服务端是svr7，客户端为pc207,完成以下案例

### 案例1：构建网络yum

利用ftp服务实现yum源提供服务
1. svr7构建vsftpd服务

    ```shell
    setenforce 0	#SELinux运行模式切换 0宽松 1强制
	/etc/selinux/config	#永久配置
    getenforce	#查看
    ststemctl stop firewall

    mount /dev/cdrom /mnt
    vim /etc/yum.repos.d/mnt.repo
    	[mnt]
    	name=Centos7.5
    	baseurl=file:///mnt
    	gpgcheck=0
    	enabled=1
    rm -rf /etc/yum.repos.d/C*
    yum clean all
    yum repolist
    
    yum -y install vsftpd
    systemctl start vsftpd
    systemctl status vsftpd #查看服务运行状态
    
    firewall-cmd --set-default-zone=trusted 
    
    curl ftp://192.168.4.7
    ```

2. 利用vsftpd服务提供如下内容：
a. Centos7光盘内容

    ```shell
    mkdir /var/ftp/dvd
    mount /dev/cdrom /var/ftp/dvd
    ```

b. 自定义yum仓库内容

    ```shell
    vim /etc/yum.repos.d/dvd.repo
    	[dvd]
    	name=CentOS7.5
    	baseurl=ftp://192.168.4.7/dvd
    	enabled=1
    	gpgcheck=0
    
    yum clean all
    yum repolist
    ```

### 案例2：高级远程管理

1. 实现svr7远程管理pc207，无密码验证

    ```shell
    ssh root@192.168.4.207
    ssh-keygen
    ssh-copy-id root@192.168.4.207
    
    ssh root@192.168.4.207
    ```

2. 将svr7的/home目录拷贝到pc207的/opt目录下

    ```shell
    scp -r /home root@192.168.4.207:/opt/
    ls /opt
    ```

3. 将svr7的/etc/passwd文件拷贝到tom用户的家目录下，以用户tom的密码验证（用户tom密码为redhat）

    ```shell
    ssh root@192.168.4.207
    useradd tom
    echo 'redhat' | passwd --stdin tom
    scp -r /etc/passwd tom@192.168.4.207:/home/tom/
    ls /home/tom
    ```

### 案例练习
配置iSCSI服务端
1. 配置svr7提供iSCSI服务，磁盘名为iqn.2016-02.com.example:svr7，服务端口为3260，使用store作其后端卷，其大小为3GiB

    ```shell
    fdisk /dev/sdb
    	+3G
    partprobe /dev/sdb	#刷新分区
    lsblk
    
    yum -y install targetcli
    systemctl stop firewalld
    targetcli
    	ls
    	backstores/block create dev=/dev/sdb1 name=store
    	iscsi/ create iqn.2016-02.com.example:svr7
    	iscsi/iqn.2016-02.com.example:svr7/tpg1/luns create /backstores/block/store
    	iscsi/iqn.2016-02.com.example:svr7/tpg1/acls create iqn.2016-02.com.example:client
    	ls
    	exit
    systemctl restart target.service
    ```

配置iSCSI客户端

2. 配置pc207使其能连接上svr7提供的iqn.2016-02.com.example.svr7，iSCSI设备在系统启动期间自动挂载，块设备iSCSI上包含一个大小为2100MiB的分区，并格式化为ext4文件系统，此分区挂载在/mnt/data上，同时在系统启动的期间自动挂载

    ```shell
    #安装客户端软件
    yum -y install iscsi-initiator-utils
    rpm -q iscsi-initiator-utils
    
    #修改配置文件，指定客户端声称的名称
    vim  /etc/iscsi/initiatorname.iscsi
    	InitiatorName=iqn.2016-02.com.example.client
    
    #重启iscsi服务（主服务），使用共享存储
    systemctl restart iscsi	d
    iscsiadm --mode discoverydb --type sendtargets --portal 192.168.4.7 --discover	#利用命令发现服务端共享存储
    
    #iSCSI自动挂载
    systemctl restart iscsi	
    systemctl enable iscsi	
    
    #重起iscsid服务，仅仅是刷新客户端声称的名称
    systemctl restart iscsi
    
    #添加iSCSI 2100M分区
    fdisk /dev/sdb
    	+2100M
    partprobe /dev/sdb	#刷新分区
    lsblk
    
    #格式化为ext4文件系统类型?
    mkfs.ext4 /dev/sdb2
    
    #挂载到 /mnt/data
    umount /mnt
    mkdir /mnt/data
    mount /mnt/data
    mount /dev/sdb2 /mnt/data
    
    #系统启动自动挂载
    vim /etc/fstab
    	/dev/sdb2 /mnt/data ext4 defaults 0 0
    
    mount -a
    df -h
    ```

## 5.10
### 案例ISCSI练习

1. 为svr7添加一块10G硬盘
2. 在svr7操作，采用MBR分区模式利用/dev/sdb/划分一个主分区，大小为5G

    ```shell
    lsblk
    fdisk /dev/sdb
    n
    +5G
    w
    
    lsblk
    ```

3. 在svr7创建iscsi服务，磁盘名为iqn.2020-05.com.example:server，
服务端口号为3260，使用nsd做后端卷，大小为5G

    ```shell
    yum -y install targetcli	#安装服务软件包 targetcli
    systemctl stop firewalld    #关闭防火墙
    targetcli	#运行 targetcli 命令进行配置
    	ls
    	
    	#创建后端存储
    	backstores/block create name=nsd dev=/dev/sdb1
    	ls
    	
    	#创建磁盘组target，使用IQN名称规范
    	iscsi/ create iqn.2020-05.com.example:server
    	
    	#创建lun关联
    	iscsi/iqn.2020-05.com.example:server/tpg1/luns/ create /backstores/block/nsd
    	
    	#设置访问控制（acl），设置客户端的名称
    	iscsi/iqn.2020-05.com.example:serve/tpg1/acls create iqn.2020-05.com.example:client
    
    	ls
    	exit
    systemctl restart target
    
    getenforce 0
    systemctl status firewalld.service
    ```
    



4. 在pc207上连接使用服务端提供的iqn.2020-05.com.example:server，
并利用共享过来的磁盘划分一个主分区，大小为2G，格式化xfs文件系统类型，
挂载到/data文件夹下

    ```shell
    #安装客户端软件
    yum -y install iscsi-initiator-utils
    rpm -q iscsi-initiator-utils
    
    #修改配置文件，指定客户端声称的名称
    vim  /etc/iscsi/initiatorname.iscsi
    	InitiatorName=iqn.2020-05.com.example:client
    
    #重起iscsid服务，刷新客户端声称的名称
    systemctl restart iscsid
    
    #利用命令发现服务端共享存储
    man iscsiadm	#查看iscsiadm帮助	/example按n向下匹配，按b向上匹配
    iscsiadm --mode discoverydb --type sendtargets --portal 192.168.4.7 --discover
    
    #重启iscsi服务（主服务），使用共享存储
    systemctl restart iscsi
    lsblk
    fdisk /dev/sdb
        n
        +2G
        
    mkfs.xfs /dev/sdb1
    mount /dev/sdb1 /data
    df -h
    ```


## 5.11 练习
### 案例：虚拟主机练习

1. 配置域名为www.tedu.cn，访问页面内容为I AM KING.
    
    ```shell
    yum -y install httpd
    vim /etc/httpd/conf.d/nsd01.conf
        <VirtualHost *:80>
        	ServerName www.tedu.cn
        	DocumentRoot /var/www/tedu
        </VirtualHost>
        <VirtualHost *:80>
        	ServerName www0.qq.com
        	DocumentRoot /var/www/qq
        </VirtualHost>
        <VirtualHost *:80>
        	ServerName www.baidu.com
        	DocumentRoot /var/www/baidu
        </VirtualHost>
    
    mkdir /var/www/qq /var/www/baidu /var/www/tedu
    
    echo I AM KING  > /var/www/tedu/index.html
    ```

2. 配置域名为www0.qq.com，访问页面内容为I GOOD STUDY.

    ```shell
       echo I GOOD STUDY  > /var/www/qq/index.html
    ```
    
3. 配置域名为www.baidu.com，访问页面内容为I AM girl.

    ```shell
    echo I AM girl  > /var/www/qq/index.html
    
    systemctl restart httpd
    ```



4. 用客户端pc207测试访问3个页面

    ```shell
    vim /etc/host
        192.168.4.7 www.baidu.com
        192.168.4.7 www.tedu.cn
        192.168.4.7 www0.qq.com
    
    curl www.baidu.com
    curl www.tedu.cn
    www0.qq.com
    ```




5. 书写页面内容为wo shi abc，用pc207测试页面内容（用IP地址访问）

    ```shell
    #svr7
    echo "wo shi abc" > /var/www/html/index.html
    
    vim /etc/httpd/conf.d/nsd01.conf
        <VirtualHost *:80>
                ServerName www.test.cn
                DocumentRoot /var/www/html
        </VirtualHost>
    
    systemctl restart httpd.service 
    
    
    #pc207
    vim /etc/hosts
        192.168.4.7 www.test.cn
    
    curl www.test.cn
    ```


### 案例15:为虚拟机A配置以下虚拟Web主机
实现三个网站的部署
1. 实现客户端访问server0.example.com网页内容为 大圣归来
2.  实现客户端访问www0.example.com网页内容为  大圣又归来
3.  实现客户端访问webapp0.example.com网页内容为 大圣累了

    ```shell
    setenforce 0
    systemctl stop firewalld.services	#关闭防火墙
    
    vim /etc/httpd/conf.d/nsd01.conf
        <VirtualHost *:80>
        	ServerName server0.example.com
        	DocumentRoot /var/www/server0
        </VirtualHost>
        <VirtualHost *:80>
        	ServerName www0.example.com
        	DocumentRoot /var/www/www0
        </VirtualHost>
        <VirtualHost *:80>
        	ServerName webapp0.example.com
        	DocumentRoot /var/www/webapp0
        </VirtualHost>
    
    mkdir /var/www/server0 /var/www/www0 /var/www/webapp0
    
    echo "大圣归来" > /var/www/server0/index.html
    echo "大圣又归来" > /var/www/www0/index.html
    echo "大圣累了" > /var/www/webapp0/index.html
    
    systemctl restart httpd
    
    
    #客户端测试
    curl server0.example.com
    curl www0.example.com
    curl webapp0.example.com
    ```
    

### 案例16：为虚拟机A配置web服务访问控制
1. 修改默认网页文件位置为/webapp1

    ```shell
    #服务端配置
    mkdir /webapp1
    vim /etc/httpd/conf/httpd.conf
    	DocumentRoot /webapp1
    ```


2. 实现访问/webapp1页面文件为index.html,内容为奔跑吧 骆驼

    ```shell
    #服务端配置
    echo "奔跑吧 骆驼" > /webapp1/index.html
    systemctl restart httpd
    
    #客户端测试
    curl http://192.168.4.7	#出现测试页面
    ```


### 案例17：发布iSCSI网络磁盘

配置 A提供 iSCSI 服务，要求如下：

1. 磁盘名为iqn.2020-06.com.example:server0
2. 服务端口为 3260
3. 使用 iscsi_store（后端存储的名称） 作其后端卷，其大小为 3GiB
4. 在A配置客户端ACL为iqn.2020-06.com.example:desktop0

    ```shell
    fdisk /dev/sdb
    	+3G
    partprobe /dev/sdb	#刷新分区
    lsblk

    yum -y install targetcli	#安装服务软件包 targetcli
    systemctl stop firewalld    #关闭防火墙
    targetcli	#运行 targetcli 命令进行配置
    	ls
    	
    	#创建后端存储
    	backstores/block create dev=/dev/sdb1 name=store
    	
    	#创建磁盘组target，使用IQN名称规范
    	iscsi/ create iqn.2020-06.com.example:server0
    	
    	#创建lun关联
    	iscsi/iqn.2020-06.com.example:server0/tpg1/luns create /backstores/block/store
    	
    	#设置访问控制（acl），设置客户端的名称
    	iscsi/iqn.2020-06.com.example:server0/tpg1/acls create iqn.2020-06.com.example:desktop0
    
    	ls
    	exit
    systemctl restart target.service
    ```


5. 配置虚拟机B使用虚拟机A提供 iSCSI 服务

    ```shell
    #安装客户端软件
    yum -y install iscsi-initiator-utils
    rpm -q iscsi-initiator-utils
    
    #修改配置文件，指定客户端声称的名称
    vim  /etc/iscsi/initiatorname.iscsi
    	InitiatorName=iqn.2020-06.com.example:desktop0
    
    #重起iscsid服务，仅仅是刷新客户端声称的名称
    systemctl restart iscsid
    
    #利用命令发现服务端共享存储（A的ip地址：192.168.4.7）
    man iscsiadm	#查看iscsiadm帮助	/example按n向下匹配，按b向上匹配
    iscsiadm --mode discoverydb --type sendtargets --portal 192.168.4.7 --discover
    
    #重启iscsi服务（主服务），使用共享存储
    systemctl restart iscsi
    lsblk
    ```
    
## 5.12 练习

在虚拟机svr7上配置NFS共享，完成如下操作
1. 以读写的方式访问目录/public，只能被192.168.4.0/24系统访问

    ```shell
    rpm -q nfs-utils
    yum -y install nfs-utils
    mkdir /public
    
    vim /etc/exports
    	/public 192.168.4.0/24(rw,no_root_squash)	#开放权限
    
    systemctl restart nfs-server
    systemctl enable nfs-server
    systemctl stop firewall
    ```

2. 在虚拟机pc207上访问NFS共享目录，挂载点为/nfs

    ```shell
    rpm -q nfs-utils
    yum -y install nfs-utils
    showmount -e 192.168.4.7
    
    mkdir /nfs
    mount 192.168.4.7:/public /nfs
    df -h
    ls /abc
    ```


3. 实现开机自动挂载

> _netdev：声明网络设备，系统在网络服务配置完成后，再挂载本设备

```shell
vim /etc/fstab
192.168.4.7:/test /abc nfs defaults,_netdev 0 0
mount /abc
mount -a
df -h
```



## 5.17 练习
案例：
提供以下正向解析记录的解析
1. svr7.tedu.cn --> 192.168.4.7

    pc207.tedu.cn --> 192.168.4.207

    www.tedu.cn --> 192.168.4.100

```shell
#服务器配置
systemctl stop firewalld.service 
setenforce 0

yum -y install bind bind-chroot.x86_64	#安装named包默认端口号53
rpm -q bind bind-chroot

vim /etc/named.conf
    options {
            directory       "/var/named";
    };
    
    #指定这台机器要解析的域名
    zone "tedu.cn" IN {
            type master;
            file "tedu.cn.zone";
    };

named-checkconf /etc/named.conf	#检查主配置文件是否存在语法问题

cp -p /var/named/named.localhost /var/named/tedu.cn.zone
#第二种方法：相对路径方式
cd /var/named/
cp -p named.localhost tedu.cn.zone

vim /var/named/tedu.cn.zone
	$TTL 1D
	@       IN SOA  @ rname.invalid. (
	                                        0       ; serial
	                                        1D      ; refresh
	                                        1H      ; retry
	                                        1W      ; expire
	                                        3H )    ; minimum
	
	tedu.cn.        NS      svr7.tedu.cn.
	svr7.tedu.cn.   A       192.168.4.7
	pc207.tedu.cn.  A       192.168.4.207
	www.tedu.cn.    A       192.168.4.100


named-checkzone tedu.cn /var/named/tedu.cn.zone	#检查地址库文件是否存在语法问题

systemctl restart services	#重启服务
```

2. 在客户机上验证查询结果

    ```shell
    #客户端测试
    yum -y install bind-utils
    echo "nameserver 192.168.4.7" > /etc/resolv.conf
    
    nslookup pc207.tedu.cn
    nslookup www.tedu.cn
    ```


## 5.18 练习
案例：构建多区域DNS
实现以下正向解析记录
1. 访问www.tedu.cn ---> 192.168.4.100
2. 访问www.baidu.com ---> 10.20.30.40
3. 访问ftp.baidu.com ---> 50.60.70.80

    ```shell
    #服务器配置
    systemctl stop firewalld.service 
    setenforce 0
    
    yum -y install bind bind-chroot.x86_64	#安装named包默认端口号53
    rpm -q bind bind-chroot
    
    vim /etc/named.conf	#指定这台机器要解析的域名
        options {
        	directory 	"/var/named";
        };
        
        zone "tedu.cn" IN {
        	type master;
        	file "tedu.cn.zone";
        };
        zone "baidu.com" IN {
        	type master;
        	file "baidu.com.zone";
        };
    
    named-checkconf /etc/named.conf	#检查主配置文件是否存在语法问题
    
    cp -p /var/named/named.localhost /var/named/tedu.cn.zone
    cp -p /var/named/named.localhost /var/named/baidu.com.zone
    
    vim /var/named/tedu.cn.zone
        $TTL 1D
        @	IN SOA	@ rname.invalid. (
        					0	; serial
        					1D	; refresh
        					1H	; retry
        					1W	; expire
        					3H )	; minimum
        tedu.cn.	NS	svr7
        svr7	A	192.168.4.7
        www	A	192.168.4.100
    
    vim /var/named/baidu.com.zone
        $TTL 1D
        @	IN SOA	@ rname.invalid. (
        					0	; serial
        					1D	; refresh
        					1H	; retry
        					1W	; expire
        					3H )	; minimum
        baidu.com.	NS	svr7
        svr7	A	192.168.4.7
        www	A	10.20.30.40
        ftp	A	50.60.70.80
    
    named-checkzone tedu.cn /var/named/tedu.cn.zone	#检查地址库文件是否存在语法问题
    named-checkzone baidu.com /var/named/baidu.com.zone
    
    systemctl restart services	#重启服务
    
    #客户端测试
    yum -y install bind-utils
    echo "nameserver 192.168.4.7" > /etc/resolv.conf
    
    nslookup www.tedu.cn
    nslookup www.baidu.com
    nslookup ftp.baidu.com
    ```


## 5.19 练习
案例：搭建主/从DNS服务器
1. 准备3台虚拟机，主机名及IP地址要求如下：


| 主机名 | IP地址 |
| -- | -- |
| svr7.tedu.cn | 192.168.4.7 |
| pc207.tedu.cn | 192.168.4.207 |
| A.tedu.cn | 192.168.4.10 |

虚拟机svr7
```shell
nmcli connection modify ens33 ipv4.method manual ipv4.addresses 192.168.4.7/24 connection.autoconnect yes 
nmcli connection up ens33 
ifconfig
hostname svr7.tedu.cn
echo svr7.tedu.cn > /etc/hostname
```

虚拟机pc207
```shell
nmcli connection modify ens33 ipv4.method manual ipv4.addresses 192.168.4.207/24 connection.autoconnect yes 
nmcli connection up ens33 
ifconfig
hostname pc207.tedu.cn
echo pc207.tedu.cn > /etc/hostname
```

虚拟机A
```shell
nmcli connection modify ens33 ipv4.method manual ipv4.addresses 192.168.4.10/24 connection.autoconnect yes 
nmcli connection up ens33 
ifconfig
hostname A.tedu.cn
echo A.tedu.cn > /etc/hostname
```


2. 构建主/从DNS服务


| 主DNS | svr7.tedu.cn | 192.168.4.7 |
| -- | -- | -- |
| 从DNS | pc207.tedu.cn | 192.168.4.207 |
| 提供 | www.tedu.cn | 1.2.3.4 |

用虚拟机A测试。

虚拟机svr7
```shell
yum -y install bind bind-chroot.x86_64

vim /etc/named.conf
	options {
		directory 	"/var/named";
		allow-transfer     { 192.168.4.207; };
	};
	
	zone "tedu.cn." IN {
		type master;
		file "tedu.cn.zone";
	};

cp -p /var/named/named.localhost /var/named/tedu.cn.zone
vim /var/named/tedu.cn.zone
	$TTL 1D
	@	IN SOA	@ rname.invalid. (
						0	; serial
						1D	; refresh
						1H	; retry
						1W	; expire
						3H )	; minimum
	tedu.cn.	NS	svr7
	tedu.cn.	NS	pc207
	svr7	A	192.168.4.7
	pc207	A	192.168.4.207
	www	A	1.2.3.4

systemctl restart named	#重启服务
systemctl stop firewalld.service 
setenforce 0
```


虚拟机pc207
```shell
yum -y install bind bind-chroot.x86_64

vim /etc/named.conf 
	options {
		directory 	"/var/named";
	};
	zone "tedu.cn." IN {
		type slave;
		file "/var/named/slaves/tedu.cn.slave";
		masters { 192.168.4.7; };
	};

systemctl restart named
systemctl stop firewalld.service 
setenforce 0
```

虚拟机A
```shell
vim /etc/resolv.conf 
	nameserver 192.168.4.7
	nameserver 192.168.4.207

nslookup www.tedu.cn
```

## 5.20 练习
多区域DNS分离解析
1. 分类(配户端相同)相同：


192.168.4.207 --> www.tedu.cn --> 192.168.4.100


		www.qq.com


其他地址 --> www.tedu.cn --> 1.2.3.4


		www.qq.com



2. 分类(匹配客户端来源不相同)不相同：


客户端192.168.4.207 --> www.tedu.cn --> 192.168.4.100


客户端其他地址 --> www.tedu.cn --> 1.2.3.4


客户端192.168.4.10 --> www.qq.com -->192.168.10.100


客户端其他地址 --> www.qq.com --> 172.25.0.11



> 分析：
>
> 192.168.4.207 --> www.tedu.cn --> 192.168.4.100 --> 地址库tedu.cn.zone
>
> 192.168.4.207 --> www.qq.com --> 172.25.0.11 --> qq.com.other
>
>
>
> 192.168.4.10 --> www.tedu.cn --> 1.2.3.4 --> tedu.cn.other
>
> 192.168.4.10 --> www.qq.com --> 192.168.10.100 --> qq.com.other
>
>
>
> 其他地址 --> www.tedu.cn --> 1.2.3.4 --> tedu.cn.other
>
> 其他地址 --> www.qq.com --> 172.25.0.11 --> qq.com.zone

```shell
#服务端(svr7)
yum -y install bind bind-chroot
vim /etc/named.conf
	options {
		directory "/var/named";
	};
	view "nsd" {
		match-clients { 192.168.4.207; };
		zone "tedu.cn" IN {
			type master;
			file "tedu.cn.zone";	#解析结果为192.168.4.100
		};
		zone "qq.com" IN {
			type master;
			file "qq.com.zone";	#解析结果为172.25.0.11
		};
	 };
	view "vip" {
		match-clients { 192.168.4.10; };
		zone "tedu.cn" IN {
			type master;
			file "tedu.cn.other";	#解析结果为1.2.3.4
		};
		zone "qq.com" IN {
			type master;
			file "qq.com.other";	#解析结果为192.168.10.100
		};
	 };
	view "others" {
		match-clients { any; };
		zone "tedu.cn" IN {
			type master;
			file "tedu.cn.other";	#解析结果为1.2.3.4
		};
		zone "qq.com" IN {
			type master;
			file "qq.com.zone";	#解析结果为172.25.0.11
		};
	 };

cd /var/named/
cp -p named.localhost tedu.cn.zone
vim tedu.cn.zone
	$TTL 1D
	@	IN SOA	@ rname.invalid. (
						0	; serial
						1D	; refresh
						1H	; retry
						1W	; expire
						3H )	; minimum

	tedu.cn.	NS	svr7
	svr7	А	192.168.4.7
	www	A	1.2.3.4

cp -p tedu.cn.zone tedu.cn.other
vim tedu.cn.other
	$TTL 1D
	@	IN SOA	@ rname.invalid. (
						0	; serial
						1D	; refresh
						1H	; retry
						1W	; expire
						3H )	; minimum

	tedu.cn.	NS	svr7
	svr7	А	192.168.4.7
	www	A	192.168.4.100


cp -p tedu.cn.zone qq.com.zone
vim qq.com.zone
	$TTL 1D
	@	IN SOA	@ rname.invalid. (
						0	; serial
						1D	; refresh
						1H	; retry
						1W	; expire
						3H )	; minimum

	qq.com.	NS	svr7
	svr7	А	192.168.4.7
	www	A	172.25.0.11

cp -p qq.com.zone qq.com.other
vim qq.com.other
	$TTL 1D
	@	IN SOA	@ rname.invalid. (
						0	; serial
						1D	; refresh
						1H	; retry
						1W	; expire
						3H )	; minimum

	qq.com.	NS	svr7
	svr7	А	192.168.4.7
	www	A	192.168.10.100

systemctl restart named
```

客户机(pc207)
```shell
echo "nameserver 192.168.4.7" > /etc/resolv.conf
yum -y install bind-utils
nslookup www.qq.com
nslookup www.tedu.cn
```

客户机A
```shell
echo "nameserver 192.168.4.7" > /etc/resolv.conf
nslookup www.qq.com
nslookup www.tedu.cn
```

服务端(svr7)
```shell
echo "nameserver 192.168.4.7" > /etc/resolv.conf
yum -y install bind-utils
nslookup www.qq.com
nslookup www.tedu.cn
```

> 如有侵权，请联系作者删除