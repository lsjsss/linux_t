@[TOC]( Network & Shell & Operation & Automation Topic | Cloud computing )

---
# Single Choice
1、在Shell脚本中，若要屏蔽终端的输出默认显示功能，可以执行_____命令。
A.set  tty   -echo 
B.stty -echo 
C.-echo 
D.stty echo 
【答案】**B**
【解析】**read -p默认读取的密码为明文，通过stty -echo可以防止密码输出**

---
2、使用test进行条件判断，测试两个数字的关系时，小于用_____表示。
A.-lt 
B.-gt 
C.-eq 
D.-ge 
【答案】**A**
【解析】**-lt是小于，-gt是大于，-ge是大于等于，-eq是等于**

---
3、如果abc=3 ，不能使循环任务执行3次的是_____。
A.for i in {1..\$abc} 
B.for i in seq \$ abc 
C.for i in echo \$ abc 
D.for i in \`seq \$abc\` 
【答案】**A**
【解析】**{1..\$abc}在for循环的值中只会被识别为1个整体，循环任务也只是1次**

---
4、关于变量，以下描述不正确的是_____。
A.变量名区分字母大小写 
B.变量名称可以使用字母、数字、下划线 
C.使用export可设置全局变量 
D.变量名不区分字母大小写 
【答案】**D**
【解析】**变量名可以是字母、数字、下划线（不能数字开始），变量名区 分大小写**

---
5、如果输入who命令后查看的结果为两行，执行[ \$(who | wc -l) -ge 3 ] && echo "ok" || echo "no" 会显示_____。
A.无显示 
B.3 
C.ok 
D.no 
【答案】**D**
【解析】**-ge在条件测试中表示大于等于，判断失败后不执行&&后的任务，结果为||前任务失败，会执行||后任务**

---
6、以下_____可以重新加载nginx配置文件。
A.reload 
B.restart 
C.stop 
D.start 
【答案】**A**
【解析】**nginx -s reload**

---
7、在正则表达式中，符号 *  [ ]  ? 分别代表的含义是_____。
A.匹配前面字符出现任意次，集合，匹配前面字符出现0~1次 
B.匹配前面字符出现任意次，组合为整体，匹配前面字符出现0~1次 
C.匹配任意，组合为整体，匹配前面字符出现1~多次 
D.匹配任意，集合，匹配前面字符出现0~1次 
【答案】**A**

---
8、_____关键词配置可以实现nginx地址重写。
A.reset 
B.remake 
C.rewrite 
D.release 
【答案】**C**

---
9、Shell脚本中，使用_____语句可以直接退出脚本。
A.q 
B.exit 
C.kill 
D.quit 
【答案】**B**
【解析】**break中断整个循环，continue中断当前一次循环，exit中断整个脚本**

---
10、在命令行中执行如下命令： 
#sed '2d' a.txt 
关于最后的执行结果，以下描述正确的是_____。
A.从文件的第2行开始删除至最后一行 
B.共删除1行 
C.删除文件中的第1~2行 
D.命令语法格式错误 
【答案】**B**
【解析】**2d代表删除第2行，也就是共删除1行**

---
11、启动nginx程序时，其命令选项_____可用于查看版本信息。
A.-c 
B.-t 
C.-V 
D.-s 
【答案】**C**
【解析】**-V选项用于查看版本信息以及编译选项的信息**

---
12、memcached服务的作用是_____。
A.可以解析域名 
B.可以搭建网站 
C.可以存储数据 
D.可以解析动态网站 
【答案】**C**
【解析】**memcached是个数据库服务，可以用内存存储数据**

---
13、awk命令使用_____变量存储行号。
A.NF 
B.NR 
C.NU 
D.NP 
【答案】**B**
【解析】**awk中NR代表当前行，NF代表当前行有几列**

---
14、Linux命令行中，对多个命令进行逻辑分隔时，仅前一个命令不成功才执行下一个命令，应该使用_____分隔符。
A.& 
B.%% 
C.&& 
D.|| 
【答案】**D**
【解析】**&&仅前一个命令成功才执行后一个命令 ||仅前一个命令失败才执行后一个命令**

---
15、在命令行中执行如下命令 
#sed  -i  '1~2d' a.txt  
关于最后的执行结果，以下描述正确的是_____。
A.删除文件中的前2行 
B.删除文件中的第2行 
C.删除文件中的奇数行 
D.删除文件中的第1行和第2行 
【答案】**C**
【解析】**sed使用行定位操作对象时，1~2表示1，3，5，7… 2是步长**

---
16、Shell脚本中可以进行小数运算的命令工具是_____。
A.gc 
B.bc 
C.ac 
D.tc 
【答案】**B**
【解析】**bc命令支持小数运算**

---
17、在awk指令中出现的BEGIN{ }任务会执行_____次。
A.3次 
B.1次 
C.2次 
D.4次 
【答案】**B**
【解析】**BEGIN{ }任务只会执行一次**

---
18、使用_____工具可以对Web服务器进行压力测试。
A.ab 
B.web 
C.test 
D.press 
【答案】**A**
【解析】**对web进行压力测试的软件很多，ab是其中之一**

---
19、对指awk 'BEGIN{x=100}{x++}END{print x}'令描述错误的是_____。
A.BEGIN中的任务只会执行1次 
B.如果BEGIN中的任务在执行完后无任何变化则不会执行END任务 
C.END中的任务只会执行1次 
D.中间的{ }任务执行次数与被处理文档的行数有关 
【答案】**B**
【解析】**BEGIN中的任务执行之后无论是否有变化不会影响END任务的执行**

---
20、使用stty –echo命令后，以下错误的是_____。
A.敲击任何按键将无任何输出 
B.仅输入命令时无输出，但执行命令后可以看到结果 
C.stty echo可以恢复正常 
D.不影响其他命令的执行结果 
【答案】A
【解析】输入命令后按回车键可以看到输出

---
21、有可能查看到单词good的搜索方式是_____。
A.grep –E "goo{0,2}d" 
B.grep "goo+d" 
C.grep "goooo*d" 
D.grep "go{2}d" 
【答案】**A**
【解析】**+与{}均属于扩展正则，grep需要使用-E支持**

---
22、使用sed修改test.txt可以实现永久效果的是_____。
A.sed -n 's/a/b/' test.txt 
B.sed -r 's/a/b/' test.txt 
C.sed -i 's/a/b/' test.txt 
D.sed -F 's/a/b/' test.txt 
【答案】**C**
【解析】**在sed中-i选项可以修改并保存入文件**

---
23、Shell脚本中使用_____命令可以对数据进行排序。
A.sort  
B.sed 
C.uniq 
D.more 
【答案】**A**
【解析】**Linux中sort命令可以将数据排序**

---
24、若执行如下命令 
#head  -5  /etc/passwd  |  awk -F: 'END{print NR,NF}'   
则最后输出的结果是_____。
A.1   7 
B.4   5 
C.3   6 
D.5   7 
【答案】**D**
【解析】**awk的END{}指令仅在读取完文件后才执行，所以NR当前行的 行号为5，NF为列共7列**

---
25、下面关于ansible描述错误的是_____。
A.ansible支持自定义模块 
B.ansible是基于ssh架构 
C.ansible不支持自定义模块 
D.ansible支持对windows进行自动化管理 
【答案】**C**
【解析】**ansible支持对windows的自动化管理；支持自定义模块；默认是基于ssh协议进行远程管理**

---
26、执行ls -l /opt/test.txt 命令后显示的结果是
---------- 1 root root 33139 12-11 10:43 /opt/test.txt
则以下_____命令会显示ok。
A.[root@svr5 ~]$ [ -r "/opt/test.txt" ] && echo "ok" 
B.[root@svr5 ~]# [ -x "/opt/test.txt" ] && echo "ok" 
C.[root@svr5 ~]# [ -r "/opt/test.txt" ] || echo "ok" 
D.[root@svr5 ~]# [ -r "/opt/test.txt" ] && echo "ok" 
【答案】**D**
【解析】**读写权限对root无限制**

---
27、关于命令 hostname=www.tarena.com; echo \${hostname\%\%.*} 的执行结果，以下描述正确的是_____。
A.tarena.com 
B.com 
C.www.tarena 
D.www 
【答案】**D**
【解析】**echo ${变量#}可以掐头；echo ${变量%}可以去尾**

---
28、sudo的配置文件是_____。
A./etc/visudoer 
B./etc/visudoers 
C./etc/sudoer 
D./etc/sudoers 
【答案】**D**
【解析】**主配置文件是/etc/sudoers**

---
29、使用export命令发布全局变量，错误的是_____。
A.执行export a=100后，在当前命令行输入bash指令后查看$a则显示100 
B.执行export a=100后，使用另一台计算机远程该服务器查看$a则无任何内容 
C.export –n a 可以取消变量a的全局效果，恢复为局部效果 
D.export –n a 可以取消变量a的定义 
【答案】**D**
【解析】**export –n 不可以取消变量的定义，只能恢复为局部效果**

---
30、若执行 head -5 /etc/passwd | awk '{i++}END{print i}'  操作，
输出的结果是_____。
A.1 
B.0 
C.没有值 
D.5 
【答案】**D**
【解析】**awk读取一行执行一次i++，读取5行后i的值为5**

---
31、Nginx配置文件中_____指令可以定义客户端浏览器缓存数据的时间。
A.ttl 
B.cached 
C.expires 
D.time 
【答案】**C**
【解析】**expires 30d可以设置缓存30天**

---
32、Linux操作系统对能够打开的最大文件数量进行了限制，默认为1024，通过_____命令可以调整这个限制。
A.ulimit 
B.limit 
C.glimit 
D.climit 
【答案】**A**
【解析】**ulimit -n可以修改最大文件数量**

---
33、Shell脚本中使用，_____命令可以取消一个已经定义的变量。
A.unset 变量名 
B.clear 变量名 
C.set 变量名 
D.delete 变量名 
【答案】**A**
【解析】**取消变量可以使用unset命令**

---
34、grep "[^0-9]"可以搜索到_____。
A.可以搜索含有数字之外内容的行 
B.不可以搜索到数字0和9 
C.可以搜索含有数字的行 
D.可以搜索到数字0和9 
【答案】**A**
【解析】**[ ] 在正则表达式中代表集合，内加^代表取反查找​​​​​​​**

---
35、命令行如下命令：
x=10;y=\${x:-30};echo \$y，其输出结果是_____。
A.0 
B.无值 
C.10 
D.30 
【答案】**C**
【解析】**\${x:-30}这个是看x有没有值，有值就返回x的值，没有就 返回30**

---
36、在memcached服务查看数据的指令是_____。
A.new 
B.write 
C.flush 
D.get 
【答案】**D**
【解析】**set写数据，get查数据。**

---
37、Linux命令行中，对多个命令进行逻辑分隔时，仅前一个命令成功才执行下一个命令，应该使用_____分隔符。
A.& 
B.% 
C.&& 
D.| 
【答案】**C**
【解析】**&&仅前一个命令成功才执行后一个命令 ||仅前一个命令失败才执行后一个命令**

---
38、使用什么（  　）指令可以清空memcached数据库中的所有数据。
A.flush 
B.delete_all 
C.flush_all 
D.delete 
【答案】**C**
【解析】**执行flush_all命令可以清空所有memcached数据**

---
39、若执行如下命令 
x=10;unset x;y=\${x:-30};echo \$y  
则最后的输出结果是_____
A.10 
B.0 
C.30 
D.无值 
【答案】**C**
【解析】**\${x:-30}这个是看x有没有值，有值就返回x的值，没有就返回30**

---
40、Tomcat中_____关键词表示一个虚拟主机。
A.server 
B.Host 
C.service 
D.Engine 
【答案】**B**
【解析】**Tomcat中每个Host就是一个虚拟主机**

---
# Multiple Choice
41、awk命令支持有条件地执行某些指令，仅当条件满足时才执行{}中的指令，awk支持_____判断条件。
A.字符判断 
B.文件大小判断 
C.正则判断 
D.数字判断 
【答案】**A,C,D**
【解析】**awk支持==,!=,>,>=等方式，但没有直接判断文件大小的条件**

---
42、awk命令中条件判断的”并且”和”或者”分别使用_____表示。
A.|| 
B.& 
C.&& 
D.| 
【答案】**A,C**
【解析】**&&代表并且，||代表或者**

---
43、持续集成包含_____流程。
A.Test 
B.Deploy 
C.Build 
D.Merge 
【答案】**A,C,D**

---
44、目前支持JAVA的Web服务器有_____。
A.Tomcat 
B.Jboss 
C.Websphere 
D.Weblogic 
【答案】**A,B,C,D**
【解析】**Tomcat（apache），JBoss（Redhat），Websphere（IBM），Weblogic（Oracle）**

---
45、下列关于Shell脚本中的if判断语句，说法正确的是_____。
A.支持多分支条件判断 
B.仅支持单分支条件判断 
C.支持单分支条件判断 
D.不支持多分支条件判断 
【答案】**A,C**
【解析】**shell的if判断支持单分支、双分支、多分支判断**

---
46、命令_____可以实现彩色字体的输出。
A.echo -e "\033[31mXYZ" 
B.echo -e "\033[31mXYZ\033[0m" 
C.echo -e \033[31mXYZ\033[0m 
D.echo  "\033[31mXYZ\033[0m" 
【答案】**A,B**
【解析】**使用echo处理特殊字符时需要加-e选项，之后内容需要用双引号包围**

---
47、Ansible支持_____类型的变量。
A.Host facts变量 
B.Playbook变量 
C.Inventory变量 
D.位置变量 
【答案】**A,B,C**

---
48、如下_____命令，可以对变量i进行自加2的操作。
A.let ++i 
B.let i=i+2 
C.let i+=2 
D.let i++  
【答案】**B,C**
【解析】**let i+=2是let i=i+2的简写，两者都支持自加2**

---
49、在ansible剧本中_____是与变量有关的键词定义。
A.vars 
B.vars_files 
C.par_prompt 
D.parameter 
【答案】**A,B**
【解析】**在剧本中可以通过vars定义变量；通过vars_prompt定义提示变量**

---
50、下面关于YAML文件描述正确的有_____。
A.数组使用-标识 
B.键值对使用:标识 
C.不能使用tab键缩进 
D.支持tab键缩进 
【答案】**A,B,C**


> 如有侵权，请联系作者删除
