@[TOC]( YAML syntax & Ansible Playbook scripts & Ansible variables & summaries and QQS | Cloud computing )

---
# 1. Playbook应用案例
## 1.1 问题
沿用练习二，编写Ansible Playbook剧本，使用Playbook完成自动化操作，具体要求如下：

- 熟悉Playbook语法格式
- 编写Playbook管理系统账户
- 编写Playbook管理逻辑卷
- 编写Playbook管理软件包

## 1.2 方案
Ansible ad-hoc可以通过命令行形式远程管理其他主机，适合执行一些临时性简单任务。另外还有一种远程管理的方式叫Playbook，Ansible Playbook中文名称叫剧本,它将经常需要执行的任务写入一个文件，这个文件就叫剧本。

- 剧本中可以包含多个任务
- 剧本写后，我们随时根据剧本，执行相关的任务命令
- Playbook剧本要求按照YAML格式编写
- 适合执行周期性经常执行的复杂任务

YAML是什么？

- YAML是一个可读性高、用来表达数据序列的格式语言
- YAML：YAML Ain't a Markup Language
- YAML以数据为中心，重点描述数据的关系和结构

YAML的格式要求如下：
- "#"代表注释，一般第一行为三个横杠（---）
- 键值（key/value）对使用":"表示，数组使用"-"表示，"-"后面有空格
- key和value之间使用":"分隔，":"后面必须有空格
- 一般缩进由两个或以上空格组成
- 相同层级的缩进必须对齐，缩进代表层级关系
- 全文不可以使用tab键
- 区分大小写
- 扩展名为yml或者yaml
- 跨行数据需要使用>或者|，其中|会保留换行符

YAML示例展示：

1）demo1
```shell
---
"诗仙": "李白"
或者
"诗仙": 
   "李白"
```

2）demo2
```shell
#数组的例子
---
- "李白"
- "杜甫"
- "白居易"
- "唐僧"
```
3）demo3
```shell
#使用一行表示数组的例子
---
"诗人": ["李白","杜甫","白居易"]
```
4)demo4
```shell
#键值对和数组符合例子：
---
"诗人":
  - "李白"
  - "杜甫"
  - "白居易"
 ```
5)demo5
```shell
#复杂案例
---
- "诗人":
    - 唐代:
         - "李白"
         - "杜甫"
    - 宋代:
         - "苏轼"
         - "李清照"
```
6）demo6
```shell
#喜欢的电影
---   
- 芳华
- 战狼
- 霸王别姬
```
7）demo7
```shell
#人物描述
---   
- 姓名: 李白
  年龄: 61
  作品: 蜀道难
  好友: 汪伦
```
8）demo8
```shell
#跨行文本（计算机理解为一行）
---  
自我介绍:  >
  字太白,号青莲居士,
  唐代诗人,祖籍陇西郡,
  今甘肃省平凉市
```
9）demo9
```shell
#跨行文本（计算机理解为多行）
---  
自我介绍:  |
  字太白,号青莲居士,
  唐代诗人,祖籍陇西郡,
  今甘肃省平凉市 
```
10）demo10

注意-和:后面必须有空格。
```shell
#一张发票
--- 
发票编号: 34843
日期: 2028-12-12
商品:
  - 商品编号: BL394D
    描述: 足球
    价格: 100
  - 商品编号: BL4438H
    描述: 棒球
    价格: 200
税费: 10.00
总价: 310.00
备注: >
    本次采购商品均
    属于球类运动商品.   
```
11）demo11
```shell
#错误日志
---
时间: 2028-10-01  15:01:42
用户: ed
错误信息: 
  - 文件: nginx.conf
    行号: 23
    错误编码: "0x3D5FF1"
  - 文件: test.php
    行号: 12
    错误代码: "0xA4C51E"
警告信息: |
    你有两个错误信息需要查看,
    一条是配置文件错误,
    一条是脚本语法错误,
    具体内容参考错误信息.   
```
Playbook语法格式要求如下：

- playbook采用YAML格式编写
- playbook文件中由一个或多个play组成
- 每个play中可以包含:
- hosts(主机)、tasks(任务)、vars(变量)等元素组成
- 使用ansible-playbook命令运行playbook剧本

**步骤一：测试Playbook语法格式**

1）编写第一个Playbook（剧本）
```shell
hosts、tasks、name是关键词（不可修改），ping是模块，调用不同模块完成不同任务。

[root@control ansible]# vim ~/ansible/test.yml 
---
- hosts: all                                #hosts定义要远程谁？
  tasks:                                    #tasks定义远程后要执行的任务有哪些？
      - name: This is my first playbook      #name后面的具体内容可以任意
        ping:
[root@control ansible]# ansible-playbook ~/ansible/test.yml
执行效果如图-1所示。
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/736dce3f7c25445bafbf2bb9fbd69835.png)图-1

2）定义多个主机和任务的剧本

hosts由一个或多个组或主机组成，逗号分隔，tasks由一个或多个任务组成，多个任务按顺序执行，执行ansible-playbook命令可以使用-f选项自定义并发量。
```shell
[root@control ansible]# vim ~/ansible/test.yml 
- hosts: test,webserver
  tasks:
      - name: This is my first playbook     #name后面的内容可以任意
        ping:
      - name: Run a shell command
        shell: touch ~/shell.txt
#hosts定义需要远程哪些被管理主机，hosts是关键词
#tasks定义需要执行哪些任务，tasks是关键词
#第一个任务调用ping模块,该模块没有参数
#第二个任务调用shell模块在被管理主机创建一个空文件~/shell.txt
[root@control ansible]# ansible-playbook ~/ansible/test.yml  -f 5
## 验证：到node1、node3、node4主机分别执行命令ls /root/shell.txt查看是否有该文件
```
3）多个play的Playbook文件
```shell
[root@control ansible]# vim ~/ansible/test.yml
#第一个play剧目
---
- hosts: test
  tasks:
      - name: This is first play
        ping:
#第二个play剧目
- hosts: webserver
  tasks:
      - name: This is second play
        ping:
```
**步骤二：Playbook应用案例**

1）用户管理，创建系统账户、账户属性、设置密码（ansible-doc user）。
```shell
[root@control ansible]# vim ~/ansible/test_john.yml
---
- hosts: webserver
  tasks:
    - name: Add the user 'johnd' 
      user:
        name: johnd
        uid: 1040
        group: daemon
        password: "{{ '123' | password_hash('sha512') }}"
#hosts定义需要远程的对象是webserver组，hosts是关键词
#tasks定义需要执行的任务，tasks是关键词
# name是第一个任务的描述信息，描述信息可以任意
# user是第一个任务需要调用的模块，user下面的缩进内容是给user模块的参数
# name是需要创建的用户名，uid是用户ID号
# group是用户属于哪个基本组
# password是用户的密码，密码是123，密码经过sha512算法加密
[root@control ansible]# vim ~/ansible/user_james.yml
---
- hosts: webserver
  tasks:    
    - name:  Add 'james' with a bash shell
      user:
        name: james
        shell: /bin/bash
        groups: bin,adm
        password: "{{ '123' | password_hash('sha512') }}" 
#与上一个案例类似，groups指定用户属于哪些附加组.
[root@control ansible]# vim ~/ansible/user_johnd.yml
---
- hosts: webserver
  tasks:
    - name: Remove the user 'johnd'
      user:
        name: johnd
        state: absent
#删除系统账户johnd，state的值设置为absent是删除用户
```
2）使用playbook管理逻辑卷

准备工作：给node2主机再添加一块磁盘（以下实验磁盘名称仅为参考，不要照抄）。

`注意：请确保node2主机提前安装了lvm2软件包。`

（ansible-doc parted，ansible-doc lvg，ansible-doc lvol）
```shell
[root@control ansible]# vim ~/ansible/lvm.yml
---
- hosts: node2                            #远程node2主机
  tasks:
    - name: Create a new primary partition with a size of 1GiB  #任务的描述信息
      parted:                                 #调用parted模块进行分区         
        device: /dev/vdb                     #对/dev/vdb磁盘进行分区(磁盘名称不要照抄)
        label: gpt                          #分区表类型为gpt，或msdos
        number: 1                           #分区编号(创建第几个分区)
        state: present                     #present是创建分区,absent是删除分区
        part_start: 1MiB                   #分区的开始位置（默认从最开始位置分区）
        part_end: 1GiB                     #分区的结束位置（不写就分到磁盘最后位置）
    - name: Create a volume group on top of /dev/vdb1     #第二个任务的描述信息
      lvg:                                  #调用lvg模块,创建VG卷组
        vg: my_vg                          #要创建的卷组名称
        pvs: /dev/vdb1                     #使用哪个分区创建PV
    - name: Create a logical volume of 512m          #第三个任务的描述信息
      lvol:                                 #调用lvol模块创建LV
        vg: my_vg                          #使用哪个VG创建LV
        lv: my_lv                          #需要创建的LV名称
        size: 512m                         #要创建的LV大小,可以不指定单位，默认单位m
```
3）使用playbook管理软件（ansible-doc yum）

RHEL或CentOS系统中的软件有组包的概念，使用yum grouplist或者dnf grouplist可以查看组包的名称。
```shell
[root@control ansible]# vim ~/ansible/package.yml
---
- hosts: webserver                        #需要远程的主机是谁
  tasks:                                   #定义剧本需要执行的任务
    - name: Install a list of packages  #第一个任务的描述信息 
      yum:                                 #调用yum模块安装软件
        name:                              #安装软件的名字，它的值有多个，使用数组-
          - httpd                          #安装httpd软件
          - mariadb                        #安装mariadb软件
          - mariadb-server                #安装mariadb-server
    - name: install the 'RPM Development Tools' package group   #第二个任务的描述信息
      yum:                                  #调用yum模块安装软件组包
        name: "@RPM Development Tools"        #安装哪个组包，@是关键词
    - name: update software               #第三个任务的描述信息
      yum:                                  #调用yum模块升级软件
        name: '*'                           #需要升级哪些软件
        state: latest                       #latest代表升级软件
#备注:state的值可以是(present|absent|latest)
#present代表安装软件(默认是present)；absent代表卸载软件
#latest代表升级软件
```

# 2. Ansible变量应用案例
## 2.1 问题
沿用前面课程环境，继续练习Ansible 特殊模块并掌握自定义变量的方式，具体要求如下：

- 熟悉setup与debug模块
- 熟悉各种常见的变量定义方式

**步骤一：Ansible特殊模块**

1）setup模块

ansible_facts用于采集被管理设备的系统信息，所有收集的信息都被保存在变量中，每次执行playbook默认第一个任务就是Gathering Facts，使用setup模块可以查看收集到的facts信息。
```shell
[root@control ansible]# ansible test -m setup
192.168.4.10 | SUCCESS => {
"ansible_facts": {
   "ansible_all_ipv4_addresses": [
… 省略部分内容…
```
试试自己找出下列变量：

- ansible_all_ipv4_addresses #IP地址
- ansible_bios_version #主板BIOS版本
- ansible_memtotal_mb #总内存
- ansible_hostname #主机名
- ansible_fqdn #主机的域名
- ansible_devices.vda.partitions.vda1.size #某个磁盘分区的大小

2）debug模块

debug模块可以显示变量的值，可以辅助排错，通过msg可以显示变量的值，变量需要使用{{}}扩起来。
```shell
[root@control ansible]# vim ~/ansible/debug.yml
---
- hosts: test
  tasks:
    - debug:
        msg: "主机名是:{{ ansible_hostname }}"
    - debug:
        msg: "总内存大小:{{ ansible_memtotal_mb }}"
#备注调用debug模块显示某些具体的变量值
#debug模块可以显示变量的值，可以辅助排错
```
**步骤二：定义变量的方法**

Ansible支持十几种定义变量的方式，这里我们仅介绍其中一部分变量。

下面是根据优先级排序的定义方式：

1. Inventory变量
2. Host Facts变量
3. Playbook变量
4. 变量文件

1）Inventory变量(在主机清单配置文件中定义变量）。
```shell
[root@control ansible]# vim ~/ansible/inventory
[test]
node1  iname="nb" 
[proxy]
node2
[webserver]
node[3:4]
[webserver:vars]
iname="dachui"
#备注，在node1主机后面给该主机添加变量iname,值为nb.
#给webserver组定义变量,vars是关键词不可以改变,webserver是上面定义的组
#给这个组定义变量iname="dachui"
... ...<部分后面的内容省略>... ...
```
下面编写剧本调用刚才的变量：(在剧本中需要调用变量是要使用{{}})
```shell
[root@control ansible]# vim ~/ansible/inventory_var.yml
---
- hosts: node1,webserver                         #定义需要远程管理的主机是谁               
  tasks:                                           #剧目要完成哪些任务
    - name: create a user with var.              #剧目中的第一个任务描述信息
      user:                                        #调用user模块创建用户
        name: "{{ iname }}"                      #需要创建的用户名是iname这个变量
#注意事项：
#在ansible剧本中当调用变量时，开始位置就调用变量,就需要在{{}}外面加双引号
#如果是在后面或者中间位置调用变量{{}}外面可以不加双引号,也可以加双引号
#如:
#  "{{ iname }}"
#  nihao {{ iname }}
```
2）Host Facts变量（可以直接调用ansible收集的系统信息）
```shell
[root@control ansible]# vim ~/ansible/facts_var.yml
---
- hosts: test
  tasks:
    - name: create user.
      user:
        name: "{{ansible_hostname}}"
#定义剧本，远程所有被管理主机，调用user模块，创建用户
#需要创建的用户名ansible_hostname是一个ansible_facts变量
#验证： 到node1主机查看是否有一个与主机名同名的用户
```
3）Playbook变量(使用vars关键词可以在playbook内定义变量）。
```shell
[root@control ansible]# vim ~/ansible/playbook_var.yml
---
- hosts: test
  vars:                                     #vars是关键词，用来定义变量用的
    iname: heal                            #具体变量名是iname，值是heal
    ipass: '123456'                       #再定义一个变量名是ipass，值是123456
#注意密码必须是字符串，需要引号                           
  tasks:                                   #tasks定义需要执行的任务
    - name: Use variables create user.  #给任务写个描述信息   
      user:                                #调用user模块创建用户
        name: "{{ iname }}"               #用户名的是前面定义的变量
        password: "{{ ipass | password_hash('sha512') }}"
#密码是前面定义好的ipass,管道给password_hash把密码加密.
```
4）单独定义个变量文件，在playbook中用vars_files调用该文件。
```shell
[root@control ansible]# vim ~/ansible/file_var.yml
---
- hosts: test
  vars_files: variables.yml             #当变量比较多时，专门定义一个文件用来存变量
  tasks:
    - name: create user.
      user:
        name: "{{ iname }}"
        password: "{{ ipass | password_hash('sha512') }}"
#调用user模块创建用户
#用户名是变量文件variables.yml中定义的变量iname，密码也是变量文件中定义的变量
[root@control ansible]# vim  ~/ansible/variables.yml
---
iname: cloud
ipass: '123456'
```
附加思维导图，如图-2所示：

![在这里插入图片描述](https://img-blog.csdnimg.cn/af36ba35d9fe4627b408cfe1c6765312.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-2


# Exercise
## 1 在YAML文件中使用什么符号支持跨行文本
\> 或者 |

## 2 在Ansible的Playbook剧本中使用什么关键词定义任务？
tasks

## 3 YAML文件中用什么代表数组，什么代表kv数据？

`-`代表数组
`:`代表kv数据

## 4 简单描述ansible_facts的作用？
- ansible_facts用于采集被管理设备的系统信息
- 所有收集的信息都被保存在变量中
- 每次执行playbook默认第一个任务就是Gathering Facts
- 使用setup模块可以查看收集到的facts信息

> 如有侵权，请联系作者删除
