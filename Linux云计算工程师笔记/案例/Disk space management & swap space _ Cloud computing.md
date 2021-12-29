@[TOC]( Disk space management & swap space | Cloud computing )

---
# 1 案例1：硬盘分区及格式化
## 1.1 问题
本例要求熟悉硬盘分区结构，使用fdisk分区工具在磁盘 /dev/sdb 上按以下要求建立分区：

1. 采用默认的 msdos 分区模式
2. 第1个分区 /dev/sdb1 的大小为 200MiB
3. 第2个分区 /dev/sdb2 的大小为 2000MiB
4. 第3个分区 /dev/sdb3 的大小为 1000MiB

完成分区后，能够配置开机自动挂载 /dev/sdb2 分区：

1. 文件系统类型为 EXT4
2. 将其挂载到 /mnt/part2 目录

## 1.2 方案
fdisk分区工具用来建立msdos分区方案，其交互模式中的主要指令如下：

- m：列出指令帮助
- p：查看当前的分区表信息
- n：新建分区
- d：删除分区
- q：放弃分区更改并退出
- w：保存对分区表所做的更改

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：新建分区表**

1）打开fdisk工具，操作磁盘/dev/sdb
```shell
[root@server0 ~]# fdisk  /dev/sdb
Welcome to fdisk (util-linux 2.23.2).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.
Device does not contain a recognized partition table
Building a new DOS disklabel with disk identifier 0x9ac1bc10.
Command (m for help):                         //交互操作提示信息
```
2）新建第1个分区/dev/sdb1
```shell
Command (m for help): n                                  //新建分区
Partition type:
   p   primary (0 primary, 0 extended, 4 free)
   e   extended
Select (default p): p                                 //类型为p（主分区）
Partition number (1-4, default 1): 1                     //分区编号1
First sector (2048-20971519, default 2048):              //起始位置默认
Using default value 2048
Last sector, +sectors or +size{K,M,G} (2048-20971519, default 20971519): +200M  
Partition 1 of type Linux and of size 200 MiB is set      //结束位置+200MiB大小
Command (m for help): p                                  //确认当前分区表
.. ..
   Device Boot      Start         End      Blocks   Id  System
/dev/sdb1            2048      411647      204800   83  Linux
```
3）新建第2个分区/dev/sdb2
```shell
Command (m for help): n
Partition type:
   p   primary (1 primary, 0 extended, 3 free)
   e   extended
Select (default p): p                                 //类型为p（主分区）
Partition number (2-4, default 2): 2                    //分区编号2
First sector (411648-20971519, default 411648):         //起始位置默认
Using default value 411648
Last sector, +sectors or +size{K,M,G} (411648-20971519, default 20971519): +2000M
Partition 2 of type Linux and of size 2 GiB is set       //结束位置+2000MiB大小
Command (m for help): p                                  //确认当前分区表
.. ..
   Device Boot      Start         End      Blocks   Id  System
/dev/sdb1            2048      411647      204800   83  Linux
/dev/sdb2          411648     4507647     2048000   83  Linux
```
4）新建第3个分区/dev/sdb3
```shell
Command (m for help): n     
Partition type:
   p   primary (2 primary, 0 extended, 2 free)
   e   extended
Select (default p): p
Partition number (3,4, default 3): 3
First sector (4507648-20971519, default 4507648): 
Using default value 4507648
Last sector, +sectors or +size{K,M,G} (4507648-20971519, default 20971519): +1000M
Partition 3 of type Linux and of size 1000 MiB is set
Command (m for help): p                                  //确认当前分区表
.. ..
   Device Boot      Start         End      Blocks   Id  System
/dev/sdb1            2048      411647      204800   83  Linux
/dev/sdb2          411648     4507647     2048000   83  Linux
/dev/sdb3         4507648     6555647     1024000   83  Linux
```
5）保存分区更改，退出fdisk分区工具
```shell
Command (m for help): w                                  //保存并退出
The partition table has been altered!
Calling ioctl() to re-read partition table.
Syncing disks.
```
6）刷新分区表
```shell
[root@server0 ~]# partprobe  /dev/vdb         //重新检测磁盘分区
//或者
[root@server0 ~]# reboot                     //对已使用中磁盘的分区调整，应该重启一次
.. ..
```
**步骤二：格式化及挂载分区**

1）将分区/dev/sdb2格式化为EXT4文件系统
```shell
[root@server0 ~]# mkfs.ext4  /dev/sdb2
.. .. 
Allocating group tables: done  
Writing inode tables: done 
Creating journal (8192 blocks): done
Writing superblocks and filesystem accounting information: done
```
2）配置开机自动挂载
```shell
[root@server0 ~]# vim  /etc/fstab
.. ..
/dev/sdb2       /mnt/part2      ext4    defaults        0 0
```
3）创建挂载点，并验证挂载配置
```shell
[root@server0 ~]# mkdir  /mnt/part2                 //创建挂载点
[root@server0 ~]# mount  -a                         //挂载fstab中的可用设备
[root@server0 ~]# df  -hT  /mnt/part2/                 //检查文档所在的文件系统及设备
Filesystem     Type  Size  Used Avail Use% Mounted on
/dev/sdb2      ext4  1.9G  5.9M  1.8G   1% /mnt/part2
```

# 2. 分区扩展Swap空间
## 2.1 问题
1. 从磁盘sdd上划分一个2G的分区sdd1
2. 将/dev/sdd1格式化为Swap文件系统
3. 启用/dev/sdd1分区，查看Swap空间大小
4. 停用/dev/sdd1分区，查看Swap空间大小

## 2.2 方案
首先要明白Swap分区空间是来源于硬盘，而要想扩充Swap空间的大小，思路很简单就是把硬盘的分区格式成Swap文件系统，再扩充到Swap空间中区。

对于Swap分区有它独立的格式化命令和扩充命令，这里要和普通分区的格式化命令和挂载命令区分开。此外它还有独立查看Swap空间组成的命令。

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：从磁盘sdd上划分一个2G的分区sdd1**

命令操作如下所示：
```shell
[root@localhost ~]# fdisk /dev/sdd
欢迎使用 fdisk (util-linux 2.23.2)。
更改将停留在内存中，直到您决定将更改写入磁盘。
使用写入命令前请三思。
Device does not contain a recognized partition table
使用磁盘标识符 0x6faf1c3f 创建新的 DOS 磁盘标签。
命令(输入 m 获取帮助)：n
Partition type:
   p   primary (0 primary, 0 extended, 4 free)
   e   extended
Select (default p):                  #回车
Using default response p
分区号 (1-4，默认 1)：        #回车
起始 扇区 (2048-41943039，默认为 2048)：     #回车
将使用默认值 2048
Last 扇区, +扇区 or +size{K,M,G} (2048-41943039，默认为 41943039)：+2G  
分区 1 已设置为 Linux 类型，大小设为 2 GiB
命令(输入 m 获取帮助)：p
磁盘 /dev/sdd：21.5 GB, 21474836480 字节，41943040 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
磁盘标签类型：dos
磁盘标识符：0x6faf1c3f
   设备 Boot      Start         End      Blocks   Id  System
/dev/sdd1            2048     4196351     2097152   83  Linux
命令(输入 m 获取帮助)：w
The partition table has been altered!
Calling ioctl() to re-read partition table.
正在同步磁盘。
[root@localhost ~]#
```
**步骤二：将/dev/sdd1格式化为swap文件系统**

命令操作如下所示：
```shell
[root@localhost ~]# mkswap /dev/sdd1   //格式化为swap文件系统
Setting up swapspace version 1, size = 1951740 KiB
no label, UUID=848ca15c-a03e-4e0b-9ac0-bfd6507d0b7e
```
**步骤三：启用/dev/sdd1分区，查看swap空间大小**

命令操作如下所示：
```shell
[root@localhost ~]# swapon –s          //未启用之前，查看swap空间组成成员
Filename                                Type            Size    Used    Priority
/dev/sda5                               partition       8388600 0       -1
[root@localhost ~]# swapon /dev/sdd1  //启用/dev/sdd1交换分区
[root@localhost ~]# swapon –s          //启用之后，查看swap空间组成成员
Filename                                Type            Size    Used    Priority
/dev/sda5                               partition       8388600 0       -1
/dev/sdd1                               partition       1951736 0       -2
[root@localhost ~]#
```

**步骤四：停用/dev/sda8分区，查看swap空间大小**

命令操作如下所示：
```shell
[root@localhost ~]# swapoff /dev/sdd1   //停用/dev/sdd1交换分区
[root@localhost ~]# swapon -s
Filename                                Type            Size    Used    Priority
/dev/sda5                               partition       8388600 0       -1
[root@localhost ~]#
```

# 3. 文件扩展Swap空间
## 3.1 问题
1. 使用dd命令创建一个大小为2048MB的交换文件，放在/opt/swap.db
2. 将swap.db文件格式化成Swap文件系统
3. 启用swap.db文件，查看Swap空间大小
4. 停用swap.db文件，查看Swap空间大小

## 3.2 方案
Swap空间来源于硬盘空间，这个思路不变。我们可以换种方式，来扩展Swap空间。就是可以创建一个大的文件，文件占用的是磁盘空间，再将这个文件格式化使用。这个方式是可行的，但难点在于文件怎么生成呢？我们可以用dd这条命令。

例如 dd if=/dev/zero of=/opt/swap.db bs=1M count=2048 ，相关说明如下：

- dd：为命令字。
- if：读取数据的来源是哪，而/dev/zero是一个特殊的设备它可以产生无限的数据，常用来与dd命令搭配使用。
- of：将数据写入到哪里去，可以是其他设备，也可以是指定路径下的一个文件名。
- bs：每次读取和写入数据的大小为1M。
- count：为读取和写入的次数为2048次。

## 3.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：使用dd命令创建一个大小为2048MB的交换文件，放在/opt/swap.db**

命令操作如下所示：
```shell
[root@localhost ~]# dd if=/dev/zero of=/opt/swap.db bs=1M count=2048
记录了2048+0 的读入
记录了2048+0 的写出
2147483648字节(2.1 GB)已复制，95.5419 秒，22.5 MB/秒
[root@localhost ~]# ls -lh /opt/swap.db 
-rw-r--r--. 1 root root 2.0G 2月  27 21:24 /opt/swap.db
```
**步骤二：将swap.db文件格式化成Swap文件系统**

命令操作如下所示：
```shell
[root@localhost ~]# mkswap /opt/swap.db       //将文件格式化为Swap文件系统
mkswap: /opt/swap.db: warning: don't erase bootbits sectors
        on whole disk. Use -f to force.
Setting up swapspace version 1, size = 2097148 KiB
no label, UUID=4dc743fd-86a6-477b-a3fc-a811f41dbd43
[root@localhost ~]#
```
**步骤三：启用swap.db文件，查看Swap空间大小**

命令操作如下所示：
```shell
[root@localhost ~]# swapon /opt/swap.db  //启用swap.db文件
[root@localhost ~]# swapon -s
Filename                                Type            Size    Used    Priority
/dev/sda5                               partition       8388600 0       -1
/opt/swap.db                            file            2097144 0       -2
[root@localhost ~]#
```
**步骤四：停用swap.db文件，查看Swap空间大小**

命令操作如下所示：
```shell
[root@localhost ~]# swapoff /opt/swap.db //停用swap.db文件
[root@localhost ~]# swapon -s
Filename                                Type            Size    Used    Priority
/dev/sda5                               partition       8388600 0       -1
[root@localhost ~]#
```

# Exercise
## 1 列出创建ext3、ext4、xfs、vfat文件系统的格式化工具及用法

mkfs.ext3 分区设备路径

mkfs.ext4 分区设备路径

mkfs.xfs 分区设备路径

mkfs.vfat 分区设备路径

## 2 简述/etc/fstab开机挂载配置记录的格式组成
设备路径  挂载点  类型  参数  备份标记  检测顺序
  
## 3 分区标识。
执行（ ）或（ ）可以查看系统中已挂载的分区设备信息。执行（ ）命令可以重新识别分区表信息，使用（ ）命令可以查看块设备的UUID标识符。


- df -h
- mount
- partprobe
- blkid


> 如有侵权，请联系作者删除
