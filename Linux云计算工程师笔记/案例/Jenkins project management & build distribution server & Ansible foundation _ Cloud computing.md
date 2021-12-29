@[TOC]( Jenkins project management & build distribution server & automation go live & Ansible foundation | Cloud computing )

---
# 1 案例1：Jenkins项目管理
## 1.1 问题
本案例要求管理Jenkins项目，要求如下：

- 创建Jenkins项目
- 修改Jenkins项目配置

## 1.2 方案
实验环境准备（沿用DAY02的实验环境）：

1）5台RHEL8虚拟机，主机名分别为develop、git、jenkins、web1和web2。
2）develop主机的IP地址为192.168.4.10，不需要配置网关和DNS。
3）git主机的IP地址为192.168.4.20，不需要配置网关和DNS。
4）jenkins主机的IP地址为192.168.4.30，不需要配置网关和DNS。
5）web1和web2主机的IP地址分别为192.168.4.100和192.168.4.200，不需要配置网关和DNS。
6）所有主机都需要配置可用的系统YUM源，设置防火墙信任所有，SELinux放行所有。

备注：跨网段走路由，相同网段不需要配置网关就可以互联互通！实验拓扑如图-1所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/a443fc463ff94bb388e8c267332c0303.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-1

程序类型：编译型（如C、C++）和解释型（如Python、JavaScript）。

CI/CD流程：Jenkins下载代码、打包代码、编译代码、测试代码、上线服务器。

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：创建项目**

1）浏览器访问Jenkins服务器8080端口。

firefox或google-chrome http://192.168.4.30:8080。

登录后，点击《新建任务》，创建jenkins项目，效果如图-2所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/5687697bb5504cbaa97d62696821a1e3.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-2

填写任务名称，选择任务风格，效果如图-3所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/f4fb7e7f00054a91942cf1c14c2a8bcf.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_17,color_FFFFFF,t_70,g_se,x_16)
图-3

设置Git参数，效果如图-4所示。

默认Jenkins会拉取最新版本的代码，这里的设置可以让Jenkins拉取特定的分支或标签（tag）的代码。注意：这里的git参数名称后面会经常用到！

![在这里插入图片描述](https://img-blog.csdnimg.cn/3c41e301a28d4c1cbb2835d83f499646.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-4

继续设置Git参数，定义Git仓库的URL路径，以及需要下载克隆的版本或分支，效果如图-5所示。注意这里的URL是前面课程GitLab创建的代码仓库的链接地址。

![在这里插入图片描述](https://img-blog.csdnimg.cn/8250fe4740f74f94be503e72236cabc6.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-5

2)构建（build）Jenkins项目。

首先需要找到刚刚常见的项目，如图-6所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/275517dc123d478592cff7611cb2333d.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-6

在项目菜单下选择《Build with Parameters》,效果如图-7所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/2ffd7eae850440cc9735dc6a5ecb0e18.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_18,color_FFFFFF,t_70,g_se,x_16)
图-7

此时Jenkins会自动连接GitLab服务器获取仓库数据，我们可以选择一个版本，点击《开始构建》，效果如图-8所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/1f8d0567aae442fcadd692d71d69297e.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_19,color_FFFFFF,t_70,g_se,x_16)
图-8

接下来可以在控制台中查看构建日志，查看构建过程，效果如图-9所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/97b851f563074babbe82f735591326cb.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-9

3）查看Jenkins拉取的代码数据。

在Jenkins服务器操作（192.168.4.30主机操作），默认Jenkins会加拉取的代码数据保存到/var/lib/Jenkins/workspace/目录。

[root@jenkins ~]# ls /var/lib/jenkins/
[root@jenkins ~]# ls /var/lib/jenkins/workspace/
[root@jenkins ~]# ls /var/lib/jenkins/workspace/myweb/
[root@jenkins ~]# rm -rf  /var/lib/jenkins/workspace/myweb/*
4）修改项目配置

如果代码有多个版本或分支，每次都将代码拉取到相同位置，会产生数据覆盖，我们可以修改项目配置，将不同的版本和分支数据保存到不同子目录下。

点击《配置》，重新修改Jenkins项目配置，如图-10所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/b46430267c674cccb38ad41449f21d7e.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_13,color_FFFFFF,t_70,g_se,x_16)
图-10

为Jenkins项目添加附加动作行为，将代码拉取输出到子目录，效果如图-11所示。

注意：这里的子目录调用了前面Git参数的名称（$web）。

![在这里插入图片描述](https://img-blog.csdnimg.cn/735a354c6be04c8bb157b593e0e17d34.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-11

设置邮件通知，在构建失败时可以给特定人员发送邮件，效果如图-12所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/526e7dd4378d4fabaaca4f3e1a215fd1.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-12

5）再次构建项目，并查看数据。

重新构建项目，效果如图-13所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/1c4e530646d344c7872ef0066c0386e8.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-13

在Jenkins服务器查看数据（在192.168.4.30主机操作）。

[root@jenkins ~]# # ls /var/lib/jenkins/workspace/myweb/
# 2. 构建分发服务器
## 2.1 问题
沿用练习一，构建分发服务器，具体要求如下：

- 安装、配置vsftpd
- 修改项目配置
- 重新构建项目

## 2.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：安装、配置FTP共享服务器（仅在192.168.4.30主机操作）**

1）设置防火墙、SELinux。
```shell
[root@jenkins ~]# firewall-cmd --set-default-zone=trusted
[root@jenkins ~]# setenforce 0
[root@jenkins ~]# sed -i '/SELINUX/s/enforcing/permissive/' /etc/selinux/config
```
2) 安装配置vsftpd、启动服务
```shell
[root@jenkins ~]# dnf  -y   install   vsftpd              #安装软件
[root@jenkins ~]# vim /etc/vsftpd/vsftpd.conf            #修改vsftpd配置文件
anonymous_enable=YES                       #12行          #允许匿名访问ftp
[root@jenkins ~]# mkdir -p /var/ftp/deploy/packages
#创建目录，未来jenkins将拉取的代码数据拷贝到该目录，共享给应用服务器
#-p是创建多级子目录
[root@jenkins ~]# chown -R :jenkins /var/ftp/deploy/
#修改权限将目录所属组修改为jenkins
[root@jenkins ~]# chmod -R 775 /var/ftp/deploy/
#修改权限让jenkins组对该目录有读写权限
[root@jenkins ~]# systemctl enable vsftpd --now
#设置服务为开机自启动服务，并立刻启动该服务
```
**步骤二：修改GitLab项目配置**

1）修改项目配置，添加构建步骤。

添加构建步骤，效果如图-14所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/b84d63b576a6403ebdd36ff4bf9c48dd.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-14

2）编写构建脚本，脚本内容如下。
```shell
pkg_dir=/var/ftp/deploy/packages
cp -r myweb-$web $pkg_dir
rm -rf $pkg_dir/myweb-$web/.git
cd $pkg_dir/
tar czf myweb-$web.tar.gz myweb-$web
rm -rf myweb-$web
md5sum myweb-$web.tar.gz | awk '{print $1}' > myweb-$web.tar.gz.md5
cd ..
echo -n $web > ver.txt
```
注释说明：
第一行，定义变量pkg_dir，变量值为ftp共享目录。
第二行，将jenkins拉取到/var/lib/Jenkins/workspace/myweb-$web目录的数据拷贝的ftp共享目录。
第三行，上一步拷贝过来的数据目录下包含一个隐藏.git目录，删除该git仓库目录。
第四行，cd到ftp共享目录下。
第五行，将ftp共享目录下的代码数据打包。
第六行，将ftp共享目录下的代码数据目录删除（上一步已经打包数据）。
第七行，校验打包文件的HASH值（哈希值），并将结果写入到一个文件中。
第八行，返回上一级目录。
第九行，将当前Git版本信息写入ver.txt文件。

3）重新构建项目，查看数据。
重新构建项目，如图-15所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/597c4998c4d3458b801a5177e560c507.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-15

使用浏览器访问FTP服务，查看数据。
firefox 或者google-chrom 访问ftp://192.168.4.30/deploy/packages/
效果如图-16所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/bd236fd2e0124d42bded4a121fcded73.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-16

# 3. 自动化上线
## 3.1 问题
沿用练习二，部署web服务器完成自动化上线，具体要求如下：

- 安装配置httpd
- 编写上线脚本
- 完成整个工作流程

## 3.2 方案
实验拓扑如图-17所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/ad2fa8db4a144e2787cad78552be50e1.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-17

**步骤一：部署Web服务器**

1）设置防火墙和SELinux
```shell
[root@web1 ~]# firewall-cmd --set-default-zone=trusted
[root@web1 ~]# setenforce 0
[root@web1 ~]# sed -i '/SELINUX/s/enforcing/permissive/' /etc/selinux/config
[root@web2 ~]# firewall-cmd --set-default-zone=trusted
[root@web2 ~]# setenforce 0
[root@web2 ~]# sed -i '/SELINUX/s/enforcing/permissive/' /etc/selinux/config
```
2）安装、配置httpd。
```shell
[root@web1 ~]# dnf  -y  install   httpd  wget   tar        #安装httpd、tar和wget
[root@web1 ~]# systemctl  enable  httpd   --now     #设置开启自启，并立刻启动
[root@web2 ~]# dnf  -y  install   httpd  wget  tar          #安装httpd、tar和wget
[root@web2 ~]# systemctl  enable  httpd   --now     #设置开启自启，并立刻启动
```
**步骤二：编写自动化上线脚本**

1）web1和web2自动从jenkins共享服务器下载代码实现持续部署。

这里仅以web1为例编写脚本，可以结合计划任务实现周期性自动上线持续部署。
```shell
[root@web1 ~]# vim web.sh
#!/bin/bash
#定义变量，指定FTP共享路径
ftp_url=ftp://192.168.4.30/deploy
#定义变量，指定网页根路径
web_dir=/var/www/html
#定义函数，行数名为down_file，该函数的作用是从FTP服务器下载代码数据到网站根目录
down_file(){
#获取FTP服务器上面最新构建的代码版本号
#curl是基于命令行的浏览器,-s选项为静默访问，不显示下载过程（可以自己对比不是用-s的差异）
  version=$(curl -s $ftp_url/ver.txt)
#将服务器上面的版本文件下载到web服务器的/var/www/html/目录下
#wget为下载工具（如果没有则需要安装），-q选项为静默模式下载，不显示下载过程
#-O选项可以指定将文件下载到哪里，这里是下载到/var/www/html/ver.txt
  wget -q $ftp_url/ver.txt -O $web_dir/ver.txt
#下载代码数据的打包文件，根据前面获取的版本号，下载对应的版本数据打包文件
  wget -q $ftp_url/packages/myweb-$version.tar.gz -O $web_dir/myweb-$version.tar.gz
#对下载下来的数据打包文件计算HASH值（哈希值），awk过滤仅显示第一列数据结果
  hash=$(md5sum $web_dir/myweb-$version.tar.gz| awk '{print $1}')
#使用curl访问ftp服务器上面的HASH值
  ftp_hash=$(curl -s $ftp_url/packages/myweb-$version.tar.gz.md5)
#对比本地和FTP服务的HASH值是否一致，如果不一致代表数据损坏了
#如果一致就可以解压该数据包，将数据解压到网站根目录下/var/www/html/
  if [ "$hash" == "$ftp_hash" ];then
     tar -xf $web_dir/myweb-$version.tar.gz -C $web_dir
  fi
}
#判断如果本地没有/var/www/html/ver.txt文件，则直接调用前面的函数下载代码数据
if [ ! -f $web_dir/ver.txt ];then
  down_file
fi
#盘如果本地有/var/www/html/ver.txt文件，则判断本地版本文件和FTP版本文件是否一致
#一致就不再下载FTP的数据，如果不一致则调用前面的函数下载新的代码数据包
if [ -f $web_dir/ver.txt ];then
  ftp_ver=$(curl -s $ftp_url/ver.txt)
  local_ver=$(cat $web_dir/ver.txt)
  if [ "$ftp_ver" != "$local_ver" ];then
      down_file
  fi
fi
[root@web1 ~]# chmod +x  web.sh                #添加可执行权限
[root@web1 ~]# ./web.sh                         #执行脚本
```
**步骤三：完成整理工作流程。**

1）工作流程。

开发人员编写代码，将代码上传到GitLab服务器，Jenkins从GitLab服务器上面拉取最新代码数据到本地，根据Jenkins项目配置，将代码拉取到本地后，可以进行编译、测试、打包等工作，最后将数据包写入到共享服务器，应用服务器最后从共享服务器拉取数据实现上线功能。

2）开发人员修改代码、上传代码（主机192.168.4.10操作）
```shell
[root@develop ~]# cd myproject                   #进入仓库目录
[root@develop myproject]# vim  index.html                #修改首页文件第4行内容
修改前：
<title>Home</title>
修改后：
<title>Tarena</title>
[root@develop myproject]# git add .                       #添加修改记录
[root@develop myproject]# git commit -m "modify index"      #提交修改  
[root@develop myproject]# git tag  v2                         #添加代表版本标签
[root@develop myproject]# git push origin master             #推送数据到服务器
[root@develop myproject]# git push origin v2                 #推送数据到服务器
```
3）Jenkins重新构建项目，效果如图-18所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/4f6b7d3c48454529a518f7b1c3d02597.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-18

4）在web服务器执行上线脚本完成持续部署。

在192.168.4.100和192.168.4.200操作，这里仅以web1为例。
```shell
[root@web1 ~]# ./web.sh
```

# 4. 部署Ansible
## 4.1 问题
本案例要求先快速搭建好一个Ansible平台，并测试环境，要求如下：

- 创建实验主机（控制端和被控制端）
- 配置SSH实验环境
- 安装Ansible自动化软件
- 修改Ansible配置

## 4.2 方案
准备如表-1所示的实验环境，操作系统为RHEL8，配置主机名称、IP地址、YUM源。

表-1 主机列表
![在这里插入图片描述](https://img-blog.csdnimg.cn/30932e1decb24348a8be0506661c7921.png)
ansible原理：
控制端主机自带很多模块（模块就是脚本）；
ansible通过ssh远程被管理主机，将控制端的模块（脚本）或命令传输到被管理主机；
在被管理端主机执行模块（脚本）或命令，执行不同的模块或命令可以实现不同的功能；
最后ansible退出ssh远程。
绝大多数模块（脚本）都需要参数才能执行成功！！！类似于shell脚本的位置变量！

拓扑结构如图-19所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/b0bf958227e849ee9b9b3a6ee8e3e1d6.png)
图-19

提醒：全天的实验不需要死记硬背每个模块的每个参数，所有参数都可以查看帮助！

## 4.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：准备基础环境**
控制节点要求：
- 域名解析（为了方便后期操作，可以不做）
- 配置SSH密钥（ansible是基于ssh实现远程控制）
- 安装Ansible软件

1）Control控制节点
修改/etc/hosts，在文件中手动添加如下内容，修改该文件的目的是做域名解析。
```shell
[root@control ~]# vim  /etc/hosts        #修改文件，手动添加如下内容（不要删除文件原来的内容）
192.168.4.253    control    
192.168.4.11        node1    
192.168.4.12        node2    
192.168.4.13        node3    
192.168.4.14        node4    
192.168.4.15        node5
```
如何验证？
```shell
[root@control ~]# ping  node1               #可以使用ping命令依次ping所有域名    
```
配置SSH密钥实现免密码登录（非常重要）

Ansible是基于SSH远程的原理实现远程控制，如果控制端主机无法免密登录被管理端主机，后续的所有试验都会失败！！
```shell
[root@control ~]#  ssh-keygen         #生成ssh密钥
[root@control ~]#  for i in node1 node2 node3 node4 node5
do
ssh-copy-id   $i 
done
#拷贝密钥到远程主机
#提示：拷贝密钥到远程主机时需要输入对方电脑的账户密码才可以！！
#拷贝密钥到node1就需要输入node1对应账户的密码，拷贝密钥到node2就需要输入node2对应的密码
```
如何验证？

警告：如果有任何一台主机远程还需要密码，就不要往下继续操作，后面实验都会失败！！！
```shell
[root@control ~]# ssh  node1            #使用ssh命令依次远程所有主机都可以免密码登录
[root@node1 ~]# exit                     #退出ssh远程登录
```
2)部署Ansible软件（仅Control主机操作，软件包在ansible_soft目录）。
```shell
安装软件方案1(提前直接将软件包拷贝到control安装):
[root@control ~]# tar -xf   ansible_soft.tar.gz
[root@control ~]# cd ansible_soft
[root@control ansible_soft]# dnf  -y  install   *
```
```shell
安装软件方案2(配置YUM安装ansible软件):
1)真机做YUM源服务器
[root@localhost ~]# tar -xf /linux-soft/2/ansible_soft.tar.gz -C /var/ftp/
[root@localhost ~]# dnf -y install createrepo
[root@localhost ~]# createrepo /var/ftp/ansible_soft/
2)control虚拟机配置YUM，安装软件
[root@control ~]# vim  /etc/yum.repos.d/ansible.repo
[ansible]
name=ansible
baseurl=ftp://192.168.4.254/ansible_soft/
gpgcheck=0
[root@control ~]# dnf  -y  install   ansible
```
被控制节点要求：

- Ansible默认通过SSH协议管理机器
- 被管理主机要开启SSH服务，并允许控制主机登录
- 被管理主机需要安装有Python

**步骤二：修改配置文件**

主配置文件说明：

主配置文件ansible.cfg（主配置文件的内容可以参考/etc/ansible/ansible.cfg）

ansible配置文件查找顺序

首先检测ANSIBLE_CONFIG变量定义的配置文件（默认没有这个变量）

其次检查当前目录下的./ansible.cfg文件

再次检查当前用户家目录下~/ansible.cfg文件

最后检查/etc/ansible/ansible.cfg文件

1) 修改主配置文件。
```shell
[root@control ~]# mkdir  ~/ansible
[root@control ~]# vim  ~/ansible/ansible.cfg
[defaults]
inventory = ~/ansible/inventory            
#主机清单配置文件（inventory可以是任意文件名），英语词汇：inventory（清单、财产清单）
#forks = 5                                    #ssh并发数量
#host_key_checking = False                  #是否校验密钥（第一次ssh时是否提示yes/no）
`
2) 修改主机清单文件（清单文件名必须与主配置文件inventory定义的一致）。
```shell
[root@control ~]# vim  ~/ansible/inventory
[test]                    #定义主机组（组名称任意）
node1                    #定义组中的具体主机，组中包括一台主机node1
[proxy]                    #定义主机组（组名称任意），英语词汇：proxy（代理人，委托人）
node2                      #proxy组中包括一台主机node2
[webserver]
node[3:4]                 #这里的node[3:4]等同于node3和node4
[database]
node5
[cluster:children]        #嵌套组（children为关键字），不需要也可以不创建嵌套组
webserver                  #嵌套组可以在组中包含其他组
database
```
附加思维导图，如图-20所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/a30f0af8b68e42a0a723c2d5a2706af3.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-20


# Exercise
## 1 Jenkins默认会把GitLab仓库代码下载到哪个目录?

/var/lib/jenkins/workspace/

## 2 如何一条命令将vsftpd设置开启自启并立刻启动？
```shell
# systemctl enable vsftpd  --now
```
## 3 如何校验数据的哈希值（如md5值）？
```shell
# md5sum  <文件名>
```
## 4 Ansible基于什么实现的远程连接远程管理？

ssh

## 5 在ansible主配置文件中，定义主机清单的参数是什么？

inventory


> 如有侵权，请联系作者删除
