@[TOC]( File object & function foundation & module foundation | Cloud computing )

---
# 1. 模拟cp操作
## 1.1 问题
创建cp.py文件，实现以下目标：

1. 将/bin/ls“拷贝”到/root/目录下
2. 不要修改原始文件

## 1.2 方案
获取用户原文件名和新文件名，打开原文件，打开新文件，从打开的原文件中读取数据，写入到打开的新文件中，关闭两个文件

cp代码的过程中，需要注意的部分在于：

如果一个文件过大，你将无法直接读取数据到内存，此时，使用while循环语句，分次读取数据，每次读4096字节，读取数据为空时，结束循环，将数据写入到目标文件

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：编写脚本**
```shell
 [root@localhost day03]# vim cp.py 
#!/usr/bin/env python3
f1 = open('/bin/ls', 'rb')
f2 = open('/root/ls', 'wb')
data = f1.read()
f2.write(data)
f1.close()
f2.close()
```
或将上面的代码改为以下写法：

循环读取文件中数据，避免读取数据过大
```shell
[root@localhost day03]# vim cp2.py 
#!/usr/bin/env python3
src_fname = '/bin/ls'
dst_fname = '/tmp/ls'
src_fobj = open(src_fname, 'rb')
dst_fobj = open(dst_fname, 'wb')
while True:
    data = src_fobj.read(4096)   # 每次读4096字节
    if data == b'':              # 读不到数据意味着读写完毕，中断循环
        break
    dst_fobj.write(data)         # 将数据写到目标文件
src_fobj.close()
dst_fobj.close()
```
或将上面的代码改为以下写法：

With打开文件读取数据或写入数据后，文件会直接关闭
```shell
[root@localhost day03]# vim cp3.py 
#!/usr/bin/env python3
src_fname = '/bin/ls'
dst_fname = '/root/ls'
with open(src_fname, 'rb') as src_fobj:
    with open(dst_fname, 'wb') as dst_fobj:
        while True:
            data = src_fobj.read(4096)
            if not data:
                break
            dst_fobj.write(data)
```
或将上面的代码改为以下写法：

sys.argv方法表示空列表，执行脚本时输入命令： python3 cp_func.py /bin/ls /root/ls，表示sys.argv=[cp_func.py，‘/bin/ls’，‘/root/ls’]，所以，调用copy函数时，列表切片方式获取实参为（‘/bin/ls’，‘/root/ls’）
```shell
[root@localhost day03]# vim cp_func.py 
#!/usr/bin/env python3
import sys
def copy(src_fname, dst_fname):
    src_fobj = open(src_fname, 'rb')
    dst_fobj = open(dst_fname, 'wb')
    while True:
        data = src_fobj.read(4096)
        if not data:
            break
        dst_fobj.write(data)
    src_fobj.close()
    dst_fobj.close()
copy(sys.argv[1], sys.argv[2])
```
**步骤二：测试脚本执行**
```shell
[root@localhost day03]# python3 cp.py
[root@localhost day03]# cd /root
[root@localhost ~]# ls
core  ls
[root@localhost day03]# python3 cp2.py
[root@localhost day03]# cd /root
[root@localhost ~]# ls
core  ls
[root@localhost day03]# python3 cp3.py
[root@localhost day03]# cd /root
[root@localhost ~]# ls
core  ls
[root@localhost day03]# python3 cp_func.py /bin/ls /root/ls
[root@localhost day03]# cd /root
[root@localhost ~]# ls
core  ls
```
# 2. 生成随机密码
## 2.1 问题
创建randpass.py脚本，要求如下：

1. 编写一个能生成8位随机密码的程序
2. 使用random的choice函数随机取出字符
3. 改进程序，用户可以自己决定生成多少位的密码

## 2.2 方案
导入random模块，通过random静态对象调用choice()方法，从自定义字符串all_chs中获取随机项，将获取到的随机字符ch与原result值进行拼接，将最终字符串结果返回给函数，for循环每循环一次获取一个随机字符，密码位数由循环次数决定，循环次数由传递参数值决定。

此程序需要注意的部分在于：
1. 导入String模块，其中ascii_letters是生成所有字母，从a-z和A-Z，digits是生成所有数字0-9
2. 将整个生成随机密码的代码封装进gen_pass()函数中，当模块文件直接执行时，调用函数即可输出结果
3. 参数传递问题：调用函数无实参时，函数调用默认参数，有实参时，函数调用实际参数

# 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：编写脚本**
```shell
[root@localhost day03]# vim randpass.py
#!/usr/bin/env python3
import random
import string
all_chs = string.digits + string.ascii_letters
def gen_pass(n=8):
    result = ''
    for i in range(n):
        ch = random.choice(all_chs)
        result += ch
    return result
if __name__ == '__main__':
    print(gen_pass())
    print(gen_pass(4))  
```
或将上面的代码改为以下写法：

利用列表推导式更简洁输出数据
```shell
[root@localhost day03]# vim randpass2.py
#!/usr/bin/env python3
from random import choice
from string import ascii_letters, digits
all_chs = ascii_letters + digits
def randpass(n=8):
    result = [choice(all_chs) for i in range(n)]
    return ''.join(result)  # 将列表的字符拼接起来
if __name__ == '__main__':
    print(randpass())
    print(randpass(4))
```
**步骤二：测试脚本执行**
```shell
[root@localhost day03]# python3 randpass.py
82wi2gOP
XzMi
[root@localhost day03]# python3 randpass.py
5wMoDEgC
BDpc
[root@localhost day03]# python3 randpass.py
Ige2VGod
Az0z
[root@localhost day03]# python3 randpass2.py 
eajAocMH
edW1
```

# Exercise
## 1 读取一个文本文件的内容，有哪些方法？
- read()：读取指定数目的字节
- readline()：读取一行
- readlines()：读取全部内容，生成一个字符串列表，文件的每一行是列表中的每一项
- 通过for循环进行遍历

## 2 打开文件时，文件对象的访问模式有r、w和a。它们的区别是什么？
- r：以读方式打开（文件不存在则报错）
- w：以写方式打开（文件存在则清空，不存在则创建）
- a：以追加模式打开（必要时创建新文件）

## 3 有一个名为fobj的文件对象，fobj.seek(0, 2)表示什么？
- 表示将文件指针移动到文件的结尾

## 4 函数默认的返回值是什么？如何自己手工指定返回值，使用哪个关键字？
- 函数返回值默认是None
- 通过return关键字返回指定的结果。

## 5 python中如何使用位置参数？
- python将位置参数放到sys模块的argv列表中了
- sys.argv列表中的第一个元素是python脚本本身
- sys.argv列表中的其他元素是命令行上其他的命令行参数，对应shell脚本的$1、$2等

> 如有侵权，请联系作者删除
