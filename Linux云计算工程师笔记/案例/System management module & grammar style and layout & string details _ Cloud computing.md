@[TOC]( System management module & grammar style and layout & string details | Cloud computing )

---
# 1. 创建文件
## 1.1 问题
编写mktxtfile.py脚本，实现以下目标：

1. 编写一个程序，要求用户输入文件名
2. 如果文件已存在，要求用户重新输入
3. 提示用户输入数据，每行数据先写到列表中
4. 将列表数据写入到用户输入的文件名中

## 1.2 方案
用三个函数分别实现文件名获取、文件内容获取、将获取到的文件内容写入get_fname()函数获取的文件中 这三个方法，最终调用三个函数，完成文件创建：

1. 获取文件名函数get_fname()：利用while语句循环判断文件名是否存在，input文件名，如果不存在，循环停止，返回用户输入的文件名，如果存在，提示已存在，重新进入循环，直至文件名不存在为止，返回文件名用户输入的文件名

2. 文件内容获取函数get_contents()：创建空列表存储获取到的数据，利用while语句让用户循环输入数据，如果输入的数据是end，循环停止，返回列表中内容，如果输入的数据不是end，将输入的数据追加到列表结尾，返回列表中内容

3. wfile()函数：用with语句将获取到的文件以写方式打开，这样打开代码块结束后文件会自动关闭，将get_contents()函数返回内容写入到已打开文件中

4. 最终当用户cat文件名时，可以看到写入结果

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：编写脚本**
```shell
[root@localhost day04]# vim mktxtfile.py
#!/usr/bin/env python3
import os
def get_fname():
    while True:
        filename = input('请输入文件名：')
        if not os.path.exists(filename):
            break
        print('%s 已存在，请重试。' % filename)
    return filename
def get_contents():
    contents = []
    print('请输入内容，结束请输入end。')
    while True:
        line = input('> ')
        if line == 'end':
            break
        contents.append(line)
    return contents
def wfile(fname, contents):
    with open(fname, 'w') as fobj:
        fobj.writelines(contents)
if __name__ == '__main__':
    fname = get_fname()
    contents = get_contents()
    contents = ['%s\n' % line for line in contents]
    wfile(fname, contents)
```
**步骤二：测试脚本执行**
```shell
[root@localhost day04]# ls
adduser.py    format_str2.py  list_method.py  mylist.py     string_op.py
checkid.py    format_str.py   mkseq.py        randpass2.py
fmtoutput.py  get_val.py      mktxtfile.py    seq_func.py
[root@localhost day04]# python3 mktxtfile.py 
请输入文件名：passwd
请输入内容，结束请输入end。
> nihao,welcom
> woshi
> end
[root@localhost day04]# python3 mktxtfile.py 
请输入文件名：mkseq.py                                                
mkseq.py 已存在，请重试。
请输入文件名：randpass.py
请输入内容，结束请输入end。
> myname
> end 
[root@localhost day04]# cat passwd
nihao,welcom
woshi
[root@localhost day04]# cat randpass.py
myname
[root@localhost day04]# ls
adduser.py    format_str2.py  list_method.py  mylist.py     randpass.py
checkid.py    format_str.py   mkseq.py        passwd        seq_func.py
fmtoutput.py  get_val.py      mktxtfile.py    randpass2.py  string_op.py
```
# 2. 创建用户
## 2.1 问题
创建adduser.py文件，实现以下目标：

1. 编写一个程序，实现创建用户的功能
2. 提示用户输入用户名
3. 随机生成8位密码
4. 创建用户并设置密码
5. 将用户相关信息写入指定文件

## 2.2 方案
创建add_user()函数，让函数具有创建用户、创建密码、将用户密码写入到指定文件三种方法，因此为函数设置3个参数，分别是用户名、密码及用户名密码存放文件，最终通过函数调用上传实参的方式，完成用户创建
1. 利用subprocess.call函数运行用户创建命令
2. subprocess.call函数运行密码设置命令
3. 用with语句将指定的文件以追加模式打开，这样打开代码块结束后文件会自动关闭，将用户密码用指定格式写入指定文件
4. 调用add_user()函数时上传的用户名实参，是利用sys.argv[]参数，在命令行调用的时候由系统传递给程序，这个变量其实是一个List列表，用于保存命令行上的参数，argv[0] 一般是“被调用的脚本文件名或全路径”，argv[1]和以后就是传入的系统命令参数

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：编写脚本**

将randpass文件的代码以模块形式导入以下代码中,直接调用gen_pass()函数获取返回值（即获取随机生成的密码）：
```shell
[root@localhost day04] # vim adduser.py
#!/usr/bin/env python3
import sys
import subprocess
from randpass import gen_pass 
def add_user(username, password, fname):
    info = """user information:
username: %s
password: %s
"""
    subprocess.run('useradd %s' % username, shell=True)
    subprocess.run(
        'echo %s | passwd --stdin %s' % (password, username),
        shell=True
    )                                                                                                           
    with open(fname, 'a') as fobj:
        fobj.write(info % (username, password))
if __name__ == '__main__':
    username = sys.argv[1]
    password = gen_pass()
    fname = '/tmp/users.txt'
    add_user(username, password, fname) 
```
步骤二：测试脚本执行
```shell
[root@localhost day04]# python3 adduser.py b c d 
更改用户 b 的密码 。
passwd：所有的身份验证令牌已经成功更新。
[root@localhost day04]# python3 adduser.py a c d 
useradd：用户“a”已存在
更改用户 a 的密码 。
passwd：所有的身份验证令牌已经成功更新。
[root@localhost day04]# cat /tmp/users.txt
user information:
username: a
password: hD31SmTS
user information:
username: b
password: DztS7ycn
user information:
username: a
password: f2iH0Znt
```
# 3. 格式化输出
## 3.1 问题
创建fmtoutput.py脚本，要求如下：

1. 提示用户输入（多行）数据
2. 假定屏幕的宽度为50，用户输入的多行数据如图-1所示（文本内容居中）：

![在这里插入图片描述](https://img-blog.csdnimg.cn/48e0a40c5b8a4a32937d8a6ef52e8ebe.png)
图-1

## 3.2 方案
利用for循环方式遍历获取到的用户输入数据列表，将用户输入的每一条数据依次遍历出来

通过format()方法，把遍历得到的字符串当作一个模版，通过传入的参数进行格式化。这个用来格式化的模版使用大括号({,})作为特殊字符，其中^代表居中对齐、48代表宽度。

## 3.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：编写脚本**

将mktxtfile文件的代码以模块形式导入以下代码中,直接调用get_contents ()函数获取返回值（即获取用户输入数据列表）：
```shell
[root@localhost day04]# vim fmtoutput.py
#!/usr/bin/env python3
from mktxtfile import get_contents
width = 48
contents = get_contents()
print('+%s+' % ('*' * 48))
for line in contents:
    print('+{:^48}+'.format(line))    
print('+%s+' % ('*' * 48))  
```
**步骤二：测试脚本执行**
```shell
[root@localhost day04]# python3 fmtoutput.py 
请输入内容，结束请输入end。
> nihao
> my name zhangzhigang
> bye
> end
+************************************************+
+                     nihao                          +
+              my name zhangzhigang                 +
+                      bye                            +
+************************************************+
```

# Exercise
## 1 使用shutil模块的copyfileobj方法，将/etc/hosts拷贝到/tmp目录下，目标文件名为zhuji
```shell
import shutil
with open('/etc/hosts', 'rb') as src_fobj:
    with open('/tmp/zhuji', 'wb') as dst_fobj:
        shutil.copyfileobj(src_fobj, dst_fobj)
```
## 2 使用shutil模块的copy方法，将/etc/hosts拷贝到/tmp目录下，目标文件名为zhuji2
```shell
import shutil
shutil.copy('/etc/hosts', '/tmp/zhuji2')
```
## 3 使用shutil模块，将/etc/security目录拷贝到/tmp目录下，目标目录名为anquan
```shell
import shutil
shutil.copytree('/etc/security', '/tmp/anquan')
```
## 4 如何将两个变量a和b的值互换？
```shell
a = 10
b = 20
a, b = b, a
```
## 5 标识符满足哪些条件，才是合法标识符？
- 第一个字符必须是字母或下划线（_）
- 其余的字符可以是字母和数字或下划线
- 大小写敏感

## 6 如何获取python中所有的关键字？
```shell
>>> import keyword
>>> print(keyword.kwlist)
['False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
```
## 7 举例说明python的模块文件布局
```shell
#!/usr/bin/env python                 #起始行
“this is a test module”               #模块文档字符串
import sys                             #导入模块
import os
debug = True                           #全局变量声明
class FooClass(object):               #类定义
    'Foo class'
    pass
def test():                            #函数定义
    "test function"
    foo = FooClass()
if __name__ == ‘__main__’:           #程序主体
    test()
```
## 8 将name和age两个字符串进行格式化，name要求点10个宽度，age占8个宽度。它们都采用左对齐。
```shell
    '%-10s%-8s' % ('name', 'age')
```
## 9 字符串变量astr的内容是hello。将其转换为大写字母的方法是astr.upper()，执行完毕后，astr会不会变成大写字母？为什么？

- 不会变成大写字母。因为字符串是不可变类型，它能返回一个新的大写字母字符串，但是它本身不变。

> 如有侵权，请联系作者删除
