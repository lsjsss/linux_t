@[TOC]( Version control & Git basics & Git advanced | Cloud computing )

---
# 1. Git基本操作
## 1.1 问题
本案例要求先快速搭建好一台Git服务器，并测试该版本控制软件，要求如下：

- 安装Git软件
- 创建版本库
- 客户端克隆版本仓库到本地
- 本地工作目录修改数据
- 提交本地修改到服务器

## 1.2 方案
今日实验环境准备：

1）准备两台RHEL8虚拟机，主机名分别为develop和git。
2）develop主机的IP地址为192.168.4.10，不需要配置网关和DNS。
3）git主机的IP地址为192.168.4.20，不需要配置网关和DNS。
4）给develop和git两台主机配置可用的YUM源。

备注：跨网段走路由，相同网段不需要配置网关就可以互联互通！

实验拓扑如图-1所示，Git工作流如图-2所示。
![在这里插入图片描述](https://img-blog.csdnimg.cn/c0a3ad41599a4b7f8a68865fe0833f3b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_15,color_FFFFFF,t_70,g_se,x_16)
图-1

![在这里插入图片描述](https://img-blog.csdnimg.cn/319a4ec4673645db97b46f16bd3861a7.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_16,color_FFFFFF,t_70,g_se,x_16)
图-2

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：部署Git服务器（192.168.4.20作为git服务器）**

1）YUM安装Git软件。
```shell
[root@git ~]# yum -y install git
```
2)初始化一个空仓库。
```shell
[root@git ~]# mkdir -p /var/lib/git
[root@git ~]# git init /var/lib/git/project --bare    #创建空仓库
[root@git ~]# ls /var/lib/git/project    #查看仓库中是否有内容
config  description  HEAD  hooks  info  objects  refs 
```
英文单词：bare[ber]裸露的；project[prəˈdʒekt]项目；init初始化。

3）设置防火墙信任所有，设置SELinux放行所有。
```shell
[root@git ~]# firewall-cmd --set-default-zone=trusted
[root@git ~]# setenforce 0
[root@git ~]# sed -i '/SELINUX/s/enforcing/permissive/' /etc/selinux/config
```
**步骤二：客户端测试(192.168.4.10作为开发人员的客户端主机)**

使用git常用指令列表如表-1所示。

表－1 git常用指令列表
![在这里插入图片描述](https://img-blog.csdnimg.cn/e5af5f2215344bb3b372e58ad8f68680.png)


1) 设置防火墙信任所有，设置SELinux放行所有。
```shell
[root@develop ~]# firewall-cmd --set-default-zone=trusted
[root@develop ~]# setenforce 0
[root@develop ~]# sed -i '/SELINUX/s/enforcing/permissive/' /etc/selinux/config
```
2）使用clone指令克隆服务器仓库到本地。

提示：默认会将仓库下载到本地的当前目录（当前目录在root家目录）！
```shell
[root@develop ~]# yum -y install git
[root@develop ~]# git clone root@192.168.4.20:/var/lib/git/project 
Are you sure you want to continue connecting (yes/no)? <第一次远程需要输入yes>
root@192.168.4.20's password:<克隆git主机的资料，需要输入git主机的密码>
[root@develop ~]# ls /root           #查看是否将仓库下载到了本地，名称为project
[root@develop ~]# cd project
[root@develop project]# ls 
[root@develop project]# git remote -v   #查看服务器信息(输出信息如下)
origin  root@192.168.4.20:/var/lib/git/project (fetch)
origin  root@192.168.4.20:/var/lib/git/project (push)
```
3) 修改git配置。
```shell
[root@develop project]# git config --global user.email "you@example.com"
[root@develop project]# git config --global user.name "Your Name"
[root@develop project]# cat ~/.gitconfig 
[user]
    email = you@example.com
    name = Your Name
```
4） 本地工作区对数据进行增删改查(必须要先进入仓库再操作数据)。
```shell
[root@develop project]# echo "init date" > init.txt
[root@develop project]# mkdir demo
[root@develop project]# cp /etc/hosts demo
```
5） 查看本地仓库中数据的状态。
```shell
[root@develop project]# git status
```
6） 将工作区的修改提交到暂存区。
```shell
[root@develop project]# git add .
```
7) 将暂存区修改提交到本地仓库。
```shell
[root@develop project]# git commit  -m  "注释，这里可以为任意字符"
[root@develop project]# git status
英语单词：status[ˈsteɪtəs]状态；add[æd]加、增加；commit[kəˈmɪt]提交、承诺。
```
8） 将本地仓库中的数据推送到远程服务器(develop将数据推送到git)。
```shell
[root@develop project]# git config --global push.default simple    #根据git版本不同，这个步骤可能需要或不需要
[root@develop project]# git push                     #将本地数据推送给git服务器
root@192.168.4.20's password:  输入git服务器root密码
[root@develop project]# git status
[root@develop project]# git remote -v                #查看远程服务器的信息
[root@develop project]# git push origin              #将数据推送至origin服务器
9) 将服务器上的数据更新到本地（git服务器的数据更新到develop）。
```
备注：可能其他人也在修改数据并提交git服务器，就会导致自己的本地数据为旧数据，使用pull指令就可以将服务器上新的数据更新到本地。
```shell
[root@develop project]# git pull
```
10) 查看版本日志。
```shell
[root@develop project]# git log
[root@develop project]# git log --pretty=oneline
[root@develop project]# git log --oneline
[root@develop project]# git reflog
```
英语单词：push[pʊʃ]推；pull[pʊl]拉；pretty[ˈprɪti]精致、漂亮。

备注：客户端也可以使用图形程序访问服务器。

Windows需要安装git和tortoiseGit。如图-3、图-4所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/77c0bb4617ef4f35a3c2a1c4803a246d.png)
图-3

![在这里插入图片描述](https://img-blog.csdnimg.cn/0bde270807494117a2a903ca5666deea.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_14,color_FFFFFF,t_70,g_se,x_16)
图-4

# 2. HEAD指针操作
## 2.1 问题
沿用练习一，学习操作HEAD指针，具体要求如下：

- 查看Git版本信息
- 移动指针
- 通过移动HEAD指针恢复数据

## 2.2 方案
HEAD指针是一个可以在任何分支和版本移动的指针，通过移动指针我们可以将数据还原至任何版本。每做一次提交操作都会导致git更新一个版本，HEAD指针也跟着自动移动。

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：HEAD指针基本操作**

1）准备工作（多对数据仓库进行修改、提交操作，以产生多个版本）。

注意：这里是在project仓库目录下做的所有操作！！
```shell
[root@develop project]# echo "new file" > new.txt
[root@develop project]# git add .
[root@develop project]# git commit -m "add new.txt"
[root@develop project]# echo "first" >> new.txt
[root@develop project]# git add .
[root@develop project]# git commit -m "new.txt:first line"
[root@develop project]# echo "second" >> new.txt
[root@develop project]# git add .
[root@develop project]# git commit -m "new.txt:second"
[root@develop project]# echo "third" >> new.txt
[root@develop project]# git add .
[root@develop project]# git commit -m "new.txt:third"
[root@develop project]# git push
[root@develop project]# echo "123" > num.txt
[root@develop project]# git add .
[root@develop project]# git commit -m "num.txt:123"
[root@develop project]# echo "456" > num.txt
[root@develop project]# git add .
[root@develop project]# git commit -m "num.txt:456"
[root@develop project]# echo "789" > num.txt
[root@develop project]# git add .
[root@develop project]# git commit -m "num.txt:789"
[root@develop project]# git push
```
2) 查看Git版本信息。
```shell
[root@develop project]# git reflog
[root@develop project]# git log --oneline
04ddc0f num.txt:789
7bba57b num.txt:456
301c090 num.txt:123
b427164 new.txt:third
0584949 new.txt:second
ece2dfd new.txt:first line
e1112ac add new.txt
1a0d908 初始化
```
3）移动HEAD指针，将数据还原到任意版本。

提示：当前HEAD指针为HEAD@{0}，HEAD@{1}是上一次指针的位置。
```shell
[root@develop project]# git reset --hard 301c0         #不能照抄这里的301c0
[root@develop project]# git reflog
301c090 HEAD@{0}: reset: moving to 301c0
04ddc0f HEAD@{1}: commit: num.txt:789
7bba57b HEAD@{2}: commit: num.txt:456
301c090 HEAD@{3}: commit: num.txt:123
b427164 HEAD@{5}: commit: new.txt:third
0584949 HEAD@{6}: commit: new.txt:second
ece2dfd HEAD@{7}: commit: new.txt:first line
e1112ac HEAD@{8}: commit: add new.txt
1a0d908 HEAD@{9}: commit (initial): 初始化
[root@develop project]# cat num.txt                  #查看文件是否为123
123
[root@develop project]# git reset --hard 7bba57b     #不能照抄这里的7bba57b
[root@develop project]# cat num.txt                 #查看文件是否为123，456
123
456
[root@develop project]# git reflog                #查看指针移动历史
7bba57b HEAD@{0}: reset: moving to 7bba57b
301c090 HEAD@{1}: reset: moving to 301c0
… …
[root@develop project]# git reset --hard 04ddc0f    #回到最后一次修改的版本
```

# 3. Git分支操作
## 3.1 问题
沿用练习二，学习操作Git分支，具体要求如下：

- 查看分支
- 创建分支
- 切换分支
- 合并分支
解决分支的冲突
3.2 方案
Git支持按功能模块、时间、版本等标准创建分支，分支可以让开发分多条主线同时进行，每条主线互不影响，分支效果如图-5所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/b0eb2355a72a4dc6b5fc6e7d2b6696ef.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_16,color_FFFFFF,t_70,g_se,x_16)
图-5

常见的分支规范如下：

MASTER分支（MASTER是主分支，是代码的核心）。
DEVELOP分支（DEVELOP最新开发成果的分支）。
RELEASE分支（为发布新产品设置的分支）。
HOTFIX分支（为了修复软件BUG缺陷的分支）。
FEATURE分支（为开发新功能设置的分支）。

**步骤一：查看并创建分支**

1）查看当前分支。
```shell
[root@develop project]# git status
# On branch master
nothing to commit, working directory clean
[root@develop project]# git branch -v
* master 0dc2b76 delete init.txt
```
2）创建分支。
```shell
[root@develop project]# git branch hotfix  #创建hotfix分支
[root@develop project]# git branch feature   #创建feature分支
[root@develop project]# git branch -v    #查看分支信息
  feature 0dc2b76 delete init.txt
  hotfix  0dc2b76 delete init.txt
* master  0dc2b76 delete init.txt
```
备注：如果需要删除分支，命令：git branch -d 分支名称。

**步骤二：切换与合并分支**

1）切换分支。
```shell
[root@develop project]# git checkout hotfix
[root@develop project]# git branch -v
  feature 0dc2b76 delete init.txt
* hotfix  0dc2b76 delete init.txt
master  0dc2b76 delete init.txt
```
2）在新的分支上可以继续进行数据操作（增、删、改、查）。
```shell
[root@develop project]# echo "fix a bug" >> new.txt
[root@develop project]# git add .
[root@develop project]# git commit -m "fix a bug"
```
3）将hotfix修改的数据合并到master分支。

注意，合并前必须要先切换到master分支，然后再执行merge命令。
```shell
[root@develop project]# git checkout master
[root@develop project]# cat new.txt    #默认master分支中没有hotfix分支中的数据
[root@develop project]# git merge hotfix
Updating 0dc2b76..5b4a755
Fast-forward
 new.txt | 1 ++
 1 file changed, 1 insertions(+)
```
英语单词：branch[bræntʃ]分支、树枝；merge[mɜːrdʒ]融合、合并。

**步骤二：解决版本分支的冲突问题**

1）在不同分支中修改相同文件的相同行数据，模拟数据冲突。
```shell
[root@develop project]# git checkout hotfix
[root@develop project]# echo "AAA" > a.txt
[root@develop project]# git add .
[root@develop project]# git commit -m "add a.txt by hotfix"
[root@develop project]# git checkout master
[root@develop project]# echo "BBB" > a.txt
[root@develop project]# git add .
[root@develop project]# git commit -m "add a.txt by master"
[root@develop project]# git merge hotfix
自动合并 a.txt
冲突（添加/添加）：合并冲突于 a.txt（Merge conflict in a.txt）
自动合并失败（merge failed），修正冲突（fix conflicts）然后提交修正的结果。
```
英语单词：conflict[kənˈflɪkt]冲突、矛盾；failed[feɪld]失败的；fix[fɪks]修正。

2）查看有冲突的文件内容，修改文件为最终版本的数据，解决冲突。
```shell
[root@develop project]# cat a.txt                #该文件中包含有冲突的内容
<<<<<<< HEAD
BBB
=======
AAA
>>>>>>> hotfix
[root@develop project]# vim a.txt              #修改该文件，为最终需要的数据，解决冲突
BBB
[root@develop project]# git add .
[root@develop project]# git commit -m "resolved"
```
总结：分支指针与HEAD指针的关系。

- 创建分支的本质是在当前提交上创建一个可以移动的指针
- 如何判断当前分支呢？答案是根据HEAD这个特殊指针

分支操作流程如图-6，图-7，图-8，图-9，图-10所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/4c0bb384c19946ae89375f09507918b8.png)
图-6 HEAD指针指向master分支

![在这里插入图片描述](https://img-blog.csdnimg.cn/f03c0ff9d97a4f7ab9ace0c3944b2b93.png)
图-7 切换分支，HEAD指针指向testing分支

![在这里插入图片描述](https://img-blog.csdnimg.cn/f8849d5400fd4182b5eb2f374a13dc90.png)
图-8 在testing分支中修改并提交代码

![在这里插入图片描述](https://img-blog.csdnimg.cn/3aa041b4f1c0428dadb115ebb42f9c32.png)
图-9 将分支切换回master分支

![在这里插入图片描述](https://img-blog.csdnimg.cn/fda6db2a06414781a51966209f6dfd2e.png)
图-10 在master分支中修改数据，更新版本

# 4. Git服务器
## 4.1 问题
沿用练习三，学习Git不同的服务器形式，具体要求如下：

- 创建SSH协议服务器

## 4.2 方案
Git支持很多服务器协议形式，不同协议的Git服务器，客户端就可以使用不同的形式访问服务器。创建的服务器协议有SSH协议、Git协议、HTTP协议。

**步骤一：SSH协议服务器（支持读写操作）**

1）创建基于密码验证的SSH协议服务器（git主机操作）。
```shell
[root@git ~]# git init --bare /var/lib/git/web
```
2)客户端访问的方式（develop主机操作）。
```shell
[root@develop ~]# cd ~                 #回到家目录(将仓库下载到本地家目录)
[root@develop ~]# git clone root@192.168.4.20:/var/lib/git/web
#默认需要密码才能下载仓库中的资料
[root@develop ~]# rm -rf web               #将刚刚下载的仓库删除
```
3）客户端生成SSH密钥，实现免密码登陆git服务器（develop主机操作）。
```shell
[root@develop ~]# ssh-keygen -f /root/.ssh/id_rsa -N ''
#-f后面指定将创建的密钥文件存放到哪里
#-N后面是空，不对生成的密钥文件加密
[root@develop ~]# ssh-copy-id  192.168.4.20
[root@develop ~]# git clone root@192.168.4.20:/var/lib/git/web  
#生成完密钥并传递密钥后，再次克隆下载服务器的资料不需要输入密码
[root@develop ~]# cd web
[root@develop web]# git push
#将本地资料推送到git服务器也不需要密码
[root@develop web]# cd ..
[root@develop ~]# rm  -rf   web                     #删除本地仓库
```
**步骤二：客户端部署新仓库**

客户端没有任何仓库资料的情况下，从服务器克隆部署新仓库。
```shell
[root@develop ~]# git clone root@192.168.4.20:/var/lib/git/web  
[root@develop ~]# cd web
[root@develop web]# touch README.md
[root@develop web]# git add .
[root@develop web]# git commit  -m  "readme"
[root@develop web]# git remote  -v                         #查看远程服务器信息
[root@develop web]# git push                               #默认推送
[root@develop web]# git push -u origin  master            #指定推送的服务器和分支
[root@develop ~]# cd ..
[root@develop ~]# rm -rf  web
```
**步骤三：在客户端现有的文件夹下克隆仓库**
```shell
[root@develop ~]# mkdir mygit
[root@develop ~]# cd mygit
[root@develop mygit]# git init                  #将当前目录创建为git空仓库
[root@develop mygit]# git remote -v            #此时该仓库没有对应的远程服务器
[root@develop mygit]# git remote add origin 192.168.4.20:/var/lib/git/web
#添加远程服务器，给远程服务器的web仓库取一个本地名称为origin
[root@develop mygit]# git remote -v           #查看远程服务器信息
[root@develop mygit]# ls                       #本地还是空目录，没有任何资料
[root@develop mygit]# git pull  origin master   
#从origin服务器的master分支拉取数据
[root@develop mygit]# ls
[root@develop mygit]# echo new > new.txt
[root@develop mygit]# git add .
[root@develop mygit]# git commit -m "newfile"
[root@develop mygit]# git push -u origin master
```
**步骤四：客户端在现有仓库基础上添加新Git仓库**
```shell
[root@develop mygit]# git remote rename origin new-name
#将老服务器信息重命名
[root@develop mygit]# git remote add origin 192.168.4.20:/var/lib/git/web
#添加新服务器信息
[root@develop mygit]# git push -u origin --all
#推送origin服务器的所有分支到服务器
英语单词：remote[rɪˈmoʊt]远程、遥远的；origin[ˈɔːrɪdʒɪn]起源、源头。
```
**步骤五：课外扩展知识：注册使用Github**

1. 登陆网站https://github.com，点击Sign up（注册），如图-11所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/3b3256e7e6c945d7a084ea2abb3b59d5.png)
图-11

2. 填写注册信息（用户名，邮箱，密码），如图-12所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/09836df636a546b892b292ecee665df1.png)
图-12

3. 初始化操作，如图-13和图-14所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/3ac4d375504c4774bb9c9cc580cc8c9c.png)
图-13

![在这里插入图片描述](https://img-blog.csdnimg.cn/fc3007034b6442e5bdac1e7783f7fd40.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_12,color_FFFFFF,t_70,g_se,x_16)
图-14

注意，初始化完成后，到邮箱中去激活Github账户。

4. 创建仓库、使用仓库

点击Start a project（如图-15所示），

![在这里插入图片描述](https://img-blog.csdnimg.cn/01718fccc1ef4d1f9c6e1ae246ac1a38.png)
图-15

填写项目名称（项目名称任意），如图-16所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/9215993104f04ac38c26c60dd6a08c57.png)
图-16

往仓库中上传文件或新建文件，如图-17所示

![在这里插入图片描述](https://img-blog.csdnimg.cn/813613816cf24f488b6c7755c3502d7d.png)
图-17

下载仓库中的代码，如图-18所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/5979b9abef9145c7b29a6125f93eddd3.png)
图-18

5. 命令行操作（需要联网的主机，如真实机）
```shell
[root@pc001 ~]# yum -y install git
[root@pc001 ~]# git clone https://github.com/账户名称/仓库名称
#clone指令用于将服务器仓库中的资料打包下载到本地
[root@pc001 ~]# cd 仓库名称
[root@pc001 ~]# 任意修改文件，或新建文件
[root@pc001 ~]# git add .
#add添加新文件
[root@pc001 ~]# git commit -m "test"
[root@pc001 ~]# git push
#commit和push实现提交代码的功能
[root@pc001 ~]# git pull
#pull可以从githuab服务器拉取数据到本地
```

**步骤三：Gitlab服务器**

GitLab是一个利用 Ruby on Rails 开发的开源应用程序，实现一个自托管的Git项目仓库，可通过Web界面进行访问公开的或者私人项目。

附加思维导图，如图-19所示。

![在这里插入图片描述](https://img-blog.csdnimg.cn/96d929e67b2e49648906f52ea553feb1.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-19


# Exercise
## 1 什么是git
git是一个自由，开源的分布式版本控制系统。在git管理下，文件和目录可以超越时空。git将文件存放在版本库里。它可以记录每一次文件和目录的修改情况，这样就可以籍此将数据恢复到以前的版本，并可以查看数据的更改细节。

## 2 客户端与git服务器通信的方式有哪些
- 本地访问 git clone file:///var/git/project
- ssh服务器方式访问 git clone root@服务器IP:/var/git/project
- git服务器方式访问 git clone git://服务器IP/var/git/project
- web服务的方式 firefox http://服务器IP/git

## 3 Git移动HEAD指针的命令是什么
- git reset --hard 版本编号

## 4 Git如何创建并切换分支
- 创建分支：git branch 分支名称
- 切换分支：git checkout 分支名称

> 如有侵权，请联系作者删除
