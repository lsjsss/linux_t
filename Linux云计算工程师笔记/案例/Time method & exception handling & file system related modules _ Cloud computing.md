@[TOC]( Time method & exception handling & file system related modules | Cloud computing )

---
# 1. 简化除法判断
## 1.1 问题
创建mydiv.py脚本，要求如下：

1. 提示用户输入一个数字作为除数
2. 如果用户按下Ctrl+C或Ctrl+D则退出程序
3. 如果用户输入非数字字符，提示用户应该输入数字
4. 如果用户输入0，提示用户0不能作为除数

## 1.2 方案
首先，执行try子句（在关键字try和关键字except之间的语句），输入数字，让这个数字被100整除，

1. 如果没有异常发生，忽略except子句，try子句执行后，执行else子句和finally子句，最后执行 try 语句之后的代码结束整个程序。

2. 如果在执行try子句的过程中发生了异常，异常的类型和 except 之后的名称相符，那么对应的except子句将被执行。然后执行finally子句，最后执行 try 语句之后的代码结束整个程序。

需要注意的是：允许用户中断这个程序（使用Ctrl+C或Ctrl+D方法）。用户中断的信息会引发KeyboardInterrupt 和EOFError 这两种异常。

一个 try 语句可能包含多个except子句，分别来处理不同的特定的异常。最多只有一个分支会被执行。

处理程序将只针对对应的try子句中的异常进行处理，而不是其他的 try 的处理程序中的异常。

try except 语句只有一个可选的else子句，使用这个子句，必须放在所有的except子句之后。这个子句将在try子句没有发生任何异常的时候执行。

finally子句是无论异常是否发生，是否捕捉都会执行的一段代码，使用finally可以保证文件总是能正常的关闭

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：编写脚本**
```shell
[root@localhost day05]# vim mydiv.py
#!/usr/bin/env python3
try:
    num = int(input("number: "))
    result = 100 / num
except ValueError:
    print('请输入数字')
except ZeroDivisionError:
    print('不允许使用0')
except (KeyboardInterrupt, EOFError):
    print('\nBye-bye')
else:
    print(result)  # 不发生异常才执行的语句
finally:
    print('Done')  # 不管异常是否发生都要执行的语句
print('end of program')  
#不是必须把所有的语句写全，常用的有try-except和try-finally组合
```
步骤二：测试脚本执行
```shell
[root@localhost day05]# python3 mydiv.py 
number: 0
不允许使用0
Done
end of program
[root@localhost day05]# python3 mydiv.py 
number: nighao
请输入数字
Done
end of program
[root@localhost day05]# python3 mydiv.py 
number: 3
33.333333333333336
Done
end of program
[root@localhost day05]# python3 mydiv.py 
number: 55^C
Bye-bye
Done
end of program
[root@localhost day05]# python3 mydiv.py 
number: 
Bye-bye
Done
end of program
```
# 2. 自定义异常
## 2.1 问题
创建myerror.py脚本，要求如下：

1. 编写第一个函数，函数接收姓名和年龄，如果年龄不在1到120之间，产生ValueError异常
2. 编写第二个函数，函数接收姓名和年龄，如果年龄不在1到120之间，产生断言异常

## 2.2 方案
两个函数，分别有引发异常及断言异常的功能：

1. 当set_age()函数调用名字与年龄两个实参时，如果年龄在0-120范围内，打印“bob is 25 years old”，如果年龄在0-120范围外，利用raise 语句抛出一个指定的异常

2. 当set_age2()函数调用名字与年龄两个实参时，如果年龄在0-120范围内，表达式为true，打印“bob is 20 years old”，如果年龄在0-120范围外，表达式为Flase，利用assert 断言语句抛出一个指定的异常

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：编写脚本**
```shell
[root@localhost day05]# vim myerror.py
#!/usr/bin/env python3
def set_age(name, age):
    if not 0 < age < 120:
        raise ValueError("age out of range.")
    print("%s is %s years old" % (name, age))
def set_age2(name, age):
    assert 0 < age < 120, 'age out of range.'
    print("%s is %s years old" % (name, age))
if __name__ == '__main__':
    set_age('bob', 25)
    set_age2('bob', 20)
```
**步骤二：测试脚本执行**
```shell
[root@localhost day05]# python3 myerror.py
bob is 25 years old
bob is 20 years old
[root@localhost day05]# python3 myerror.py 
Traceback (most recent call last):
  File "myerror.py", line 11, in <module>
    set_age('bob', 125)
  File "myerror.py", line 3, in set_age
    raise ValueError("age out of range.")
ValueError: age out of range.
[root@localhost day05]# python3 myerror.py 
bob is 25 years old
Traceback (most recent call last):
  File "myerror.py", line 12, in <module>
    set_age2('bob', 120)
  File "myerror.py", line 7, in set_age2
    assert 0 < age < 100, 'age out of range.'
AssertionError: age out of range.
```
# 3. 操作文件系统
## 3.1 问题
创建os_module.py脚本，熟悉os模块操作,要求如下：

1. 切换到/tmp目录
2. 创建example目录
3. 切换到/tmp/example目录
4. 创建test文件，并写入字符串foo bar
5. 列出/tmp/exaple目录内容
6. 打印test文件内容
7. 反向操作，把test文件以及example目录删除

## 3.2 方案
用os方法查看用户当前所在位置，切换到指定目录，创建example目录，切换到创建目录下，以读写方式打开并创建一个新文件，将指定内容写入新文件中，列出目录下有指定目录下有哪些文件，指定从开始位置读取指定文件字符串并打印出来，关闭打开文件，并删除文件，删除目录。

注意：读取打印文件内容时，要将字节转化为字符串读取出来。

## 3.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：编写脚本**
```shell
[root@localhost day05]# vim os_module.py
#!/usr/bin/env python3
import os
#1)    切换到/tmp目录
os.getcwd()        #'/root/python代码/os'
os.chdir("/tmp") 
os.getcwd()        #'/tmp'
#2)    创建example目录 
os.mkdir("example")
#3)    切换到/tmp/example目录
os.chdir("/tmp/example")
os.getcwd()        #'/tmp/example' 
#4)    创建test文件，并写入字符串foo bar
f=os.open("test.txt",os.O_RDWR|os.O_CREAT)        #以读写方式打开/创建并打开一个新文件
os.write(f,b"foo bar nihao")
#5)    列出/tmp/exaple目录内容
os.listdir("/tmp/example")     #['test.txt']
#6)    打印test文件内容 
os.lseek(f,0,0)        #指定从开始位置读取字符串
str=os.read(f,100)
str = bytes.decode(str)
print("读取的字符是：",str)
os.close(f)
#7)    反向操作，把test文件以及example目录删除
os.remove("/tmp/example/test.txt")
os.removedirs("/tmp/example")
```
步骤二：测试脚本执行
```shell
[root@localhost day05]# python3 os_module.py 
读取的字符是： foo bar
```
# 4. 记账程序
## 4.1 问题
创建account.py脚本，要求如下：

1. 假设在记账时，有一万元钱
2. 无论是开销还是收入都要进行记账
3. 记账内容包括时间、金额和说明等
4. 记账数据要求永久存储

## 4.2 方案
创建4个函数，分别实现记录开销、记录收入、查询收支、判断函数调用的四个方法，导入时间模块获取时间，导入os模块判断文件是否存在，导入pickle模块用来python特有类型与数据类型转换：

1. 调用show_menu()函数后，先判断记录余额文件是否存在，如果不存在创建文件并写入余额，如果存在，利用while循环在交互端输出提示，请用户input0/1/2/3任意数值，如果输入的值不是0/1/2/3，打印输入值无效请重新输入并重新开始循环，如果输入的值是3，停止整个循环，如果输入的值是0/1/2通过字典键值对关联关系，调用相对应函数

2. 如果输入的值是0，字典cmds中0键对应的值是spend_money，调用spend_money ()记录开销函数，让此函数实现获取当前系统日期、输入开销金额、输入开销备注信息、以二进制读方式打开记录余额文件计算本次开销后余额，以写方式打开记录余额文件将计算后开销余额写入文件，以追加方式打开记账文件，将日期、开销、备注、余额写入追加入记账文件最后

3. 如果输入的值是1，字典cmds中0键对应的值是save_money，调用save_money ()记录收入函数，让此函数实现获取当前系统日期、输入收入金额、输入收入备注信息、以二进制读方式打开记录余额文件计算本次收入后余额，以写方式打开记录余额文件将计算后收入余额写入文件，以追加方式打开记账文件，将日期、开销、备注、余额写入追加入记账文件最后

4. 如果输入的值是2，调用查询收支函数query ()，以二进制读方式打开记账文件，利用for循环遍历文件中数据，打印出来，打开记录余额文件读取余额并打印。

需要注意的是：为确保代码可以正常执行，while循环利用try except语句处理异常，优先匹配特殊异常，让用户按下Ctrl+C或Ctrl+D可以退出程序，遇到索引错误可以结束当次循环，重新开始选择选项。

将记录余额文件以及记账文件作为参数传入函数中

## 4.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：编写脚本**
```shell
[root@localhost day05]# vim account.py
#!/usr/bin/env python3
# 日期　　开销　　收入　　余额　　备注
import time
import os
import pickle as p
def spend_money(record, wallet):
    date = time.strftime('%Y-%m-%d')
    amount = int(input('金额: '))
    comment = input('备注: ')
    with open(wallet, 'rb') as fobj:
#load从数据文件中读取数据，并转换为Python的数据结构
        balance = p.load(fobj) – amount        
    with open(wallet, 'wb') as fobj:
           #dump将数据通过特殊形式转换为只有python语言认识的字符串，并写入文件
        p.dump(balance, fobj)
    with open(record, 'a') as fobj:
        fobj.write(
            "%-15s%-8s%-8s%-10s%-20s\n" %
            (date, amount, 'n/a', balance, comment)
        )
def save_money(record, wallet):
    date = time.strftime('%Y-%m-%d')
    amount = int(input('金额: '))
    comment = input('备注: ')
    with open(wallet, 'rb') as fobj:
        balance = p.load(fobj) + amount
    with open(wallet, 'wb') as fobj:
        p.dump(balance, fobj)
    with open(record, 'a') as fobj:
        fobj.write(
            "%-15s%-8s%-8s%-10s%-20s\n" %
            (date, 'n/a', amount, balance, comment)
        )
def query(record, wallet):
    with open(record) as fobj:
        for line in fobj:
            print(line, end='')
    with open(wallet, 'rb') as fobj:
          #load从数据文件中读取数据，并转换为Python的数据结构
        balance = p.load(fobj)
    print('当前余额: %s' % balance)
def show_menu():
    prompt = """(0) 记录开销
(1) 记录收入
(2) 查询收支记录
(3) 退出
请选择(0/1/2/3): """
    cmds = {'0': spend_money, '1': save_money, '2': query}
    record = 'record.txt'   # 记帐
    wallet = 'wallet.data'  # 记录余额
    if not os.path.exists(wallet):        #判断文件是否存在
        with open(wallet, 'wb') as fobj:
            p.dump(10000, fobj)
    while True:
        try:
            choice = input(prompt).strip()[0]
        except IndexError:
            continue
        except (KeyboardInterrupt, EOFError):
            print('\nBye-bye')
            choice = '3'
        if choice not in '0123':
            print('无效输入，请重试')
            continue
        if choice == '3':
            break
        cmds[choice](record, wallet)
if __name__ == '__main__':
    show_menu()
```
**步骤二：测试脚本执行**
```shell
[root@localhost day05]# python3 account.py
(0) 记录开销
(1) 记录收入
(2) 查询收支记录
(3) 退出
请选择(0/1/2/3): 0
金额: 2000
备注: huafei
(0) 记录开销
(1) 记录收入
(2) 查询收支记录
(3) 退出
请选择(0/1/2/3): 1
金额: 1000
备注: shouru
(0) 记录开销
(1) 记录收入
(2) 查询收支记录
(3) 退出
请选择(0/1/2/3): 2
2018-04-25     2000    n/a     28890     huafei              
2018-04-25     n/a     1000    29890     shouru              
当前余额: 29890
(0) 记录开销
(1) 记录收入
(2) 查询收支记录
(3) 退出
请选择(0/1/2/3): 3
[root@localhost day05]# python3 account.py
(0) 记录开销
(1) 记录收入
(2) 查询收支记录
(3) 退出
请选择(0/1/2/3): ^C
Bye-bye
[root@localhost day05]# python3 account.py
(0) 记录开销
(1) 记录收入
(2) 查询收支记录
(3) 退出
请选择(0/1/2/3): 
Bye-bye
```

# Exercise
## 1 获取字典adict['name']的值，如果没有找到，则返回'Not Found'
```shell
>>> adict.get('name', 'Not Found')
```
## 2 遍历字典adict，通过两种方法取出字典的key和value。
```shell
>>> for key in adict:
...   print('%s: %s' % (key, adict[key]))
>>> for key, val in adict.items():
...   print('%s: %s' % (key, val))
```
## 3 aset和bset是两个可变集合，举例说明什么是交集、并集和差补。
- 交集：aset & bset，取出两个集合中都包含的元素
- 并集：aset | bset，取出两个集合中所有的元素
- 差补：aset - bset，取出在第一个集合中有，而第二个集合中没有的元素
## 4 通过time模块，显示当前时间：年月-月-日 时：分：秒
```shell
>>> import time
>>> time.strftime('%Y-%m-%d %H:%H:%S')
```
## 5 time.time()返回的是什么？
- 返回的是时间戳。也就是1970年1月1日0点到执行time.time()之间的秒数。

## 6 写出异常处理的语法结构
```shell
try:
    有可能发生异常的语句
except (要补获的异常):
    发生异常时执行的语句
else:
    异常不发生才执行的语句
finally:
    不管是否发生异常都要执行的语句
```
## 7 os.path模块有哪些判断路径的方法？
- os.path.isabs(path)：判断是否为绝对路径
- os.path.isfile(path)：判断是否为文件
- os.path.ismount(path)：判断是否为挂载点
- os.path.isdir(path)：判断是否为目录
- os.path.islink(path)：判断是否为链接
- os.path.exists(path)：判断是否存在
## 8 pickle模块的主要作用和方法是什么？
- pickle模块可以将任意的数据类型保存到文件中，并且可以无损的将其取出来
- pickle.dump()：用于将数据存入文件
- pickle.load()：用于将数据从文件中取出

> 如有侵权，请联系作者删除
