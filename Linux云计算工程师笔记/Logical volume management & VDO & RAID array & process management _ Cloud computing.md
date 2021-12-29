@[TOC]( Logical volume management & VDO & RAID array & process management | Cloud computing )

---
# 1. 新建一个逻辑卷
## 1.1 问题
本例要求沿用前一天案例，使用分区 /dev/sdb1 构建 LVM 存储，相关要求如下：

1. 新建一个名为 systemvg 的卷组
2. 在此卷组中创建一个名为 vo 的逻辑卷，大小为180MiB
3. 将逻辑卷 vo 格式化为 EXT4 文件系统
4. 将逻辑卷 vo 挂载到 /vo 目录，并在此目录下建立一个测试文件 votest.txt，内容为“I AM KING.”

## 1.2 方案
LVM创建工具的基本用法：
```shell
vgcreate  卷组名  物理设备.. ..
lvcreate  -L  大小  -n  逻辑卷名  卷组名
```

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：创建卷组**

1）新建名为systemvg的卷组
```shell
[root@server0 ~]# vgcreate  systemvg  /dev/sdb1
  Physical volume "/dev/sdb1" successfully created
  Volume group "systemvg" successfully created
```

2）确认结果
```shell
[root@server0 ~]# vgscan
  Reading all physical volumes.  This may take a while...
  Found volume group "systemvg" using metadata type lvm2
```

**步骤二：创建逻辑卷**

1）新建名为vo的逻辑卷
```shell
[root@server0 ~]# lvcreate  -L  180MiB  -n  vo  systemvg 
  Logical volume "vo" created
  ```
2）确认结果
```shell
[root@server0 ~]# lvscan
  ACTIVE            '/dev/systemvg/vo' [180.00 MiB] inherit
  ```
**步骤三：格式化及挂载使用**

1）格式化逻辑卷/dev/systemvg/vo
```shell
[root@server0 ~]# mkfs.ext4  /dev/systemvg/vo
.. ..
Allocating group tables: done 
Writing inode tables: done 
Creating journal (4096 blocks): done
Writing superblocks and filesystem accounting information: done
```
2）挂载逻辑卷/dev/systemvg/vo
```shell
[root@server0 ~]# mkdir  /vo                              //创建挂载点
[root@server0 ~]# mount  /dev/systemvg/vo  /vo             //挂载
[root@server0 ~]# df  -hT  /vo/                         //检查结果
Filesystem              Type  Size  Used Avail Use% Mounted on
/dev/mapper/systemvg-vo ext4  171M  1.6M  157M   1% /vo
```
3）访问逻辑卷/dev/systemvg/vo
```shell
[root@server0 ~]# cat  /vo/votest.txt
I AM KING.
```

# 2. 扩展逻辑卷的大小
## 2.1 问题
本例要求沿用练习一，将逻辑卷 vo 的大小调整为 300MiB，要求如下：

1. 原文件系统中的内容必须保持完整
2. 必要时可使用之前准备的分区 /dev/sdb5 来补充空间
3. 注意：分区大小很少能完全符合要求的大小，所以大小在270MiB和300MiB之间都是可以接受的

## 2.2 方案
对于已经格式化好的逻辑卷，在扩展大小以后，必须通知内核新大小。

如果此逻辑卷上的文件系统是EXT3/EXT4类型，需要使用resize2fs工具；

如果此逻辑卷上的文件系统是XFS类型，需要使用xfs_growfs。

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：确认逻辑卷vo的信息**

1）找出逻辑卷所在卷组
```shell
[root@server0 ~]# lvscan
  ACTIVE            '/dev/systemvg/vo' [180.00 MiB] inherit
  ACTIVE            '/dev/datastore/database' [800.00 MiB] inherit
  ```
2）查看该卷组的剩余空间是否可满足扩展需要
```shell
[root@server0 ~]# vgdisplay  systemvg
  --- Volume group ---
  VG Name               systemvg
  System ID             
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  2
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                1
  Open LV               0
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               196.00 MiB                          //卷组总大小
  PE Size               4.00 MiB
  Total PE              49
  Alloc PE / Size       45 / 180.00 MiB
  Free  PE / Size       4 / 16.00 MiB                      //剩余空间大小
  VG UUID               czp8IJ-jihS-Ddoh-ny38-j521-5X8J-gqQfUN
  ```
此例中卷组systemvg的总大小都不够300MiB、剩余空间才16MiB，因此必须先扩展卷组。只有剩余空间足够，才可以直接扩展逻辑卷大小。

**步骤二：扩展卷组**

1）将提前准备的分区/dev/sdb5添加到卷组systemvg
```shell
[root@server0 ~]# vgextend  systemvg  /dev/sdb5
  Physical volume "/dev/sdb5" successfully created
  Volume group "systemvg" successfully extended
  ```
2）确认卷组新的大小
```shell
[root@server0 ~]# vgdisplay  systemvg
  --- Volume group ---
  VG Name               systemvg
  .. ..
  VG Size               692.00 MiB                          //总大小已变大
  PE Size               4.00 MiB
  Total PE              173
  Alloc PE / Size       45 / 180.00 MiB
  Free  PE / Size       128 / 512.00 MiB                  //剩余空间已达512MiB
  VG UUID               czp8IJ-jihS-Ddoh-ny38-j521-5X8J-gqQfUN
  ```
**步骤三：扩展逻辑卷大小**

1）将逻辑卷/dev/systemvg/vo的大小调整为300MiB
```shell
[root@server0 ~]# lvextend  -L 300MiB  /dev/systemvg/vo 
  Extending logical volume vo to 300.00 MiB
  Logical volume vo successfully resized
  ```
2）确认调整结果
```shell
[root@server0 ~]# lvscan
  ACTIVE            '/dev/systemvg/vo' [300.00 MiB] inherit
  ACTIVE            '/dev/datastore/database' [800.00 MiB] inherit
  ```
3）刷新文件系统大小

确认逻辑卷vo上的文件系统类型：
```shell
[root@server0 ~]# blkid  /dev/systemvg/vo
/dev/systemvg/vo: UUID="d4038749-74c3-4963-a267-94675082a48a" TYPE="ext4"
```
选择合适的工具刷新大小：
```shell
[root@server0 ~]# resize2fs  /dev/systemvg/vo 
resize2fs 1.42.9 (28-Dec-2013)
Resizing the filesystem on /dev/systemvg/vo to 307200 (1k) blocks.
The filesystem on /dev/systemvg/vo is now 307200 blocks long.
```
确认新大小（约等于300MiB）：
```shell
[root@server0 ~]# mount  /dev/systemvg/vo  /vo/
[root@server0 ~]# df  -hT  /vo
Filesystem              Type  Size  Used Avail Use% Mounted on
/dev/mapper/systemvg-vo ext4  287M  2.1M  266M   1% /vo
```

# 3. 查看进程信息
## 3.1 问题
本例要求掌握查看进程信息的操作，使用必要的命令工具完成下列任务：

1. 找出进程 gdm 的 PID 编号值
2. 列出由进程 gdm 开始的子进程树结构信息
3. 找出进程 sshd 的父进程的 PID 编号/进程名称
4. 查看当前系统的CPU负载/进程总量信息

## 3.2 方案
查看进程的主要命令工具：

- ps aux、ps –elf：查看进程静态快照
- top：查看进程动态排名
- pstree：查看进程与进程之间的树型关系结构
- pgrep：根据指定的名称或条件检索进程

## 3.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：找出进程 gdm 的 PID 编号值**

使用pgrep命令查询指定名称的进程，选项-l显示PID号、-x精确匹配进程名：
```shell
[root@svr7 ~]# pgrep  -lx gdm
1584 gdm  
```
**步骤二：列出由进程 gdm 开始的子进程树结构信息**

使用pstree命令，可以提供用户名或PID值作为参数。通过前一步已知进程gdm的PID为1584，因此以下操作可列出进程gdm的进程树结构：
```shell
[root@svr7 ~]# pstree  -p  1584
gdm(1584)-+-Xorg(1703)
          |-gdm-session-wor(2670)-+-gnome-session(2779)-+-gnom+
          |                       |                     |-gnom+
          |                       |                     |-{gno+
          |                       |                     |-{gno+
          |                       |                     `-{gno+
          |                       |-{gdm-session-wor}(2678)
          |                       `-{gdm-session-wor}(2682)
          |-{gdm}(1668)
          |-{gdm}(1671)
          `-{gdm}(1702)
 ```
**步骤三：找出进程 sshd 的父进程的 PID 编号/进程名称**

要查看进程的父进程PID，可以使用ps –elf命令，简单grep过滤即可。找到进程sshd所在行对应到的PPID值即为其父进程的PID编号。为了方便直观查看，建议先列出ps表头行，以分号隔开再执行过滤操作。
```shell
[root@svr7 ~]# ps  -elf  |  head  -1 ; ps  -elf  |  grep  sshd
F S UID         PID   PPID  C PRI  NI ADDR SZ WCHAN  STIME TTY          TIME CMD
4 S root       1362      1  0  80   0 - 20636 poll_s Jan05 ?        00:00:00 /usr/sbin/sshd –D
.. ..                                 //可获知进程sshd的父进程PID为1
```
然后再根据pstree –p的结果过滤，可获知PID为1的进程名称为systemd：
```shell
[root@svr7 ~]# pstree  -p  |  grep  '(1)'
systemd(1)-+-ModemManager(995)-+-{ModemManager}(1018)
```
**步骤四：查看当前系统的CPU负载/进程总量信息**

使用top命令，直接看开头部分即可；或者 top -n 次数：
```shell
[root@svr7 ~]# top
top - 15:45:25 up 23:55,  2 users,  load average: 0.02, 0.03, 0.05
Tasks: 485 total,   2 running, 483 sleeping,   0 stopped,   0 zombie
%Cpu(s):  1.7 us,  1.0 sy,  0.0 ni, 97.3 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem :  1001332 total,    76120 free,   419028 used,   506184 buff/cache
KiB Swap:  2097148 total,  2096012 free,     1136 used.   372288 avail Mem
.. ..
```
观察Tasks: 485 total部分，表示进程总量信息。

观察load average: 0.02, 0.03, 0.05 部分，表示CPU处理器在最近1分钟、5分钟、15分钟内的平均处理请求数（对于多核CPU，此数量应除以核心数）。

对于多核CPU主机，如果要分别显示每颗CPU核心的占用情况，可以在top界面按数字键1进行切换：
```shell
[root@svr7 ~]# top
top - 15:47:45 up 23:57,  2 users,  load average: 0.02, 0.03, 0.05
Tasks: 485 total,   2 running, 269 sleeping,   0 stopped,   1 zombie
Cpu0  :  0.6%us,  7.8%sy,  0.0%ni, 91.6%id,  0.0%wa,  0.0%hi,  0.0%si,  0.0%st
Cpu1  :  0.7%us,  3.7%sy,  0.0%ni, 95.6%id,  0.0%wa,  0.0%hi,  0.0%si,  0.0%st
Cpu2  :  0.7%us,  1.7%sy,  0.0%ni, 97.6%id,  0.0%wa,  0.0%hi,  0.0%si,  0.0%st
Cpu3  :  0.3%us,  1.0%sy,  0.0%ni, 98.3%id,  0.3%wa,  0.0%hi,  0.0%si,  0.0%st
Mem:  16230564k total, 15716576k used,   513988k free,   326124k buffers
Swap:  8388604k total,   220656k used,  8167948k free, 11275304k cached
.. ..
```

# 4. 进程调度及终止
## 4.1 问题
本例要求掌握调度及终止进程的操作，使用必要的工具完成下列任务：

1. 运行“sleep 600”命令，再另开一个终端，查出sleep程序的PID并杀死
2. 运行多个vim程序并都放入后台，然后杀死所有vim进程
3. su切换为zhsan用户，再另开一个终端，强制踢出zhsan用户

## 4.2 方案
进程调度及终止的主要命令工具：

- 命令行 &：将命令行在后台运行
- Ctrl + z 组合键：挂起当前进程（暂停并转入后台）
- jobs：列出当前用户当前终端的后台任务
- bg 编号：启动指定编号的后台任务
- fg 编号：将指定编号的后台任务调入前台运行
- kill [-9] PID...：杀死指定PID值的进程
- kill [-9] %n：杀死第n个后台任务
- killall [-9] 进程名...：杀死指定名称的所有进程
- pkill：根据指定的名称或条件杀死进程
- 
## 4.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：根据PID杀死进程**

1）开启sleep测试进程
```shell
[root@svr7 ~]# sleep 600
//.. .. 进入600秒等待状态
```
2）找出进程sleep的PID

另开一个终端，ps aux并过滤进程信息（第2列为PID值）：
```shell
[root@svr7 ~]# ps  aux  |  grep  sleep
root      32929  0.0  0.0   4312   360 pts/1    S+   17:25   0:00 sleep 600
```
3）杀死指定PID的进程
```shell
[root@svr7 ~]# kill  -9  32929
```
返回原终端会发现sleep进程已经被杀死：
```shell
[root@svr7 ~]# sleep 600
Killed
```
**步骤二：根据进程名杀死多个进程**

1）在后台开启多个vim进程
```shell
[root@svr7 ~]# vim  a.txt &
[1] 33152
[root@svr7 ~]# vim  b.txt &
[2] 33154
[1]+  已停止               vim a.txt
[root@svr7 ~]# vim  c.txt &
[3] 33155
[2]+  已停止               vim b.txt
```
2）确认vim进程信息
```shell
[root@svr7 ~]# jobs  -l
[1]  33152 停止 (tty 输出)     vim a.txt
[2]- 33154 停止 (tty 输出)     vim b.txt
[3]+ 33155 停止 (tty 输出)     vim c.txt
```
3）强制杀死所有名为vim的进程
```shell
[root@svr7 ~]# killall  -9  vim
[1]   已杀死               vim a.txt
[2]-  已杀死               vim b.txt
[3]+  已杀死               vim c.txt
```
4）确认杀进程结果
```shell
[root@svr7 ~]# jobs  -l 
[root@svr7 ~]#
```
**步骤三：杀死属于指定用户的所有进程**

1）登入测试用户zhsan
```shell
[root@svr7 ~]# useradd  zhsan
[root@svr7 ~]# su  -  zhsan
[zhsan@svr7 ~]$
```
2）另开一个终端，以root用户登入，查找属于用户zhsan的进程
```shell
[root@svr7 ~]# pgrep  -u  zhsan
33219
[root@svr7 ~]# pstree  -up  33219                              //检查进程树
bash(33219,zhsan)
```
3）强制杀死属于用户zhsan的进程
```shell
[root@svr7 ~]# pkill  -9  -u  zhsan
[root@svr7 ~]#
```
4）返回原来用户zhsan登录的终端，确认已经被终止
```shell
[zhsan@svr7 ~]$ 已杀死
[root@svr7 ~]#
```
# Exercise
## 1 LVM基本概念。
关于LVM逻辑卷的管理，基本概念及应用如下，请补充完整：

1）PV表示（ ），VG表示（ ），LV表示（ ）

2）创建及使用逻辑卷的主要过程：（ ） 。

> 物理卷、卷组、逻辑卷
PV物理卷-->VG卷组-->LV逻辑卷-->格式化-->挂载使用

## 2 LVM常用命令。
关于LVM逻辑卷的管理，最常用的一些操作如下，请写出各自的命令字：

> 1）扫描物理卷 （ ），创建物理卷 （ ）。
2）扫描卷组（ ），创建卷组（ ），删除卷组（ ）。
3）创建逻辑卷（ ），查看逻辑卷（ ）。
4）扩展逻辑卷（ ），扩展卷组（ ）。

1）pvscan、pvcreate
2）vgscan、vgcreate、vgremove
3）lvcreate、lvdisplay
4）lvextend、vgextend

## 3 LVM磁盘应用实战。
> 为一台RHEL6虚拟机添加2块20G的SCSI磁盘，相关要求如下：
1）将两块磁盘组合成名为data_vg的卷组。
2）从卷组data_vg中建立一个名为data_lv的逻辑卷，大小为16G。
3）确保开机后能自动将逻辑卷data_lv挂载为/mbox。
4）完成上述操作后，将data_lv的容量扩展为24G。

1）准备实验环境
```shell
[root@svr5 ~]# ls /dev/sdb1 /dev/sdc1
/dev/sdb1      /dev/sdc1  
.. ..
```
2）创建VG、验证VG
```shell
[root@svr5 ~]# vgcreate data_vg /dev/sd{b,c}1
  Volume group "data_vg" successfully created
[root@svr5 ~]# vgscan 
  Reading all physical volumes.  This may take a while...
  Found volume group "data_vg" using metadata type lvm2
[root@svr5 ~]# vgdisplay 
.. ..
```
3）创建LV、验证LV
```shell
[root@svr5 ~]# lvcreate -L 16G -n data_lv data_vg
  Logical volume "data_lv" created
[root@svr5 ~]# lvscan 
  ACTIVE            '/dev/data_vg/data_lv' [16.00 GB] inherit
  ```
4）格式化LV、挂载文件系统
```shell
[root@svr5 ~]# mkfs.ext4 /dev/data_vg/data_lv 
[root@svr5 ~]# mkdir /mbox
[root@svr5 ~]# mount /dev/data_vg/data_lv /mbox/
[root@svr5 ~]# mount | grep mbox
/dev/mapper/data_vg-data_lv on /mbox type ext4 (rw)
```
5）访问逻辑卷，测试写入、读取操作
```shell
[root@svr5 ~]# ls > /mbox/file.txt
[root@svr5 ~]# tail -n 1 /mbox/file.txt 
install.log.syslog
```
6）在线扩展逻辑卷
```shell
[root@svr5 ~]# lvextend -L 24G /dev/data_vg/data_lv 
  Extending logical volume data_lv to 24.00 GB
  Logical volume data_lv successfully resized
[root@svr5 ~]# lvdisplay /dev/data_vg/data_lv | grep Size 
  LV Size                24.00 GB
[root@svr5 ~]# resize2fs /dev/data_vg/data_lv 
resize2fs 1.39 (29-May-2006)
Filesystem at /dev/data_vg/data_lv is mounted on /mbox; on-line resizing required
Performing an on-line resize of /dev/data_vg/data_lv to 6291456 (4k) blocks.
The filesystem on /dev/data_vg/data_lv is now 6291456 blocks long.
[root@svr5 ~]# df -h
文件系统              容量  已用 可用 已用% 挂载点
/dev/sda2              19G  2.7G   16G  15% /
/dev/sda1              99M   12M   82M  13% /boot
tmpfs                 500M     0  500M   0% /dev/shm
/dev/mapper/data_vg-data_lv
                       24G  173M   23G   1% /mbox
[root@svr5 ~]# tail -n 1 /mbox/file.txt 
install.log.syslog
```

## 4 简述RAID的含义及特点。
> RAID的含义及优势？RAID0、RAID1、RAID5分别指什么、各自的特点？

1）RAID：廉价冗余磁盘阵列，指通过硬件/软件技术将多个较小/低速的磁盘整合成一个大磁盘使用的一种存储技术，其不仅可存储数据，还可以实现一定程度的冗余保障，具有“速度快、安全性高”的优势。

2）RAID0、RAID1、RAID5的含义及特点如下：

- RAID0：条带模式，由两个或两个以上的磁盘组成，同一份文档分散在不同的磁盘中，并行写入，提高写效率。
- RAID1：镜像模式，由至少两个磁盘组成，同一份文件被分别写入到不同的磁盘中，每份磁盘数据一样，实现容错，提高读效率。
- RAID5：分布式奇偶校验的独立磁盘模式，结合RAID0和RAID1的好处，同时避免它们的缺点。由至少3块以上大小相同的磁盘组成，实现冗余。

## 5 使用top命令监控进程
> 执行“dd if=/dev/sda of=/dev/null &”命令，然后查找出系统中CPU占用最高的进程，并杀死此该进程。

1）启用后台任务
```shell
[root@svr7 ~]# dd  if=/dev/zero  of=/dev/null  &
[1] 27691
```
2）通过top命令对进程排名，默认情况下排第1位的进程CPU占用最高

查看进程排名：
```shell
[root@svr7 ~]# top
top - 11:07:18 up 3 days, 14:44,  4 users,  load average: 0.23, 0.21, 0.09
Tasks: 150 total,   3 running, 146 sleeping,   0 stopped,   1 zombie
Cpu(s):  3.0%us, 16.2%sy,  0.0%ni,  0.0%id, 76.4%wa,  3.7%hi,  0.7%si,  0.0%st
Mem:   1023848k total,  1015420k used,     8428k free,   532008k buffers
Swap:  4056360k total,      200k used,  4056160k free,    82580k cached
  PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND
27691 root      18   0 63204  600  504 R 19.7  0.1   0:04.38 dd
  265 root      10  -5     0    0    0 S  0.7  0.0   0:02.42 kswapd0
27694 root      15   0 12764 1140  836 R  0.3  0.1   0:00.01 top
    1 root      15   0 10372  696  588 S  0.0  0.1   0:01.31 init
    2 root      RT  -5     0    0    0 S  0.0  0.0   0:00.00 migration/0
    3 root      34  19     0    0    0 S  0.0  0.0   0:00.00 ksoftirqd/0
    4 root      10  -5     0    0    0 S  0.0  0.0   2:33.94 events/0
    5 root      10  -5     0    0    0 S  0.0  0.0   0:00.00 khelper
   14 root      16  -5     0    0    0 S  0.0  0.0   0:00.00 kthread
   18 root      10  -5     0    0    0 S  0.0  0.0   0:01.46 kblockd/0
   19 root      20  -5     0    0    0 S  0.0  0.0   0:00.00 kacpid
  187 root      19  -5     0    0    0 S  0.0  0.0   0:00.00 cqueue/0
  190 root      10  -5     0    0    0 S  0.0  0.0   0:00.22 khubd
  192 root      10  -5     0    0    0 S  0.0  0.0   0:00.00 kseriod
  262 root      15   0     0    0    0 S  0.0  0.0   0:00.01 khungtaskd
  263 root      25   0     0    0    0 S  0.0  0.0   0:00.00 pdflush
  264 root      15   0     0    0    0 S  0.0  0.0   0:10.22 pdflush
  ```
按k键输入要结束的进程id，等待杀死对应的进程：
```shell
.. ..
PID to kill: 27691
Kill PID 27691 with signal [15]:
```
## 6 杀死名称以rh开头的所有进程
1）找出目标进程
```shell
[root@svr7 ~]# pgrep -l ^rh
790 rhsmcertd
1308 rhnsd
```
2）杀死这些进程
```shell
[root@svr7 ~]# pkill ^rh
```
3）确认结果
```shell
[root@svr7 ~]# pgrep -l ^rh
[root@svr7 ~]#
```

> 如有侵权，请联系作者删除
