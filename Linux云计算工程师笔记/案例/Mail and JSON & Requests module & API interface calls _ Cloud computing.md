@[TOC]( Mail and JSON & Requests module & API interface calls | Cloud computing )

---
# 1. 通过本机发送邮件
## 1.1 问题
编写一个send_mail.py脚本，实现以下功能：

1. 创建bob和alice帐户
2. 编写发送邮件件程序，发件人为root，收件人是本机的bob和alice帐户
## 1.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：创建bob和alice帐户**
```shell
[root@ localhost day12]# ls /home/
Student  zabbix  zhangsan
[root@localhost day12]# useradd bob
[root@localhost day12]# useradd alice
[root@localhost day12]# ls /home/
alice  bob  Student  zabbix  zhangsan
```
**步骤二：编写发送邮件件程序，发件人为root，收件人是本机的bob和alice帐户**
```shell
[root@ localhost day12]# vim send_mail.py
import smtplib
from email.mime.text import MIMEText
from email.header import Header
#邮件正文有三个参数：第一个为文本内容，第二个设置文本格式plain，第三个utf-8设置编码保证多语言兼容性
message = MIMEText('Python邮件发送测试\n', 'plain', 'utf8')    
标准邮件需要三个头部信息： From, To, 和 Subject
#发送者信息
message['From'] = Header('root@localhost', 'utf8')    
#接收者信息
message['To'] = Header('bob@localhost', 'utf8')
#主题信息
message['Subject'] = Header('mail test', 'utf8')
sender = 'root@redhat.com'        #发送方
receivers = ['bob@localhost', 'alice@126.com']    #收件方
smtp_obj = smtplib.SMTP('localhost')    #用localhost发邮件
# smtplib负责发送邮件
smtp_obj.sendmail(sender, receivers, message.as_string())
```
SMTP是发送邮件的协议，Python内置对SMTP的支持，可以发送纯文本邮件、HTML邮件以及带附件的邮件。

Python对SMTP支持有smtplib和email两个模块，email负责构造邮件，smtplib负责发送邮件。

Python SMTP 对象使用 sendmail 方法发送邮件：
```shell
smtp_obj.sendmail(sender, receivers, message.as_string())
```
参数说明：
sender: 邮件发送者地址。
receivers: 字符串列表，邮件发送地址。
message.as_string(): 发送消息 ，str模式

由于可以一次发给多个人，所以recives传入一个列表，邮件正文是一个str，as_string()把MIMEText对象变成str。

**步骤三：测试脚本执行**
```shell
[root@ localhost day12]# python3 send_mail.py
[root@ localhost day12]# mail –u bob
Heirloom Mail version 12.5 7/5/10.  Type ? for help.
“/var/mail/bob”: 1 message 1 new
>N  1 =?utf8?q?root=4Oloca  Mon Jul 30 09:36  18?663  “”
& 1
From root@redhat.com Mon Jul 30 09:36:44 2018
Return- Path: <root@redhat.com>
X- Original- To: bob@localhost.tedu.cn
Content- Type: text/plain; charset=“utf8”
From: root@localhost@room8pc16.tedu.cn
To: bob@localhost@room8pc16.tedu.cn
Subject: mail test
Date: Mon, 30 Jul 2018 09:36:44 +0800 (CST)
Status: R
Python邮件发送测试
&
```
# 2. 通过互联网服务器发送邮件
## 2.1 问题
编写一个mail_client.py脚本，实现以下功能：

1. 通过自己互联网注册的邮箱，为其他同学互联网邮箱发邮件

## 2.2 方案
导入sys模块，用sys.argv方法获取get_web函数实参，让用户在命令行上提供http://www.tedu.cn和/tmp/tedu.html两个参数，调用get_web函数实现如下功能：

1) 导入urllib模块，使用urllib模块的urlopen函数打开url（即网址），赋值给html
2) 以写方式打开/tmp/tedu.html文件
3) 以循环方式：
读html获取的数据，保存到data
将data写入/tmp/tedu.html
4) 关闭html

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：环境准备**

使用SMTP协议发送的邮件，需要先查看您的发件人邮箱是否有开启SMTP协议，如没有需要开启，测试使用的是126.com的邮箱作为发信人邮箱，开启SMTP协议如下

1. 先登录到126.com邮箱，如图-1所示：

![在这里插入图片描述](https://img-blog.csdnimg.cn/61935878136a41479f7f40a7d3ce1021.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-1

2. 看到邮箱上面的功能栏中有一个“设置”的选项，单击该选项，然后选择下拉菜单的“POP3/SMTP/IMAP”，如图-2所示：

![在这里插入图片描述](https://img-blog.csdnimg.cn/5022edfc0bad4744985e33f135492442.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-2

3. 如图-3所示，上面红框的两个必须勾选上，如没有勾选，要选择开启就可以勾选上了：

![在这里插入图片描述](https://img-blog.csdnimg.cn/187aa3023a57494ea0e49a5852a5416b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-3

4. 页面向下可以可以看到下图-4红框里是：SMTP服务器是:smtp.126.com：

![在这里插入图片描述](https://img-blog.csdnimg.cn/1374e0da612348928bc4991b7f9e7b09.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-4

**步骤二：编写脚本**
```shell
[root@ localhost day12]# vim mail_client.py
#!/usr/bin/env python3
import smtplib
from getpass import getpass
from email.mime.text import MIMEText
from email.header import Header
mail_host = 'smtp.126.com'        #发件人邮箱账号
mail_user = 'zhangzhigang79@126.com'        #收件人邮箱账号
mail_pwd = getpass()        #获取密码
#邮件正文有三个参数：第一个为文本内容，第二个设置文本格式plain，第三个utf-8设置编码保证多语言兼容性
message = MIMEText('Python邮件发送测试\n', 'plain', 'utf8')
#发送者信息
message['From'] = Header('zhangzhigang79@126.com', 'utf8')
#接收者信息
message['To'] = Header('zhangzhigang79@126.com', 'utf8')
#主题信息
message['Subject'] = Header('python 1802 mail test', 'utf8')
sender = 'zhangzhigang79@126.com'        #发送方
receivers = ['zhangzhigang79@126.com']        #接收方
smtp_obj = smtplib.SMTP()        #创建SMTP对象
smtp_obj.connect(mail_host)    #将SMTP对象与发送人邮件简历连接建立连接
smtp_obj.login(mail_user, mail_pwd)        #登录用户名密码
# SMTP 对象使用 sendmail 方法发送邮件
smtp_obj.sendmail(sender, receivers, message.as_string())
```
**步骤三：测试脚本执行**
```shell
[root@ localhost day12]# python3 mail_client.py
Password：
```
如果发送成功，结果显示如图-5所示：

![在这里插入图片描述](https://img-blog.csdnimg.cn/bf3656e71afd493fa542ff3d019ad147.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA5bCP6aWF6aCt,size_20,color_FFFFFF,t_70,g_se,x_16)
图-5

# 3. 天气预报查询
## 3.1 问题
编写一个display_weather.py脚本，实现以下功能：

1. 运行程序时，屏幕将出现你所在城市各区县名字
2. 用户指定查询某区县，屏幕上将出现该区县当前的气温、湿度、风向、风速等

## 3.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：找到天气信息规律**

1. 首先我们想要实现的功能是天气预报，从哪获取天气这是一个问题，在这里可以使用http://www.weather.com.cn/data/sk/101051301.html这个应用程序编程接口，101051301是城市的ID，可以到http://www.weather.com.cn/查看，替换后浏览器打开，如图-6所示，图示为json格式：

![在这里插入图片描述](https://img-blog.csdnimg.cn/4321f04761634ef2a56b4c8417794588.png)
图-6

注意：图中看不懂的文字是编码问题

2. 从图-1中可以看出cityid就是城市ID，temp是温度，SD是湿度，我们编写代码可以直接获取到网站相应信息，编写脚本wather.py：
```shell
[root@ localhost day12]# vim weather.py
#!/usr/bin/python     #这里是python的目录
from urllib.request import urlopen
import json
#打开网页，使用urllib模块的urlopen函数打开url，赋值给html
html = urlopen('http://www.weather.com.cn/data/sk/101010100.html')
#读html获取的数据，保存到data
data = html.read()
#从data中获取我们想要的信息，json.loads()是将json格式数据转换为字典
#（可以理解为json.loads()函数是将字符串转化为字典）
print(json.loads(data))
#关闭html
html.close()
```
3.执行脚本结果如下：
```shell
[root@ localhost day12]# python3 weather.py
{‘weatherinfo’:{‘city’:‘北京’,‘cityid’:‘101010100’,‘temp’:‘27.9’,‘WD’:‘南风’,‘WS’:‘小于3级’,‘SD’:‘28%’,‘AP’:‘1002hPa’,‘njd’:‘暂无实况’,‘WSE’:‘<3’,‘time’:‘17:55’,‘sm’:‘2.1’,‘isRadar’:‘1’,‘Radar’:‘JC_RADAR_AZ9010_JB’}}
```
从以上脚本执行结果中我们可以看到，从网站中获取到的数据是以字典形式显示，显示信息有城市、城市id，温度、风向等等，根据这种规律，编写下面代码

**步骤二：编写代码实现如下功能**

1. 定义一个字典，该字典中键‘0’和‘1’对应的值为天气网址中城市对应的id，城市不同id则不同
2. 运行程序时，屏幕将出现你所在城市名字
3. 当用户指定查询某城市（即输入0或1时）
4. 调用get_weather函数，函数的实际参数为city_codes字典对应值（即对应的城市id）
5. 打开天气网页，使用urllib模块的urlopen函数打开url，赋值给html
6. 读html获取的数据，用json.loads()获取天气信息，获取到的信息为字典形式
7. 从获取到的字典数据中提取气温、湿度、风向、风速等信息，保存在output变量中
8. 将output变量作为get_weather函数的返回值，打印在屏幕上

```shell
[root@ localhost day12]# vim display_weather.py
#!/usr/bin/python
from urllib.request import urlopen
import json
def get_weather(city_code):        #定义一个输入城市id的函数
5. 打开天气网页，使用urllib模块的urlopen函数打开url，赋值给html
    url = 'http://www.weather.com.cn/data/sk/%s.html' % city_code
    html = urlopen(url)
6.读html获取的数据，用json.loads()获取我们想要的信息
#json.loads()是将json格式数据转换为字典
#（可以理解为json.loads()函数是将字符串转化为字典）
    data = json.loads(html.read())
7.output为返回值，即最终屏幕显示的信息
    output = '风向：%s, 风力: %s， 温度：%s, 湿度：%s' % (
#data获取到的天气信息为字典，该字典中weatherinfo键对应的值还是一个字典，这个字典中‘WD’键对应的值是风向，‘WS’键对应的值是风力，'temp'键对应的值是温度，'SD'键对应的值是湿度，利用键值对关系将相应数据显示出来即可
        data['weatherinfo']['WD'],
        data['weatherinfo']['WS'],
        data['weatherinfo']['temp'],
        data['weatherinfo']['SD']
    )
    return output
if __name__ == '__main__':
1.定义字典：键对应的值为天气网站网址接口中城市ID
    city_codes = { '0': '101010100', '1': '101121404'}
2．代码执行后，屏幕给出的提示信息
    prompt = """(0) 北京
(1) 台儿庄
请选择(0/1): """
3．根据提示信息，输入0或1
    choice = input(prompt)
4.调用get_weather函数，其实际参数为city_codes字典对应值
8.打印调用get_weather函数返回值
    print(get_weather(city_codes[choice]))
```
**步骤三：测试脚本执行**
```shell
[root@ localhost day12]# python3 display_weather.py
(0) 北京
(1) 台儿庄
请选择(0/1): 0
 风向：南风， 风力： 小于3级， 温度：27.9， 湿度：28%
[root@ localhost day12]# python3 display_weather.py
(0) 北京
(1) 台儿庄
请选择(0/1): 1
 风向：东北风， 风力： 小于3级， 温度：22.3， 湿度：64%
```
# 4. 钉钉机器人
## 4.1 问题
通过钉钉软件创建一个群聊机器人，要求：

1. 编写代码，通过python脚本实现钉钉机器人在群中发送消息
2. 使用json和requests模块

## 4.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：在钉钉中创建群聊机器人**

/

图-7

/

图-8

/

图-9

/

图-10

/

图-11

**步骤二：编写代码**
```shell
[root@ localhost day12]# vim dingtalk.py
import json
import requests
import sys
def send_msg(url, reminders, msg):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {
        "msgtype": "text",  # 发送消息类型为文本
        "at": {
            "atMobiles": reminders,
            "isAtAll": False,   # 不@所有人
        },
        "text": {
            "content": msg,   # 消息正文
        }
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.text
if __name__ == '__main__':
    msg = sys.argv[1]
    reminders = ['15055667788']  # 特殊提醒要查看的人,就是@某人一下
    url = 此处填写上面webhook的内容
    print(send_msg(url, reminders, msg))
```
**步骤三：测试脚本执行**
```shell
[root@ localhost day12]# python3 dingtalk.py "这只是一个测试而已"
```
/
图-12

# 5. 通过阿里云api查询天气
## 5.1 问题
通过阿里云开发者平台查询天气，要求：
1. 在阿里云开发者平台0元购买api产品
2. 使用json和requests模块

## 5.2 步骤
实现此案例需要按照如下步骤进行。

**步骤一：登陆阿里云平台**
1. 在浏览器中打开http://www.aliyun.com
2. 使用阿里系账户登陆

**步骤二：购买产品**
1. 登陆后在搜索框中搜索“天气”
2. 找到“杭州网尚科技”
3. 点击0元购买
4. 点击“管理控制台”，在后台找到查询所需的APPCODE

**三：编写代码**
```shell
>>> url = 'http://jisutqybmf.market.alicloudapi.com/weather/query'
>>> headers = {'Content-Type': 'application/json; charset=UTF-8', 'Authorization': 'APPCODE 你管理后台中查询到的appcode'}
>>> params = {'citycode': '101010100'}
>>> r = requests.get(url, headers=headers, params=params)
>>> data = r.json()
>>> import pprint
>>> pprint.pprint(data)
# 取出后天最高、最低温度
>>> pprint.pprint(data['result']['daily'][2]['day']['temphigh'])
'8'
>>> pprint.pprint(data['result']['daily'][2]['night']['templow'])
'-2'
```

# Exercise
## 1 smtplib和email模块的作用是什么？
- smtplib模块定义了一个SMTP客户端会话对象，可用于发送邮件。
- email模块是用于管理电子邮件的库。它不是用来发送邮件的，而是用来生成发送的邮件对象的。如，email对象可以设置email的头部结构以及正文。
## 2 什么是JSON？它的主要作用是什么？
- JSON(JavaScript Object Notation) 是一种轻量级的数据交换格式，采用完全独立于程序语言的文本格式。易读，也方便机器进行解析和生成。
- 它的主要作用是将各种数据结构转换成字符串，然后在函数之间传递字符串，或者将字符串从Web客户机传递给服务器端程序。接收端接收到字符串后，还能再转换成相应的数据类型。
## 3 如下代码所示，requests模块发送请求后，返回的数据可以用哪些方式进行读取？
> ```shell
> import requests
> r = requests.get('http://www.tedu.cn/')
> ```

- r.text：返回字符串形式的数据
- r.content：返回二进制形式的数据
- r.json()：用于读取json格式的数据

## 4 HTTP的方法用哪些？
- GET：请求获取Request-URI所标识的资源
- POST：在Request-URI所标识的资源后附加新的数据
- OPTIONS：请求与给定路径匹配的HTTP头的值
- HEAD：请求服务器做好一切发送资源的准备，但是只发送头信息
- DELETE：请求服务器删除Request-URI所标识的资源
- PUT：请求服务器存储一个资源，并用Request-URI作为其标识
- TRACE：请求服务器回送收到的请求信息，主要用于测试或诊断
- CONNECT：保留将来使用

> 如有侵权，请联系作者删除
