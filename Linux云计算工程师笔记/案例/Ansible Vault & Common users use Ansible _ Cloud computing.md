@[TOC]( Ansible Vault & Common users use Ansible | Cloud computing )

---
# 1. 综合练习（自动化部署Web集群）
## 1.1 问题
晚自习课外综合练习题，创建一个名为cluster的role，完成一个综合项目，具体要求如下：

- 创建Role，通过Role完成项目
- 部署Nginx调度器
- 部署2台http服务器

## 1.2 方案
综合练习题实验所需主机清单如表-1所示。

表-1 主机列表
![在这里插入图片描述](https://img-blog.csdnimg.cn/18c7c5c3a4e64cdda96328e5ef8ff0e5.png)


**步骤一：部署两台后端http服务器**

1）创建role角色
```shell
[root@control ansible]# ansible-galaxy  init  ~/ansible/roles/http
```
2）修改role配置文件，准备2台http网站的素材

安装httpd，拷贝一个网页文件。
```shell
[root@control ansible]# vim roles/http/tasks/main.yml
---
- name: install httpd
  yum:
    name: httpd
    state: present
- name: create index.html
  copy:
    content: "{{ansible_hostname}}"
    dest: /var/www/html/index.html
- name: set firewalld
  firewalld:
    service: http
    state: enabled
    permanent: yes
    immediate: yes
- name: start httpd
  service:
    name: httpd
    state: started
    enabled: yes
#文件中包含多个任务，每个任务可以设置一个name名字（也可以没有name）
#第一个任务调用yum模块安装httpd软件包
#第二个任务调用copy模块创建一个新的网页文件(index.html)
#调用copy模块时可以在没有源文件的情况下，直接使用content指定文件的内容
#将该内容直接拷贝到被管理主机的某个文件中(/var/www/html/index.html)
#第三个任务调用firewalld模块，设置防火墙规则，允许访问http服务
#第四个任务调用service模块将httpd服务启动，并设置开机自启。
```
3）编写Playbook调用role，并执行Playbook。
```shell
[root@control ansible]# vim web.yml
---
- hosts: webserver
  roles:
    - http
[root@control ansible]# ansible-playbook web.yml
```
**步骤二：部署nginx代理服务器**

1）创建role角色
```shell
[root@control ansible]# ansible-galaxy  init  ~/ansible/roles/proxy
```
2）准备代理服务器需要的素材

拷贝Nginx源码包，编写一个源码编译安装nginx的shell脚本。
```shell
[root@control ansible]# cp  lnmp_soft/nginx-1.17.6.tar.gz  \
~/ansible/roles/proxy/files/
[root@control ansible]# vim ~/ansible/roles/proxy/files/nginx_install.sh
#!/bin/bash
yum -y install gcc pcre-devel openssl-devel make tar
cd /tmp
tar -xf /tmp/nginx-1.17.6.tar.gz
cd nginx-1.17.6
./configure --with-http_ssl_module
make
make install
```
新建一个Nginx代理服务器的配置文件模板。
```shell
[root@control ansible]# vim ~/ansible/roles/proxy/files/nginx.conf
worker_processes  2;
#error_log  logs/error.log;
events {
    worker_connections  65535;
}
http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    tcp_nopush     on;
    keepalive_timeout  65;
    #gzip  on;
upstream webs {
   server 192.168.4.13;
   server 192.168.4.14;
}
    server {
        listen       80;
        server_name  localhost;
        location / {
            proxy_pass http://webs;
            root   html;
            index  index.html index.htm;
        }
        error_page  404              /404.html;
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}
```
3）修改role配置文件。
```shell
[root@control ansible]# vim roles/proxy/tasks/main.yml
---
- name: copy nginx-1.17.6.tar.gz to proxy.
  copy:
    src: nginx-1.17.6.tar.gz
    dest: /tmp/
#拷贝源码包软件
- name: install nginx through shell script.
  script: nginx_install.sh
  args:
    creates: /usr/local/nginx/sbin/nginx
#执行源码编译安装脚本，如果已经安装nginx，则不再执行安装脚本.
#args是关键词，设置script模块的参数，通过creates参数做判断，creates也是关键词
#creates后面跟文件名，如果creates判断文件存在的话就不再执行script模块对应的命令。
- name: copy nginx.conf to destination host.
  copy:
    src: nginx.conf
    dest: /usr/local/nginx/conf/nginx.conf
- name: run nginx service.
  shell: /usr/local/nginx/sbin/nginx
  args:
    creates: /usr/local/nginx/logs/nginx.pid
#nginx.pid存在，说明nginx已经启动。如果该文件存在，则不再启动nginx。
- name: set firewalld
  firewalld:
    service: http
    state: enabled
    permanent: yes
    immediate: yes
```
4）编写Playbook调用role,并执行Playbook。
```shell
[root@control ansible]# vim proxy.yml
---
- hosts: proxy
  roles:
    - proxy
[root@control ansible]# ansible-playbook proxy.yml
```
# 2. 加密敏感数据
## 2.1 问题
本案例要求，使用ansible-vault对敏感数据进行加密处理，具体要求如下：

- 使用ansible-vault管理敏感数据
## 2.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：使用ansible-vault处理敏感数据**

1）加密敏感数据。

encrypt（加密）、decrypt（解密）、view（查看），rekey（重置密码）。
```shell
[root@control ansible]# echo 123456 > data.txt               #新建测试文件
[root@control ansible]# ansible-vault encrypt data.txt      #加密文件
[root@control ansible]# cat data.txt
[root@control ansible]# ansible-vault view data.txt         #查看加密文件
```
2）修改密码（rekey）
```shell
[root@control ansible]# ansible-vault rekey data.txt             #修改密码
Vault password: <旧密码>
New Vault password: <新密码>
Confirm New Vault password:<确认新密码>
```
3）解密文件
```shell
[root@control ansible]# ansible-vault decrypt data.txt      #解密文件
[root@control ansible]# cat data.txt
```
4）使用密码文件

加密、解密每次都输入密码很麻烦，可以将密码写入文件。
```shell
[root@control ansible]# echo "I'm secret data" > data.txt       #需要加密的敏感数据
[root@control ansible]# echo 123456 > pass.txt                   #加密的密码
[root@control ansible]# ansible-vault  encrypt --vault-id=pass.txt  data.txt 
[root@control ansible]# cat data.txt
[root@control ansible]# ansible-vault decrypt --vault-id=pass.txt data.txt
[root@control ansible]# cat data.txt
```
# 3. 配置sudo权限
## 3.1 问题
本案例要求使用sudo提升普通用户的权限，要求如下：

- 给所有被管理主机创建系统账户
- 账户名称为alice，密码为123456
- 修改sudo配置，让alice可以执行任何管理命令

## 3.2 方案
sudo（superuser or another do）让普通用户可以以超级管理员或其他人的身份执行命令。

sudo基本流程如下：

1. 管理员需要先授权（修改/etc/sudoers文件）
2. 普通用户以sudo的形式执行命令

修改/etc/sudoers的方法如下：
1. visudo（带语法检查，默认没有颜色提示）
2. vim /etc/sudoers（不带语法检查，默认有颜色提示）

授权格式如下：
用户或组 主机列表=(提权身份) [NOPASSWD]:命令列表

注意事项：命令需要写绝对路径，对组授权需要在组名称前面加%。
```shell
[root@control ~]# cat  /etc/sudoers         #不要改，下面仅仅是语法格式的示例（例子）
… …
root           ALL=(ALL)       ALL
tom            ALL=(root)      /usr/bin/systemctl
%wheel         ALL=(ALL)       ALL
```
## 3.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：配置sudo提权**

1）远程所有被管理主机批量创建系统账户，账户名称为alice，密码为123456。
```shell
[root@control ansible]# ansible all -m user -a "name=alice \
password={{'123456' | password_hash('sha512')}}"
```
2）配置alice账户可以提权执行所有命令（control批量授权，node1主机验证）。

使用lineinfile模块修改远程被管理端主机的/etc/sudoers文件，line=后面的内容是需要添加到文件最后的具体内容。

等于是在/etc/sudoers文件末尾添加一行:alice ALL=(ALL) NOPASSWD:ALL
```shell
[root@control ansible]# ansible all -m lineinfile \
-a "path=/etc/sudoers line='alice  ALL=(ALL) NOPASSWD:ALL'"
```
如何验证？可以在node1电脑上面使用alice用户执行sudo重启服务的命令看看是否成功。
```shell
[root@control ~]# ssh alice@node1
[alice@node1 ansible]$ sudo systemctl restart sshd       #不需要输入密码
[alice@node1 ansible]$ exit
```
# 4. 修改Ansible配置
## 4.1 问题
沿用练习一，修改ansible配置实现使用普通用户远程被控制端主机，具体要求如下：

- 修改主配置文件
- 设置ansible远程被管理端主机账户为alice
- 设置ansible远程管理提权的方式为sudo
- 修改主机清单文件
- 修改主机清单配置文件，添加SSH参数

## 4.2 步骤
实现此案例需要按照如下步骤进行。

步骤一：配置普通用户远程管理其他主机

1）修改主配置文件，配置文件文件的内容可以参考/etc/ansible/ansible.cfg。
```shell
[root@control ansible]# vim ~/ansible/ansible.cfg
[defaults]
inventory = ~/ansible/inventory
remote_user = alice                #以什么用户远程被管理主机（被管理端主机的用户名）
[privilege_escalation]
become = true                    #alice没有特权，是否需要切换用户提升权限
become_method = sudo                #如何切换用户（比如用su就可以切换用户，这里是sudo）
become_user = root                #切换成什么用户（把alice提权为root账户）
become_ask_pass = no                #执行sudo命令提权时是否需要输入密码
```
思考：

如果A主机ssh远程访问B主机，应该输入哪个主机的用户名和对应的密码？

如果张三要去李四家，应该使用谁家的钥匙，打开谁家的门？

2)远程被管理端主机的alice用户，需要提前配置SSH密钥。
```shell
[root@control ansible]# for i in node1  node2  node3  node4  node5
do
  ssh-copy-id    alice@$i
done
```
验证效果：
```shell
[root@control ansible]# ssh alice@node1            #依次远程所有主机看看是否需要密码
#注意：是远程登录node1，应该输入的是node1电脑上面alice账户的密码，control没有alice用户
[root@node1 ~]# exit                                #退出远程连接
[root@control ansible]# ansible all -m command -a  "who"              #测试效果
[root@control ansible]# ansible all -m command -a  "touch /test"     #测试效果
```
常见报错（有问题可以参考，没问题可以忽略）：
```shell
node1 | UNREACHABLE! => {
    "changed": false,
    "msg": "Failed to connect to the host via ssh: alice@node1: Permission denied (publickey,gssapi-keyex,gssapi-with-mic,password).",
    "unreachable": true
}
问题分析：
英语词汇：Failed（失败），connect（连接），to（到），host（主机），via（通过）
permission（权限），denied（被拒绝）
Failed to connect to host via ssh alice@node1（通过ssh使用alice远程连接到主机失败）
Permission denied（因为无法连接，所以报错说权限被拒绝）
解决办法：手动ssh alice@主机名（如node1），看看是否可以实现免密码登录。
          Ansible的原理是基于ssh远程管理，如果无法实现alice免密码登录，则实验会失败！
        如何实现免密码登录，可以参考案例上面的命令，或者第一阶段相关知识。
```
3）修改inventory主机清单配置文件（参考即可，不需要操作）。

如果个别主机的账户不同，该如何处理呢？

如果有些主机需要使用密码远程呢？如果有些主机的SSH端口不是22呢？
```shell
[root@control ~]# cat  ~/ansible/inventory
[test]                    
node1           ansible_ssh_port=端口号                      #自定义远程SSH端口
[proxy]
node2           ansible_ssh_user=用户名                    #自定义远程连接的账户名
[webserver]
node[3:4]       ansible_ssh_pass=密码                     #自定义远程连接的密码
[database]
node5
[cluster:children]                
webserver
database
```
附加思维导图，如图-1所示：

![在这里插入图片描述](https://img-blog.csdnimg.cn/46157ce584f841b086a8b9d21c36669c.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-1


# Exercise
## 1 ansible-vault加密数据的命令是什么？
```shell
# ansible-vault  encrypt  <文件名>
```
## 2 ansible-vault解密数据的命令是什么？
```shell
# ansible-vault  decrypt  <文件名>
```
## 3 ansible-vault修改密码的命令是什么？
```shell
# ansible-vault  rekey  <文件名>
```
## 4 通过sudo给普通用户授权时使用什么关键词可以免密码执行sudo？
NOPASSWD

> 如有侵权，请联系作者删除
