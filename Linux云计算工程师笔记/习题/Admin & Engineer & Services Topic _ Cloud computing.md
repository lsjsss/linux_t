
@[TOC]( Admin & Engineer & Services Topic | Cloud computing )

---
# Single Choice
1、podman运行容器映射端口命令格式为_____。
A.podman  run   -itd   -p  真机端口:容器端口    镜像名称:标签 
B.podman  run   -itd   -c  真机端口:容器端口    镜像名称:标签 
C.podman  run   -itd   -r  真机端口:容器端口    镜像名称:标签 
D.podman  run   -itd   -t  真机端口:容器端口    镜像名称:标签 
【答案】**A**

---
2、/tmp/存放的是_____文件。
A.内存中的映射文件，不占用磁盘 
B.系统运行中使用的临时文件 
C.日志文件 
D.硬盘，键盘，鼠标，等各种设备文件 
【答案】**B**

---
3、Apache的网页文件默认根目录是在_____。
A./etc/http/httpd/ 
B./etc/http/ 
C./var/www/html/ 
D./etc/httpd	 
【答案】**C**

---
4、在搭建PXE+kickstart无人值守安装服务器时，以下_____服务不是必须的。
A.FTP/HTTP/NFS 
B.DNS 
C.TFTP 
D.DHCP 
【答案】**B**
【解析】**PXE网络装机，首先是DHCP服务分配IP地址，然后又TFTP服务提供引导文件及菜单文件，最后再由FTP/HTTP/NFS提供操作系统的众多安装包**

---
5、在/etc目录（含子目录）下查找文件名包含"passwd"的文件，可以执行_____操作。
A.ls -A /etc | grep '*passwd*' 
B.ls  /etc | grep 'passwd' 
C.find /etc -name "passwd*" 
D.find /etc -name "*passwd*" 
【答案】D
【解析】**find本身会对查找路径，进行递归查找。grep命令本身默认为模糊匹配，不能用通配符**

---
6、在Linux系统中，以下_____命令可用来查找文件所在路径。
A.whoami 
B.grep 
C.find 
D.where 
【答案】**C**
【解析】**whoami显示当前用户，grep在文本文件内容过滤指定字符串， where无此命令**

---
7、在Linux系统中，若要查询文件 /etc/dovecot.conf 是由哪个RPM软件包安装的，可以使用_____命令。
A.yum provides /etc/dovecot.conf 
B.rpm –q /etc/dovecot.conf 
C.rpm –ql /etc/dovecot.conf 
D.yum list /etc/dovecot.conf 
【答案】**A**

---
8、创建用户时使用选项_____可指定用户id值。
A.-d  
B.-G 
C.-u 
D.-s  
【答案】**C**
【解析】**-d指定家目录，-s指定登录系统的解释器，-G指定附加组**

---
9、Windows查看IP地址的命令为_____。
A.ifconfig 
B.ipconfig 
C.ifconf 
D.ipconf 
【答案】**B**

---
10、列出网上NFS共享资源的命令为_____。
A.mount -e 服务器地址 
B.showmount -e 服务器地址 
C.showmount 服务器地址 
D.mount 服务器地址 
【答案】**B**
【解析】**showmount  -e  服务器地址**

---
11、启动DNS服务的命令是_____。
A.systemctl  start  bind-chroot 
B.systemctl  start  bind 
C.systemctl  start  DNS 
D.systemctl   start  named 
【答案】**D**

---
12、在一台Linux服务器上，使用Apache作为Web服务程序，服务器名称是www.a.com，管理员把所有对外提供的文档放在/usr/local/source目录下面，希望远程用户在浏览器中使用http://www.a.com地址即能访问这些文档，他需要对Apache进行_____设置。
A.修改Apache配置文件httpd.conf中的Listen的值为8000 
B.修改Apache配置文件httpd.conf中的DocumentRoot项值为“/usr/local/source” 
C.安装Apache服务器在/usr/local/目录下即可 
D.修改Apache配置文件httpd.conf中的ServerRoot项值为“/usr/local/source” 
【答案】**B**
【解析】**A选项安装目录与网页文件根路径无关，B选项指定httpd服务 配置文件根路径与网页文件根路径无关，D选项指定端口与网页文件根路径无关**

---
13、在常见的Linux日志文件中，以下哪个文件_____的作用是记录与系统启动相关的消息。
A./var/log/secure 
B./var/log/maillog 
C./var/log/dmesg 
D./var/log/messages 
【答案】**C**
【解析】**/var/log/messages记录各种服务公共消息，/var/log/secure记录用户登录安全相关，/var/log/maillog邮件收发相关信息**

---
14、光盘的系统类型为_____。
A.iso9600 
B.defaults 
C.iso9660 
D.xfs 
【答案】**C**
【解析】**xfs是RHEL7分区与系统常用的文件系统，iso9600无此 文件系统**

---
15、在Linux系统中配置httpd服务器时，设置项_____用来指定该Web服务器的站点名。
A.ServerRoot 
B.ServerAdmin 
C.DocumentRoot 
D.ServerName 
【答案】**D**
【解析】**DocumentRoot指定网页文件根目录，ServerAdmin指定管理员的邮箱，ServerRoot指定httpd配置文件根路径**

---
16、在Linux系统中，使用lvextend命令为指定的逻辑卷动态扩容以后，
通过df命令查看时该分区显示的大小并未变化，还需要进行_____操作以便系统能够更新ext4文件系统大小。
A.mount 
B.partprobe 
C.resize2fs 
D.lvscan 
【答案】**C**
【解析】**partprobe为刷新分区表，lvscan为查看逻辑卷信息，mount为mount 挂载**

---
17、在Linux 系统中，执行 tail –n 5 /var/log/messages 后得到的其中一行信息如下：  
Oct 29 13:19:48 web5 dhclient: DHCPACK from 192.168.8.254 (xid=0x7c.. ..)，其中的dhclient指的是_____。
A.主机名 
B.时间标签 
C.消息内容 
D.程序名 
【答案】**D**
【解析】**本题考查日志记录的格式，按照时间、地点、人物、发生的事件进行记录，在计算机中人物会写具体用户名或服务名、程序名，所以dhclinet为程序名**

---
18、下面关于列出内核版本命令正确的是_____。
A.cat   /proc/meminfo 
B.cat    /etc/redhat-release 
C.lscpu  
D.uname     -r 
【答案】**D**
【解析】**lscpu查看CPU信息，cat /etc/redhat-release是查看系统 具体版本，cat /proc/meminfo是查看内存信息，查看内核版本为 uname -r**

---
19、MBR分区最大支持_____个主分区。
A.128个 
B.3个 
C.64个 
D.4个 
【答案】**D**
【解析】**MBR分区表在硬盘中占用64字节空间，而每个主分区需要占用16字节空间，所以至多有4个主分区**

---
20、在Linux系统中，若执行 scp dumb bilbo@www.foobar.com: 命令，
可以实现_____功能？
A.将远程服务器www.foobar.com 上用户“bilbo”主目录下的一个名为 “dumb”的文件拷贝到本地计算机当前目录下，并且登录远程服务器上的账号名为 “bilbo” 
B.将本地计算机当前目录下的一个名为“dumb”的文档拷贝到远程主机www.foobar.com中用户 “bilbo”的主目录下 
C.将本地计算机“dumb”目录下所有的文件拷贝到远程服务器www.fobar.com的根目录下，并且登录远程服务器上的密码为“bilbo” 
D.将本地计算机当前目录下的一个名为“dumb”的文件发送到邮件 bilbo@www.foobar.com 
【答案】**B**

---
21、在Linux系统中，MBR分区模式第四块SCSI硬盘中的第三个逻辑分区表示为_____。
A./dev/sdd3 
B./dev/hda3 
C./dev/sdd7 
D./dev/sdc7 
【答案】**C**
【解析】**在MBR分区模式中，分区方案为前三个为主分区，第四个为扩展分区，第一逻辑分区为第五个分区，依次类推第七个分区为第三个逻辑分区**

---
22、UNIX诞生日是_____。
A.1970年1月1号 
B.1969年年底 
C.1973年 
D.1991年10月 
【答案】**A**
【解析】**UNIX操作系统诞生为1970-1-1**

---
23、配置Postfix邮件服务时，以下_____参数表示外发邮件时的发件域地址。
A.inet_interfaces 
B.mydomain 
C.myorigin 
D.mydestination 
【答案】**C**
【解析】**inet_interfaces指定网络接口，mydomain指定本机域名，mydestination指定收件人域名为本域邮件**

---
24、在Linux系统中，用来记录用户账号的用户名、家目录、登录Shell等信息的文件是_____。
A./root/.bashrc 
B./etc/shadow 
C./etc/bashrc 
D./etc/passwd 
【答案】**D**
【解析】**/etc/passwd存放用户基本信息，/root/.bashrc定义root自定义初始化信息例如别名定义、变量定义等，/etc/shadow保存用户密码信息，/etc/bashrc为全局配置文件**

---
25、创建卷组是指定PE大小的命令是_____。
A.lvextend  -s PE大小 卷组名  空闲分区 
B.vgextend -s PE大小 卷组名  空闲分区 
C.lvcreate -s PE大小 卷组名  空闲分区 
D.vgcreate -s PE大小 卷组名  空闲分区 
【答案】**D**
【解析】**lvcreate为创建逻辑卷，lvextend为扩展逻辑卷，在创建及扩展 逻辑卷时，均不能指定PE大小，vgextend为扩展卷组，扩展卷组时也不能指定PE大小**

---
26、下面关于IP地址的组成正确的是_____。
A.IP地址由32个十进制数组成 
B.IP地址由40个十进制组成 
C.IP地址由48个二进制数组成 
D.IP地址由32个二进制数组成 
【答案】**D**

---
27、在Linux系统中，使用命令rpm -e卸载软件包时，返回错误提示：
“Failed dependencies”，这可能是由于_____。
A.该软件包已不存在 
B.该软件包已存在 
C.该软件包与其他软件包之间存在依赖关系 
D.该软件包已损坏 
【答案】**C**
【解析】**报错信息为错误的依赖关系**

---
28、在Linux系统中配置防火墙策略时，通过_____命令设置默认区域为trusted。
A.firewall-cmd --default --zone=trusted 
B.firewall-cmd --permanent  --zone=trusted 
C.firewall-cmd --set-default-zone=trusted 
D.firewall-cmd --get-default-zone=trusted 
【答案】**C**

---
29、关于硬RAID实现的方式，以下说法正确的是_____。
A.主板—>操作系统—>磁盘—>阵列卡—>数据 
B.主板—>磁盘—>操作系统—>阵列卡—>数据 
C.主板—>磁盘—>阵列卡—>操作系统—>数据 
D.主板—>阵列卡—>磁盘—>操作系统—>数据 
【答案】**D**
【解析】**服务器是同过阵列卡来识别磁盘，识别硬盘后才可以安装操作系统或读取操作系统数据**

---
30、使用grep过滤时选项_____可以忽略大小写。
A.$  
B.^ 
C.-i 
D.-v  
【答案】**C**
【解析】**-v为取反查找，^为匹配以字符串开头，$为匹配以字符串结尾**

---
31、在Linux系统中，执行_____命令可以把/dev/sdb6格式化成交换分区。
A.format /dev/sdb6 
B.mkfs  -t  ext3  /dev/sdb6 
C.fdisk /dev/sdb6 
D.mkswap /dev/sdb6 
【答案】**D**

---
32、在Linux系统中，执行_____操作可以将/mail文件夹的属组设置为postfix。
A.chmod :postfix /mail 
B.chmod postfix /mail 
C.chown :postfix /mail 
D.groupmod postfix /mail 
【答案】**C**
【解析】**chmod无法修改归属关系，groupmod修改组账号属性的命令**

---
33、对于IP地址的分类，C类IP地址的范围是_____。
A.191至223 
B.192至224 
C.192至223 
D.190至223  
【答案】**C**
【解析】**IP地址分类A类为1-127，B类为128-191，C类为192-223， D类为224-239，E类为240-254**

---
34、若要删除用户lily且把她的宿主目录一起删除，可以执行_____命令。
A.userdel -r lily 
B.userdel -R lily 
C.userkill -d lily 
D.userkill -D lily 
【答案】**A**
【解析】**userkill无此命令，userdel -r为将用户家目录一并删除**

---
35、在配置DNS服务的时候，正向解析记录的资源类型是_____。
A.PTR 
B.A 
C.CNAME 
D.SOA 
【答案】**B**
【解析】**PTR代表方向解析记录，CNAME代表解析记录别名，SOA代表授权记录**

---
36、在Linux系统中，若要实现开机自动挂载文件系统，需要修改_____配置文件。
A./etc/fstab 
B./etc/mount 
C./etc/startup 
D./etc/auto.master 
【答案】**A**
【解析】**/etc/auto.master为autofs触发挂载配置文件**

---
37、使用命令_____可以查看后台所有的进程，并且输出进程的PID。
A.jobs -l 
B.bg 
C.jobs 
D.fg 
【答案】**A**

---
38、在Linux系统中从源代码安装软件时，编译的过程由_____操作完成。
A../configure 
B.make 
C.make all 
D.make install 
【答案】**B**

---
39、格式化swap分区时使用_____命令。
A.mkfs.ext4 分区设备路径 
B.mkfs.xfs 分区设备路径 
C.swapon  分区路径 
D.mkswap分区路径 
【答案】**D**
【解析】**mkfs.ext4格式化ext4文件系统，mkfs.xfs格式化xfs文件系 统，swapon为启用swap交换分区**

---
40、配置Postfix邮件服务时，通常应修改主配置文件_____。
A./etc/postfix/master.conf 
B./etc/postfix/main.cf 
C./etc/postfix/main.conf 
D./etc/postfix/mail.conf 
【答案】**B**

---
# Multiple Choice
41、vim编辑器中调到首行的快捷键是_____。
A.1G 
B.1g 
C.gg 
D.GG 
【答案】**A,C**
【解析】**GG跳转到末行，1g无作用**

---
42、以下_____属于Linux发行版本。
A.Red Hat Enterprise Linux 
B.IBM AIX 
C.Windows Server 2008 
D.CentOS 
【答案】**A,D**

---
43、selinux切换运行模式的方法是_____。
A.临时切换：setenforce  1或0 
B.临时切换：getenforce  1或0 
C.固定配置：/etc/selinux/config 文件 
D.固定配置：/etc/selinux/selinux.cnf 
【答案】**A,C**
【解析】**修改SELinux模式，两个方面临时修改与固定修改，临时修改通过命令setenforce而getenforce为查看不能达到修改，固定修改 需要修改/etc/selinux/config 文件**

---
44、关于Linux系统的常见目录，以下描述正确的是_____。
A./tmp是临时目录 
B./root目录是所有用户的家目录 
C./boot目录用来存放启动相关文件 
D./dev目录用来存放配置文件 
【答案】**A,C**

---
45、常见的数据库软件有_____。
A.MySQL 
B.SQL Server 
C.DB2 
D.virtualbox 
【答案】**A,B,C**

---
46、Apache虚拟主机的类型包括_____。
A.基于路由的虚拟主机 
B.基于端口的虚拟主机 
C.基于域名的虚拟主机 
D.基于ip的虚拟主机 
【答案】**B,C,D**
【解析】**虚拟Web主机没有基于路由的类型**

---
47、selinux的运行模式有_____。
A.disabled 
B.enable 
C.enforcing 
D.permissive 
【答案】**A,C,D**
【解析】**SELinux无enable模式**

---
48、关于Linux命令行环境的通配符，以下描述正确的是_____。
A.* 匹配单个字符 
B.？匹配任意多个字符 
C.[a-z] 匹配连续多个字符a-z中的一个 
D.{a,min,xy} 分别匹配不连续的a,min,xy多组字符 
【答案】**C,D**
【解析】***匹配任意多个字符，？匹配单个字符**

---
49、把命令cp /ISO/1.txt /mnt无论状态如何，放入后台的命令是_____。
A.快捷键Ctrl+z 
B.cp /ISO/1.txt  /mnt& 
C.cp /ISO/1.txt  /mnt $ 
D.Ctrl+C 
【答案】**A,B**

---
50、(多选题)安装源码包时需要安装编译工具有_____。
A.make 
B.C++	 
C.g++ 
D.gcc 
【答案】**A,D**


> 如有侵权，请联系作者删除
