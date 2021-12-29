@[TOC]( Function foundation & function advanced application & module | Cloud computing )

---
# 1. 简单的加减法数学游戏
## 1.1 问题
编写math_game.py脚本，实现以下目标：

1. 随机生成两个100以内的数字
2. 随机选择加法或是减法
3. 总是使用大的数字减去小的数字
4. 如果用户答错三次，程序给出正确答案

## 1.2 方案
创建4个函数，分别实现返回两数之和、返回两数之差、判断表达式正确性、是否继续计算四种方法：

1. 首先调用main()函数（是否继续计算功能），main函数利用循环无限次调用exam()函数进行计算，计算结束，用户选择是否继续（此过程利用try语句捕获索引错误、ctrl+c（中断）错误、ctrl+d错误），如果选择n即结束循环，不再调用exam()函数，否则循环继续

2. 调用exam()函数：

a) 输出运算公式：利用列表切片将随机生成的两个数打印（这两个数利用random模块及列表生成式随机生成，并利用sort()方法进行降序排序，确保相减时一直是大的数字减小的数字），利用random模块随机生成“+”“-”号，输出在两数之间

b) 用户输入值，利用for循环进行三次判断，如果运算公式结果与用户输入值相同，循环结束，系统输出“你赢了”，exam()函数执行结束，否则系统输出“你答错了”，循环继续，3次都回答错误，利用循环的else分支输出运算公式及结果

c) 上诉运算公式结果：利用random模块随机生成“+”“-”值对关系调用（其中“+”“-”号作为字典键，返回和函数add()及返回差函数sub()作为值，调用时将随机生成的两个数字作为参数传递给add()函数及sub()函数）

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：编写脚本**
```shelll
[root@localhost day06]# vim math_game.py
#!/usr/bin/env python3
import random
def add(x, y):
    return x + y
def sub(x, y):
    return x - y
def exam():
    cmds = {'+': add, '-': sub}  # 将函数存入字典
    nums = [random.randint(1, 100) for i in range(2)] # 生成两个数
    nums.sort(reverse=True)  # 降序排列
    op = random.choice('+-')
    result = cmds[op](*nums)  # 调用存入字典的函数，把nums列表拆开，作为参数传入
    prompt = "%s %s %s = " % (nums[0], op, nums[1])
    for i in range(3):
        try:
            answer = int(input(prompt))
        except:
            continue
        if answer == result:
            print('你真棒，答对了！')
            break  # 答对了就不要再回答了，结束循环
        else:
            print('答错了')
    else:
        print("%s%s" % (prompt, result))   # 只有循环不被break才执行
def main():
    while True:
        exam()
        try:
            go_on = input('Continue(y/n)? ').strip()[0]
        except IndexError:
            continue
        except (KeyboardInterrupt, EOFError):
            go_on = 'n'
        if go_on in 'nN':
            print('\nBye-bye.')
            break
if __name__ == '__main__':
    main()
```
实现此案例还可利用while循环：
```shelll
[root@localhost day06]# vim mygui.py
#!/usr/bin/env python3
import random
def add(x, y):
    return x + y
def sub(x, y):
    return x - y
def exam():
    cmds = {'+': add, '-': sub}  # 将函数存入字典
    nums = [random.randint(1, 100) for i in range(2)] # 生成两个数
    nums.sort(reverse=True)  # 降序排列
    op = random.choice('+-')
    result = cmds[op](*nums)  # 调用存入字典的函数，把nums列表拆开，作为参数传入
    prompt = "%s %s %s = " % (nums[0], op, nums[1])
    tries = 0
    while tries < 3:
        try:
            answer = int(input(prompt))
        except:
            continue
        if answer == result:
            print('你真棒，答对了！')
            break  # 答对了就不要再回答了，结束循环
        else:
            print('答错了')
            tries += 1
    else:
        print("%s%s" % (prompt, result))   # 只有循环不被break才执行
def main():
    while True:
        exam()
        try:
            go_on = input('Continue(y/n)? ').strip()[0]
        except IndexError:
            continue
        except (KeyboardInterrupt, EOFError):
            go_on = 'n'
        if go_on in 'nN':
            print('\nBye-bye.')
            break
if __name__ == '__main__':
    main()
```
**步骤二：测试脚本执行**
```shelll
[root@localhost day06]# python3 math_game.py 
54 + 19 = 
54 + 19 = 
54 + 19 = 73
你真棒，答对了！
Continue(y/n)? y
60 + 39 = 99
你真棒，答对了！
Continue(y/n)? y
18 + 15 = 33
你真棒，答对了！
Continue(y/n)? y
35 + 20 = 55
你真棒，答对了！
Continue(y/n)? y
37 + 35 = 72
你真棒，答对了！
Continue(y/n)? y
77 - 57 = 20
你真棒，答对了！
Continue(y/n)? y
35 + 23 = 5
答错了
35 + 23 = 6
答错了
35 + 23 = 7
答错了
35 + 23 = 58
Continue(y/n)? y
75 + 47 = 122
你真棒，答对了！
Continue(y/n)? ^C
Bye-bye.
```
# 2. 进制转换函数
## 2.1 问题
创建myint.py脚本，要求如下：

1. 基于int内建函数，创建int2函数，实现2进制字符串转换成10制数整数
2. 基于int内建函数，创建int8函数，实现8进制字符串转换成10制数整数
3. 基于int内建函数，创建int16函数，实现16进制字符串转换成10制数整数

## 2.2 方案
1. 导入functools模块

2. 修改现有的int函数，将base参数固定值

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：编写脚本**
```shelll
[root@localhost day06]# vim myint.py
# 改造int函数，将base=2固定下来，生成的新函数叫int2
int2 = partial(int, base=2)
print(int2('10101100'))
int8 = partial(int, base=8)
print(int8('11'))
int16 = partial(int, base=16)
print(int16('11'))
```
步骤二：测试脚本执行，结果如图-1、图-2、图-3所示：
```shelll
[root@localhost day06]# python3 myint.py
172
9
17
```
# 3. 备份程序
## 3.1 问题
编写backup.py脚本，实现以下目标：

1. 需要支持完全和增量备份
2. 周一执行完全备份
3. 其他时间执行增量备份
4. 备份文件需要打包为tar文件并使用gzip格式压缩

## 3.2 方案
整体框架创建3个函数，分别实现完全备份、增量备份、文件加密3种功能：

1. 首先导入time模块，利用if进行判断，如果当地时间是星期一，执行完全备份函数，否则执行增量备份函数，其中，通配符%a代表时间星期几缩写，上传参数分别为要备份的原目录、目标目录、md5字典存放目录

2. 调用完全备份函数：

a) 首先获取新文件名，将新文件名放入目标目录下，目的是定义备份文件的绝对路径，以写压缩方式打开目标目录下新文件，将原目录写入新文件中，完成完全备份，其中os.path.join作用是将目录名和文件的基名拼接成一个完整的路径

b) 了解os.walk()目录遍历器输出文件结构，利用for循环将要备份原目录中文件遍历出来作为字典键值对键， md5加密结果作为字典键值对的值（此时将原目录中文件作为上传参数调用文件加密函数），存入空字典中，字典中每个文件对应一个md5值，最后将字典写入到md5字典存放目录中

3. 调用文件加密函数：将原目录文件循环读取逐一加密，返回加密结果

4. 调用增量备份函数：

a) 增量备份函数代码与完全备份函数基本一致

b) 区别在于，备份前要先以二进制读方式打开md5字典存放目录，读取旧数据，判断旧数据中键对应的加密值与新加密值是否相同，如果不相同，则将新增内容写入到目标文件中（即只备份新数据）

5. 注意：md5主要用于原文件与新文件判断

## 3.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：编写脚本**
```shelll
[root@localhost day06]# vim backup.py
#!/usr/bin/env python3
import time
import os
import tarfile
import hashlib
import pickle
#用于判断两个文件是否相同，提取每个文件中的前4字节的内容然后输出md5码进行比较
def check_md5(fname):
    m = hashlib.md5()
    with open(fname, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)
    return m.hexdigest()
def full_backup(src_dir, dst_dir, md5file):
    fname = os.path.basename(src_dir.rstrip('/'))
    fname = '%s_full_%s.tar.gz' % (fname, time.strftime('%Y%m%d'))
    fname = os.path.join(dst_dir, fname)
    md5dict = {}
    tar = tarfile.open(fname, 'w:gz')
    tar.add(src_dir)
    tar.close()
    for path, folders, files in os.walk(src_dir):
        for each_file in files:
            key = os.path.join(path, each_file)
            md5dict[key] = check_md5(key)
    with open(md5file, 'wb') as fobj:
        pickle.dump(md5dict, fobj)
def incr_backup(src_dir, dst_dir, md5file):
    fname = os.path.basename(src_dir.rstrip('/'))
    fname = '%s_incr_%s.tar.gz' % (fname, time.strftime('%Y%m%d'))
    fname = os.path.join(dst_dir, fname)
    md5dict = {}
    with open(md5file, 'rb') as fobj:
        oldmd5 = pickle.load(fobj)
    for path, folders, files in os.walk(src_dir):
        for each_file in files:
            key = os.path.join(path, each_file)
            md5dict[key] = check_md5(key)
    with open(md5file, 'wb') as fobj:
        pickle.dump(md5dict, fobj)
    tar = tarfile.open(fname, 'w:gz')
    for key in md5dict:
        if oldmd5.get(key) != md5dict[key]:
            tar.add(key) 
    tar.close()
if __name__ == '__main__':
    # mkdir /tmp/demo; cp -r /etc/security /tmp/demo
    src_dir = '/tmp/demo/security'
    dst_dir = '/var/tmp/backup'   # mkdir /var/tmp/backup
    md5file = '/var/tmp/backup/md5.data'
    if time.strftime('%a') == 'Mon':
        full_backup(src_dir, dst_dir, md5file)
    else:
        incr_backup(src_dir, dst_dir, md5file)
```
**步骤二：测试脚本执行**
```shelll
[root@localhost day07]# python3 backup.py 
[root@localhost day07]# cd /var/tmp/backup/
[root@localhost backup]# ls
md5.data  security_full_20180502.tar.gz  security_incr_20180502.tar.gz
```

# Exercise
## 1 以下函数定义是否正确？为什么？
> ```shelll
> def myfunc(age=22, name):
>    pass
> ```

- 不正确。因为函数的参数的一个要求是非关键字参数必须在关键字参数前面。
## 2 编写函数时，如果函数的参数个数不固定，可能有N个也可能一个没有，该如何解决？
- 使用参数组，如：
- *arg：表示将非关键字参数保存到名为arg的元组中
- **kwarg：表示将关键字参数保存到名为kwarg的字典中

## 3 请将以下函数改为匿名函数。
> ```shelll
> def add(x, y):
>     return x + y
> ```
```shelll
add = lambda x, y: x + y
```
## 4 请通过map()函数简化以下代码。
> ```shelll
> time_str = '2019-12-1'
> time_str = time_str.split('-')
> year = int(time_str[0])
> month = int(time_str[1])
> date = int(time_str[2])
> ```

```shelll
year, month, date = map(int, time_str.split('-'))
```
## 5 分析以下代码。请问变量x的值是什么？为什么？
> ```shelll
> x = 10
> def change_x():
>     global x
>     x = 'hello'
> print(x)
> ```
- x的值是10。因为change_x函数没有调用。

## 6 使用递归函数，计算6的阶乘。
```shelll
def fac(n):
    if n == 1:
        return 1
    return n * fac(n - 1)
if __name__ == '__main__':
    print(fac(6))
```
## 7 Python的模块命名有哪些约定？
- 首字符可以是字母或下划线
- 后续字符可以是字母、数字或下划线
- 区分大小写

## 8 python文件和模块的关系是什么？
- 文件是物理上组织的代码的形式，模块是逻辑上组织代码的形式
- 将文件的扩展名.py移除就是模块名

## 9 在导入模块时，python到哪些路径查找模块文件。
- sys.path所定义的路径
- PYTHONPATH环境变量所定义的路径

> 如有侵权，请联系作者删除
