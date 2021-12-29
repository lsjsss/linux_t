@[TOC]( Basic rights and ownership & additional rights & and ACL policy management | Cloud computing )

---
# 1. 设置基本权限
## 1.1 问题
1. 新建/nsddir1/目录，在该目录下新建文件readme.txt
2. 使用户zhangsan能够在/nsddir1/目录下创建/删除子目录
使用户zhangsan能够修改/nsddir1/readme.txt文件，调整/nsddir1/目录的权限，使任何用户都不能进入该目录，测试用户zhangsan是否还能修/nsddir1/readme.txt文件的内容
4. 将/nsddir1/目录及其下所有内容的权限都设置为 rwxr-x---
## 1.2 方案
设置基本权限的命令主要是chmod，本实验要分清三个基本权限rwx的意义。用户在访问一个目录或文件时，由设置的访问权限+归属关系共同决定最终权限访问权限。

- r 读取：允许查看内容-read
- w 写入：允许修改内容-write
- x 可执行：允许运行和切换-excute

若对目录有r权限，表示可列出该目录内容。

若对目录有w权限，表示可在该目录下新建/删除/移动文件或子目录。

若对目录有x权限，表示允许cd到该目录下。

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：新建/nsddir1/目录，在该目录下新建文件readme.txt**

命令操作如下所示：
```shell
[root@localhost ~]# mkdir /nsddir1
[root@localhost ~]# ls -ld /nsddir1/             //查看是否创建成功
drwxr-xr-x. 2 root root 4096 2月  26 09:55 /nsddir1/
[root@localhost ~]# touch /nsddir1/readme.txt
[root@localhost ~]# ls -l /nsddir1/readme.txt   //查看是否创建成功
-rw-r--r--. 1 root root 0 2月  26 09:56 /nsddir1/readme.txt
[root@localhost ~]#
```

**步骤二：使用户zhangsan能够在/nsddir1/目录下创建/删除子目录（此题考查对目录w权限的理解）**

命令操作如下所示：
```shell
[root@localhost ~]# id zhangsan          //查看zhangsan用户是否存在
id: zhangsan：无此用户
[root@localhost ~]# useradd zhangsan    //创建zhangsan用户
[root@localhost ~]# ls -ld /nsddir1/    //查看nsddir1目录的权限
drwxr-xr-x. 2 root root 4096 2月  26 09:56 /nsddir1/
```
分析： 首先看zhangsan对于此目录具备有什么权限，zhangsan很明显属于其他人，权限对应为rx，要想让其能够创建、删除子目录，必须让其具备w权限
```shell
[root@localhost ~]# su – zhangsan                   //切换zhangsan用户测试
[zhangsan@localhost ~]$ mkdir /nsddir1/zhangdir    //测试是否有权限创建
mkdir: 无法创建目录"/nsddir1/zhangdir": 权限不够
[zhangsan@localhost ~]$exit
[root@localhost ~]# chmod o+w /nsddir1/             //为其他人添加W权限
[root@localhost ~]# ls -ld /nsddir1/                //查看是否添加成功
drwxr-xrwx. 2 root root 4096 2月  26 09:56 /nsddir1/
[root@localhost ~]# su – zhangsan                   //再次切换到zhangsan用户测试
[zhangsan@localhost ~]$ mkdir /nsddir1/zhangdir    //测试是否有权限创建
[zhangsan@localhost ~]$ ls /nsddir1/                //查看是否创建成功
readme.txt  zhangdir
[zhangsan@localhost ~]$
```
**步骤三：使用户zhangsan能够修改/nsddir1/readme.txt文件，调整/nsddir1/目录的权限，使任何用户都不能进入该目录，测试用户zhangsan是否还能修/nsddir1/readme.txt文件的内容。**

分析： 首先要解决zhangsan用户能够修改readme.txt内容

命令操作如下所示：
```shell
[root@localhost ~]# ls -ld /nsddir1/readme.txt      //查看readme.txt文件的权限
-rw-r--r--. 1 root root 0 2月  26 09:56 /nsddir1/readme.txt
```
分析： 首先看zhangsan对于此目录具备有什么权限，zhangsan很明显是其他人的权限是r权限，在想如何实现让zhangsan修改其内容，需加w权限
```shell
[root@localhost ~]# su – zhangsan                    //切换zhangsan用户测试
[zhangsan@localhost ~]$ echo 123 > /nsddir1/readme.txt   //测试是否有权限写入
-bash: /nsddir1/readme.txt: 权限不够
[zhangsan@localhost ~]$ exit
logout
[root@localhost ~]# chmod o+w /nsddir1/readme.txt        //添加w权限
[root@localhost ~]# ls -l /nsddir1/readme.txt            //查看是否添加成功
-rw-r--rw-. 1 root root 0 2月  26 09:56 /nsddir1/readme.txt
[root@localhost ~]# su – zhangsan                          //切换zhangsan用户测试
[zhangsan@localhost ~]$ echo 123 > /nsddir1/readme.txt   //测试是否有权限写入
[zhangsan@localhost ~]$ cat /nsddir1/readme.txt           //查看写入成功
123
```
分析： zhangsan能够修改readme.txt内容了。现在设置/nsddir1权限是任何人都不能进入该目录，只需将所有人的x执行权限去掉即可。

命令操作如下所示：
```shell
[root@localhost ~]# ls -ld /nsddir1/
drwxr-xr-x. 2 root root 4096 3月  31 11:38 /nsddir1/
[root@localhost ~]# chmod a-x /nsddir1/
[root@localhost ~]# ls -ld /nsddir1/
drw-r--r--. 2 root root 4096 3月  31 11:38 /nsddir1/
[root@localhost ~]# su - zhangsan
[zhangsan@localhost ~]$ cd /nsddir1/
-bash: cd: /nsddir1/: 权限不够
[zhangsan@localhost ~]$ echo 123 > /nsddir1/readme.txt   //zhangsan用户无权限修改
-bash: /nsddir1/readme.txt: 权限不够 
```

**步骤四：将/nsddir1/目录及其下所有内容的权限都设置为 rwxr-x---（本题主要考察选项-R，依然是利用chmod来完成）**

命令操作如下所示：
```shell
[root@localhost ~]# chmod -R 750 /nsddir1/           //-R为递归修改
[root@localhost ~]# ls -ld /nsddir1/                     //查看目录本身权限是否修改
drwxr-x---. 3 root root 4096 2月  26 16:00 /nsddir1/
[root@localhost ~]# ls -l /nsddir1/                 //查看子目录子文件权限是否修改
总用量 8
-rwxr-x---. 1 root     root        4 2月  26 16:14 readme.txt
drwxr-x---. 2 zhangsan zhangsan 4096 2月  26 16:00 zhangdir
```

# 2. 文件/目录的默认权限
## 2.1 问题
1）以用户root登入，测试umask掩码值

- 查看当前的umask值
- 新建目录udir1、文件ufile1，查看默认权限
- 将umask设为077，再新建目录udir2、文件ufile2，查看默认权限
- 请把umask值重新设置为022

2）以用户zhangsan登入，查看当前的umask值

3）请问为什么普通用户的家目录权限都是700

## 2.2 方案
本题的主要目的主要是让大家能够记住并理解umask值的作用，它决定着这个Shell环境创建文件以及目录的默认权限。

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：以用户root登入，测试umask掩码值**

- 查看当前的umask值
- 新建目录udir1、文件ufile1，查看默认权限
- 将umask设为077，再新建目录udir2、文件ufile2，查看默认权限
- 请把umask值重新设置为022

命令操作如下所示：
```shell
[root@localhost ~]# whoami       //确保自己登录身份是root
root
[root@localhost ~]# umask        //查看当前umask值，需用最大权限777减去022
0022
[root@localhost ~]# umask –S     //另外一种查看方式，-S选项是直接显示默认权限
u=rwx,g=rx,o=rx
```
分析： 查看创建目录以及文件的默认权限，是否与umask一致，注意文件默认安全起见没有赋予x执行权限
```shell
[root@localhost ~]# mkdir /udir1        //创建测试目录
[root@localhost ~]# touch /ufile1       //创建测试文件
[root@localhost ~]# ls -ld /udir1/      //查看是否与umask值相符合
drwxr-xr-x. 2 root root 4096 2月  26 16:37 /udir1/
[root@localhost ~]# ls -l /ufile1        //查看是否与umask值相符合
-rw-r--r--. 1 root root 0 2月  26 16:37 /ufile1
[root@localhost ~]# umask 077            //更改umask值
[root@localhost ~]# umask                //查看是否修改成功
0077
[root@localhost ~]# umask –S             
u=rwx,g=,o=
[root@localhost ~]# mkdir /udir2         //创建测试目录
[root@localhost ~]# touch /ufile2        //创建测试文件
[root@localhost ~]# ls -ld /udir2        //查看是否与umask值相符合
drwx------. 2 root root 4096 2月  26 16:43 /udir2
[root@localhost ~]# ls -l /ufile2        //查看是否与umask值相符合
-rw-------. 1 root root 0 2月  26 16:44 /ufile2
[root@localhost ~]# umask 022             //更改umask值为022
[root@localhost ~]# umask                 //查看是否修改成功
0022
```
**步骤二：以用户zhangsan登入，查看当前的umask值（本题的目的主要是为了让大家知道管理员与普通用户的默认umask是不同的）**

命令操作如下所示：
```shell
[root@localhost ~]# umask    //查看root的umask值
0022
[root@localhost ~]# su – zhangsan   //切换zhangsan用户身份
[zhangsan@localhost ~]$ umask       //查看zhangsan的umask值
0002
```

**步骤三：请问为什么普通用户的家目录权限都是700**

分析： 本题主要考察，useradd这条命令在执行的时候，与那些默认配置文件相关，有两个配置文件分别为/etc/default/useradd、/etc/login.defs。

命令操作如下所示：
```shell
[root@localhost ~]# grep -v "^#" /etc/login.defs | grep -v "^$" | grep -i umask
UMASK           077       //此配置文件规定创建用户家目录时，需遵循的umask值
```

# 3. 设置归属关系
## 3.1 问题
1. 新建/tarena1目录
2. 将属主设为gelin01，属组设为tarena组
3. 使用户gelin01对此目录具有rwx权限，其他人对此目录无任何权限
4. 使用户gelin02能进入、查看/tarena1文件夹
5. 请将gelin01加入tarena组，并将tarena1目录权限设置为450，测试gelin01用户能否进入该目录

## 3.2 方案
大家要记得更改归属关系是利用chown命令来完成的，其中要特别注意的是此命令既可以更改所有者，也可以更改所属组。要分清所有者与所属组的位置，并以冒号或者点隔开。

## 3.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：新建/tarena1目录**

命令操作如下所示：
```shell
[root@localhost ~]# mkdir /tarena1
```
**步骤二：将属主设为gelin01，属组设为tarena组**

命令操作如下所示：
```shell
[root@localhost ~]# ls -ld /tarena1/                 //想查看归属关系
drwxr-xr-x. 2 root root 4096 2月  26 17:10 /tarena1/
[root@localhost ~]# id gelin01                        //检查是否有gelin01用户
id: gelin01：无此用户 
[root@localhost ~]# grep tarena /etc/group           //检查是否有tarena组
[root@localhost ~]#
[root@localhost ~]# useradd gelin01                   //创建用户gelin01
[root@localhost ~]# groupadd tarena                   //创建组tarena
[root@localhost ~]# id gelin01                         //检查是否创建成功
uid=501(gelin01) gid=501(gelin01) 组=501(gelin01)
[root@localhost ~]# grep tarena /etc/group            //检查是否创建成功
tarena:x:502:
[root@localhost ~]# chown gelin01:tarena /tarena1/   //更改其归属关系
[root@localhost ~]# ls -ld /tarena1/                  //查看是否更改成功
drwxr-xr-x. 2 gelin01 tarena 4096 2月  26 17:10 /tarena1/
[root@localhost ~]#
```

**步骤三：使用户gelin01对此目录具有rwx权限，其他人对此目录无任何权限（更改时需注意对象要弄清，不要弄混）**

命令操作如下所示：
```shell
[root@localhost ~]# ls -ld /tarena1/        //查看其权限划分情况
drwxr-xr-x. 2 gelin01 tarena 4096 2月  26 17:10 /tarena1/
```
分析：想要gelin01用户权限为rwx，那么首先看gelin01是属于哪一种归属关系。可以看出是所有者身份。
```shell
[root@localhost ~]# chmod u=rwx /tarena1/   //更改所有者权限为rwx
[root@localhost ~]# ls -ld /tarena1/         //查看是否更改成功
drwxr-xr-x. 2 gelin01 tarena 4096 2月  26 17:10 /tarena1/
```
分析： 其他人无任何权限，利用命令chmod o= /tarena1/
```shell
[root@localhost ~]# ls -ld /tarena1/       //查看其权限划分情况
drwxr-xr-x. 2 gelin01 tarena 4096 2月  26 17:10 /tarena1/
[root@localhost ~]# chmod o= /tarena1/     //更改权限o没有任何权限
[root@localhost ~]# ls -ld /tarena1/       //查看其权限划分情况
drwxr-x---. 2 gelin01 tarena 4096 2月  26 17:10 /tarena1/
[root@localhost ~]#
```
**步骤四：使用户gelin02能进入、查看/tarena1文件夹**

命令操作如下所示：
```shell
[root@localhost ~]# ls -ld /tarena1/     //查看其权限划分情况
drwxr-x---. 2 gelin01 tarena 4096 2月  26 17:10 /tarena1/
```
分析： 首先gelin02这个用户对于tarena1目录的归属关系，因属于其他人，如果想让其能够查看必须要有r权限，想要进入必须要有x权限。可能有同学会想到利用chmod o=rx /tarena1 命令来完成此题，但这样做与上题相违背，所以不可。我们可以换一种方式，我们可以看到此目录的所属组具备rx权限，所以我们可以把gelin02加入到tarena组里，才是此题的正解。
```shell
[root@localhost ~]# id gelin02                    //查看是否有gelin02用户
id: gelin02：无此用户
[root@localhost ~]# useradd gelin02               //创建gelin02用户
[root@localhost ~]# gpasswd -a gelin02 tarena    //将gelin02用户加入组tarena
Adding user gelin02 to group tarena
[root@localhost ~]# grep tarena /etc/group       //查看是否加入成功
tarena:x:502:gelin02
[root@localhost ~]# su - gelin02                  //切换身份测试
[gelin02@localhost ~]$ ls -l /tarena1/           //查看是否具备r权限
总用量 0
[gelin02@localhost ~]$ cd /tarena1/              //查看是否具备x权限
[gelin02@localhost tarena1]$ pwd
/tarena1
```
**步骤五：请将gelin01加入tarena组，并将tarena1目录权限设置为450，测试gelin01用户能否进入该目录**

命令操作如下所示：
```shell
[root@localhost ~]# grep tarena /etc/group       //查看该组成员列表
tarena:x:502:gelin02
[root@localhost ~]# gpasswd -a gelin01 tarena    //将gelin01用户加入tarena组
Adding user gelin01 to group tarena
[root@localhost ~]# grep tarena /etc/group       //查看该组成员列表是否加入成功
tarena:x:502:gelin02,gelin01
[root@localhost ~]# ls -ld /tarena1/              //查看其权限划分情况
drwxr-x---. 2 gelin01 tarena 4096 2月  26 17:10 /tarena1/
[root@localhost ~]# chmod 450 /tarena1/           //更改权限
[root@localhost ~]# ls -ld /tarena1/              //查看其权限划分情况
dr--r-x---. 2 gelin01 tarena 4096 2月  26 17:10 /tarena1/
```
分析： 此时注意首先归属关系要清楚，gelin01是所有者而gelin01又属于tarena组，那接下来在看所有者权限是只读权限只有一个r权限，而所属组成员所具备的的是rx权限，这个时候我们要想一想了，现在权限发生不一致的情况，那么gelin01具备什么权限呢？是r还是rx。我们可以测试一下。
```shell
[root@localhost ~]# su - gelin01        //切换用户身份测试
[gelin01@localhost ~]$ ls /tarena1/     //查看是否具备r权限
[gelin01@localhost ~]$                   //可以看到具备r权限
[gelin01@localhost ~]$ cd /tarena1/     //能够切换成功说明是rx，否则是只读r权限
-bash: cd: /tarena1/: 权限不够
```
分析： 很明显不能够切换成功，是只读权限。这里告诉大家Linux对于权限判别的一个优先顺序，是所有者>所属组>其他人，也就是说首先Linux系统判别的是你属于本目录的归属关系的哪一种，首先看你是不是所有者，再看你是不是所属组，最后看你是不是其他人。就拿本题来举例，首先看gelin01是不是所有者，可以看出gelin01是所有者那么权限直接就按照所有者的权限执行，也不会再看后面。也不会所有者权限与所属组权限取交或并，本题目的是让大家记住和体会Linux对于权限判别的一个优先顺序。

# 4. SUID权限测试
## 4.1 问题
1. 将mkdir命令复制为/bin/mymd1，添加SUID
2. 以用户zhangsan登入，做下列测试：在其家目录下分别使用mkdir、mymd1命令尝试创建snew01、snew02
3. 查看snew01、snew02权限及归属关系
## 4.2 方案
SUID是Linux特殊权限的一种，能够用来传递可执行程序所有者的身份及具备所有者的权限。

注意事项：只针对可执行程序文件、可执行程序所有者必须具备可执行权限、显示占用的是所有者的x位置。

## 4.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：将mkdir命令复制为/bin/mymd1，添加SUID**

分析： 要想复制mkdir命令程序并改名，首先得找到该命令的绝对路径。可以利用which命令搜索。
```shell
[root@localhost ~]# which mkdir       //利用which找到mkdir命令的绝对路径
/bin/mkdir
[root@localhost ~]# cp /bin/mkdir /bin/mymd1    //复制并改名
[root@localhost ~]# ls -l /bin/mymd1             //查看是否生成mymd1
-rwxr-xr-x. 1 root root 49384 2月  27 10:34 /bin/mymd1
[root@localhost ~]# chmod u+s /bin/mymd1         //添加SUID权限
[root@localhost ~]# ls -l /bin/mymd1             //查看是否添加成功
-rwsr-xr-x. 1 root root 49384 2月  27 10:34 /bin/mymd1
```
**步骤二：以用户zhangsan登入，做下列测试：在其家目录下分别使用mkdir、mymd1命令尝试创建snew01、snew02**
```shell
[root@localhost ~]# id zhangsan             //查看zhangsan用户是否存在
uid=500(zhangsan) gid=500(zhangsan) 组=500(zhangsan)
[root@localhost ~]# su – zhangsan           //切换用户身份测试
[zhangsan@localhost ~]$ ls -l /bin/mkdir   //查看mkdir命令程序权限的划分
-rwxr-xr-x. 1 root root 49384 10月 17 2013 /bin/mkdir    //可以看到没有SUID
[zhangsan@localhost ~]$ mkdir snew01       //创建测试目录snew01
[zhangsan@localhost ~]$ ls -ld snew01/     //查看snew01权限及归属关系
drwxrwxr-x. 2 zhangsan zhangsan 4096 2月  27 10:40 snew01/  //属主与属组均是zhangsan
[zhangsan@localhost ~]$ ls -l /bin/mymd1   //查看mymd1命令程序权限的划分
-rwsr-xr-x. 1 root root 49384 2月  27 10:34 /bin/mymd1   //可以看到具备SUID
[zhangsan@localhost ~]$ mymd1 snew02        //创建测试目录snew02
[zhangsan@localhost ~]$ ls -ld snew02       //查看snew02权限及归属关系
drwxrwxr-x. 2 root zhangsan 4096 2月  27 10:47 snew02
```
分析： 可以看到归属关系中所有者发生变化，继承了mymd1命令程序的所有者root。

# 5. SGID权限测试
## 5.1 问题
1. 创建/nsdpublic目录，将属组改为tarena。
2. 新建子目录nsd01、子文件test01.txt，查看两者的权限及归属。
3. 为此目录添加SGID权限，再新建子目录nsd02、子文件test02.txt。
4. 查看上述子目录及文件的权限及归属。

## 5.2 方案
SGID是Linux特殊权限的一种，其作用主要体现如下：

1） 在一个具有SGID权限的目录下，新建的文档会自动继承此目录的属组身份。

注意事项：对可执行的程序/目录有效、可执行程序所属组必须具备可执行权限、显示占用的是所属组的x位置。

## 5.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：创建/nsdpublic目录，将属组改为tarena**

命令操作如下所示：
```shell
[root@localhost ~]# mkdir /nsdpublic           //创建测试目录
[root@localhost ~]# ls -ld /nsdpublic/         //查看权限及归属关系
drwxr-xr-x. 2 root root 4096 2月  27 11:27 /nsdpublic/
[root@localhost ~]# grep tarena /etc/group    //查看tarena组是否存在
tarena:x:502:gelin02,gelin01
[root@localhost ~]# chown :tarena /nsdpublic/ //更改目录所属组为tarena组
[root@localhost ~]# ls -ld /nsdpublic/         //查看是否修改成功
drwxr-xr-x. 2 root tarena 4096 2月  27 11:27 /nsdpublic/
```
**步骤二：新建子目录nsd01、子文件test01.txt，查看两者的权限及归属**

命令操作如下所示：
```shell
[root@localhost ~]# mkdir /nsdpublic/nsd01       //在nsdpublic目录下创建nsd01目录
[root@localhost ~]# touch /nsdpublic/test01.txt //在nsdpublic目录下创建测试文件
[root@localhost ~]# ls -l /nsdpublic/            //查看归属关系其属组均为root组
总用量 4
drwxr-xr-x. 2 root root 4096 2月  27 11:49 nsd01
-rw-r--r--. 1 root root    0 2月  27 11:50 test01.txt
```
**步骤三：为此目录添加SGID权限，再新建子目录nsd02、子文件test02.txt**

命令操作如下所示：
```shell
[root@localhost ~]# chmod g+s /nsdpublic/     //为nsdpublic添加SGID权限
[root@localhost ~]# ls -ld /nsdpublic/        //查看设置成功
drwxr-sr-x. 3 root tarena 4096 2月  27 11:50 /nsdpublic/
[root@localhost ~]# mkdir /nsdpublic/nsd02
[root@localhost ~]# touch /nsdpublic/test02.txt
[root@localhost ~]# ls -l /nsdpublic/          
总用量 8
drwxr-xr-x. 2 root root   4096 2月  27 11:49 nsd01
drwxr-sr-x. 2 root tarena 4096 2月  27 11:57 nsd02
-rw-r--r--. 1 root root      0 2月  27 11:50 test01.txt
-rw-r--r--. 1 root tarena    0 2月  27 11:57 test02.txt
```
分析： 可以看到当nsdpublic目录具备SGID权限时，之前创建的nsd01与test01.txt其所属组均为发生变化，但新创建的nsd02与test02.txt两者都继承的所属组身份及权限，其中还需注意的一点是我们也可以看到nsd02子目录也同样继承了SGID权限。

# 6. Sticky权限测试
## 6.1 问题
1. 为/tarena/public/目录设权限777，并添加粘滞位t权限
2. 以用户zhangsan登入，在/tarena/public/目录下创建文件zhsfile2
3. 以用户lisi登入，在/tarena/public/目录下创建文件lsfile2
4. 查看文件zhsfile2、lsfile2的权限和归属
5. 尝试删除zhsfile2、lsfile2文件

## 6.2 方案
Sticky权限是Linux特殊权限的一种，主要用来对公共目录的w权限进行限制。

注意事项：适用于目录，用来限制用户滥用写入权、其他人必须具备可执行权限、显示占用的是其他人的x位置。

## 6.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：为/tarena/public/目录设权限777，并添加粘滞位**

命令操作如下所示：
```shell
[root@localhost ~]# mkdir -p /tarena/public   //创建多级目录
[root@localhost ~]# ls -R /tarena              //递归查看目录结构
/tarena:
public
/tarena/public:
[root@localhost ~]# ls -ld /tarena/public      //查看权限的划分情况
drwxr-xr-x. 2 root root 4096 2月  27 14:47 /tarena/public/
[root@localhost ~]# chmod 777 /tarena/public  //设置权限为777
[root@localhost ~]# ls -ld /tarena/public      //查看设置结果
drwxrwxrwx. 2 root root 4096 2月  27 14:47 /tarena/public/
[root@localhost ~]# chmod o+t /tarena/public   //设置特殊权限t权限
[root@localhost ~]# ls -ld /tarena/public      //查看设置结果
drwxrwxrwt. 2 root root 4096 2月  27 14:47 /tarena/public/
[root@localhost ~]#
```

**步骤二：以用户zhangsan登入，在/tarena/public/目录下创建文件zhsfile2**

命令操作如下所示：
```shell
[root@localhost ~]# id zhangsan                //查看zhangsan用户是否存在
uid=500(zhangsan) gid=500(zhangsan) 组=500(zhangsan)
[root@localhost ~]# su – zhangsan              //切换用户身份测试
[zhangsan@localhost ~]$ touch /tarena/public/zhsfile2
[zhangsan@localhost ~]$ ls -l /tarena/public  //测试是否创建成功
总用量 0
-rw-rw-r--. 1 zhangsan zhangsan 0 2月  27 14:57 zhsfile2
[zhangsan@localhost ~]$
```
**步骤三：以用户lisi登入，在/tarena/public/目录下创建文件lsfile2**

命令操作如下所示：
```shell
[root@localhost ~]# id lisi                 //查看lisi用户是否存在
uid=503(lisi) gid=504(lisi) 组=504(lisi)
[root@localhost ~]# su – lisi               //切换用户身份
[lisi@localhost ~]$ touch /tarena/public/lsfile2   
[lisi@localhost ~]$ ls -l /tarena/public   //测试是否创建成功
总用量 0
-rw-rw-r--. 1 lisi     lisi     0 2月  27 15:03 lsfile2
-rw-rw-r--. 1 zhangsan zhangsan 0 2月  27 14:57 zhsfile2
[lisi@localhost ~]$
```
**步骤四：查看文件zhsfile2、lsfile2的权限和归属**

命令操作如下所示：
```shell
[lisi@localhost ~]$ ls -l /tarena/public/ 
总用量 0
-rw-rw-r--. 1 lisi     lisi     0 2月  27 15:03 lsfile2
-rw-rw-r--. 1 zhangsan zhangsan 0 2月  27 14:57 zhsfile2
[lisi@localhost ~]$
```
**步骤五：尝试删除zhsfile2、lsfile2文件（以lisi身份）**

命令操作如下所示：
```shell
[lisi@localhost ~]$ whoami                    //查看当前用户身份
Lisi
[lisi@localhost ~]$ ls -ld /tarena/public    //查看目录权限
drwxrwxrwt. 2 root root 4096 2月  27 15:07 /tarena/public/
[lisi@localhost ~]$ ls -l /tarena/public
总用量 0
-rw-rw-r--. 1 lisi     lisi     0 2月  27 15:03 lsfile2
-rw-rw-r--. 1 zhangsan zhangsan 0 2月  27 14:57 zhsfile2
[lisi@localhost ~]$ rm -rf /tarena/public/lsfile2    //删除lisi自己文件
[lisi@localhost ~]$ rm -rf /tarena/public/zhsfile2   //删除其他用户的文件
rm: 无法删除"/tarena/public/zhsfile2": 不允许的操作
```

# 7. 定义ACL控制策略
## 7.1 问题
1. 创建账户：mike、john、kaka
2. 创建文件：/data/file1.txt
3. mike对文件有读写权限，john只有读权限。其他用户没有任何权限
4. kaka具有与john相同权限
5. 创建lily用户，lily对file1.txt具有读执行权限，其他用户没有任何权限

## 7.2 方案
并不是所有的分区都支持ACL策略设置，后续会学习怎样让一个分区支持ACL。在安装系统时划分的分区默认是支持ACL策略的，而如果该分区是在安装系统之后创建的默认是不支持的。

ACL策略应用的情况是，当所有者、所属组、其他人三个归属关系，三种身份的权限都不能满足某个用户或组的权限设置。这个时候ACL可以为这个用户或组单独设置权限，使Linux权限划分设置更加灵活。

## 7.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：创建账户：mike、john、kaka**

命令操作如下所示：
```shell
[root@localhost ~]# useradd mike
[root@localhost ~]# useradd john
[root@localhost ~]# useradd kaka
```
**步骤二：创建文件：/data/file1.txt**

命令操作如下所示：
```shell
[root@localhost ~]# touch /data/file1.txt
[root@localhost ~]# ls -l /data/file1.txt
-rw-r--r--. 1 root root 0 2月  27 15:38 /data/file1.txt
```
**步骤三：mike对文件有读写权限，john只有读权限。其他用户没有任何权限**

分析： 此题涉及到三种不同的权限，我们可以这样来做，让mike来做所有者，让john属于此文件所属组成员，当然其他人就好说了直接设置即可。

命令操作如下所示：
```shell
 [root@localhost ~]# ls -l /data/file1.txt              //查看权限及归属关系
-rw-r--r--. 1 root root 0 2月  27 15:38 /data/file1.txt
[root@localhost ~]# chown mike:john /data/file1.txt    //更改所有者与所属组
[root@localhost ~]# ls -l /data/file1.txt               //查看更改结果
-rw-r--r--. 1 mike john 0 2月  27 15:38 /data/file1.txt
[root@localhost ~]# chmod o= /data/file1.txt            //设置权限，其他人无权限
[root@localhost ~]# ls -l /data/file1.txt               //查看呢设置结果
-rw-r-----. 1 mike john 0 2月  27 15:38 /data/file1.txt
[root@localhost ~]#
```

**步骤四：kaka具有与john相同权限**

分析： 我们可以把kaka加入到john组里面

命令操作如下所示：
```shell
[root@localhost ~]# id kaka                //查询kaka用户信息
uid=506(kaka) gid=507(kaka) 组=507(kaka)
[root@localhost ~]# gpasswd -a kaka john  //将kaka用户加入到john组
Adding user kaka to group john
[root@localhost ~]# id kaka                //查询kaka用户信息
uid=506(kaka) gid=507(kaka) 组=507(kaka),506(john)
[root@localhost ~]#
```

**步骤五：创建lily，lily对file1.txt具有读执行权限，其他用户没有任何权限**

分析： 这个时候就出现基本权限及归属关系不能解决，首先所有者已确定是mike，所属组权限rw所以也不行，最后其他人上面题有要求无任何权限。所以ACL策略就派上用场了。

命令操作如下所示：
```shell
[root@localhost ~]# echo 123456 > /data/file1.txt  //写入测试文字
[root@localhost ~]# cat /data/file1.txt             //管理员测试
123456
[root@localhost ~]# id lily                          //查询是否存在lily用户
id: lily：无此用户
[root@localhost ~]# useradd lily                     //创建lily用户
[root@localhost ~]# su – lily                        //切换用户身份
[lily@localhost ~]$ cat /data/file1.txt       //测试在没有设置ACL前lily能否查看
cat: /data/file1.txt: 权限不够
[lily@localhost ~]$ exit                              //退到root用户身份
logout
[root@localhost ~]# getfacl /data/file1.txt         //查看文件ACL策略
getfacl: Removing leading '/' from absolute path names
# file: data/file1.txt
# owner: mike
# group: john
user::rw-
group::r--
other::---
[root@localhost ~]# setfacl -m u:lily:r /data/file1.txt   //设置ACL策略
[root@localhost ~]# getfacl /data/file1.txt                //查看ACL策略
getfacl: Removing leading '/' from absolute path names
# file: data/file1.txt
# owner: mike
# group: john
user::rw-
user:lily:r--
group::r--
mask::r--
other::---
[root@localhost ~]# su – lily             //切换用户
[lily@localhost ~]$ cat /data/file1.txt  //测试是否具有r权限
123456
```

# Exercise
## 1 如何禁止用户harry对/opt/private目录有任何权限，但不影响其他用户对此目录的访问
```shell
[root@server0 ~]# mkdir  /opt/private
[root@server0 ~]# setfacl  -m  u:harry:-  /opt/private/
[root@server0 ~]# getfacl /opt/private/
getfacl: Removing leading '/' from absolute path names
# file: opt/private/
# owner: root
# group: root
user::rwx
user:harry:---                                     //确认结果
group::r-x
mask::r-x
other::r-x
```

## 2 新建目录/var/public，允许任何人写入，但禁止更改其他用户的文件

```shell
[root@server0 ~]# mkdir  /var/public
[root@server0 ~]# chmod  ugo=rwx  /var/public
[root@server0 ~]# chmod  o+t  /var/public
[root@server0 ~]# ls -ld /var/public/
drwxrwxrwt. 2 root root 6 Nov 26 00:11 /var/public/
```
## 3 新建目录新建/tarena目录使用户gelin01对此目录具有rwx权限，其他人对此目录无任何权限
```shell
[root@svr7 ~]# mkdir /tarena
[root@svr7 ~]# useradd gelin01
[root@svr7 ~]# ls -ld /tarena/
drwxr-xr-x. 2 root root 6 3月   3 14:39 /tarena/
[root@svr7 ~]# chown gelin01 /tarena/
[root@svr7 ~]# chmod o=--- /tarena/
[root@svr7 ~]# ls -ld /tarena/
drwxr-x---. 2 gelin01 root 6 3月   3 14:39 /tarena/
[root@svr7 ~]#
```

## 4 为lisi创建ACL访问权限，使得lisi可以查看/etc/shadow文件

```shell
[root@svr7 ~]# useradd lisi
[root@svr7 ~]# setfacl -m u:lisi:r /etc/shadow
[root@svr7 ~]# getfacl /etc/shadow
getfacl: Removing leading '/' from absolute path names
# file: etc/shadow
# owner: root
# group: root
user::---
user:lisi:r--
group::---
mask::r--
other::---

[root@svr7 ~]# su - lisi
[lisi@svr7 ~]$ cat /etc/shadow
root:$6$SEs4pO9FblvOFnNk$ZIMUYUpSjS9UQHPsscuNe/xYGYjMqxV/uFqRJVAi.nNJawAC05Ah8fwV.HVEF58yuhVRYKt4wOBEoqKsr1/ZX/::0:99999:7:::
bin:*:17632:0:99999:7:::
daemon:*:17632:0:99999:7:::
adm:*:17632:0:99999:7:::
lp:*:17632:0:99999:7:::
……
```


> 如有侵权，请联系作者删除
