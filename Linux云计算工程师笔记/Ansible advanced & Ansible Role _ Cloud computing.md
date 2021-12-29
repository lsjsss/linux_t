﻿@[TOC]( Ansible advanced & Ansible Role | Cloud computing )

---
# 1. ansible应用案例
## 1.1 问题
本案例要求掌握Ansible更多高级语法知识，具体要求如下：

- 熟悉firewalld和template模块的使用
- 熟悉error处理机制
- 熟悉handlers任务
- 熟悉when条件判断
- 熟悉block任务块
- 熟悉loop循环的使用方法

## 1.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：firewalld模块**

使用firewalld模块可以配置防火墙策略。
```shell
[root@control ~]#  vim ~/ansible/firewall.yml
---
- hosts: test                           #hosts定义需要远程的主机
  tasks:                                 #tasks定义需要执行哪些任务
    - name: install firewalld.         #name为第一个任务定义描述信息
      yum:                               #第一个任务调用yum模块安装软件
        name: firewalld                 #需要安装的软件名称为firewalld
        state: present                  #state等于present代表安装软件
    - name: run firewalld.             #定义第二个任务的描述信息
      service:                          #第二个任务调用service模块启动服务
        name: firewalld                #启动的服务名称为firewalld
        state: started                 #state等于started代表启动服务
        enabled: yes                    #enabled等于yes是设置服务为开机自启动
    - name: set firewalld rule.       #第三个任务的描述信息
      firewalld:                        #第三个任务调用firewalld模块设置防火墙规则
        port: 80/tcp                    #在防火墙规则中添加一个放行tcp，80端口的规则
        permanent: yes                  #permaenent 是设置永久规则
        immediate: yes                  #immediate 是让规则立刻生效
        state: enabled                  #state等于enabled是添加防火墙规则
#最终：在默认zone中添加一条放行80端口的规则
```
**步骤二：template模块**

copy模块可以将一个文件拷贝给远程主机，但是如果希望每个拷贝的文件内容都不一样呢？如何给所有web主机拷贝index.html内容是各自的IP地址？

Ansible可以利用Jinja2模板引擎读取变量，之前在playbook中调用变量，也是Jinja2的功能，Jinja2模块的表达式包含在分隔符"{{ }}"内。

这里，我们给webserver主机拷贝首页，要求每个主机内容不同。
```shell
[root@control ansible]# vim ~/ansible/index.html
Welcome to {{ansible_hostname}} on {{ ansible_eth0.ipv4.address }}. 
#注意网卡名称根据实际情况填写，不可以完全照抄，不知道网卡名可以通过ip a s查询！
#{{ansible_hostname}}和{{ ansible_eth0.ipv4.address }}是ansible自动的facts变量。         
```
2）编写Playbook将网页模板文件拷贝到远程主机。
```shell
[root@control ansible]# vim ~/ansible/template.yml
---
- hosts: webserver
  tasks:
    - name: use template copy index.html to webserver.
      template:
        src: ~/ansible/index.html
        dest: /tmp/index.html
#hosts定义需要远程的目标主机是谁；tasks定义需要执行的任务是什么
#- name定义任务的描述信息；任务需要调用的模块是template模块
#template模块需要两个参数，src指定需要拷贝的源文件，dest指定需要拷贝的目标位置
#src: ~/ansible/template/index.html是上面创建的文件,文件中包含变量
#dest: /tmp/index.html拷贝到目标主机放在/tmp目录下
```

**步骤三：Ansible高级语法应用**

1）error错误处理

默认ansible在遇到error会立刻停止playbook，使用ignore_errors可以忽略错误，继续后续的任务。

如果一个剧本里面有20个任务，执行到第3个时失败，则不再往下执行。

下面这个这个Playbook在执行时会意外中断。
```shell
[root@control ansible]# vim ~/ansible/error.yml
---
- hosts: test
  tasks:
    - name: start a service that does not exist.
      service:
        name: hehe         #注意：没有这个服务（启动一个不存在的服务）                                       
        state: started
    - name: touch a file.
      file:
        path: /tmp/service.txt
        state: touch
```
下面这个Playbook在执行时因为忽略了错误（针对某一个任务），不会被中断。
```shell
[root@control ansible]# vim ~/ansible/error.yml
---
- hosts: test
  tasks:
    - name: start a service that does not exist.
      service:
        name: hehe
        state: started
      ignore_errors: true       #针对某一个任务忽略错误(ignore_errors是关键词)                          
    - name: touch a file.
      file:
        path: /tmp/service.txt
        state: touch
```
下面这个Playbook在执行时因为忽略了错误，不会被中断。
```shell
[root@control ansible]# cat ~/ansible/error.yml
---
- hosts: test
  ignore_errors: true      #针对playbook全局忽略错误                             
  tasks:
    - name: start a service that does not exist.
      service:
        name: hehe
        state: started
    - name: touch a file.
      file:
        path: /tmp/service.txt
        state: touch
```
2）handlers

在剧本中tasks用来定义任务（一定会执行），handlers也可以定义任务（不一定执行），handlers任务要想执行必须要被别人触发才能执行。
```shell
实例草稿：
---
- hosts: test
  tasks:
    - 任务1
       notify:任务5
    - 任务2
  handlers:
    - 任务5
    - 任务6
```
可以通过handlers定义一组任务，仅当某个任务触发(notify)handlers时才执行相应的任务，如果有多个notify触发执行handlers任务，也仅执行一次。

仅当任务的执行状态为changed时handlers任务才执行，handlers任务在所有其他任务都执行后才执行。

下面编写一个通过notify触发执行handlers任务的案例。
```shell
[root@control ansible]# vim ~/ansible/handlers.yml
---
- hosts: test
  tasks:
    - name: create directory.           #多次执行playbook该任务状态不再是changed
      file:                               #调用file模块创建目录
        path: /tmp/parents/subdir/      #需要创建的具体目录名称
        state: directory                #state等于directory代表创建目录
      notify: touch file                #notify后面名称必须和handlers中的任务名称一致           
  handlers:                              #通过handlers再定义一组任务
    - name: touch file                  #给任务写描述信息（任务的名字，名字可以任意）
      file:                              #调用file模块创建文件
        path: /tmp/parents/subdir/new.txt    #需要创建的文件名
        state: touch                           #state等于touch代表创建文件
#备注：仅当file模块执行成功，
#并且状态为changed时才会通过notify触发执行handlers下面的任务，
#所以多次执行该剧本时，handlers任务不会被重复执行,
#notity后面的名称必须和handlers下面name定义的任务名称一致（名称可以任意）。
```
3）when条件判断

when可以定义判断条件，条件为真时才执行某个任务。

常见条件操作符有：==、!=、>、>=、<、<=。

多个条件可以使用and(并且)或or（或者）分割，when表达式中调用变量不要使用{{ }}。

下面编写Playbook，远程主机剩余内存不足700M则关闭NetworkManager服务
```shell
[root@control ansible]# vim ~/ansible/when_1.yml
---
- hosts: test
  tasks:
    - name: check memory size.
      service:
        name: NetworkManager
        state: stopped
      when: ansible_memfree_mb < 700
#被管理端主机剩余内存不足700M则关闭NetworkManager服务(也可以关闭别的不需要的服务)
#ansible_memfree_mb这个是ansible自带的facts变量,代表剩余内存的容量。
```
下面再编写一个Playbook，判断操作系统是RedHat8则创建测试文件。YAML的语法格式中>支持多行输入，但不保留换行符。
```shell
[root@control ansible]# vim ~/ansible/when_2.yml
---
- hosts: test
  tasks:
    - name: touch a file
      file:
        path: /tmp/when.txt
        state: touch
      when:  >
        ansible_distribution == "RedHat"
        and
        ansible_distribution_major_version == "8"
#判断操作系统是RedHat8则创建测试文件
#YAML的语法格式中>支持多行输入，但不保留换行符（计算机会认为实际是一行内容）
#ansible_distribution和ansible_distribution_major_version都是自带的facts变量
#可以使用setup模块查看这些变量
```
4）block任务块

如果我们需要当条件满足时执行N个任务,我们可以给N个任务后面都加when判断(但是很麻烦),此时可以使用block定义一个任务块,当条件满足时执行整个任务块.

任务块就是把一组任务合并为一个任务组，使用block语句可以将多个任务合并为一个任务组。
```shell
[root@control ansible]# vim ~/ansible/block_1.yml
---
- hosts: test
  tasks:
    - name: define a group of tasks.
      block:                                          #block是关键词，定义任务组
        - name: install httpd                       #任务组中的第一个任务
          yum:                                        #调用yum模块安装httpd软件包
            name: httpd
            state: present
        - name: start httpd                          #任务组中的第二个任务
          service:                                    #调用service模块启动httpd服务
            name: httpd
            state: started
      when: ansible_distribution == "RedHat"       #仅当条件满足再执行任务组
#注意:when和block是对齐的,他们在一个级别,当条件满足时要执行的是任务组（不是某一个任务）
#判断条件是看远程的目标主机使用的Linux发行版本是否是RedHat.
```
对于block任务块，我们可以使用rescue语句定义在block任务执行失败时要执行的其他任务，还可以使用always语句定义无论block任务是否成功，都要执行的任务。

下面编写一个包含rescue和always的示例。
```shell
[root@control ansible]# vim ~/ansible/block_2.yml
---
- hosts: test
  tasks:
    - block:
        - name: touch a file test1.txt
          file:
            name: /tmp/test1.txt      #如果修改为/tmp/xyz/test1.txt就无法创建成功                        
            state: touch
      rescue:
        - name: touch a file test2.txt
          file:
            name: /tmp/test2.txt
            state: touch
      always:
        - name: touch a file test3.txt
          file:
            name: /tmp/test3.txt
            state: touch
#默认在/tmp/目录下创建test1.txt会成功，所以不执行rescue(创建test2.txt)
#如果我们把block中的任务改为创建/tmp/xyz/test1.txt（因为没有xyz目录所以会失败)
#当block默认任务失败时就执行rescue任务(创建test2.txt)
#但是不管block任务是否成功都会执行always任务(创建test3.txt)
```
5）loop循环

相同模块需要反复被执行怎么处理？使用loop循环可以避免重复。

编写Playbook，循环创建目录。
```shell
[root@control ansible]# vim ~/ansible/simple_loop.yml
---
- hosts: test
  tasks:
    - name: mkdir multi directory.
      file:
        path=/tmp/{{item}}       #注意，item是关键字，调用loop循环的值                                
        state=directory
      loop:                       #loop是关键词,定义循环的值,下面是具体的值
        - School
        - Legend
        - Life
#最终在/tmp目录下创建三个子目录.file模块被反复执行了三次。
#mkdir  /tmp/School;  mkdir  /tmp/Legend;   mkdir  /tmp/Life。
```
编写Playbook，循环创建用户并设置密码。
```shell
[root@control ansible]# vim ~/ansible/complex_loop.yml
---
- hosts: test
  tasks:
    - name: create multi user.
      user:
        name: "{{item.iname}}"
        password: "{{item.ipass | password_hash('sha512')}}"
      loop:
        - { iname: 'term', ipass: '123456' }
        - { iname: 'amy' , ipass: '654321' }
#loop循环第一次调用user模块创建用户,user模块创建用户会读取loop里面的第一个值.
#loop第一个值里面有两个子值,iname和ipass
#创建用户item.iname就是loop第一个值里面的iname=term
#修改密码item.ipass就是loop第一个值里面的ipass=123456
#loop循环第二次调用user模块创建用户,user模块创建用户会读取loop里面的第二个值.
#loop第二个值里面有两个子值,iname和ipass
#创建用户item.iname就是loop第二个值里面的iname=amy
#修改密码item.ipass就是loop第二个值里面的ipass=654321
```
# 2. Ansible Roles
## 2.1 问题
学习Ansible Roles基本概念，掌握Roles应用案例，具体要求如下：

- 自定义Ansible Role
- 编写playbook调用role
- 使用ansible-galaxy管理Roles

## 2.2 方案
在实际生产环境中，为了实现不同的功能，我们会编写大量的playbook文件。而且，每个playbook还可能会调用其他文件（如变量文件），对于海量的、无规律的文件，管理起来非常痛苦！

Ansible从1.2版本开始支持Role（角色），Role（角色）是管理ansible文件的一种规范（目录结构），Role（角色）会按照标准的规范，自动到特定的目录和文件中读取数据。

如果我们创建了一个名称为user.example的Role（角色），则其标准的目录结构如下图-1所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/75f8bdd4719d4368aee96ece87fe5a80.png)
图-1

Roles目录结构中主要文件的作用是什么呢？

- defualts/main.yml：定义变量的缺省值，优先级较低
- files目录：存储静态文件的目录，如tar包、音乐、视频等
- handlers/main.yml:定义handlers
- meta/main.yml:写作者、版本等描述信息
- README.md:整个角色(role)的描述信息
- tasks/main.yml:定义任务的地方
- templates目录：存放动态数据文件的地方（文件中包含了变量的模板文件）
- vars/main.yml:定义变量，优先级高

**步骤一：Role应用案例**

1）创建Roles

下面这个案例目的：编写一个包含变量的模板文件，编写任务调用template模块，将模板文件拷贝给被管理端主机。

ansible-galaxy命令可以创建、管理自己的roles。
```shell
[root@control ansible]# mkdir ~/ansible/roles
[root@control ansible]# ansible-galaxy init  ~/ansible/roles/issue
#创建一个Role，该Role的目的是拷贝自己新建的一个模板文件到远程主机的/etc/issue
[root@control ansible]# tree  ~/ansible/roles/issue/
#查看目录结构，如果没有tree命令则需要使用yum安装该软件
```
2）修改Role文件

定义名称为myfile.txt的模板文件（该文件包含变量,因此必须放置templates目录）
```shell
[root@control ansible]# vim ~/ansible/roles/issue/templates/myfile.txt
This is the system {{ansible_hostname}}
Today's date is:{{ansible_date_time.date}}
Contact to {{ admin }}
```
自定义变量文件（前面调用了admin这个变量，这里需要定义admin变量并赋值）
```shell
[root@control ansible]# vim ~/ansible/roles/issue/vars/main.yml
---
# vars file for /root/ansible/roles/issue
admin: yoyo@tedu.cn
#变量名为admin，变量的值为yoyo@tedu.cn
```
文件准备好了，计算机不会自动将文件拷贝给被管理端主机！需要编写任务调用模块实现拷贝的功能。

修改任务文件，任务文件中不需要tasks关键词，Role的各个文件之间相互调用不需要写文件的路径。
```shell
[root@control ansible]# vim ~/ansible/roles/issue/tasks/main.yml
---
# tasks file for /root/ansible/roles/issue
-  name: delever issue file
   template:
     src: myfile.txt
     dest: /etc/issue
#调用template模块将myfile.txt文件拷贝给被管理端主机.
```
3）在Playbook中调用Role

Role创建好了，role不会自己运行，需要编写一个剧本调用上面的role。

编写playbook剧本文件,通过roles关键词调用role。
```shell
[root@control ansible]# vim  ~/ansible/issue.yml
---
- hosts: test
  roles:
    - issue
#- role2              #支持加载多个role
```
修改ansible.cfg配置文件，定义roles目录。
```shell
[root@control ansible]# vim  ~/ansible/ansible.cfg 
[defaults]
inventory = ./inventory
roles_path = ./roles                    #指定到哪个目录下找role
```
**步骤二：ansible-galaxy命令**

公共Roles仓库(https://galaxy.ansible.com)管理。
```shell
[root@control ansible]# ansible-galaxy  search 'httpd' 
#联网搜索roles
[root@control ansible]# ansible-galaxy info acandid.httpd 
#查看roles基本信息
[root@control ansible]# ansible-galaxy install acandid.httpd -p ~/ansible/roles/
#下载roles到特定的目录，-p可以指定下载到哪个目录
```
使用ansible-galaxy install可以直接下载Role，也可以编写requirements.yml文件下载Role。
```shell
[root@control ansible]# vim ~/ansible/roles/requirements.yml
#格式一：可以直接从Ansible Galaxy官网下载
- src: acandid.httpd
#格式二：可以从某个git服务器下载
- src: http://gitlab.com/xxx/xxx.git
  scm: git
  version: 56e00a54
  name: nginx-acme
#格式三：可以指定位置下载tar包，支持http、https、file
- src:  http://example.com/myrole.tar
  name:  myrole
[root@control ansible]# ansible-galaxy install \
-r ~/ansible/roles/requirements.yml \
-p roles
# -r后面跟文件名,该文件中包含了需要下载哪些role以及他们的链接位置
# -p 指定将下载的role保存到哪个目录
```
附加思维导图，如图-2所示：

![在这里插入图片描述](https://img-blog.csdnimg.cn/3d4bc0e55c354f9aad26d370aaaad72d.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-2



# Exercise
## 1 Ansible使用什么语句实现循环功能？

loop语句
## 2 Ansible使用什么关键词可以定义任务块？
block

## 3 Ansible剧本中使用when进行条件判断时，变量是否使用{{}}引用？
否（不适用{{}}）

## 4 哪些是ansible role的标准目录？
- tasks
- defaults
- vars
- files
- handlers

> 如有侵权，请联系作者删除
