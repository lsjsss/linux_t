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
umount /abc
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

## 主/从DNS服务器

### 主域名服务器

特定DNS区域的官方服务器，具有唯一性

负责维护该区域内所有的“域名 <--> IP地址”记录

### 从域名服务器

也称为`辅助域名服务器`，可以没有

其维护的“域名 <--> IP地址”记录取决于主域名服务器

### 主/从DNS应用场景
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

## 基础邮件服务
电子邮件通信


电子邮件服务器的基本功能

> 为用户提供电子邮箱存储空间（用户名@邮件域名）
>
> 处理用户发出的邮件 -- 传递给收件服务器
>
> 处理用户收到的邮件 -- 投递到邮箱 


### 配置邮件服务器的DNS

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


### 构建邮件服务器

#### 邮件服务搭建

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

#### 交互式mail命令

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

#### 非交互式mail命令

语法格式：

> echo "邮件内容" | mail -s '邮件标题' -r 发件人 收件人

```shell
echo abc | mail -s 'mail title' -r fajianren shoujianren	#使用非交互式命令发送邮件
mail -u shoujianren	#检查邮件
```


## 分离解析概述

### 分离解析：

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


### BIND的view视图

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


### 分离解析实例

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
	svr7	A	192.168.4.7
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
	svr7	A	192.168.4.7
	www	A	1.2.3.4

systemcti restart named
```

分别用pc207和虚拟机A验证

```shell
nslookup www.tedu.cn
```


## 缓存DNS概述
作用：缓存解析记录，加快解析速度


缓存DNS的适用场景


主要适用环境：


> 互联网出口带宽较低的企业局域网络
>
> ISP服务商的公共DNS服务器


### 构建缓存服务器

客户端（pc207）
```shell
yum -y install bind bind-chroot
vim /etc/namd.conf
	options {
		directory"/var/named";
		forwarders	{ 192.168.4.7 };	#转发地址
	};

systemctl restart named
```

客户端验证（A）
```shell
nalookup www.tedu.cn 192.168.4.207
```


## 批量装机PXE
### 部署DHCP服务器
#### DHCP概述及原理

 * Dynamic Host Configuration Protocol


动态主机配置协议，由IETF (Internet网络工程师任务小组)组织制定，用来简化主机地址分配管理。


主要分配以下入网参数：

> IP地址/子网掩码/广播地址
> 默认网关地址、DNS服务器地址


 * DHCP地址分配的四次会话

> -DISCOVERY -> OFFER - REQUEST ->ACK


 * 服务端基本概念

> 租期：允许客户机租用IP地址的时间期限，单位为秒
> 作用域：分配给客户机的IP地址所在的网段
> 地址池：用来动态分配的IP地址的范围



#### 配置 dhcpd 地址分配服务

 * 装软件包dhcp
 * 配置文件 /etc/dhcp/dhcpd.conf
 * 起服务 dhcpd

```shell
vim /etc/dhcp/dhcpd.conf
	subnet 192.168.4.0 netmask 255.255.255.0 {	//声明网段
		range 192.168.4.10 192.168.4.200;	//IP范围
	}
	netstat -antpu I grep dhcpd	//确认结果
	udp	0	00.0.0.0:67	0.0.0.0:*	8380/dhcpd
```


```shell
yum -y install dhcp
vim /etc/dhcp/dhcpd.conf
	:r /usr/share/doc/dhcp-4.2.5/dhcpd.conf.example
	subnet 192.168.4.0 netmask 255.255.255.0 {
		range 192.168.4.100 192.168.4.200;
		option domain-name-servers 192.168.4.10;
		option routers 192.168.4.254;	#网关
		default-lease-time 600;	#租约时间600秒
		max-lease-time 7200;	#最大祖约时间
	}
systemctl restart dhcpd
ss -anptu | grep 67

#svr7
dhclient-r	#临时释放IP地址
dhclient-d	#临时获取IP地址
```

### 网络装机的优势
 * 规模化：同时装配多台主机
 * 自动化：装系统、配置各种服务
 * 远程实现：不需要光盘、U盘等物理安装介质

#### 什么是PXE网络
 * PXE，Pre-boot eXecution Environment
 - 预启动执行环境在操作系统之前运行
 - 可用于远程安装

 * 工作模式
 - PXE client集成在网卡的启动芯片中
 - 当计算机引导时，从网卡芯片中把PXE client调入内存执行，获取PXE server配置、显示菜单，根据用户选择将远程引导程序下载到本机运行

#### PXE组件及过程分析

 * 需要哪些服务组件？
 - DHCP服务，分配1P地址、定位引导程序
 - TFTP服务,提供引导程序下载
 - HTTP服务（或FTP/NFS），提供yum安装源

 * 客户机应具备的条件
 - 网卡芯片必须支持PXE协议
 - 主板支持从网卡启动


#### 配置dhcpd服务

 * 装软件包 dhcp
 * 配置文件 /etc/dhcp/dhcpd.conf
 * 起服务dhcpd

```shell
vim /etc/dhcp/dhcpd.conf
	:r /usr/share/doc/dhcp-4.2.5/dhcpd.conf.example
	subnet 192.168.4.0 netmask 255.255.255.0 {
		range 192.168.4.100 192.168.4.200;
		option domain-name-servers 192.168.4.10;
		option routers 192.168.4.254;	#网关
		default-lease-time 600;	#租约时间600秒
		max-lease-time 7200;	#最大祖约时间

		next-server 192.168.4.10;	#指定下一台服务器的IP地址
		filename "pxelinux.0";	#网卡引导文件（网络装机说明书，二进制文件）
	}
systemctl restart dhcpd
```


### 部署TFTP服务

#### 启用TFTP服务端
 * TFTP，Trivial File Transfer Protocol
 - 小文件传输协议，UDP 69端口
 - 主要用来传送小文件，不支持认证和复杂FTP操作
 - 默认资源目录：/var/lib/tftpboot 

```shell
yum -y install tftp-server
systemctl restart tftp
ss -anptu | grep 69
```

#### 部署引导文件pxelinux.0
```shell
yum provides */pxelinux.0	#//查找产生的软件包
yum -y install syslinux
ls /usr/share/syslinux
rpm -ql syslinux | grep pxelinux.0	#查看软件相应的安装内容
cp /usr/share/syslinux/pxelinux.0 /var/lib/tftpboot/
```

#### 部署菜单文件

```shell
mkdir /var/lib/tftpboot/pxelinux.cfg
ls /var/lib/tftpboot/
cp /mnt/isolinux/isolinux.cfg /var/lib/tftpboot/pxelinux.cfg/default
ls /var/lib/tftpboot/pxelinux.cfg
```


#### 部署引导程序

```shell
cp /mnt/isolinux/vesamenu.c32	 /mnt/isolinux/splash.png /mnt/isolinux/vmlinuz /mnt/isolinux/initrd.img /var/lib/tftpboot	#图形模块
ls /var/lib/tftpboot/
```

#### 修改菜单文件

```shell
vim /var/lib/tftpboot/pxelinux.cfg/default
	#1行
	default vesamenu.c32	#默认加载图形模块
	timeout 600	#默认读秒时间1/10

	#10行
	menu background splash.png
	menu title Centos7	#装机界面标题

	#61行
	label linux	#菜单名
		menu label ^Install CentOS 7	#菜单显示内容
		menu default	#默认进入菜单
		kernel vmlinuz	#默认进入菜单
		append initrd=initrd.img	#加载的驱动程序

setenforce 0
systemctl stop firewalld.service
```

### 部署 WEB 服务器
#### 搭建httpd服务

```shell
#安装软件包 httpd
yum -y install httpd

#挂载光盘内容并启动 httpd 服务
mkdir /var/www/html/centos
mount /dev/cdrom /var/www/html/centos
systemctl restart httpd
firefox http://192.168.4.7/centos
```


#### 生成应答文件

```shell
#图形工具 system-config-kickstart 进行生成应答文件
yum -y install system-config-kickstart 

#运行
system-config-kickstart

vim /etc/yum.repos.d/centos.repo 
    [development] 
    name=CentOS7.5
    baseurl=file:///dvd 
    enabled=1 
    gpgcheck=0 

#再次运行 点击 "软件包选择(Package Selection)" 查看是否可以进行选择（可以进行选择）
system-config-kickstart
```


## PXE网络装机

```shell
nmcli connection modify ens33 ipv4.method manual ipv4.addresses 192.168.4.10/24 connection.autoconnect yes
nmcli connection up ens33
mount /dev/cdrom /mnt

vim /etc/yum.repos.d/mnt.repo
	[development]
	name=Centos7.5
	baseurl=file:///mnt
	enabled=1
	gpgcheck=0

rm -rf /etc/yum.repos.d/C*
yum clean all

yum repolist

setenforce 0
systemctl stop firewalld.service 
yum -y install httpd
yum -y install dhcp
rpm -q dhcp
systemctl restart dhcpd
ss -anptu | grep 67

vim /etc/dhcp/dhcpd.conf 
	subnet 192.168.4.0 netmask 255.255.255.0 {
	  range 192.168.4.100 192.168.4.200;
	  option domain-name-servers 192.168.4.10;
	  option routers 192.168.4.254;
	  default-lease-time 600;
	  max-lease-time 7200;
	  next-server 192.168.4.10;
	  filename "pxelinux.0";
	}
	
systemctl restart dhcpd
yum -y install tftp-server.x86_64 
systemctl restart tftp
ss -anptu | head -69
yum provides */pxelinux.0
yum -y install syslinux
rpm -ql syslinux | grep pxelinux.0
cp /usr/share/syslinux/pxelinux.0  /var/lib/tftpboot/
mkdir /var/lib/tftpboot/pxelinux.cfg
cp /mnt/isolinux/isolinux.cfg /var/lib/tftpboot/pxelinux.cfg/default
cp /mnt/isolinux/vesamenu.c32 /mnt/isolinux/splash.png /mnt/isolinux/initrd.img /mnt/isolinux/vmlinuz /var/lib/tftpboot/

vim /var/lib/tftpboot/pxelinux.cfg/default 
	label linux
	  menu label ^Install CentOS 7
	  menu default
	  kernel vmlinuz
	  append initrd=initrd.img ks=http://192.168.4.10/ks.cfg

systemctl restart dhcpd
systemctl restart tftp
setenforce 0
yum -y install httpd
systemctl restart httpd
mkdir /var/www/html/centos
mount /dev/cdrom /var/www/html/centos/
yum -y install system-config-kickstart.noarch 
yum -y install system-config-kickstart

#编辑配置文件
vim /var/www/html/ks.cfg

install
keyboard 'us'
rootpw --iscrypted $1$6/ldzaKw$dsdWMg2fX1l40RTZ2BoN50
url --url="http://192.168.4.10/centos"
lang en_US
auth  --useshadow  --passalgo=sha512
graphical
firstboot --disable
selinux --disabled
firewall --disabled
network  --bootproto=dhcp --device=eth0
reboot
timezone Asia/Shanghai
bootloader --location=mbr
zerombr
clearpart --all --initlabel
part / --fstype="xfs" --grow --size=1

%packages
@base

%end



systemctl restart httpd.service 
systemctl restart dhcpd.service 
systemctl restart tftp.service

#########################################################
#法二

system-config-kickstart
	#基本配置 - 时区 - Asia/Shanghai
	#基本配置 - Root密码 - 1
	#基本配置 - 确认密码 - 1
	#基本配置 - 安装后重启 - v
	#安装方法 - HTTP - v
	#HTTP服务器 - 192.168.4.10
	#HTTP目录 - centos
	#引导装载程序选项 - 安装新引导装载程序
	#分区信息 - 清除主引导记录 - v
	#分区信息 - 初始化磁盘标签 - v
	#分区信息 - 添加 - 挂载点：/
	#分区信息 - 添加 - 使用磁盘上全部未用空间 - v
	#网络配置 - 添加网络设备 - 网络设备：eth0
	#防火墙配置 - SELinux： 禁用
	#软件包选择 - 系统- 基本
	文件 - 保存

cp /root/ks.cfg /var/www/html/ks.cfg

##

#设置永久关闭
vim /etc/selinux/config 
	SELINUX=disabled

systemctl enable dhcpd
systemctl enable tftp
systemctl enable httpd
```

shell脚本
```shell
nmcli connection modify ens33 ipv4.method manual ipv4.addresses 192.168.4.10/24 connection.autoconnect yes
nmcli connection up ens33
mount /dev/cdrom /mnt

echo "[development]
name=Centos7.5
baseurl=file:///mnt
enabled=1
gpgcheck=0" > /etc/yum.repos.d/mnt.repo 

rm -rf /etc/yum.repos.d/C*
yum clean all 
yum repolist

setenforce 0
systemctl stop firewalld.service 
yum -y install httpd
yum -y install dhcp
rpm -q dhcp
systemctl restart dhcpd
ss -anptu | grep 67

echo "subnet 192.168.4.0 netmask 255.255.255.0 {
  range 192.168.4.100 192.168.4.200;
  option domain-name-servers 192.168.4.10;
  option routers 192.168.4.254;
  default-lease-time 600;
  max-lease-time 7200;
  next-server 192.168.4.10;
  filename \"pxelinux.0\";
}" > /etc/dhcp/dhcpd.conf 

systemctl restart dhcpd
yum -y install tftp-server.x86_64 
systemctl restart tftp
ss -anptu | head -69
yum provides */pxelinux.0
yum -y install syslinux
rpm -ql syslinux | grep pxelinux.0
cp /usr/share/syslinux/pxelinux.0  /var/lib/tftpboot/
mkdir /var/lib/tftpboot/pxelinux.cfg
cp /mnt/isolinux/isolinux.cfg /var/lib/tftpboot/pxelinux.cfg/default
cp /mnt/isolinux/vesamenu.c32 /mnt/isolinux/splash.png /mnt/isolinux/initrd.img /mnt/isolinux/vmlinuz /var/lib/tftpboot/

sed -i '61d' /var/lib/tftpboot/pxelinux.cfg/default 
sed -i '61d' /var/lib/tftpboot/pxelinux.cfg/default 
sed -i '61d' /var/lib/tftpboot/pxelinux.cfg/default
sed -i '61d' /var/lib/tftpboot/pxelinux.cfg/default

sed -i "61a label linux" /var/lib/tftpboot/pxelinux.cfg/default 
sed -i "62a   menu default" /var/lib/tftpboot/pxelinux.cfg/default 
sed -i "63a   kernel vmlinuz" /var/lib/tftpboot/pxelinux.cfg/default 
sed -i "64a   append initrd=initrd.img ks=http://192.168.4.10/ks.cfg" /var/lib/tftpboot/pxelinux.cfg/default 

systemctl restart dhcpd
systemctl restart tftp
setenforce 0
yum -y install httpd
systemctl restart httpd
mkdir /var/www/html/centos
mount /dev/cdrom /var/www/html/centos/
yum -y install system-config-kickstart.noarch 
yum -y install system-config-kickstart

echo "install
keyboard 'us'
rootpw --iscrypted $1$6/ldzaKw$dsdWMg2fX1l40RTZ2BoN50
url --url=\"http://192.168.4.10/centos\"
lang en_US
auth  --useshadow  --passalgo=sha512
graphical
firstboot --disable
selinux --disabled
firewall --disabled
network  --bootproto=dhcp --device=eth0
reboot
timezone Asia/Shanghai
bootloader --location=mbr
zerombr
clearpart --all --initlabel
part / --fstype=\"xfs\" --grow --size=1

%packages
@base

%end" > /var/www/html/ks.cfg

systemctl restart httpd.service 
systemctl restart dhcpd.service 
systemctl restart tftp.service
```



# 数据库

### 常见软件

主流操作系统：Unix, Linux, Windows

| 软件名 | 开源 | 跨平台 | 厂商 |
| -- | -- | -- | -- |
| Oracle | 否 | 是 | 甲骨文 |
| MysQL | 是 | 是 | 甲骨文 |
| SQL Server | 否 | 否 | 微软 |
| DB2 | 否 | 是 | IBM |
| Redis | 是 | 是 | 开源软件 |
| Memcached | 是 | 是 | 开源软件 |
| MongoDB | 是 | 是 | 开源软件 |


### 专业术语
* DB (DataBase)
- 数据库
- 依照某种数据模型进行组织并存放到存储器的数据集合

* DBMS (DataBase Management System)
- 数据库管理系统
- 用来操纵和管理数据库的服务软件

* DBS (DataBase System)
- 数据库系统:即DB+DBMS
- 指带有数据库并整合了数据库管理软件的计算机系统


### 相关参数
* 软件安装后自动创建相关目录与文件

| 文件 | 说明 |
| -- | -- |
| /etc/my.cnf | 主配置文件 |
| /var/ib/mysql | 数据库目录 |
| 默认端口号 | 3306 |
| 进程名 | mysąld |
| 传输协议 | TCР |
| 进程所有者 | mysql |
| 进程所属组 | mysql |
| 错误日志文件 | /var/log/mysqld.log |


### 环境准备

1. 创建新虚拟机1台
2. 关闭firewalld
3. 禁用SELinux
4. 配置yum源
5. 配置IP地址192.168.4.50
6. 软件mysq-5.7.1
7. tar官网地址 http://dev.mysql.com/downloads/mysql


```shell
systemctl stop firewalld.service 
setenforce 0
tar -xf mysql-5.7.17.tar
yum -y install mysql-community-*.rpm
rpm -qa | grep mysql
systemctl start mysqld
systemctl enable mysqld
netstat -anptu | grep :3306
ls /var/lib/mysql
```

### 连接数据库，使用初始密码登录并重置密码

```sql
grep password /var/log/mysqld.log
mysql -uroot -p'qg1wpZ;G+deg'
	show databases;    -- 报错,需要重置密码
	alter user root@localhost identified by "123Qqq...";    -- 重置密码
	show databases;	    -- 成功
	exit
mysql -uroot -p123Qqq...
```

修改密码策略

| 策略名称 | 验证方式 |
| -- | -- |
| LoW(0) | 长度 |
| MEDIUM(1) | 长度；数字，小写/大写，和特殊字符 |
| STRONG (2) | 长度；数字，小写/大写和特殊字符；字典文件 |


```shell
#永久配置
vim /etc/my.cnf
	[mysqld]
	validate_password_policy=0
	validate_password_length=6
```

```sql
mysql -uroot -p123Qqq...
	show variables like "%password%";    -- 查看变量
	set global validate_password_policy=0;    -- 修改密码策略
	set global validate_password_length=6;    -- 修改密码长度
	alter user root@localhost identified by "123456";    -- 重置密码
	exit
mysql -uroot -p123456
```


## 连接 mySQL 服务

* 客户端连接MySQL服务的方法
	- 命令行
	- 图形工具软件(软件自带图形界面、web页面)
	- 编写脚本(php, Java, python ..)

* 使用 mysql 命令
	- mysql -h服务器IP -u用户名 -p密码 [数据库名]
	- quit 或 exit #退出

登录时直接切换到mysql库

```sql
mysql -uroot -p123456 mysql
	select database();    -- 查看当前所处的数据库
```


### 数据存储流程

* 客户端把数据存储到数据库服务器上的步骤
	- 连接数据库服务器
	- 建库(类似于文件夹)
	- 建表(类似于文件夹)
	- 插入记录(类似于文件内容)
	- 断开连接


### SQL命令使用规则

* SQL命令不区分字母大小写(密码、变量值除外)
* 每条SQL命令以 `;` 结束
* 默认命令不支持 `Tab键` 自动补齐
* `\c` 终止sql命令

### 常用的SQL命令分类
* 管理数据库使用SQL (结构化查询语言)
* DDL 数据定义语言如：create、alter、drop
* DML 数据操作语言如：insert、update、delete
* DCL 数据控制语言如：grant、revoke
* DTL 数据事务语言如：commit、rollback、savepoint

## mysql基本操作
> 库管理命令：库类似于文件夹,用来存储表

* 可以创建多个库,通过库名区分

```sql
show databases;	-- 显示已有的库
select user();	-- 显示连接用户
use 库名;	-- 切换库
select database();	-- 显示当前所在的库
create database 库名;	-- 创建新库
show tables;	-- 显示已有的表
drop database 库名;	-- 删除库
```

```sql
mysql -uroot -p123456 mysql

create database bbsdb;
create database BBSDB
show databases;
drop database BBSDB;    -- 删除库
use bbsdb;    -- 切换库
select databse();    -- 显示当前所在库
select user();    -- 显示连接用户
show tables;    -- 显示已有的表
```



### 表管理命令

#### 创建表

* 表存储数据的文件

```sql
create table 库名.表名(
	字段名1 类型(宽度),
	字段名2 类型(宽度)
	.......
) DEFAULT CHARSET=utf8;	-- 指定中文字符集,可以给字段慰值中文
```

```sql
mysql -uroot -p123456 mysql

use bbsdb;
select database();
create table user(name char(10), age int, homedir char(20));
show tables;
desc user;
select * from bbsdb.user;
select * from user;
insert into bbsdb.user values("tom", 18, "beijing");
select * from user;
insert into user values("abc", 20,"chifeng");
select * from user;
select name from user; 
select name,age from user;
```


#### 修改、删除表

```sql
update bbsdb.user set homedir="china";
select * from user;	-- 更新表数据
delete from bbsdb.user;	-- 删除表数据,但表还在
show tables;
select * from user;
drop table bbsdb.user;	-- 删除表
show tables;
create table user(name char(10), age int, homedir char(20));
show tables;
show create table bbsdb.user\G
create table 学生表(姓名 char(15), 地址 varchar(20)) DEFAULT CHARSET=utf8; -- 设置字符集为utf8,支持中文
show tables;
show tables;
desc 学生表;
insert into 学生表 values("张三峰", "武当山");
select * from 学生表;
```

### 数据类型：
#### 常见信息种类

> 数值型：体重、身高、成绩、工资
> 字符型：姓名、工作单位、通信地址
> 枚举型：兴趣爱好、性别、专业
> 日期时间型：出生日期、注册时间

#### 字符类型

* 定长：char(字符个数）
    - 最大字符个数255
    - 不够指定字符个数时在右边用空格补全
    - 字符个数超出时，无法写入数据。

* 变长：varchar(字符个数）
    - 按数据实际大小分配存储空间
    - 字符个数超出时，无法写入数据。

* 大文本类型：text/blob
    - 字符数大于65535存储时使用


```sql
create table  t1(name char(5), email varchar(15));
desc t1;
create table t2( name char, email varchar(3) ); -- char类型不指存储几个字符，默认存储一个
desc t2;
insert into t2 values("a", "bac");  -- 成功
insert into t2 values("aa", "bacd");    -- 失败2
insert into t2 values("b", "bacd"); -- 失败
select * from t2;
```

#### 数值类型
##### 整数型：只能存整数

| 类型 | 名称 | 有符号范围 | 无符号范围 |
| tinyint | 微小整数 | -128~127 | 0~255 |
| smallint | 小整数 | -32768~32767 | 0~65535 |
| mediumint | 中整型 | -223~223-1 | 0~224-1 |
| int | 大整型 | -231~231-1 | 0~232-1 |
| bigint | 极大整型 | -263~263-1 | 0~264-1 |
| unsigned | 使用无符号存储范围 | | |

创建一张表 t3，用于存储学生信息(用户名，年龄，等级)，tinyint 类型，unsigned 无符号存储(0~255)，默认有符号存储(-128~127)

```sql
create table t3(name char(15), age tinyint unsigned, level tinyint);
insert into t3 values("bob", 21, 7); #成功
insert into t3 values("tom", -1, -129); #失败，条件不满足
insert into t3 values("tom", 0, -129); #失败，超出范围
insert into t3 values("tom", 0, -127); #成功
存储小数，会四舍五入
insert into t3 values("jim", 21.5, 3); #21.5四舍五入存为22
select * from t3;
insert into t3 values("jim", 21.5, 3.43); #3.43四舍五入存为3
select * from t3;3
```

##### 浮点型：存储有小数点的数

| 类型 | 名称 | 有符号范围 | 无符号范围 |
| —- | —- | —- | —- |
| float | 单精度 | -3.402823466E+38到1.175494351E-38 | -1.175494351E-38到3.402823466E+38 |
| double | 双精度 | -1.7976931348623157E+308到2.2250738585072014E-308 | -22250738585072014E-308 到1.7976931348623157E+308 |

```sql
float(7,2)  -- 7 指整个浮点数的最大位数，2 指 7 位数字中有两位是小数位, 则取值范围 为：
-99999.99 ~ 99999.99
float(5,3)     -- 5 指整个浮点数的最大位数，3 指 5 位数字中有三位是小数位, 则取值范围为：-
99.999 ~ 99.999
float(数字 1,数字 2)    -- 数字 1：总的位数 数字 2：小数位的个数
```

```sql
create table t4(name char(10), pay float(5,2));
insert into t4 values("john", 1000.88); -- 失败，超出范围
insert into t4 values("john", 999.88);  -- 成功
insert into t4 values("john", -999.99); -- 成功
select * from t4;
insert into t4 values("john3", 218);    -- 存储整数，小数位默认补0
```

### 日期时间类型
#### 类型格式

创建与日期时间相关的表，指定名称，年份，上课时间，生日，聚会时间

```sql
create table t5(name char(15), s_year year, uptime time, birthday date, party datetime);
insert into t5 values("bob", 1990,083000, 20231120, 20230214183000);
select * from t5;
```

### 时间函数


```sql
select curtime();     —- 获取当前的系统时间
select curdate();     —- 获取当前的系统日期5
select now();     —- 获取当前的系统日期和系统时间
select year(now());     —- 从当前系统时间中只取出年份
select month(now());     —- 从当前系统时间中只取出月份
select day(now());     —- 从当前系统时间中只取出天数
select date(now());     —- 从当前系统时间中只取出年月日
select time(now());     —- 从当前系统时间中只取出时分秒
```

```sql
—- 根据时间函数在 t5 表中插入一条数据
insert into t5 values("tom",2000,time(now()),curdate(),now());
select * from t5;
```

### 日期时间字段 datetime 与 timestamp 的区别

关于日期时间字段：当未给timestamp字段赋值时，自动以当前系统时间赋值，而datetime值为NULL（空）

```sql
—- 创建 t6 表，指定姓名，约会时间，聚会时间，验证 timestamp 和 datetime 的区别
create table t6(name char(10), meetting datetime, party timestamp);
insert into t6 values("bob", now(), now());     —- 两个字段都有值
select * from t6;
```

```sql
—- t6 表中重新插入一条数据，只插入 name 和 metting 字段的值，party 字段采用默认值
insert into t6(name,meetting) values("bob", 20231120224058);
select * from t6;    —- party字段同样有值，字段类型为timestamp，用当前系统时间
```

```sql
—- t6 表中重新插入一条数据，只插入 name 和 party 字段的值，meetting 字段采用默认值
insert into t6(name,party) values("john", 19731001223000 );
select * from t6;     —- meetting字段类型为datetime，没有指定时间，默认为空NULL)
```


### year 类型

要求使用 4 位赋值6

当使用 2 位数赋值时：01-99

01 ~ 69 视为 2001 ~ 2069

70 ~ 99 视为 1970 ~ 1999


```sql
—- 插入数据，只给 t5 表中的 s_year 字段赋值
show tables;
desc t5;
select s_year from t5;
insert into t5(s_year) values(03),(81);
select s_year from t5;     —- 查看t5表中s_year字段的数据，验证结果
```

### 枚举类型

字段的值不能自己输入，必须在设置的范围内选择(有单选和多选之分)

#### enum 单选

格式：字段名 enum（值 1，值 2，值 N）

仅能在列表里选择一个值


### set 多选

格式：字段名 set(值 1，值 2，值 3)

在列表里选择一个或多个值

```sql
—- 创建 t7 表，指定字段：姓名(name)，性别(sex)，爱好(likes)
create table t7(name char(15), sex enum("boy", "girl", "no"), likes set("eat","money", "game", "music"));
desc t7;
insert into t7 values('bob','boy','eat,game,music');     —- 成功
Select * from t7;7
insert into t7 values('bob','man','girl,book');     —- 字段sex的类型中没有man,存储失败
insert into t7 values('bob','no','girl,book');     —- 字段likes的类型中没有girl和book,存储失败，使用类型enum(单选)，set(多选)，值必须在其范围之内

## 约束条件：
### 作用

限制字段赋值

```sql
desc t1;

Null Key Default Extra     —- 这四列为约束条件
Null     —- 指是否允许为字段赋空值；
         —-  YES，允许给字段赋空值，默认也是允许赋空值；
         —-  NO， 不允许给字段赋空值；
Key：键值
Default    —- 当不给字段赋值时，则使用默认值，初始默认值为 NULL，可以修改
Extra     —- 额外的设置, 例如：可以设置学号为自动增长的

### 设置约束条件

| null | 允许为空（默认设置） |
| —- | —- |
| not null | 不允许为 null（空）|
| key | 键值类型 |
| default | 设置默认值，缺省为 NULL |
| extra | 额外设置 |



#### 环境准备：

```sql
create database test;
use test;
create table t1(name char(15), s_year year, uptime time, birthday date, party datetime);2
insert into t1 values("bob", 1990,083000, 20231120, 20230214183000);
insert into t1 values("tom",2000,time(now()),curdate(),now());
insert into t1(s_year) values(03),(81);
select * from t1;
create table t2(name char(15), sex enum("boy", "girl", "no"), likes set("eat","money", "game", "music"));
desc t2;
```


#### 验证约束条件 Null,可以给字段赋空值

```sql
insert into t2 values ('bob','boy','eat,game');
select * from t2;
insert into t2 values (null,null,null);     —-  t2表中可以插入null（没有数据）
select * from t2;
insert into t2(name) values ('tom');     —- 只给name字段赋值，其他字段会使用默认值赋值
select * from t2;
```

#### 建表时指定字段值不为空和设置默认值

```sql
create table t3( name char(10) not null, age tinyint unsigned default 18, class char(8) not null default 'NSD2006');
desc t3;
insert into t3(name) values("john");     —- 只插入name字段，则其他字段采用默认值
select * from t3;
```


#### 向t3表中插入数据，所有字段自己定义，可以不使用默认值

```sql
insert into t3 values("tom", 29, "nsd2003");
select * from t3;
```

#### 验证 null 值和"null"值

null 指的是没有任何的数据3
"null" 指的是有数据，但数据的内容为"null"

```sql
desc t3;
insert into t3 values(null,null,null);     —-  name字段不能为空，存储失败
insert into t3 values("null",null,null);     —- 给name字段加引号，不代表空值，而是代表字符串，存储失败，class 字段不能为空
insert into t3 values("null",null,"");     —-  class字段直接加引号，不为空，是0个字符
select * from t3;
```

### 修改表结构：
#### 语法结构：

##### 用法：
```sql
alter table 库名.表名 执行动作;
```

#### 执行动作：

> add：添加新字段
>
> modify：修改字段类型
>
> drop：删除字段
>
> change：修改字段名
>
> rename：修改表名


### 添加新字段

#### 用法
    —- 新字段默认添加在字段末尾
```sql
alter table 库名.表名
add 字段名 类型(宽度) 约束条件 [after 字段名 | first];
```


向 t1 表中插入一个字段 email, 不为空，默认值为"stu@tedu.cn"，不指定表字段的位置，默认会插入到表的最后

```sql
desc t1;
alter table t1 add email varchar(30) not null default "stu@tedu.cn";
desc t1;     —-  email字段在最下方
select * from t1;     —- t1表中的数据也会多出一行，值为默认值
```

向 t1 表的最前面插入一个字段 stu_id, 约束条件采用默认系统设置

```sql
alter table t1 add stu_id char(9) first;
desc t1;     —-  stu_id字段位于表的首位
select * from t1;     —-  stu_id没有指定默认值，默认为NULL
```

在 t1 表中的 name 字段后，插入一个新字段 sex，类型为枚举类型，默认值为：boy

```sql
alter table t1 add sex enum("boy", "girl") default "boy" after name;
desc t1;     —-  sex字段位于name字段的后面
select * from t1;     —- 多出一列sex,默认值为boy
```

### 修改字段类型

#### 基本用法

 - 修改的字段类型不能与已存储的数据冲突

```sql
alter table 库名.表名
modify 字段名 类型(宽度) 约束条件 after 字段名 | first];
```


修改 t1 表的 sex 字段，设置默认值为 man

```sql
alter table t1 modify sex enum("man", "woman") default "man";#修改失败，字段里需要包含原表中的数据类型boy,否则冲突
alter table t1 modify sex enum("man", "woman", "boy") default "man"; #修改成功，sex字段中存在和表中数据相同的类型'boy'5
desc t1;
```

修改 t1 表中的 name 字段类型，修改为 varchar(15)

```sql
desc t1;
alter table t1 modify name varchar(15);
desc t1;
```

##### 使用 modefy 实现字段值的位置调换

将 email 字段移到 sex 字段的后面


alter table t1 modify email varchar(30) not null default "stu@tedu.cn" after sex;
desc t1;
select * from t1; #数据不发生变化


### 删除字段
#### 基本用法
- 表中有多条记录时，所有列的此字段的值都会被删除
    
```sql
after table 库名.表名 drop 字段名;
```


删除 t1 表中的字段 stu_id

```sql
select * from t1;
alter table t1 drop stu_id;
select * from t1;
desc t1;
```

删除 t1 表中的多个字段(email 和 party)

```sql
alter table t5 drop email,drop party;6
```

### 修改字段名
#### 基本用法

```sql
after table 库名.表名 change 原字段名 新字段名 类型 约束条件;
```


修改 t1 表中 s_year 的字段名，使用 change 命令将字段 s_year 的名字改为 abc

```sql
alter table t1 change s_year abc year;
```


### 修改表名
#### 基本用法
 - 表对应的文件名，也被改变
 - 表记录不受影响

```sql
after table 表名 rename 新表名;
```

使用rename命令来修改t5表的表名为stuinfo

```sql
alter table t1 rename stuinfo;
show tables;
```


## Mysql 键值概述

根据数据存储要求，选择键值

| index | 普通索引 |
| —- | —- |
| unique | 唯一索引 |
| fulltext | 全文索引 |
| primary key | 主键 |
| foreign key | 外键 |

> index、primary key、foreign key #生产环境一定会用到的键值类型

### 索引介绍

> 类似于书的目录
>
> 对表中字段值进行排序
>
> 索引算法：Btree、B+tree、hash

#### Btree 算法(二叉树)：


1. 查找数字 5 时，先用数字 5 和数字 4 对比；
2. 当数字 5 大于数字 4，则直接从数字 4 的右分支进行查找；
3. 接下来用要查找的数字 5 和数字 6 对比；2
4. 当数字 5 小于数字 6，则直接从数字 6 的左分支进行查找；
5. 按照以上的方式继续比对查找，直到查找到数据为止；

### 索引的优缺点

> 生产环境下，对数据查的请求远远高于对数据写的请求；

### 普通索引 index

使用规则

### 创建索引

> 建表的时候创建索引：index(字段名), index(字段名)....
>
> 创建 t1 表时，将 name 字段和 class 字段设置为索引


```sql
create table t1(name char(10), class char(9), sex enum("m", "w"), index(name),index(class));
desc t1;    —- 约束条件Key变为MUL(索引的标志)
```

```sql
在已有的表里创建索引：

```sql
create index 索引名 on 表名(字段名);
```

```sql
create table t2 ( name char(16), pay float(5,2) );
desc t2;
```

在已有表 t2 表中为字段创建索引 xxx(索引名称可以随便定义)

```sql
create index xxx on t2(name);
desc t2;
```

### 查看索引

语法格式：
```sql
show index from 表名 \G;
```

```sql
show index from t1\G;
    *************************** 1. row ***************************
    Table: t9    —- 表名
    Non_unique: 1
    Key_name: name    —- 索引名
    Seq_in_index: 1
    Column_name: name    —- 字段名
    ...
```


### 删除索引

语法格式：

```sql
drop index 索引名 on 表名;
```

删除 t1 表中的索引 name

```sql
drop index name on t1;
desc t1;
show index from t1\G;4
```

## MySQL 主键 primary key：

### 创建主键
#### 主键的作用：限制字段赋值


#### 主键的使用规则

> 创建表时，表中存在类似身份证号，编号等时，将表中的该字段设置为主键，让其不能重复，可以自动增长。

#### 创建主键

> 建表时创建主键，命令：`primary key`(字段名)
>
> 创建 t3 表，字段有：姓名(name)，年龄(age) ，将 name 字段设置为主键 primary key

```sql
create table t3(name char(10) primary key, age int);
desc t10;    —- 查看t3表的表结构，key的值为PRI，则代表该字段为主键,在表t3中插入数据，主键所在的字段，数据不能重复，不允许有空值
insert into t3 values("bob",29);    —- 成功
insert into t3 values("bob",39);     —- 失败，主键字段的数据重复
insert into t3 values("jim",19);     —- 成功
insert into t3 values(null,29);     —- 失败，主键所在的字段值不能为NULL值
insert into t3 values("null",39);     —- 成功，加引号代表的是字符串5
insert into t3 values("",59);     —- ””指没有内容，不代表null
select * from t3;
```

> 在已有表里创建主键

语法格式：　
```sql
alter table 表名 add primary key(字段名列表);
```

> 将表中的字段设置为主键时，则表中该字段的值不能为空，也不能重复，否则添加失败; 表中没有数据时，添加成功

```sql
select * from t1;
desc t1; #查看t1表的表结构，原先没有主键，允许数据重复
alter table t1 add primary key(name); #将t1表中的字段name设置为主键
desc t1;
```

### 删除主键

语法格式：
```sql
alter table 表名 drop primary key;
```

删除 t1 表的主键

```sql
alter table t1 drop primary key;
desc t1; #主键消失，但是name字段的约束条件不许为空，可以重复插入数据
insert into t1 values('bob','NSD2001','m'); #成功
insert into t1 values('bob','NSD2002','m'); #成功
insert into t1 values(null,'NSD2002','m'); #失
```











```sql
create table yg(yg_ id int primary key auto increment,name char(15))engine=innodb;
desc yg;
insert into yg(name) values('bob);
insert into yg(name) values('tom");
select * from yg;
create table gz(
gz_id int,
pay float(5,2),
foreign key(gz id) references yg(yg id) on update cascade on delete cascade)engine=innodb;
show create table gz\G	-- 通过查看建表过程，来查看表是否创建
```

外键外键设置成功之后，gz (工资表)插入数据时，编号必须在yg (员工表)的yg_id范围之内
```sql
select * from ygi
insert into gz values(1,300.00);
insert into gz values(2,500.00);
insert into gz values(3,300.00);	-- 插入失败,编号必须在yg (员工表)编号范围之内
```


在yg表里插入一条记录，用户名为john，编号采用自增长
```sql
insert into yg(name) values(john);
select * from yg
```


在gz表里插入记录,是否可以插入
```sql
insert into gz values(3,300.00);
select * from gz;
```

### 测试同步删除和同步更新
```sql
delete from yg where yg_id=3;
select * from yg;
select from gz;
update yq set yg id=6 where name="tom"
select * from yg;
select * from gz;
```


### 设置成外键的表字段也必须将其设置为主键,否则会出现对于同一个编号可以插入多次数据的情况,也会出现编号为null,插入数据同样成功的情况

```sql
desc gz;
insert into gz values(1,200.00);
insert into gz values(6,200.00);
select * from gz;
insert into gz values(null,200.00);
select * from gz;
```

### 将表中的外键字段设置为主键

```sql
delete from gz;
select * from gz;
alter table gz add primary key(gz id);
desc gz;
insert into gz values(null,200.00);
insert into gz values(1,200.00);
insert into gz values(1,200.00);
insert into gz values(6,200.00);
insert into gz values(6,200.00);
insert into gz values(7,200.00);
```

###删除表当一个表被其他表所依赖时,该表则不可以被删除删除方法有2种:
> 1. 删除表中的外键
> 2. 先删除gz (工资表)

```sql
drop table yg;#直接删除失败
```

### 删除外键：

语法格式：

```sql
alter table 表名 drop foreign key 名称;
```

```sql
show create table gz\G
alter table gz drop foreign key gz_ibfk_1;
show create table gz\G 
drop table yg;
```

### 构建mysq图形管理界面

```shell
yum -y install httpd
systemctl start httpd
yum -y install php php-mysql
tar -xf phpMyAdmin-2.11.11-all-languages.tar.gz
ls phpMyAdmin-2.11.11-all-languages
mv phpMyAdmin-2.11.11-all-languages /var/www/html/phpmyadmin
ls /var/www/html/
ls /var/www/html/phpmyadmin/
cd /var/www/html/phpmyadmin/
cp config.sample.inc.php config.inc.php

vim config.inc.php
	17 $cfg['blowfish_secret'] = 'wj123';	#指定COOKIE的值，做认证，自定义
	31 $cfg['Servers'][$i]['host'] = 'localhost';	#指定数据库服务器的地址


systemctl restart httpd
firefox http://192.168.4.10/phpmyadmin
```



### 范围匹配

| in (`值列表`) | 在....里 |
| -- | -- |
| not in (`值列表`) | 不在...里... |
| between `数字` and `数字` | 在...之间… |

举例：
```sql
select name,uid from user where name in("mysql","bin","null");
select name,uid from user where uid in(3,6,9,15);
select name,shell from user where shell not in("/bin/bash","/sbin/nologin")
select name,uid from user where uid between 15 and 30;
select name,uid from user where uid between 15 and 100;
select id,name,uid from user where id between 10 and 13;
```

#### 逻辑匹配


多个条件判断时使用


| or | 逻辑或 | 有一个条件成立即可 |
| -- | -- | -- |
| and | 逻辑与(且) | 所有条件都要成立才可以 |
| !或not | 逻辑非 |

举例
```sql
select name,uid from user where name="root" and shell ="/sbin/nologin";
select name,uid from user where name="root" and shell="/bin/bash";
select name,uid from user where name="root" or shell="/sbin/nologin";
select name,uid,shell from user where name="root" or shell="/sbin/nologin";
select name,uid,shell from user where shell !="/bin/bash";

select name,uid,shell from user where shell="/bin/bash";
select name,uid,shell from user where shell in ("/bin/bash","/sbin/nologin");
select name,uid,shell from user where shell not in ("/bin/bash","/sbin/nologin");
```



### 高级匹配条件

#### 模糊查询

格式: where 字段名 like "通配符"

| _ | 表示1个字符 |
| -- | -- |
| % | 表示0-n个字符 |

```sql
select name from user where name like "_";
select name from user where name like "____";
select name from user where name like "%a%";
select name from user where name like "a%";
select name from user where name like "__%__";
```



#### 正则表达式格式

> 格式: ` where 字段 regexp "正则表达式" `
>
> 正则元字符: `^` `$` `.` `[]` `*` `|`

| ^ | 匹配输入字符串的开始位置 |
| -- | -- |
| $ | 匹配输入字符串的结束位置 |
| . | 匹配除 "\n" 之外的任何单个字符 |
| [...] | 字符集合。匹配所包含的任意一个字符。例如， '[abc]' 可以匹配 "plain" 中的 'a' |
| * | 匹配前面的子表达式零次或多次。例如，zo* 能匹配 "z" 以及 "zoo"。* 等价于{0,} |
| p1\|p2\|p3 | 匹配 p1 或 p2 或 p3。例如，'z\|food' 能匹配 "z" 或 "food"。'(z\|f)ood' 则匹配 "zood" 或 "food" |

```sql
select name from user where name regexp "^r";
select name from user where name regexp "^a";
select name from user where name regexp "^a|t$";;
select name from user where name regexp "^r.*t$";
select name from user where name regexp "[0-9]";
insert into user(name) values("haha99"),("66haha"),("6xixi"),("ya7ya");
select name from user;
select name from user where name regexp "[0-9]";	-- 查询user表用户名包含数字的name字段
```




```sql
select id,name,uid from user where id<=5;
update user set uid=uid+1 where id<=5;
select id,name,uid from user where id <=5;
update user set uid=uid-1 where id<=5;
select id,name,uid from user where id<=5;
select name,uid from user where id<=5;
select name,uid from user where uid % 2=0;
select name,uid from user where uid % 2 !=0;
select name,uid,gid from user where name="halt";
select name,uid,gid,(uid+gid)/2 from user where name="halt";	-- 显示uid和gid的平均值,默认以算法作为临时字段名
alter table user add age tinyint unsigned default 20 after name;
desc user;
select * from user;
select name,age,2023-age start_y from user where name="root";	-- start_y临时字段名
```



### 聚集函数

> MySQL内置数据统计函数(字段必须是数值类型)

| avg(字段名) | 统计字段平均值 |
| sum(字段名) | 统计字段之和 |
| min(字段名) | 统计字段最小值 |
| max(字段名) | 统计字段最大值 |
| count(字段名) | 统计字段值个数 |

举例
```sql
select avg(uid) from user;
select sum(uid) from user;
select min(uid) from user;
select max(uid) from user;
select count(*) from user;
select count(*) from user where name like "___";
select count(name) from user where name like "___";
```



### 排序

> 格式: SQL查询 order by 字段名 [asc|desc] 升序|降序

```sql
select name,uid from user where uid>=10 and uid<=200;
select name,uid from user where uid>=10 and uid<-200 order by uid;
select name,uid from user where uid>=10 and uid<=200 order by uid desc;
```


### 分组

> 格式: SQL查询 group by 字段名

```sql
select shell from user where uid<500;
select shell from user where uid<500 group by shell;
```

> 去重显示格式: select distinct 字段名 from 表名

```sql
select distinct shell from user where uid<500;
```


### 限制查询结果

> 显示行数用法


> SQL查询limit数字;	//显示查询结果前多少条记录
>
> SQL查询limit数字1,数字2;	//显示指定范围内的查询记录

数字1 起始行(0表示第1行)

数字2 总行数

```sql
select name,uid,gid from user limit 3;
select name,uid,gid from user limit 3,3;
```


查询user表中gid最大的前5个用户使用的shell

```sql
select name,gid,shell from user order by gid desc limit 5;
```

把gid最小的前5个用户信息保存到/myload/min5.txt文件里

```sql
select name,gid,shell from user order by gid limit 5 into outfile "/var/lib/mysql-files/min5.txt";
system cat /var/lib/mysql-files/min5.txt 1
```



## 用户授权
### grant 授权

> 授权：添加用户并设置权限

命令格式

```sql
-- 客户端
grant 权限列表 on 库名 to 用户名@"客户端地址"
	identified by "密码"	-- 授权用户密码
	with grant option;	-- 有授权权限，可选项

grant all on db4.* to yaya@"%" identified by"123qqq...A"; 
```

#### 权限列表

> all	-- 所有权限
>
> usage	-- 无权限
>
> select,update,insert	-- 个别权限
>
> select, update (字段1, .字段N)	-- 指定字段库名

#### 库名

> *.*	-- 所有库所有表
>
> 库名.*	-- —个库
>
> 库名.表名	-- 一张表 

* 用户名
 - 授权时自定义 要有标识性
 - 存储在mysql库的user表里

#### 客户端地址

> %	-- 所有主机
>
> 192.168.4.%	-- 网段内的所有主机
>
> 192.168.4.1	-- 1台主机
>
> localhost	-- 数据库服务器本机


##### 应用示例1
 - 添加用户mydba，对所有库、表有完全权限
 - 允许从任何客户端连接，密码123qqq...A
 - 且有授权权限

```sql
grant all on *.* to mydba@"%" 	dentified by "123qqq...A" with grant option; 
```

##### 应用示例2
 - 添加admin用户，允许从192.168.4.0/24网段连接，对db3库的user表有查询权限，密码123qqq...A
 - 添加admin2用户，允许从本机连接，允许对db3库的所有表有查询/更新/插入/删除记录权限，密码123qqq...A

```sql
grant select on db3.user to admin@"192.168.4.%" identified by "123qqq...A";
grant select,insert,update,delete on db3.* to admin2@"localhost" identified by "123qq...A"; 
```

#### 示例3：

> 添加用户mydba，对所有库所有表有完全权限，允许从任何客户端连接，密码为123qqq...A，且有授权权限

```sql
-- 虚拟机svr7操作
mysql -uroot -p'123qqq...A'
grant all on *.* to mydba@"%" identified by '123qq...A' with grant option;

``虚拟机pc207测试:
yum -y install mariadb
mysql -h192.168.4.7 -umydba -p'123qq...A' 
```         


### 登录用户使用

```sql
select user();	-- 显示登录用户名及客户端地址
show grants;	-- 用户显示自身访问权限
show grants for用户名@"客户端地址";	-- 管理员查看已有授权用户权限
set password=password("密码");	-- 授权用户连接后修改连接密码
set password for用户名@"客户端地址"= password("密码");	-- 管理员重置授权用户连接密码
drop user 用户名@"客户端地址";	-- 删除授权用户(必须有管理员权限) 
```


示例：

虚拟机pc207

```shell
yum-y install mariadb
mysql -h192.168.4.7-umydba -p'123qqq...A'
```

```sql
select user();	-- 查看当前的登录用户及客户端地址
show grants;	-- 查看当前登录用户mydba所拥有的权限
```

虚拟机svr7
```sql
show grants for mydba@"%";	-- 管理员查看已有授权用户权限
```

虚拟机pc207
```sql
set password=password("456aaa...A");	-- 授权用户修改自己的连接密码
exit

mysql -h192.168.4.7 -umydba -p'456aaa...A'
exit	-- 使用新密码登录数据库
```

虚拟机svr7
```sql
set password for mydba@"%"=password("123qqq ..A");	-- 管理员重置授权用户连接密码
```

虚拟机pc207
```shell
mysql-h192.168.4.7 -umydba -p'123qqq...A'
```


#### 测试权限

pc207
```shell
mysql -h192.168.4.7 -umydba -p'123qqq...A'
```
```shell
show grants;
show databases
drop database test;
create database test;
create database bbsdb;
grant all on bbsdb.* to abc@"localhost" identified by '123qqq..A;	-- 用户mydba可以给其他用户授权虚拟机
```

svr7
```shell
mysql -uabc -p'123qq..A'
```
```shell
# 删除授权用户mydba (必须有管理员权限)
mysql -uroot -p '123qqq...A';
```
```sql
drop user mydba@"%";
```

pc207
```sql
mysql -h192.168.4.7 -umydba -p'123qqq...A'	-- 连接失败
```


##### 应用示例4:
- 添加admin用户，允许从192.168.4.0/24网段连接，对db3库的user表有查询权限,密码123qqq...A
- 添加admin2用户，允许从本机连接，允许对db3库的所有表有查询/更新/插入/删除记录权限，密码123qqq...A

```sql
grant select on db3.user to admin@"192.168.4.%" identified by "123qqq...A";
grant select,insert,update,delete on db3.* to admin2@"localhost" identified by "123qqq...A"; 
```

svr7
```sql
mysql -uroot -p'123qqq...A'
```

添加admin用户，允许从192.168.4.0/24网段连接，对db3库的user表有查询权限，密码为123qqq...A
```sql
grant create,select on db3.user to admin@"192.168.4.%" identified by '123qqq...A';	-- 给用户授权时如果不是all权限,当对应的库和表不存在时必须有create权限
```
添加admin2用户,允许从本机连接,对db3库的所有表有查询/更新/插入/删除权限,密码为123qqq...A
```sql
grant create,select,update,insert,delete on db3.* to admin2@"localhost" identified by '123qqq...A';
create database db3;
exit
```
pc207：测试admin用户的权限
```sql
mysql -h192.168.4.7 -uadmin -p'123qqq...A'
show grants;
create table db3.user(name char(50),sex enum("m","w");
select * from db3.user;
insert into db3.user values("bob","m");	-- 插入失败
```
svr7：测试admin2用户的权限,只能从本机登录
```sql
mysql -uadmin2 -p'123qqq...A'
show grants;
use db3;
show tables;
insert into db3.user values("bob","m");
select * from user;
delete from user;
create table t1(id int);
```


### 授权库

mysql库记录授权信息,主要表如下:

| user表 | 记录已有的授权`用户`及权限 |
| -- | -- |
| db表 | 记录已有授权用户对`数据库`的访问权限 |
| tables_priv表 | 记录已有授权用户对`表`的访问权限 |
| columns_priv表 | 记录已有授权用户对`字段`的访问权限 |

`查看表记录可以获取用户权限;也可以通过更新记录,修改用户权限`


* mysql库记录授权信息,主要表如下:

| user表 | 记录已有的授权用户及权限 |
| -- | -- |
| db表 | 记录已有授权用户对数据库的访问权限 |
| tables_priv表 | 记录已有授权用户对表的访问权限 |
| columns_priv表 | 记录已有授权用户对字段的访问权限 |

```sql
mysql -uroot-p'123qq...A'
select user,host from mysql.user;
show grants for admin@"192.168.4.%";	-- 查看admin用户的权限
select * from mysql.user where host="192.168.4.%" and user="admin"\G
select * from mysgl.tables priv where host="192.168.4.%" and user="admin"\G
desc mysql.tables priv\G
update mysql.tables_priv set Table_priv="select,create,insert,update" where user="admin" and host="192.168.4.%";	-- 通过改表字段的值修改授权用户权限
flush privileges;	-- 刷新，让配置生效
select * from mysql.tables_priv where host="192.168.4.%" and user="admin"\G 
show grants for admin@"192.168.4.%";
desc mysql.db;
select host,db,user from mysgl.db;
select * from mysql.db where db="db3"\G
show grants for admin2@"localhost";
update mysql.db set Delete_priv="N" where user="admin2";
flush privileges;
show grants for admin2@"localhost";
select * from mysql.db where db="db3"\G 
desc mysql.columns_priv;
select * from mysql.columns_priv;
grant select,update(name) on db3.user to admin2@"localhost" identified by "123qqq...A";
select * from mysql.columns_priv;
show grants for admin2@"localhost";
```




### 撤销权限
* 命令格式
revoke 权限列表 on 库名.表 from 用户名@"客户端地址";

```sql
REVOKE insert,drop ON test.* FROM sqler02@'localhost';
```


















































































































































---

```shell
setenforce 0
systemctl stop firewalld.service 
echo A.tedu.cn > /etc/hostname
cat /etc/hostname
hostname A.tedu.cn
exit
nmcli connection  modify ens33 ipv4.method manual ipv4.addresses 192.168.4.10/24 connection.autoconnect yes
nmcli connection up ens33 


yum源安装
mount /dev/cdrom /mnt
vim /etc/yum.repos.d/mnt.repo

[mnt]
name=1
enabled=1
gpgcheck=0
baseurl=file:///mnt


rm -rf /etc/yum.repos.d/C*
yum clean all
yum repolist 



为本机第一张网卡添加ip地址 192.168.100.1、24
ip address add 192.168.100.1/24 dev ens33

利用ip命令添加路由，去往200.0.0.0/24 下一跳为192.168.100.10
ip route add 200.0.0.0/24 via 192.168.100.10 dev ens33

安装vsftpd软件包
yum -y install vsftpd

启动vsftpd服务 （systemctl restart vsftpd）
systemctl restart vsftpd

查看vsftpd服务监听的端口号
netstat -anptu |grep vsftpd

将tools.tar.gz包传到虚拟机A
	ls

将tools.tar.gz解压到/tools文件夹下
mkdir /tools
tar  -xf /root/tools.tar.gz -C /tools


源码编译安装inotify-tools-3.13tar.gz，安装位置为/opt/abc
createrepo /tools/tools/other/
ls /tools/tools/
ls /tools/tools/other/
mount /dev/cdrom /mnt
vim /etc/yum.repos.d/mnt.repo

[mnt]
name=1
enabled=1
gpgcheck=0
baseurl=file:///mnt

[mmmmmnt]
name=1
enabled=1
gpgcheck=0
baseurl=file:///tools/tools/other

rm -rf /etc/yum.repos.d/C*
ls /etc/yum.repos.d/
yum clean all
yum repolist 
tar -xf /tools/tools/
tar -xf /tools/tools/inotify-tools-3.13.tar.gz -C /opt
cd /opt/inotify-tools-3.13/
yum -y install gcc
yum -y install make
./configure --prefix=/opt/abc
make
make install
ls /opt/abc/


在虚拟机A上构建ftp服务
安装vsftpd软件包
yum -y install vsftpd

查看有没有安装httpd
rpm -p httpd

启动httpd服务
systemctl start httpd

测试
firefox http://192.168.4.10
vim /var/www/html/index.html
<marquee> <font color=red> <h1> i an king.

firefox http://192.168.4.10
yum -y install elinks
elinks http://192.168.4.10
elinks --dump http://192.168.4.10
curl http://192.168.4.10


启动vsftpd服务
systemctl start vsftpd

测试
firefox ftp://192.168.4.10
touch /var/ftp/a.txt
firefox ftp://192.168.4.10

关闭虚拟机A的selinux
vim /etc/selinux/config 
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.

SELINUX=disabled

# SELINUXTYPE= can take one of three two values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected. 
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted 



查看防火墙默认区域
firewall-cmd --get-default-zone  

svr7  ping 192.168.4.10	可以ping通
        curl http://192.168.4.10  	拒绝访问
        curl ftp://192.168.4.10	拒绝访问

修改防火墙默认区域为trusted  		允许任何访问 （关闭防火墙）
firewall-cmd --set-default-zone=trusted
firewall-cmd --get-default-zone

svr7  ping 192.168.4.10              可以ping通
        curl http://192.168.4.10     可以访问
        curl ftp://192.168.4.10 	可以访问

修改防火墙默认区域为block		阻塞任何来访请求
firewall-cmd --set-default-zone=block
firewall-cmd --get-default-zone

svr7  不可以ping通    但是有回应

修改防火墙默认区域为drop  	丢弃任何来访数据包
firewall-cmd --set-default-zone=drop
firewall-cmd --get-default-zone

不可以ping通，没有回应

设置允许http协议通过public区域
A  firewall-cmd --zone=public --add-service=http
A  firewall-cmd --zone=public --list-all

sev7  curl http://192.168.4.10
          123	

设置允许ftp协议通过public区域
A    firewall-cmd --zone=public --add-service=ftp
A    firewall-cmd --zone=public --list-all

ser7  curl ftp://192.168.4.10


永久设置允许ftp协议和http协议通过public区域（永久设置--permanent）
firewall-cmd --permanent --zone=public --add-service=ftp
firewall-cmd --permanent --zone=public --add-service=http
firewall-cmd --reload
firewall-cmd --zone=public --list-all

srv7测试
curl ftp://192.168.4.10	可以访问
curl http://192.168.4.10	可以访问

拒绝svr7访问本机所有服务
firewall-cmd -zone=block -add-source=192.168.4.7

sev7测试
curl ftp://192.168.4.10	失败
curl http://192.168.4.10	失败

删除规则
firewall-cmd -zone=block --remove-source=192.168.4.7

sev7测试
curl ftp://192.168.4.10	可以访问
curl http://192.168.4.10	可以访问


seten tab   0   宽松



网络yum
虚拟机A
利用web服务共享光盘所有内容，默认共享位置为：/var/www/html
yum -y install httpd
systemctl start httpd
mkdir /var/www/html/nsd
mount /dev/cdrom /var/www/html/nsd
firewall-cmd --set-default-zone=trusted
setenforce 0

sev7
vim /etc/yum.repos.d/mnt.repo
[mnt]
name=Centos7.5
baseurl=http://192.168.4.10/nsd
enabled=1
gpgcheck=0
firewall-cmd --set-default-zone=teusted
setenforce 0
yum clean all
yun repolist



构建网络yum
利用FTP服务实现yum源提供
1 svr7构建vsftpd服务
服务器：
	setenforce 0 
	getenforce
	systemctl stop firewalld	关闭防火墙
	yum -y install vsftpd
	mkdir /var/ftp/ftpyum
	mount /dev/cdrom /var/ftp/nsd
	systemctl start vsftpd
客户端：
	setenforce 0
	getenforce
	systemctl stop firewalld	关闭防火墙
	vim /etc/yum.repos.d/mnt.repo
	[mnt]
	name=Centos7.5
	baseurl=ftp://192.168.4.7/nsd
	enabled=1
	gpgcheck=0

	yum clean all
	yum repolist
2 利用vsftpd服务提供如下内容
   Centos7光盘内容
   自定义yum仓库内容
3 利用pc207进行测试






高级远程管理
实现svr7远程管理pc207，无密码验证
ssh-keygen	生成公私钥
ls /root/.ssh	--查看	
ssh-copy-id root@192.168.4.207  --传递公钥
验证：ssh root@192.168.4.207

将svr7的/home目录拷贝到pc207的/opt目录下
上传操作：scp -r /home root@192.168.4.207:/opt
ls /opt

将svr7的/etc/passwd文件拷贝到tom用户的家目录下，以用户tom的密码验证（用户tom密码为redhat）
ssh root@192.168.4.207
useradd tom
echo redhat | passwd --stdin tom
scp /etc/passwd tom@192.168.4.207:/home/tom
ls /home/tom






NTP时间同步
svr7
rpm -q chrony
rpm -qc chrony			查看配置文件
vim /etc/chrony.conf
3 #server 0.centos.pool.ntp.org iburst
4 #server 1.centos.pool.ntp.org iburst
5 #server 2.centos.pool.ntp.org iburst
6 #server 3.centos.pool.ntp.org iburst
26 allow 0.0.0.0/0
29 local stratum 10
systemctl restart chronyd
setenforce 0
systemctl stop firewalld		关闭防火墙


客户端操作pc207
vim /etc/chrony.conf
3 #server 192.168.4.7 iburst
4 #server 1.centos.pool.ntp.org iburst
5 #server 2.centos.pool.ntp.org iburst
6 #server 3.centos.pool.ntp.org iburst
systemctl restart chronyd
chronys sources -v			出现^*为成功






查看分区   lsdlk
分区 fdisk /dev
n
p





安装服务端软件包targetcli
svr7   yum -y install targetcli

运行targetcli命令进行配置
targetcli
ls

1.创建后端存储
backstores/block create dev=/dev/sdb1 name=nsd
ls

2.创建磁盘组target
iscsi/ create iqn.2019-09.cn.tedu:server
ls

3.进行lun关联
iscsi/iqn.2019-09.cn.tedu:server/tpg1/luns create /backstores/block/nsd
ls

4.设置访问控制（acl）设置 客户端声称的名字
iscsi/iqn.2019-09.cn.tedu:server/tpg1/acls create iqn.2019-09.cn.tedu:client
ls />exit

重启服务并加入开机自启
	systemctl restart target.service
	systemctl enable target.service




1.安装客户端软件 iscsi-initiator-utils
pc207   yum -y install iscsi-initiator-utils
rpm -q iscsi-initiator-utils

2.修改配置文件，指定客户端声称的名字
pc207 vim /etc/iscsi/initiatorname.iscsi
InitiatorName=iqn.2019-09.cn.tedu:client

3.重起iscsid服务，仅仅是刷新客户端声称的名字
pc207 systemctl restart iscsid

4.利用命令发现服务端共享存储
pc207  man iscsiadm 		#iscsiadm man帮助查看
全文查找/example 按n向下跳转匹配
pc207  iscsiadm --mode discoverydb --type sendtargets --portal 192.168.4.7 --discover

重启iscsi服务，使用共享存储
systemctl restart iscsi
lsblk





配置iscsi服务端
配置svr7提供iscsi服务，磁盘名为iqn.2016-02.com.example:svr7,服务端口为3206，使用store作其后端卷，其大小为3GiB
配置iscsi客户端
配置pc207使其能连接上svr7提供的iqn.2016-02.com.example:svr7,iscsi设备在系统启动的期间自动加载，块设备iscsi上包含一个大小为2100MiB的分区，并格式化为ext4
文件系统 此分区挂载在/mnt/data上，同时在系统启动的期间自动挂载




ISCSI练习
为svr7添加一块10G硬盘
在svr7操作，采用MBR分区模式利用/dev/sdb划分一个主分区，大小为5G
在svr7创建iscsi服务，磁盘名为iqn.2020-05.com.example:server,服务端口号为3260，使用nsd做后端卷，大小为5G
在pc207上连接使用服务端提供的iqn.2020-05.com.example:server,并且利用共享过来的磁盘划分一个主分区，大小为2G，
格式化xfs文件系统类型，挂载到/data文件夹下



构建独立的web服务器：
服务端svr7操作
安装httpd软件包
yum -y install httpd
书写页面文件内容
echo abc > /var/www/html/index.html
启动服务
systemctl restart httpd 

客户端pc207测试
curl http://192.168.4.7

服务端操作svr7
修改主配置文件/etc/httpd/conf/httpd.conf,改变网页文件存放路径
vim /etc/httpd/conf/httpd.conf
/DocumentRoot  
/var/www/myweb
mkdir /var/www/myweb
echo wo shi myweb > /var/www/myweb/index.html
systemctl restart httpd

pc207
curl http://192.168.4.7

svr7修改配置文件/etc/httpd/conf/httpd.conf,改变监听端口号
/etc/httpd/conf/httpd.conf
Listen   8080
systemctl restart httpd
netstat -antpu | grep httpd

pc207
curl http://192.168.4.7
curl http://192.168.4.7:8080



对/webapp目录允许任何人访问
服务端操作svr7
修改主配置文件/etc/httpd/conf/httpd.conf,改变网页文件存放路径
vim /etc/httpd/conf/httpd.conf
/DocumentRoot  
/webapp
mkdir /webapp
echo wo shi myweb > /webapp/index.html
systemctl restart httpd

pc207
curl http://192.168.4.7



服务端操作svr7
修改主配置文件/etc/httpd/conf/httpd.conf,改变网页文件存放路径
vim /etc/httpd/conf/httpd.conf
<Directory  "/webapp">	#新添加
Require all granted		对/webapp目录允许任何人访问
</Directory>
systemctl restart httpd

pc207 curl http://192.168.4.7



svr7操作
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
echo "wo shi qq " > /var/www/qq/index.html
echo "wo shi baidu" > /var/www/baidu/index.html
systemctl restart httpd

pc207
vim /etc/hosts
192.168.4.7 www.qq.com www.baidu.com
curl www.qq.com
curl www.baidu.com



多区域DNS服务
修改主配置文件，在下面新添加
svr7
vim /etc/named.conf
.....

zone "baidu.com" IN {
	type master;
	file "baidu.com.zone";
};

cp -p /var/named/tedu.cn.zone /var/named/baidu.com.zone
vim /var/named/baidu.com.zone

.....

baidu.com.	NS svr7
svr7	A	192.168.4.7
www	A	10.20.30.40

systemctl restart named


pc207
nslookup www.tedu.cn
nslookup www.baidu.com


泛域名解析
svr7
vim /var/named/baidu.com.zone
.....

*   A  10.20.30.40

systemctl restart named


pc207
nslookup www.baidu.com



构建DNS服务器
svr7
yum -y install bind bind-chroot
vim /etc/named.conf
options {
	directory "/var/named"
};
zone "example.com" IN {
	type master;
	file "example.com.zone";
};
cp -p /var/named/named.localhost /var/named/example.com.zone
vim /var/named/example.com.zone
$TTL 1D
@       IN SOA  @ rname.invalid. (
                                        0       ; serial
                                        1D      ; refresh
                                        1H      ; retry
                                        1W      ; expire
                                        3H )    ; minimum
example.com.	NS	svr7
example.com.	MX	10	mail		#MX邮件交换记录，10为第几台邮件服务器
svr7		A	192.168.4.7
mail		A	192.168.4.207

systemctl restart named

pc207
echo nameserver 192.168.4.7 > /etc/resolv.conf
yum -y install bind-utils
host -t MX example.com		#查看在example.com域中邮件服务器是谁
rpm -q postfix
vim /etc/postfix/main.cf

99 myorigin = example.com
116 inet_interfaces = all
164 mydestination = example.com

systemctl restart postfix
useradd yg
useradd xln
yum -y install mailx

mail交互式语法格式：
mail -s 邮件标题	-r 发件人	  收件人
mail非交互式语法格式：
echo  邮件内容 |  mail  -s  邮件标题     -r   发件人   收件人

mail -s 'test01' -r yg xln
mail -u xln
echo "yg" | mail -s 'test02' -r yg xln
mail -u xln


分离解析
svr7
vim /etc/named.conf
options {
	directoy "/var/named"
};
view "VIP" {
	math-clients {192.168.4.207;};
	zone "tedu.cn" IN {
	type master;
	file "tedu.cn.zone";
};
};
view "other" {
	math-clients {any;};
	zone "tedu.cn" IN {
	type master;
	file "tedu.cn.other";
};
};
cp -p /var/named/named.localhost /var/named/tedu.cn.zone
vim /var/named/tedu.cn.zone
.....
tedu.cn.	NS	svr7
svr7	A	192.168.4.7
www	A	192.168.4.100
cp -p /var/named/tedu.cn.zone /var/named/tedu.cn.other
vim /var/named/tedu.cn.other
....
tedu.cn.	NS	svr7
svr7	A	192.168.4.7
www	A	1.2.3.4

systemctl restart named



搭建PXE服务端
mount /dev/cdrom /mnt
vim /etc/yum.repos.d/mnt.repo

[development]
name=Centos7.5
enabled=1
gpgcheck=0
baseurl=file:///mnt

setenforce 0
 systemctl stop firewalld.service 
 rpm -q httpd

 yum -y install httpd
 yum -y install dhcp
rpm -q dhcp

 systemctl restart dhcpd

 rpm -q dhcp

 vim /etc/dhcp/dhcpd.conf 
 systemctl restart dhcpd
 ss -anptu | grep 67
 vim /etc/dhcp/dhcpd.conf 
cat /etc/dhcp/dhcpd.conf
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp*/dhcpd.conf.example
#   see dhcpd.conf(5) man page


subnet 192.168.4.0 netmask 255.255.255.0 {
  range 192.168.4.100 192.168.4.200;
  option domain-name-servers 192.168.4.10;
  option routers 192.168.4.254;
  default-lease-time 600;
  max-lease-time 7200;
  next-server 192.168.4.10;
  filename "pxelinux.0";
}



 systemctl restart dhcpd
 yum -y install tftp-server.x86_64 
systemctl restart tftp
 ss -anptu | head -69
 yum provides */pxelinux.0
 yum -y install syslinux
 rpm -ql syslinux | grep pxelinux.0


cp /usr/share/syslinux/pxelinux.0  /var/lib/tftpboot/
 ls /var/lib/tftpboot/

mkdir /var/lib/tftpboot/pxelinux.cfg
 ls /var/lib/tftpboot/

 cp /mnt/isolinux/isolinux.cfg /var/lib/tftpboot/pxelinux.cfg/default
ls /var/lib/tftpboot/pxelinux.cfg/

 vim /var/lib/tftpboot/pxelinux.cfg/default            



label linux
  menu label Install CentOS 7
  menu default
  kernel vmlinuz
  append initrd=initrd.img ks=http://192.168.4.10/ks.cfg 


 cp /mnt/isolinux/vesamenu.c32 /mnt/isolinux/splash.png /mnt/isolinux/initrd.img /mnt/isolinux/vmlinuz /var/lib/tftpboot/
 ls /var/lib/tftpboot/



 systemctl restart dhcpd
 systemctl restart tftp


 yum -y install httpd
systemctl restart httpd
 mkdir /var/www/html/centos
 mount /dev/cdrom /var/www/html/centos/

 yum -y install system-config-kickstart.noarch 
 yum -y install system-config-kickstart
 system-config-kickstart 


     	

基本时区	   shanghai
root密码   A
确认密码   A
安装方法   HTTP
HTTP服务器   192.168.4.10
HTTP目录	     centos
引导装载程序选项        安装新引导装载程序
分区信息      清除主引导记录
分区信息	   初始化磁盘标签
分区信息      添加  挂载点：/
分区信息      添加  使用磁盘上全部未用空间
网络配置     添加网络配置   网络设备  eth0
防火墙配置     SELinux：禁用
软件包选择      系统  基本
文件   保存
cp /root/ks.cfg /var/www/html/ks.cfg

systemctl restart dhcpd
systemctl restart tftp
 systemctl restart httpd











数据库
数据库
数据库
默认端口号  3306
svr7



setenforce 0
systemctl stop firewalld.service 
tar -xf mysql-5.7.17.tar 
ls
yum -y install mysql-community-*.rpm
rpm -qa | grep mysql
ls /etc/my.cnf
ls /var/lib/mysql
systemctl start mysqld
systemctl enable mysqld		-- enable开机自启
netstat -anptu | grep :3306


链接数据库用初始密码登录

grep password /var/log/mysqld.log
mysql -uroot -p' '
mysql>
alter user root@"localhost" identified by "123qqq...A";
show databases;
exit

修改密码策略
查找相关密码的策略
mysql>
show variables like "%password%";		-- 过滤密码字样的，%匹配0个或者多个
set global validate_password_policy=0;		-- 修改密码策略
set global validate_password_length=6;		-- 修改密码长度
alter user root@"localhost" identified by "tarena";

永久修改密码策略
vim /etc/my.cnf
[mysqld]
validate_password_policy=0
validate_password_length=6

systemctl restart mysqld
mysql -uroot -ptarena
mysql>
alter user root@"localhost" identified by "123456";
exit

mysql -uroot -p123456


链接数据库
mysql -h服务端ip地址   -u用户名    -p密码 [数据库名]

svr7
mysql -uroot -p'123456' mysql
mysql>
select database();		-- 查看当前在哪个数据库下
create database bbsdb;	-- 创建库
create database BBSDB;	
show databases;		-- 查看库
drop database BBSDB;	-- 删除库
use bbsdb;		-- 切换库
select database();		-- 显示当前所在库
select user();		-- 显示链接用户
show tables;		-- 显示已有表


mysql>
use bbsdb;
Database changed

select database();
create table user(name char(10),age int, homedir char(20));		-- 创建表
show tables;
desc user;			-- 查看表结构
select * from bbsdb.user;
select * from user;
insert into bbsdb.user values("tom",18,"beijing");		-- 插入记录
select * from user;
insert into user values ("abc",20,"chifeng");
select * from user;			--查看添加完成的表
select name from user;		-- 只查name字段
select name,age,from user;		-- 只查name和age字段

update bbsdb.user set homedir="china";		-- 更新表数据
select * from user;
delete from bbsdb.user;			-- 删除表数据，但表还在
show tables;
select * from user;
drop table bbsdb.user;			-- 删除表
show tables;
create table user(name char(10),age int, homedir char(20));
show tables;
show create table bbsdb.user\G
create table 学生表(姓名 char(15),地址 varchar(20)) DEFAULT CHARSET=utf8;	-- 设置字符集为utf8,支持中文
show tables;
show tables;
desc 学生表；
insert into 学生表 values("张三丰","武当山");
select * from 学生表;






案例1：构建mysql服务
1、虚拟机svr7上构建mysql数据库服务

setenforce 0
systemctl stop firewalld.service 
tar -xf mysql-5.7.17.tar 
ls
yum -y install mysql-community-*.rpm
rpm -qa | grep mysql
ls /etc/my.cnf
ls /var/lib/mysql
systemctl start mysqld
systemctl enable mysqld		
netstat -anptu | grep :3306


2、数据库管理员密码设置为tarena

grep password /var/log/mysqld.log
mysql -uroot -p' '
mysql>
show databases;
alter user root@"localhost" identified by "123qqq...A";
show databases;
exit
show variables like "%password%";		
set global validate_password_policy=0;		
set global validate_password_length=6;		
alter user root@"localhost" identified by "tarena";


案例2：数据库基本原理
  1）使用mysql命令连接数据库，并查看连接用户
	select user();
  2）创建数据库名为test
	create database test;
  3）在数据库test下创建一个名为stu的表，表记录包含如下内容：
      学号，姓名，性别，手机号，通信地址  （注：性别用enum类型）
	create table stu(学号 char(20),姓名 char(15),性别 char(2),手机号 char(20),通信地址 varchar(20)) DEFAULT CHARSET=utf8;
  4）往stu表里添加如下记录：
       NSD131201  张三   男    13012345678   朝阳区劲松南路
       NSD131202  李四   男    18722223333   海淀区北三环西路
       NSD131203  韩梅梅  女    18023445678   东城区珠市口	
	
insert into test.stu values("NSD131201","张三","男",13012345678,"朝阳区劲松南路");
insert into test.stu values("NSD131202","李四","男",18722223333,"海淀区北三环西路");
insert into test.stu values("NSD131203","韩梅梅","女",18023445678," 东城区珠市口");

  5）删除stu表记录

delete from bbsdb.user;			
show tables;

  6）删除stu表

drop table bbsdb.user;
show tables;

  7）删除test库

drop database test;
show databases;


==============================================================================================================================================================================================================================================================================================================



tinyint unsigned	(小数四舍五入为整数，正整数）
tinyint		（整数）
float(6,2)		(自然数）


### 时间日期字段用法

```sql
create table t5(name char(10),s_year year,uptime time,birthday date,party datetime);
desc t5;
insert into t5 values ('bob',1990,08000,20231120,202030214183000);
select * from t5;
select curtime();				-- 获取当前系统时间
select curdate();				-- 获取当前系统日期
select now();				-- 获取当前系统日期和时间
select year(now());				-- 从当前系统时间中只取出年份
select month(now());				-- 从当前系统时间中只取出月份
select day(now());				-- 从当前系统时间中只取出天数
select date(now());				-- 从当前系统中只取出年月日
select time(now());				-- 从当前系统中只取出时分秒
insert into t5 values ('tom',2000,time(now()),curdate(),now());		-- 利用时间函数插入表记录
select * from t5;
create table t6(name char(10),meeting datetime,party timestamp);
desc t6;
insert into t6 values('bob',now(),now());
select * from t6;
insert into t6(name,meeting) values ('bob',20230214103000);		-- 当未给timestamp字段赋值时，自动以当前系统时间赋值
select * from t6;
insert into t6(name,party) values ('tom',19730701083000);		-- 当未给datetime字段赋值时，为NULL（空）
select * from t6;
desc t5;
select s_year from t5;
insert into t5(s_year) values(03),(81);
select s_year from t5;
```



#### enum  set字段用法

```sql
create table t7(name char(10),sex enum('boy','girl'),likes set('eat','money','play','game','music'));
desc t7;
insert into t7 values ('bob','boy','eat,money');
select * from t7;


insert into t2 values (null,null,null);	-- 插入全为空
insert into t2(name) values('tom')	-- name字段不为空，其余为空

create table t3(name char(10) not null,age tinyint unsigned default 18,class char(8) not null default 'NSD2006');
desc t3;
insert into t3(name) values('zs');
select * from t3;			-- 显示name字段，其余自动赋值
insert into t3 values ('tom',29,'NSD2007');
select * from t3;			-- 正常赋值
insert into t3 values (null,null,null);	-- 失败，name字段不允许为空
insert into t3 values ("null",null,null);	-- 失败，class字段不允许为空
insert into t3 values ("null",null,"");    -- null用引号引起来代表是普通字符，直接加引号，不为空，是0个字符
select * from t3;



#### 向t1表添加字段email，不指定字段位置，默认插入到表的最后
alter table t1 add email varchar(30) not null default "stu@tedu.cn";
desc t1;

#### 向t1表最前面添加字段stu_id
alter table t1 add stu_id char(9) first;
desc t1;

#### 向t1表中name字段后插入新字段sex
alter table t1 add sex enum('boy','girl') default 'boy' after name;
desc t1;

#### 使用modify修改t1表的sex字段，设置默认值为man
alter table t1 modify sex enum('man','woman','boy')default 'man';	--字段里需要包含原表中的数据类型boy，否则冲突
desc t1;
select * from t1;
desc t1;


#### 修改t1表中的name字段类型，修改为varchar
alter table t1 modify name varchar(15);
desc t1;


#### 将email字段移动到sex字段的后面，其他不变
alter table t1 modify email varchar(30) not null default 'stu@tedu.cn' after sex;
desc t1;
select * from t1;		-- 数据不发生变化

#### 删除t1表中的stu_id字段
alter table t1 drop stu_id;
desc t1;
select * from t1;


#### 删除t1表中的多个字段（email和party）
alter table t1 drop email,drop party;
desc t1; 
select * from t1;

#### 修改t1表的name字段名称改为abc
desc t1;
alter table t1 change name abc varchar;
desc t1;



#### 将t1表重命名为stuinfo
alter table t1 rename stuinfo;
show tables;
desc stuinfo;




index  		普通索引
unique 		唯一索引
fulltext  		全文索引
primary key	主键
foreign  key 	外键


查看索引
show index from t1\G;

创建索引
create table t1( name char(15),class char(9), sex enum('boy','girl'), index(name),index(class) );

create table t2(name char(16),pay float(5,2));
desc t2;
create index xxx on t2(name);
desc t2;


删除索引
drop index name on t1;
desc t1;
show index from t1\G;






主键
create table t3(name char(16) primary key,age int);
desc t3;
insert into t3 values ('bob',29);
mysql> insert into t3 values ('bob',39);
ERROR 1062 (23000): Duplicate entry 'bob' for key 'PRIMARY'
insert into t3 values ('tom',39);
select * from t3;
mysql> insert into t3 values (null,39);
ERROR 1048 (23000): Column 'name' cannot be null
select * from t3;
show tables;
desc t1;
alter table t1 add primary key(name);
desc t1;
alter table t1 drop primary key;
desc t1;



主键auto_increment连用
语法格式：字段名  类型  primary key auto_increment
功能：字段通过自加一方式赋值
auto_increment：自增长（如果不给自增长字段赋值，该字段每次自加1给自己赋值），自增长通常和主键一起连用

create table t1( id int primary key auto_increment,name char(10),age tinyint,class char(10));
desc t1;
insert into t1(name,age,class) values('bob',19,'nsd2002');
select * from t1;
insert into t1(name,age,class) values('tom',29,'nsd2002');
select * from t1;
insert into t1(name,age,class) values('tom',29,'nsd2003');
select * from t1;

自增长字段也可以给字段赋值，下次该字段自增长时，从新的数字自加1赋值
insert into t1 values (7,'lucy',18,'nsd2011');
select * from t1;
insert into t1 (name,age,class) values('toma',29,'nsd2003');
select * from t1;

主键的值不能为null，也不能重复，当给一个字段添加了主键，并设置自增长，在赋值时如果该字段的值为null，也可以成功插入数据
因为自增长属性会自动加1插入数据
insert into t1 values (null,'john',19,'nsd2011');
select * from t1;


设置了自增长字段id的表，当删除所有数据后，重新插入数据如果不指定id字段的值，默认还是以前的id值继续增长
delete from t1;
insert into t1 (name,age,class) values ('tomb',29,'nsd2003');
select * from t1;




create table t2 (cip char(15),port int, status enum("yes","no"),primary key(cip,port));
desc t2;
insert into t2 values('1.1.1.1',21,'no');		--成功
select * from t2;
insert into t2 values('1.1.1.1',21,'yes');		--失败，cip字段和port字段同时重复
insert into t2 values('1.1.1.1',22,'yes');		--cip字段值相同，port字段值不同，成功
insert into t2 values('2.1.1.1',22,'yes');		--cip字段值不同，port字段值相同，成功
select * from t2;


删除表的复合主键
alter table t2 drop primary key;
desc t2;


没有复合主键后，插入记录允许重复，不允许赋空值，约束条件NULL限制
insert into t2 values('2.1.1.1',22,'yes');
insert into t2 values(null,null,'yes');


在已有表里创建复合主键
语法格式：alter table 表名  add  primary key (字段名1，字段名2....)
alter table t2 add primary key(cip,port);		--创建失败，表中的记录有重复
delete from t2;
alter table t2 add primary key(cip,port);
desc t2;
insert into t2 values('2.2.2.2',22,'no');
select * from t2;




create table yg(yg_id int primary key auto_increment,name char(15))engine=innodb;
desc yg;
insert into yg(name) values('bob');
insert into yg(name) values('tom');
select * from yg;
create table gz( gz_id int,pay float(5,2),foregin key(gz_id) references yg(yg_id) on update cascade on delete cascade)engine=innodb;
show create table gz\G		--通过查看建表过程，来查看表是否创建外键

外键设置成功之后，gz（工资表）插入数据时，编号必须在yg（员工表）的yg_id范围之内
select * from yg;
insert into gz values(1,300.00);
insert into gz values(2,500.00);
insert into gz values(3,300.00);		--插入失败，编号必须在yg（员工表）编号范围之内


在yg表里插入一条记录，用户名为john，编号采用自增长
insert into yg(name) values('john');
select * from yg;


在gz表里插入记录，是否可以插入
insert into gz values(3,300.00);
select * from gz;


测试同步删除和同步更新
delete from yg where yg_id=3;
select * from yg;
select * from gz;
update yg set yg_id=6 where name="tom";
select * from yg;
select * from gz;


设置成外键的表字段也必须将其设置为主键,否则会出现对于同一个编号可以插入多次数据的情况,也会出现编号为null,插入数据同样成功的情况


desc gz;
insert into gz values(1,200.00);
insert into gz values(6,200.00);
select * from gz;
insert into gz values(null,200.00);
select * from gz;


将表中的外键字段设置为主键
delete from gz;
select * from gz;
alter table gz add primary key(gz_id);
desc gz;
insert into gz values(null,200.00);
insert into gz values(1,200.00);
insert into gz values(1,200.00);
insert into gz values(6,200.00);
insert into gz values(6,200.00);
insert into gz values(7,200.00);

删除表当一个表被其他表所依赖时,该表则不可以被删除
删除方法有2种:
1)删除表中的外键
2)先删除gz (工资表)
drop table yg;	#直接删除失败

删除外键:
语法格式:
alter table 表名 drop foreign key 名称;
show create table gz\G
alter table gz drop foreign key gz_ibfk_1;
show create table gz\G
drop table yg;




数据导入/导出

检索目录
show variables like '%file%';		--查看文件默认的检索目录
system ls /var/lib/mysql-files;		--在mysql下执行Linux系统命令
exit

修改检索目录
vim /etc/my.cnf
secure_file_priv="/myload"

mkdir /myload
chown mysql /myload/
ls -ld /myload
systemctl restart mysqld
mysql -uroot -p'123qqq...A'
show variables like '%file%';



数据导入：把系统文件的内容存储到数据库的表里，默认只有数据库管理员root用户有数据导入权限
数据导入步骤：
1、建表
2、拷贝文件到检索目录下
3、导入数据

语法格式：load data infile "/目录名/文件名" into table 库名.表名  fields terminated by "分隔符" lines terminated by "\n";

use test;
create table test.user( name char(50),password char(1),uid int,gid int,comment varchar(150),homedir char(100),shell char(50));
desc user;
select * from user;
system cp /etc/passwd /myload;
system ls /myload;

passwd

load data infile "/myload/passwd" into table user fields terminated by ":" lines terminated by "\n";
select * from user;

为了方便管理，在user表的最前面设置行号字段id（主键和自增长）

alter table user add id int primary key auto_increment first;
select * from user;

数据导入注意事项
1、字段分隔符要与文件一致
2、表字段类型和字段个数要与文件内容匹配
3、导入数据时指定文件的绝对路径




数据导出：
语法格式：
格式1：select 命令 into outfile  "/目录名/文件名";
格式2：select 命令 into outfile  "/目录名/文件名"  fields terminated by "分隔符";
格式3：select 命令 into outfile  "/目录名/文件名"  fields terminated by "分隔符" lines terminated by "\n";

从user表中，查询出name，homedir，shell字段的前3行记录

select name,homedir,shell from user limit 3;

导出查询出的数据到user.txt文件中，不指定分隔符时，默认以一个tab为分隔符

select name,homedir,shell from user limit 3 into outfile "/myload/user.txt";
system cat /myload/user.txt;

导出查询出的数据到user2.txt文件中，各字段之间以#分隔

select name,homedir,shell from user limit 3 into outfile "/myload/user2.txt" fields terminated by "###";
system cat /myload/user2.txt


导出查询出的数据到user3.txt文件中，指定行的间隔符为！默认以"\n"换行符分隔

select name,homedir,shell from user limit 3 into outfile "/myload/user3.txt" fields terminated by "###" lines terminated by "!!!";
system cat /myload/user3.txt;

数据导出注意事项：
1、导出数据行数由SQL查询决定
2、导出的是表记录，不包含字段名
3、自动创建存储数据的文件
4、存储数据文件，具有唯一性



表管理记录
insert into user values(30,'bob','x',3001,3001,'test user','/home/bob','/sbin/nologin');
select * from user;
insert into user values(31,'bob','x',3001,3001,'test user','/home/bob','/sbin/nologin'),(41,'tom','x',3002,3002,'student','/home/tom','/sbin/nologin');
select * from user;
insert into user(name,homedir) values('alice','/home/alice');
select * from user;
insert into user(name) values('alice'),('jack'),('toma');
select * from user;

注意事项：
1、字段值要与字段类型相匹配
2、字符类型的字段，要用""括起来
3、依次给所有字段赋值时，字段名可以省略
4、只给部分字段赋值时，必须明确写出对应的字段名称
5、没有赋值的字段使用默认值或自增长赋值
6、新纪录追加在末尾



查询表记录
语法格式：
格式1：查看所有记录
	select   字段1，字段1.....字段N  from 库名.表名
格式2：条件查询
	select   字段1，字段1.....字段N  from 库名.表名  where  条件表达式


select * from user;
select id,name from test.user;
select id,name from test.user where id<=2;
select id,name from test.user where id<4;


注意事项：
1、*代表所有字段
2、查看当前库表记录时库名可以省略
3、字段列表决定显示列个数
4、条件决定显示行个数



条件匹配更新
语法格式：
格式1：批量更新
	update  库名.表名  set  字段名=值，字段名=值，字段名=值........
格式2：条件匹配更新
	update  库名.表名  set  字段名=值，字段名=值，字段名=值........  where表达式

update user set password='A',comment='student';
update user set password='x',comment='root' where name='root';


注意事项：
1、字段值要与字段类型相匹配
2、对于字符类型的字段，值要用双引号括起来
3、若不使用where限定条件，会更新所有记录
4、限定条件时，只更新匹配条件的记录




删除表记录
基本匹配条件

数值比较
字段类型必须是数值类型

select * from user where uid!=0;
select * from user where id=1;
select name,uid,gid from user where uid=gid;
select name,uid from user where uid<10;




字符比较
字段类型必须是字符类型

select name from user where shell='/sbin/nologin';
select name,shell from user where shell!='/sbin/nologin';
select name,shell from user where name='root';
select name,id from user where name='root';
insert into user(name) values(null),("null"),(""),(NULL);
select name from user;
select name,id from user where name is null;
select name,id from user where name is not null;
select name,id from user where name="";





虚拟机A
yum -y install httpd
systemctl start httpd
yum -y install php php-mysql
tar -xf phpMyAdmin-2.11.11-all-languages.tar.gz
ls phpMyAdmin-2.11.11-all-languages
mv phpMyAdmin-2.11.11-all-languages /var/www/html/phpmyadmin
ls /var/www/html/
ls /var/www/html/phpmyadmin/
cd /var/www/html/phpmyadmin/
cp config.sample.inc.php config.inc.php
vim config.inc.php
17  $cfg['blowfish_secret'] = 'wj123';
31  $cfg['Servers'][$i]['host'] = 'localhost';
systemctl restart httpd
firefox http://192.168.4.10/phpmyadmin


==============================================================================================================================================================================================================================================================================================================

```



---

















































































































































































































































































































































































































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

### 案例2（重复）(最小化装机）： 配置网络参数，要求如下：
1. 永久设置主机名为 A.tedu.cn

    ```shell
    echo A.tedu.cn > /etc/hostname
    hostname A.tedu.cn
    
    hostname
    ```

2. 永久配置静态IP地址为192.168.4.20/24

    ```shell
    nmcli connection modify ens33 ipv4.addresses 192.168.4.20/24 connection.autoconnect yes

    #安装yum源
    mount /dev/cdrom /mnt/	#先连接光盘
    echo "/dev/cdrom /mnt iso9660 defaults 0 0" >> /etc/fstab
    
    echo "[mnt]
    name=Centos7.5
    baseurl=file:///mnt
    enable=1
    gpgcheck=0" > /etc/yum.repos.d/mnt.repo
    
    rm -rf /etc/yum.repos.d/CentOS-*
    yum clean all
    yum repolist
    
    yum -y install vim-enhanced	#安装vim包
    yum -y install net-tools	#安装ifconfig支持包
    yum -y install bash-completion	#安装Tab键支持包
    reboot	#重启以生效
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
    
    yum -y install httpd
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
    echo 192.168.4.10 server0.example.com >> /etc/hosts
    echo 192.168.4.10 www0.example.com >> /etc/hosts
    echo 192.168.4.10 webapp0.example.com >> /etc/hosts
    
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
    ls /nfs
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
	svr7	A	192.168.4.7
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
	svr7	A	192.168.4.7
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
	svr7	A	192.168.4.7
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
	svr7	A	192.168.4.7
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


案例

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210601185635109.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDM0MDEyOQ==,size_16,color_FFFFFF,t_70)

web 服务器和 DNS 服务结合（web 服务器做需要开启基于域名的虚拟主机，DNS 需要使用分离解析技术）

| - | 主机名 | ip地址 |
| -- | -- | -- |
| 虚拟机 A | A.tedu.cn | 192.168.4.10 |
| 虚拟机 B | B.tedu.cn | 192.168.4.20 |
| 虚拟机 C | C.tedu.cn | 192.168.4.208 |
| 虚拟机 svr7 | svr7.tedu.cn | 192.168.4.7 |
| 虚拟机 pc207 | pc207.tedu.cn | 192.168.4.207 |

虚拟机 A 操作：

```shell
#1.安装软件包 httpd
yum -y install httpd

#2.建立修改调用配置文件
vim /etc/httpd/conf.d/nsd01.conf
    <VirtualHost *:80>
        ServerName www.qq.com
        DocumentRoot /var/www/qq
    </VirtualHost>
    <VirtualHost *:80>
        ServerName www.163.com
        DocumentRoot /var/www/163
    </VirtualHost>

mkdir /var/www/qq /var/www/163
echo '<h1> Web1 QQ' > /var/www/qq/index.html
echo '<h1> Web1 163' > /var/www/163/index.html

systemctl restart httpd
```

虚拟机 B 操作：

```shell
yum -y install httpd

#从虚拟机A拷贝nsd01配置文件
scp /etc/httpd/conf.d/nsd01.conf 192.168.4.20:/etc/httpd/conf.d/
mkdir /var/www/qq /var/www/163
echo '<h1>Web2 QQ' > /var/www/qq/index.html
echo '<h1>Web2 163' > /var/www/163/index.html

systemctl restart httpd
```

虚拟机 svr7 操作：

```shell
#1、修改主配置文件
vim /etc/named.conf
        ……
        view "vip" {
            match-clients { 192.168.4.207; };
            zone "163.com" IN {
                type master;
                file "163.com.zone";
            };
            zone "qq.com" IN {
                type master;
                file "qq.com.zone";
            };
        };
        view "other" {
            match-clients { any; };
            zone "163.com" IN {
                type master;
                file "163.com.other";
            };
            zone "qq.com" IN {
                type master;
                file "qq.com.other";
            };
        };

#2、建立地址库文件
cd /var/named/
cp -p qq.com.zone 163.com.zone
cp -p qq.com.zone 163.com.other

vim 163.com.zone
        …….
        163.com. NS svr7
        svr7 A 192.168.4.7
        www A 192.168.4.10

vim qq.com.zone
        …
        qq.com. NS svr7
        svr7 A 192.168.4.7
        www A 192.18.4.10

vim 163.com.other
        …
        163.com. NS svr7
        svr7 A 192.168.4.7
        www A 192.168.4.20

vim qq.com.other
        ……
        qq.com. NS svr7
        svr7 A 192.168.4.7
        www A 192.168.4.20

systemctl restart named
```

测试：指定 DNS 服务器地址
虚拟机pc207

```shell
echo nameserver 192.168.4.7 > /etc/resolv.conf
curl www.qq.com
curl www.163.com
```

虚拟机C
```shell
echo nameserver 192.168.4.7 > /etc/resolv.conf
curl www.qq.com
curl www.163.com
```

## 6.2 练习
### 案例19：普通NFS共享的实现
1. 只读的方式共享目录 /public，只允许192.168.4.0网段访问

    ```shell
    rpm -q nfs-utils
    yum -y install nfs-utils
    mkdir /public
    touch /public/p1.txt
    
    echo "/public *(ro)" >> /etc/exports
    ```

2. 可读写共享目录/protected，允许所有人访问

    ```shell
    mkdir /protected
    touch /protected/p2.txt
    echo "/protected 192.168.4.0/24(rw,no_root_squash)" >> /etc/exports
    
    systemctl restart nfs-server
    systemctl enable nfs-server
    systemctl stop firewall.service
    ```

3. 在虚拟机 B上访问NFS共享目录
3.1. 将A 的 /public 挂到本地 /nfsmount

    ```shell
    #虚拟机B操作
    yum -y install nfs-utils
    showmount -e 192.168.4.10
    
    mkdir /nfsmount
    mount 192.168.4.10:/public /nfsmount
    df -h
    ls /nfsmount
    ```


4. 这些文件系统在系统启动时自动挂载
4.1. 将/protected实现触发挂载到/abc/mynfs下

    ```sehll
    mkdir -p /abc/mynfs
    
    echo "192.168.4.10:/public /nfsmount nfs defaults,_netdev 0 0" >> /etc/fstab
    echo "192.168.4.10:/protected /abc/mynfs nfs defaults,_netdev 0 0" >> /etc/fstab
    
    umount /nfsmount
    mount -a
    df -h
    ```



### 案例20：iscsi磁盘共享

0. 配置 虚拟机A提供 iSCSI 服务，要求如下：
1. 磁盘名为iqn.2020-08.tedu.cn:server0
2. 服务端口为 3260
3. 使用 store（后端存储的名称） 作其后端卷，其大小为 3GiB
4. 配置客户端ACL为iqn.2020-08.tedu.cn:desktop0
5. 配置虚拟机B使用 虚拟机svr7提供 iSCSI 服务

```shell
partprobe /dev/sdc
lsblk
yum -y install targetcli
systemctl stop firewalld
targetcli
	ls
	backstores/block create dev=/dev/sdc1 name=store
	iscsi/ create iqn.2020-08.tedu.cn:server0
	iscsi/iqn.2020-08.tedu.cn:server0/tpg1/luns create /backstores/block/store
	iscsi/iqn.2020-08.tedu.cn:server0/tpg1/acls create iqn.2020-08.tedu.cn:desktop0
	ls
	exit
systemctl restart target.service
```

```shell
#虚拟机B
yum -y install iscsi-initiator-utils
rpm -q iscsi-initiator-utils

echo "InitiatorName=iqn.2020-08.tedu.cn:desktop0" > /etc/iscsi/initiatorname.iscsi

systemctl restart iscsid
iscsiadm --mode discoverydb --type sendtargets --portal 192.168.4.10 --discover

systemctl restart iscsi	
systemctl enable iscsi	

systemctl restart iscsi
	
lsblk
```


### 案例21：NTP时间同步
0. 在虚拟机A设置ntp时间同步
1. 设置时间服务器上层与0.centos.pool.ntp.org同步
2. 设置本地服务器层数为10
3. 允许192.168.4.0/24网络的主机同步时间
4. 客户端B验证时间是否同步

```shell
yum -y install chrony
rpm -qc chrony	#查看配置文件（.conf结尾的文件）

vim /etc/chrony.conf
	server 0.centos.pool.ntp.org iburst	#网络标准时间服务器（快速同步）
	allow 192.168.4.0/24	#允许同步时间的主机网络段
	local statum 10	#访问层数

systemctl restart chronyd	#重启时间同步服务

setenforce 0
systemctl stop firewalld	#关闭防火墙
```


```shell
#虚拟机B
vim /etc/chrony.conf
	server 192.168.4.10 iburst	#指定要同步时间的服务器（192.168.4.7）
systemctl restart chronyd	#重启时间同步服务
chronyc sources -v	#验证时间是否同步成功
```


### 案例22：利用FTP服务实现网络yum源
1. 虚拟机A构建ftp服务

    ```shell
    yum -y install vsftpd
    systemctl restart vsftpd
    ```


2. 利用ftp服务提供Centos7光盘内容，自定义yum仓库内容

    ```shell
    ls /var/ftp/
    mkdir /var/ftp/centos
    mount /dev/cdrom /var/ftp/centos/
    ls /var/ftp//centos/
    firefox ftp://192.168.4.10/centos
    
    #虚拟机软件-toos.tar.gz -> /root
    tar -xf tools.tar.gz
    ls tools/other/
    mkdir /var/ftp/other/
    cp tools/other/* /var/ftp/other/
    ls /var/ftp/other
    createrepo /var/ftp/other/
    ls /var/ftp/other
    ```

3. 利用虚拟机B进行测试，并安装软件包sl


    ```shell
    vim /etc/yum.repos.d/mnt.repo
    	[centos]
    	name=Centos7.5
    	baseurl=ftp://192.168.4.10/centos
    	gpgcheck=0
    	[myrpm]
    	name=myyum
    	baseurl=ftp://192.168.4.10/other
    	gpgcheck=0
    
    yum clean all
    yum repolist
    
    yum -y install sl
    sl
    ```
    

## 6.8 练习
### 案例1：构建mysql服务
1. 虚拟机svr7上构建mysql数据库服务

```shell
systemctl stop firewalld.service 
setenforce 0
tar -xf mysql-5.7.17.tar
yum -y install mysql-community-*.rpm
systemctl start mysqld
systemctl enable mysqld
```

2. 数据库管理员密码设置为tarena

```shell
vim /etc/my.cnf
	validate_password_policy=0
	validate_password_length=6

grep password /var/log/mysqld.log
```

```sql
mysql -uroot -p'mysqld.log中的密码'
	set global validate_password_policy=0;
	set global validate_password_length=6;
	alter user root@localhost identified by "tarena";
	exit
mysql -uroot -ptarena
```

### 案例2：数据库基本原理
1. 使用mysql命令连接数据库，并查看连接用户

```sql
mysql -uroot -ptarena
	select user();
```

2. 创建数据库名为test

```sql
create database test;
use test;
```

3. 在数据库test下创建一个名为stu的表，表记录包含如下内容：
      学号，姓名，性别，手机号，通信地址  （注：性别用enum类型）

```sql
create table stu(学号 char(10), 姓名 char(15), 性别 enum('男','女'), 手机号 char(11), 通信地址 varchar(20)) DEFAULT CHARSET=utf8;
```

4. 往stu表里添加如下记录：

| 学号 | 姓名 | 性别 | 手机号 | 通信地址 |
| -- | -- | -- | -- | -- |
| NSD131201 | 张三 | 男 | 13012345678 | 朝阳区劲松南路 |
| SD131202 | 李四 | 男 | 18722223333 | 海淀区北三环西路 |
| NSD131203 | 韩梅梅 | 女 | 18023445678 | 东城区珠市口 |

```sql
insert into stu values("NSD131201","张三","男",13012345678,"朝阳区劲松南路");
insert into stu values("NSD131202","李四","男",18722223333,"海淀区北三环西路");
insert into stu values("NSD131203","韩梅梅","女",18023445678,"东城区珠市口");
select * from stu;
```

5. 删除stu表记录

```sql
delete from test.stu;
select * from stu;
```

6. 删除stu表

```sql
drop table test.stu;
show tables;
```

7. 删除test库

```sql
drop database test;
show databases;
```

    
    

## 6.11练习
### 案例1：构建mysql服务器
要求如下：
1. 在虚拟机svr7上构建mysql服务

```sql
systemctl stop firewalld.service 
setenforce 0
tar -xf mysql-5.7.17.tar
yum -y install mysql-community-*.rpm
rpm -qa | grep mysql
systemctl start mysqld
systemctl enable mysqld
netstat -anptu | grep :3306
ls /var/lib/mysql
```

2. 设置数据库管理员root本机登录密码为redhat

```shell
vim /etc/my.cnf
	validate_password_policy=0
	validate_password_length=6

grep password /var/log/mysqld.log
```

```sql
mysql -uroot -p'mysqld.log中的密码'
	show variables like "%password%"; 
	set global validate_password_policy=0;
	set global validate_password_length=6;
	alter user root@localhost identified by "redhat";
	exit
mysql -uroot -predhat
```

### 案例2：SQL命令练习
1. 连接到数据库

```sql
mysql -uroot -predhat
```

2. 查看所有的数据库

```sql
show databases;
```

3. 创建数据库名为tedu，test


```sql
create database tedu;
create database test;
```

4. 切换到数据库tedu


```sql
use tedu;
```

5. 显示当前在哪个数据库


```sql
select database();
```

6. 显示连接的用户


```sql
select user();
```

7. 删除数据库tedu

```sql
drop database tedu;
show databases;
```

8. 创建stu表，表字段包含name，homedir

```sql
create table stu(name char(10), homedir varchar(20));
```

9. 往stu表里添加记录为jim，usa；lilei，china


```sql
insert into stu values("jim", "usa");
insert into stu values("lilei", "china");
```

10. 查看表记录


```sql
select * from stu;
```

11. 只查看name字段


```sql
select name from stu;
```

12. 将homedir表记录值改为beijing


```sql
date stu set homedir="beijing";
select * from stu;
```

13. 删除表记录

```sql
delete from stu;
```

14. 删除stu表

```sql
drop table stu;
```

### 案例3：练习数据类型的使用
1. 根据如下的表结构创建对应的表并插入记录

表-1

| Field    | Type        | Null | Key | Default | Extra |
| -- | -- | -- | -- | -- | -- |
| name     | char(5)     | YES  |     | NULL    |       |
| mail     | varchar(10) | YES  |     | NULL    |       |
| homeaddr | varchar(50) | YES  |     | NULL    |       |


表-2

| Field   | Type       | Null | Key | Default | Extra |
| -- | -- | -- | -- | -- | -- |
| stu_num | int(11)    | YES  |     | NULL    |       |
| name    | char(5)    | YES  |     | NULL    |       |
| age     | tinyint(4) | YES  |     | NULL    |       |
| pay     | float      | YES  |     | NULL    |       |
| money   | float(5,2) | YES  |     | NULL    |       |

表-3

| Field     | Type     | Null | Key | Default | Extra |
| -- | -- | -- | -- | -- | -- |
| name      | char(10) | YES  |     | NULL    |       |
| you_start | year(4)  | YES  |     | NULL    |       |
| up_time   | time     | YES  |     | NULL    |       |
| birthday  | date     | YES  |     | NULL    |       |
| party     | datetime | YES  |     | NULL    |       |

表-4

| Field | Type | Null | Key | Default | Extra |
| -- | -- | -- | -- | -- | -- |
| name  | char(5) | YES  |     | NULL    |       |
| likes | set('cat','game','film','music') | YES  |     | NULL    |       |
| sex   | enum('boy','girl','no') | YES  |     | NULL    |       |

注：表3插入记录要求如下：
1. 所有字段值自定义

    ```sql
    create table b1(name char(5), mail varchar(10), homeaddr varchar(50));
    create table b2(stu_num int(11), name char(5), age tinyint(4), pay float, money float(5,2));
    create table b3(name char(10), you_start year(4), up_time time, birthday date, party datetime);
    create table b4(name char(5), likes set(`cat`,`game`,`film`,`music`), sex enum(`boy`,`girl`,`no`));
    ```

2. 用时间函数进行赋值

    ```sql
    insert into b3 values('tom', year(now()), time(now()), curdate(), now());
    ```

### 案例4：表结构练习
1. 按照表结构创建如下表，并插入记录

    ```sql
    create table b5(class char(9) DEFAULT NULL, name char(10) NOT NULL DEFAULT '', age tinyint(4) NOT NULL DEFAULT 19, likes set('a','b','c','d') DEFAULT 'a,b');
    ```

2. 只给class字段和name字段赋值

    ```sql
    insert into b5(class,name) values('class1','name1');
    ```

3. 在age字段后面添加字段值为性别（sex），默认值为boy

    ```sql
    alter table b5 add sex enum('boy', 'girl') default 'boy' after age;
    ```

4. 在表最前面添加学号（stu_id）字段

    ```sql
    alter table b5 add stu_id int(11) first;
    ```

5. 添加邮箱（email）字段，该字段不允许为空，默认值tarena@tedu.cn

    ```sql
    alte b5 add email varchar(30) not null default 'tarena@tedu.cn';
    ```

6. 修改sex字段类型，默认值为man

    ```sql
    alter table b5 modify sex enum('man','boy','girl') default 'man' after age;
    desc b5;
    ```

7. 将email字段移到age字段后面，其他属性不变
    
    ```sql
    alter table b5 modify email varchar(30) not null default 'tarena@tedu.cn' after age;
    ```

8. 删除表字段email和stu_id

    ```sql
    alter table b5 drop email,drop stu_id;
    ```

9. 将该表名改为abc

    ```sql
    rename table b5 to abc;
    ```
    
    
## 6.18练习

环境准备

1. 将虚拟机A开机
2. 关闭防火墙和SELinux

    ```shell
    systemctl stop firewalld.service 
    setenforce 0
    ```

3. 配置IP地址为192.168.4.10

    ```shell
    nmcli connection modify ens33 ipv4.method manual ipv4.addresses 192.168.4.10/24 connection.autoconnect yes 
    nmcli connection up ens33 
    ```

4. 配置本地yum源

    ```shell
    mount /dev/cdrom /mnt
    echo "[mnt]
    	name=Centos7.5
    	baseurl=file:///mnt
    	enabled=1
    	gpgcheck=0" > /etc/yum.repos.d/mnt.repo
    
    ls /etc/yum.repos.d/
    mkdir /etc/yum.repos.d/bind
    mv /etc/yum.repos.d/bind
    mv /etc/yum.repos.d/CentOS-* /etc/yum.repos.d/bind
    ls /etc/yum.repos.d/
    yum repolist
    ```

5. 构建mysql数据库

    ```shell
    systemctl stop firewalld.service 
    setenforce 0
    tar -xf mysql-5.7.17.tar
    yum -y install mysql-community-*.rpm
    systemctl start mysqld
    systemctl enable mysqld
    ```

6. 数据库管理员密码设置为123qqq...A

```shell
vim /etc/my.cnf
	validate_password_policy=0
	validate_password_length=6

grep password /var/log/mysqld.log
```

```sql
mysql -uroot -p'mysqld.log中的密码'
	show variables like "%password%"; 1
	set global validate_password_policy=0;
	set global validate_password_length=6;
	alter user root@localhost identified by "123qqq...A";
	exit
mysql -uroot -p123qqq...A
```
    
    
    
    
    练习:


1. 用命令行的形式连接到数据库

```sql
mysql -uroot -p123qqq...A
```

2. 在test库下创建一个user表

```sql
 show variables like '%file%'; --查看文件默认的检索目录 system ls /var/lib/mysql-files; --在mysql下执行Linux系统命令 exit
修改检索目录 vim /etc/my.cnf secure_file_priv="/myload"
mkdir /myload chown mysql /myload/ ls -ld /myload systemctl restart mysqld mysql -uroot -p'123qqq...A' show variables like '%file%';
数据导入：把系统文件的内容存储到数据库的表里，默认只有数据库管理员root用户有数据导入权限 数据导入步骤： 1、建表 2、拷贝文件到检索目录下 3、导入数据
语法格式：load data infile "/目录名/文件名" into table 库名.表名 fields terminated by "分隔符" lines terminated by "\n";
use test; create table test.user( name char(50),password char(1),uid int,gid int,comment varchar(150),homedir char(100),shell char(50)); desc user; select * from user; system cp /etc/passwd /myload; system ls /myload;
passwd
load data infile "/myload/passwd" into table user fields terminated by ":" lines terminated by "\n"; select * from user;
为了方便管理，在user表的最前面设置行号字段id（主键和自增长）
alter table user add id int primary key auto_increment first; select * from user;
```

3. 把存放用户信息的文件导入到test库下的user表

```sql
load data infile "/目录名/文件名" into table 库名.表名 fields terminated by "分隔符" lines terminated by "\n";
use test; create table test.user( name char(50),password char(1),uid int,gid int,comment varchar(150),homedir char(100),shell char(50)); desc user; select * from user; system cp /etc/passwd /myload; system ls /myload;
```



## 6.21 练习

环境准备
1. 将虚拟机svr7开机
2. 关闭SELiunx和防火墙

    ```shell
    systemctl stop firewalld.service 
    setenforce 0
    ```

3. 构建MySQL数据库

    ```shell
    tar -xf mysql-5.7.17.tar
    yum -y install mysql-community-*.rpm
    rpm -qa | grep mysql
    systemctl start mysqld
    systemctl enable mysqld
    netstat -anptu | grep :3306
    ls /var/lib/mysql
    ```

4. 数据库管理员密码设置为123qq..A

```shell
vim /etc/my.cnf
	validate_password_policy=0
	validate_password_length=6

grep password /var/log/mysqld.log
```

```sql
mysql -uroot -p'mysqld.log中的密码'
	show variables like "%password%"; 
	set global validate_password_policy=0;
	set global validate_password_length=6;
	alter user root@localhost identified by "123qq..A";
	exit
mysql -uroot -p123qq..A
```

5. 将/etc/passwd文件导入到test.user

```sql
show variables like '%file%';		-- 查看文件默认的检索目录
system ls /var/lib/mysql-files;		-- 在mysql下执行Linux系统命令
exit
```

```shell
# 修改检索目录
vim /etc/my.cnf
	secure_file_priv="/myload"

mkdir /myload
chown mysql /myload/
ls -ld /myload
systemctl restart mysqld
mysql -uroot -p123qq..A
	show variables like '%file%';

create database test;
use test;
create table test.user( name char(50),password char(1),uid int,gid int,comment varchar(150),homedir char(100),shell char(50));
desc user;
select * from user;
system cp /etc/passwd /myload;
system ls /myload;

load data infile "/myload/passwd" into table user fields terminated by ":" lines terminated by "\n";
select * from user;
```

6. 往user表里添加新字段id,设置类型为自增长

    ```sql
    alter table user add id int primary key auto_increment first;
    desc user;
    ```

7. 给name字段添加4条记录分别为(null,"null,",NULL)

    ```sql
    insert into user(name) values(null),("null"),(""),(NULL);
    select * from user;
    ```
    
    
   




## 6.22 练习

1. 构建mysql数据库，管理员密码为123qqq…A创建一个名为test库，将/etc/passwd文件导入到test.user

```shell
systemctl stop firewalld.service 
setenforce 0

tar -xf mysql-5.7.17.tar
yum -y install mysql-community-*.rpm
rpm -qa | grep mysql
systemctl start mysqld
systemctl enable mysqld
netstat -anptu | grep :3306
ls /var/lib/mysql

grep password /var/log/mysqld.log
```

```sql
mysql -uroot -p'mysqld.log中的密码'
	show variables like "%password%"; 
	set global validate_password_policy=0;
	set global validate_password_length=6;
	alter user root@localhost identified by "123qqq...A";
	exit
mysql -uroot -p123qqq...A
exit
```

```sql
vim /etc/my.cnf
	secure_file_priv="/myload"
cat /etc/my.cnf

mkdir /myload
chown mysql /myload/
ls -ld /myload
systemctl restart mysqld
mysql -uroot -p123qqq...A
	show variables like '%file%';

	create database test;
	show databases;
	use test;
	create table test.user( name char(50),password char(1),uid int,gid int,comment varchar(150),homedir char(100),shell char(50));
	desc user;
	select * from user;
	system cp /etc/passwd /myload;
	system ls /myload;
	system chown mysql /myload;
	load data infile "/myload/passwd" into table user fields terminated by ":" lines terminated by "\n";
	select * from user;
```

2. 在用户名字段下方添加s_year字段 存放出生年份 默认值是1990

```sql
alter table user add s_year year default 1990 after name;
```

3. 在用户名字段下方添加字段名sex 字段值只能是gril 或boy 默认值是 boy

```sql
alter table user add sex enum('girl','boy') default 'boy' after name;
```

4. 在sex字段下方添加 age字段  存放年龄 不允许输入负数。默认值 是 21

```sql
alter table user add age tinyint unsigned default 21 after sex;
```

5. 把uid字段值是10到50之间的用户的性别修改为 girl

```sql
update user set sex='girl' where uid between 10 and 50;
```

6. 统计性别是girl的用户有多少个。(count(*)统计个数)

```sql
select count(*) from user where sex="girl";
```

7. 查看性别是girl用户里 uid号 最大的用户名 叫什么。（看最大值用max）

```sql
select name from user where uid=(select max(uid) from user where sex='girl');
```

8. 添加一条新记录只给name、uid 字段赋值 值为rtestd  1000

```sql
insert into  user(name,uid) values("rtestd", 1000);
```

9. 加一条新记录只给name、uid 字段赋值 值为rtest2d   2000

```sql
insert into  user(name,uid) values("rtest2d", 2000);
```

10. 显示uid 是四位数的用户的用户名和uid值。

```sql
select name, uid from user where uid>=1000;
```

11. 显示名字是以字母r 开头 且是以字母d结尾的用户名和uid。

```sql
select name, uid from user where name regexp "^r.*d$"; 
```

12. 查看是否有名字以字母a开头 并且是以字母c结尾的用户。

```sql
select name, uid from user where name regexp "^a&c$"; 
```

13. 把 gid  在100到500间用户的家目录修改为/root

```sql
update user set comment='/root' where gid between 100 and 500;
```

14. 把用户是  root 、 bin 、  sync 用户的shell 修改为  /sbin/nologin

```sql
update user set shell='/sbin/nologin' where name in('root','bin','sync');
```

15. 查看  gid 小于10的用户 都使用那些shell

```sql
select shell from user where gid<10;
```

16. 删除  名字以字母d开头的用户。

```sql
delete from user where name regexp '^d';
```

17. 查看那些用户没有家目录

```sql
select name from user where lujing='/';
```

18. 使用系统命令useradd 命令添加登录系统的用户名为lucy

```sql
system useradd lucy;
system ls /home;
```

19. 把lucy用户的信息添加到user表里

```sql
system cat /etc/passwd
insert into user values('lucy',null,null,null,'x',1001,1001,null,'/home/lucy','/bin/bash');
```

20. 删除表中的 comment 字段

```sql
alter table user drop comment;
desc user;
```

21. 设置表中所有name字段值不允许为空

```sql
alter table user modify name char(50) not null;
```

22. 删除root用户家目录字段的值

```sql
update user set homedir=null where name='root';
```

23. 显示 gid 大于500的用户的用户名家目录和使用的shell

```sql
select name,homedir,shell from user where gid>500;
```

24. 删除uid大于100的用户记录

```sql
delete from user where uid>100;
```

25. 显示uid号在10到30区间的用户有多少个。

```sql
select count(*) from user where uid between 10 and 30;
```

26. 显示uid号是100以内的用户使用的shell。

```sql
select shell from user where uid<=100;
```

27. 显示uid号小于50且名字里有字母a 用户的详细信息

```sql
select * from user where  uid<50 and name like "%a%";
```

28. 只显示用户 root   bin   daemon  3个用户的详细信息。

```sql
select * from user where name in('root','bin','daemon');
```

29. 显示除root用户之外所有用户的详细信息。

```sql
select * from user where name!='root';
```

30. 显示名字里含字母c用户的详细信息

```sql
select * from user where name like '%c%';
```

31. 在sex字段下方添加名为pay的字段，用来存储工资，默认值15000.00

```sql
alter table user add pay float(7,2) default 15000.00 after sex;
```

32. 把所有女孩的工资修改为10000

```sql
update user set pay=10000.00 where sex='girl';
```

33. 把root用户的工资修改为30000

```sql
update user set pay=30000 where name='root';
```

34. 给adm用户涨500元工资

```sql
update user set pay=pay+500 where name='adm';
```

35. 查看所有用户的名字和工资

```sql
select name,pay from user;
```

36. 查看工资字段的平均值（平均值用avg）

```sql
select avg(pay) from user;
```

37. 显示工资字段值小于平均工资的用户名

```sql
select name from user where pay<(select avg(pay) from user);
```

38. 查看女生里uid号最大用户名

```sql
select name from user where  uid=(select max(uid) from user where sex='girl');
```

39. 查看bin用户的uid gid 字段的值 及 这2个字段相加的和

```sql
select uid,gid,uid+gid from user where name='bin';
```


40. 显示uid号最小的前10个用户的信息

```sql
select * from user order by uid limit 10;
```

41. 显示表中第10条记录到第15条记录

```sql
select * from user limit 9,5;
```

42. 统计name字段不为空有多少条记录

```sql
select count(*) from user where name is not null;
```

    
    
    
> 如有侵权，请联系作者删除