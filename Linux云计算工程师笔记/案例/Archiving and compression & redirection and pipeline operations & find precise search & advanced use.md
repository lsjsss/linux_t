@[TOC]( Archiving and compression & redirection and pipeline operations & find precise search & advanced use of VIM   | Cloud computing )

---
# 1. 创建一个备份包
## 1.1 问题
本例要求使用 tar 工具完成以下备份任务：

1. 创建一个名为 /root/backup.tar.bz2 的归档文件
2. 其中包含 /usr/local 目录中的内容
3. tar 归档必须使用 bzip2 进行压缩

## 1.2 方案
制作归档压缩包：

- tar -zcf 备份文件.tar.gz 文档....
- tar -jcf 备份文件.tar.bz2 文档....
- tar -Jcf 备份文件.tar.xz 文档....

查看归档压缩包：
- tar -tf 备份文件

释放归档压缩包：
- tar -xf 备份文件 [-C 目标目录]

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：创建备份文件**

使用tar命令制作归档备份，结合-j选项调用bzip2压缩工具，保留绝对路径：
```shell
[root@server0 ~]# tar  -jcf  /root/backup.tar.bz2  /usr/local/
```
**步骤二：确认结果**
```shell
[root@server0 ~]# ls  -lh  /root/backup.tar.bz2          //确认文件
-rw-r--r--. 1 root root 1.9K 12月 23 23:22 /root/backup.tar.bz2
[root@server0 ~]# tar  -tf  /root/backup.tar.bz2         //确认内容
usr/local/
usr/local/bin/
usr/local/bin/lab
usr/local/etc/
usr/local/games/
```
# 2. 重定向与管道操作
## 2.1 问题
1. 显示ifconfig命令的前两行内容
2. 显示/etc/passwd第九行内容
3. 将hostname命令的输出内容，覆盖写入到/opt/hn.txt
4. 利用echo命令,将“tmooc”内容追加写入到/opt/hn.txt
## 2.2 方案
重新定向命令的输出：将前面命令的输出，写入到后面文本文件中

- \>：覆盖重定向
- \>>:追加重定向

管道 :将前面命令的输出，传递到后面命令，作为后面命令的参数

## 2.3 步骤
实现此案例需要按照如下步骤进行。

> 1）显示ifconfig命令的前两行内容
```shell
[root@server0 ~]# ifconfig  |  head  -2
```
> 2）显示/etc/passwd第九行内容
```shell
[root@server0 ~]# head  -9  /etc/passwd  |  tail -1
```
> 3）将hostname命令的输出内容，覆盖写入到/opt/hn.txt
```shell
[root@server0 ~]# hostname  >  /opt/hn.txt
```
>  4）利用echo命令,将“tmooc”内容追加写入到/opt/hn.txt
```shell
[root@server0 ~]# echo  tmooc  >>  /opt/hn.txt
```
# 3. 查找并处理文件
## 3.1 问题
1. 利用find查找所有用户 student 拥有的必须是文件,把它们拷贝到 /root/findfiles/ 文件夹中
2. 利用find查找/boot目录下大于10M并且必须是文件，拷贝到/opt
3. 利用find查找/boot/ 目录下以 vm 开头且必须是文件，拷贝到/opt
4. 利用find查找/boot/ 目录下为快捷方式
5. 利用find查找/etc 目录下，以 tab 作为结尾的 必须是文件
## 3.2 方案
根据预设的条件递归查找对应的文件

格式：find [目录] [条件1]

常用条件表示：

- -type 类型（f文件、d目录、l快捷方式）
- -name "文档名称"
- -size +|-文件大小（k、M、G）
- -user 用户名
- -mtime 修改时间

高级使用（处理find查找的结果）
- -exec 额外操作的开始
- \; 表示额外操作的结束
- {} 前面find命令每一个查询的结果
## 3.3 步骤
实现此案例需要按照如下步骤进行。

> 1）利用find查找所有用student 拥有的必须是文件,把它们拷贝到 /root/findfiles/ 文件夹中（确保本机具有student用户）
```shell
[root@server0 ~]# id student
[root@server0 ~]# mkdir /root/findfiles
[root@server0 ~]# find /   -user   student   -type f
[root@server0 ~]# find /   -user   student   -type f  -exec  cp  {}  /root/findfiles \;
 [root@server0 ~]#  ls  /root/findfiles
```
> 2）利用find查找/boot目录下大于10M并且必须是文件，拷贝到/opt
```shell
[root@server0 ~]# find  /boot  -size +10M
[root@server0 ~]# find  /boot  -size +10M   -exec  cp  {}  /opt  \;
[root@server0 ~]# ls  /opt
```
> 3）利用find查找/boot/ 目录下以 vm 开头且必须是文件，拷贝到/opt
```shell
[root@server0 ~]# find  /boot  -name  “vm*”  
[root@server0 ~]# find  /boot  -name  “vm*”   -exec  cp  {}   /opt  \;
[root@server0 ~]# ls   /opt
```
> 4）利用find查找/boot/ 目录下为快捷方式
```shell
[root@server0 ~]# find  /boot  -type  l
```
> 5）利用find查找/etc 目录下，以 tab 作为结尾的 必须是文件
```shell
[root@server0 ~]# find  /etc   -name  “*tab”  -type f
```
# 4. vim效率操作
## 4.1 问题
本例要求掌握使用vim文本编辑器时能够提高操作效率的一些常用技巧和方法，完成下列任务：

1. 将文件 /etc/passwd 复制为 /opt/nsd.txt，然后打开 /opt/nsd.txt 文件，练习命令模式下的切换/复制/删除/查找操作
2. 将文件 /etc/man_db.conf 复制到 /opt 目录下，然后打开 /opt/man_db.conf 文件，将第50~100行内的“man”替换为“MAN”，在 vim 中设置显示行号查看效果
## 4.2 方案
命令模式常用操作：

- 1G 或 gg ，跳转到文件的首行
- G ，跳转到文件的末尾行
- yy、#yy ，复制光标处的一行、#行
- p、P ，粘贴到光标处之后、之前
- x 或 Delete键 ，删除光标处的单个字符
- dd、#dd ，删除光标处的一行、#行
- d^、d$ ，从光标处之前删除至行首/行尾
- /word 向后查找字符串“word”，再按n/N跳至后/前一个结果
- u ，撤销最近的一次操作
- U ，撤销对当前行的所有修改
- Ctrl + r 取消前一次撤销操作
- ZZ 保存修改并退出

末行模式常用操作：

- :s/old/new ，替换当前行第一个“old”
- :s/old/new/g ，替换当前行所有的“old”
- :n,m s/old/new/g ，替换第n-m行所有的“old”
- :% s/old/new/g ，替换文件内所有的“old”
- :w /root/newfile ，另存为其它文件
- :r /etc/filesystems ，读入其他文件内容
- :set nu|nonu ，显示/不显示行号
- :set ai|noai ，启用/关闭自动缩进
## 4.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：vim命令模式下的切换/复制/删除/查找**

> 1）建立练习文件

将文件 /etc/passwd 复制为 /opt/nsd.txt：
```shell
[root@svr7 ~]# cp  /etc/passwd  /opt/nsd.txt
```
> 2）使用vim打开练习文件，默认处于命令模式
```shell
[root@svr7 ~]# vim  /opt/nsd.txt
.. ..
```
> 3）在命令模式下完成下列操作

切换操作：G 最后一行，5G 第5行，gg 第一行。
复制操作：按2yy复制2行，7G移动到第7行，p 粘贴。
删除操作：25G 移动到第25行，200dd 从此行开始删除200行（不够就剩下全删）。
查找操作：gg 第一行，/adm 查找关键词adm，n 跳转到下一个结果。

> 4）保存并退出编辑器

ZZ 保存退出。

**步骤二：vim末行模式下的替换/设置操作**

> 1）建立练习文件

将文件 /etc/man_db.conf 复制到 /opt/ 目录下：
```shell
[root@svr7 ~]# cp  /etc/man_db.conf  /opt/
```
> 2）使用vim打开练习文件，输入:切换到末行模式
```shell
[root@svr7 ~]# vim  /opt/man_db.conf
.. ..
: 
```
> 3）在末行模式下完成下列操作

输入 :set nu ，确认后显示行号。

输入 :50,100 s/man/MAN/g ，确认将第50~100行内的“man”替换为“MAN”。

> 4）保存并退出编辑器

输入 :wq ，确认后保存并退出编辑器。



# Exercise
## 1 将目录/usr/local压缩备份为/root/ulocal.tar.xz文件
```shell
[root@server0 ~]# tar  -Jcf  /root/ulocal.tar.xz  /usr/local/
[root@server0 ~]# ls  -lh  /root/ulocal.tar.xz 
-rw-r--r--. 1 root root 8.0K Nov 26 00:02 /root/ulocal.tar.xz
```
## 2 重定向与管道的区别

重新定:将前面命令的输出，写入到后面文本文件中，能够连接命令与文件

管道:将前面命令的输出，传递到后面命令，作为后面命令的参数，能够连接命令与命令

## 3 利用find查找/etc 目录下，以dow作为结尾的并且必须是文件
```shell
[root@server0 ~]# find  /etc   -name   “*dow”    -type   f
```
## 4 vim编辑器的删除、复制、粘贴操作
使用vim编辑器时，在命令模式下按（ dd ）可删除当前光标行，按（ yy ）可复制当前行，按（ p ）将剪贴板中的文本粘贴到当前行之后。


> 如有侵权，请联系作者删除
