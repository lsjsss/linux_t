@[TOC]( Cluster & Security & Python Topic | Cloud computing )
 
---
# Single Choice
1、程序如下：
```shell
try:
    number = int(input("请输入数字："))
    print("number:",number)
    print("=======hello======")
except Exception as e:
    # 报错错误日志
    print("打印异常详情信息： ",e)
else:
    print("没有异常")
finally:#关闭资源
    print("finally")
print("end")
```
输入的是 1a 结果是_____。
A.
```shell
number: 1
打印异常详情信息：  invalid literal for int() with base 10:
finally
End 
```
B.
```shell
打印异常详情信息：  invalid literal for int() with base 10:
finally
End 
```
C.
```shell
========hello===========
打印异常详情信息：  invalid literal for int() with base 10:
finally
End 
```
D.以上都正确 
【答案】**B**

---
2、能够返回当前时间戳的方法是_____。
A.time.strftime() 
B.time.ctime() 
C.time.localtime() 
D.time.time() 
【答案】**D**

---
3、下列选项中_____是Zabbix_server服务默认监听的端口号。
A.10050 
B.10500 
C.10055 
D.10051 
【答案】**D**

---
4、在使用passwd命令时，下列_____选项可以查看账户的密码状态。
A.-U 
B.-S 
C.-L 
D.-M 
【答案】**B**

---
5、Zabbix监控获得的数据信息存放在了_____。
A.mysql 
B.excel 
C.zabbix.log 
D.zabbix.conf 
【答案】**A**

---
6、在使用passwd命令时，下列_____选项可以锁定账户。
A.-S 
B.-l 
C.-L 
D.-U 
【答案】**B**

---
7、下列_____语句在Python中是非法的。
A.x  +=  y 
B.x, y = y, x 
C.x = (y = z + 1) 
D.x = y = z = 1 
【答案】**C**

---
8、用户使用_____命令生成登录sshd服务的秘钥对。
A.gpg 
B.md5sum 
C.ssh-keygen 
D.openssl 
【答案】**C**

---
9、有关进程和线程说法错误的是_____。
A.线程的执行离不开进程的资源调度 
B.线程是程序执行的最小单位 
C.一个进程当中可以没有线程也可以包含一个或多个线程 
D.进程是争夺CPU资源的最小单位 
【答案】**C**

---
10、有如下列表：users = [('tom', 20), ('jerry', '19')] 使用_____选项可以取出jerry 。
A.users[1] 
B.users[1][0] 
C.users[0] 
D.users[-1][1] 
【答案】**B**

---
11、print()函数打印多项内容时，默认用空格分隔输出的各项。如果使用---替换空格，正确的参数是_____。
A.start='---' 
B.seq='---' 
C.sep='---' 
D.end='---' 
【答案】**C**

---
12、关于多线程编程，下面说法正确的是_____。
A.一个进程可以产生一到多个线程 
B.线程与进程完全一样，只是不同的称呼 
C.Python中主要使用Thread模块来实现多线程编程 
D.每个线程都有自己独立的运行空间 
【答案】**A**

---
13、在使用chage命令时，下列_____选项可以实现用户首次登陆系统
强制修改密码的功能。
A.-d 
B.-l 
C.-W 
D.-E 
【答案】**A**

---
14、关于模块导入，下面说法确的是_____。
A.模块不管导入（import）多少次，只会加载（load）一次 
B.为了防止循环导入，两个模块不能互相import 
C.多次导入模块，以最后一次导入为准 
D.只有管理员有权限导入模块 
【答案】**A**

---
15、使用字符串的_____方法，用于去除字符串左端的空白字符。
A.strip 
B.trim 
C.ltrim 
D.lstrip 
【答案】**D**

---
16、下列关于类的方法错误的是_____。
A.子类当中只能继承父类的普通方法，不能继承初始化方法 
B.对象是类的实例 
C.类是用来描述具有相同的属性和方法的对象的集合 
D.方法是类中定义的函数 
【答案】**A**
【解析】**从类中定义的方法必须和类或对象有关 改成 子类当中只能继承父类的普通方法，不能继承初始化方法**

---
17、使用nmap命令对目标主机做TCP SYN扫描半开式扫描，使用_____选项。
A.-sS 
B.-sT 
C.-sP 
D.-sU 
【答案】**A**
【解析】**nmap命令的选项中-sT是做tcp扫描，-sU是做udp扫描，-sS是 半开扫描（不执行完整的3次握手4次断开）**

---
18、有以下代码：
```shell
if -0.0:
    print('yes')
else:
    print('no')
```
程序的运行结果是_____。
A.no 
B.yes 
C.0 
D.报错 
【答案】**A**

---
19、关于函数的返回值，下面说法错误的是_____。
A.函数内部可以出现多个return语句 
B.函数可以通过return返回多个值 
C.函数没有明确的返回值，则返回None 
D.函数通过return进行返回 
【答案】B

---
20、list(range(0, 10, 2))产生的值是_____。
A.[2, 4, 6, 8] 
B.[0, 2, 4, 6, 8] 
C.[2, 4, 6, 8, 10] 
D.[0, 2, 4, 6, 8, 10] 
【答案】**B**

---
21、有关匿名函数，下面说法正确的是_____。
A.匿名函数没有返回值 
B.匿名函数的多行语句通过逗号分隔 
C.匿名函数不支持参数 
D.通过关键字lambda定义匿名函数 
【答案】**D**

---
22、程序执行期间，用户按下ctrl + c，将会触发_____异常。
A.KeyboardInterrupt 
B.ValueError 
C.NameError 
D.EOFError 
【答案】**A**

---
23、给文件添加_____属性后，仅可以使用追加的方式向文件内添加新内容。
A.a 
B.e 
C.i 
D.s 
【答案】**A**
【解析】**+i锁定文件，+a仅可追加**

---
24、创建两个集合s1 = set('abc'); s2 = set('bcd')，那么s1 | s2的结果是_____。
A.{'bc'} 
B.{'b', 'c'} 
C.{'a'} 
D.{'a', 'b', 'c', 'd'} 
【答案】**D**

---
25、下列选项中作为Zabbix_agentd服务监听的端口号是_____。
A.10051 
B.10500 
C.10055 
D.10050 
【答案】**D**
【解析】**zabbix_agent默认是10050，zabbix_server默认是 10051**

---
26、下列选项中_____是Zabbix_agentd服务的主配置文件。
A.zabbix.conf 
B.zabbix_server.conf 
C.zabbix_agent.conf 
D.zabbix_agentd.conf 
【答案】**D**

---
27、关于OOP中self的说法正确的是_____。
A.self代表实例本身 
B.class中所有方法的self都是可有可无的 
C.只有创建实例对象时，才会用到self 
D.self是关键字 
【答案】A

---
28、以下不能创建一个字典的语句是_____。
A.dict4 = {(1,2,3): "uestc"} 
B.dict1 = {} 
C.dict2 = { 3 : 5 } 
D.dict3 = {[1,2,3]: "uestc"} 
【答案】**D**

---
29、通过pickle模块将字典data写入文件fobj的方法是_____。
A.pickle.dump(fobj, data) 
B.pickle.dump(data, fobj) 
C.pickle.load(fobj, data) 
D.pickle.load(data, fobj) 
【答案】**B**

---
30、以下表达式可以正确的运行的有_____。
A.(123, 456) + 123 
B.[123, 456] + 123 
C.(123) + 123 
D.'abc' + 123 
【答案】**C**

---
31、以下表达式，正确定义了一个集合数据对象的是_____。
A.x = [ 200, ’flg’, 20.3 ] 
B.x = {‘flg’ : 20.3} 
C.x = ( 200, ’flg’, 20.3) 
D.x = { 200, ’flg’, 20.3} 
【答案】**D**

---
32、有如下函数声明：def fn(name, age): pass。下面方法使用正确的是_____。
A.fn('tom', 'jerry', 20) 
B.fn('tom') 
C.fn(name='tom', 20) 
D.fn('tom', age=20) 
【答案】**D**

---
33、关于循环语句说法正确的是_____。
A.循环如果执行了continue，它的else语句不会执行 
B.循环如果被break结束，它的else语句将会执行 
C.循环如果执行了continue，它的else语句将会执行 
D.循环如果被break结束，它的else语句不会执行 
【答案】**D**

---
34、下面有关hashlib模块计算md5值，说法错误的是_____。
A.只要原始数据有微小改动，md5值一定大不相同 
B.hashlib.md5()函数中的参数类型是字节串类型 
C.hashlib模块在使用前需要先下载，再导入 
D.md5值一般使用16进制数表示 
【答案】**C**

---
35、小王执行n = input("number: ")语句时，输入了10。运行结果为15的是_____。
A.n + 5 
B.n + str(5) 
C.int(n) + 5 
D.str(n) + 5 
【答案】**C**

---
36、'to' in 'python'的结果是_____。
A.True 
B.yes 
C.False 
D.no 
【答案】**C**

---
37、使用nmap暴力破解ssh密码的脚本是_____。
A.ssh-passwd.nse 
B.sshd-brute.nse 
C.sshd-passwd.nse 
D.ssh-brute.nse 
【答案】**D**

---
38、有以下代码：
```shell
if [5 > 10]:
    print('yes')
else:
    print('no')
```
程序的运行结果是_____。
A.True 
B.False 
C.yes 
D.no 
【答案】**C**

---
39、使用tcpdump命令抓包时，要求多个条件必须同时匹配使用_____选项。
A.and 
B.not 
C.or 
D.host 
【答案】**A**
【解析】**and代表逻辑与，or代表逻辑或**

---
40、以下叙述正确的是_____。
A.else只能和if连用，不能和循环语句连用 
B.在循环体内使用break语句或continue语句的作用相同 
C.只能在循环体内使用break语句 
D.continue语句的作用是结束整个循环的执行 
【答案】**C**

---
# Multiple Choice
41、以下字符串格式正确的有_____。
A.“abc”ab” 
B.“abc\nab” 
C.‘abc”ab’ 
D.‘abc”ab” 
【答案】**B,C**

---
42、下列软件能够提供监控服务有_____。
A.Cacti  
B.Nagios 
C.Zabbix 
D.nmap 
【答案】**A,B,C**
【解析】**常用监控软件有：cacti、nagios、zabbix**

---
43、以下可以生成192.168.1.1~192.168.1.254整个范围内的所有IP地址有_____。
A.['192.168.1.%s'  %  i  for  i  in  range(1, 254)] 
B.['192.168.1.%s'  %  i  for  i  in  range(1, 255)] 
C.['192.168.1.'  +  str(i)  for  i  in  range(1, 254)] 
D.['192.168.1.'  +  str(i)  for  i  in  range(1, 255)] 
【答案】**B,D**

---
44、zabbix监控服务，发送监控报警消息的方式有_____。
A.邮件 
B.短信 
C.只能使用邮件发送报警消息 
D.打电话 
【答案】**A,B**
【解析】**Zabbix支持短信和邮件发送报警信息**

---
45、有一个字典adict = {'name': 'bob', 'age': 23}，以下说法正确的有_____。
A.通过adict['name']可以取出bob 
B.字典长度为2 
C.通过adict[0]可取出字典中的第一个元素 
D.字典的长度为4 
【答案】**A,B**

---
46、有如下列表：users = ['tom', 'jerry', 'jack', 'rose']。可以取出rose的选项有_____。
A.users[4] 
B.users[-1] 
C.users[0] 
D.users[3] 
【答案】**B,D**

---
47、a = (10, 20, 30)，则a属于_____类型。
A.顺序 
B.不可变 
C.映射 
D.标量 
【答案】**A,B**

---
48、下列选项中是对称加密算法有_____。
A.AES 
B.RSA 
C.DES 
D.DSA 
【答案】**A,C**
【解析】**AES和DES是对称算法，RSA和DSA是非对称算法**

---
49、可以使用shutil的_____方法拷贝文件。
A.copy 
B.copyfileobj 
C.move 
D.copytree 
【答案】**A,B**

---
50、Prometheus有哪些组件？ 
A.PHP 
B.Node_exporter 
C.MySQL 
D.Prometheus server 
【答案】**B,D**


> 如有侵权，请联系作者删除
