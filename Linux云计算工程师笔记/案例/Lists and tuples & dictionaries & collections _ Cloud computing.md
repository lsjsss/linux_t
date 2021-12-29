@[TOC]( Lists and tuples & dictionaries & collections | Cloud computing )

---
# 1. 用列表构建栈结构
## 1.1 问题
创建stack.py脚本，要求如下：

1. 栈是一个后进先出的结构
2. 编写一个程序，用列表实现栈结构
3. 需要支持压栈、出栈、查询功能

## 1.2 方案
创建空列表存储数据，创建4个函数，分别实现压栈、出栈、查询以及判断函数调用的方法。

此程序需要注意的是堆栈的结构特点，先进后出，后进先出：
1. 调用show_menu()函数后，利用while循环交互端输出提示，请用户input0/1/2/3任意数值，如果输入的值不是0/1/2/3，打印输入值无效请重新输入并重新开始循环，如果输入的值是3，停止整个循环，如果输入的值是0/1/2通过字典键值对关联关系，调用相对应函数
2. 如果输入的值是0，字典cmds中0键对应的值是push_it，push_it()调用压栈函数，压栈函数利用stack.append()方法将输入数据追加到列表结尾
3. 如上，如果输入的值是1，调用出栈函数pop_it()，出栈函数如果stack列表中有数据，弹出列表最后一个元素（根据堆栈结构特点stack.pop()中参数为空），如果stack列表没有数据，输出空列表
4. 如果输入的值是2，调用查询函数view_it()，显示当前列表

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：编写脚本**

让输出的文字带颜色：\033[31;1m高亮度红色字体、\033[31;1m高亮度绿色字体、\033[0m关闭所有属性
```shell
[root@localhost day04]# vim stack.py
#!/usr/bin/env python3
stack = []
def push_it():
    item = input('item to push: ')
    stack.append(item)
def pop_it():
    if stack:   
        print("\033[31;1mPopped %s\033[0m" % stack.pop())
    else:
        print('\033[31;1mEmpty stack\033[0m')
def view_it():
    print("\033[32;1m%s\033[0m" % stack)
def show_menu():
    prompt = """(0) push_it
(1) pop_it
(2) view_it
(3) quit
Please input your choice(0/1/2/3): """
    cmds = {'0': push_it, '1': pop_it, '2': view_it}
    while True:
        # strip() 方法用于移除字符串头尾指定的字符（默认为空格）
        choice = input(prompt).strip()[0]    
        if choice not in '0123':
            print('Invalid input. Try again.')
            continue     #结束本次循环
    
        if choice == '3':
            break       #结束整个循环
   
        cmds[choice]()   # push_it()  pop_it()
        # if choice == '0':
        #     push_it()
        # elif choice == '1':
        #     pop_it()
        # elif choice == '2':
        #     view_it()
if __name__ == '__main__':
    show_menu()
```
**步骤二：测试脚本执行**
```shell
[root@localhost day04]# python3 stack.py
(0) push_it
(1) pop_it
(2) view_it
(3) quit
Please input your choice(0/1/2/3): 6
Invalid input. Try again.
(0) push_it
(1) pop_it
(2) view_it
(3) quit 
Please input your choice(0/1/2/3): 0
item to push: nihao
(0) push_it
(1) pop_it
(2) view_it
(3) quit
Please input your choice(0/1/2/3): 1 
Popped nihao
(0) push_it
(1) pop_it
(2) view_it
(3) quit
Please input your choice(0/1/2/3): 2
[]
(0) push_it
(1) pop_it
(2) view_it
(3) quit
Please input your choice(0/1/2/3): 0
item to push: a         
(0) push_it
(1) pop_it
(2) view_it 
Please input your choice(0/1/2/3): 0
item to push: b
(0) push_it
(1) pop_it
(2) view_it
(3) quit
Please input your choice(0/1/2/3): 0
item to push: c
(0) push_it
(1) pop_it
(2) view_it
(3) quit
Please input your choice(0/1/2/3): 1
Popped c
(0) push_it
(1) pop_it
(2) view_it
(3) quit
Please input your choice(0/1/2/3): 2
['a', 'b']
(0) push_it
(1) pop_it
(2) view_it
(3) quit
Please input your choice(0/1/2/3): 3
(3) quit
```
# 2. 模拟用户登陆信息系统
## 2.1 问题
编写login.py脚本，实现以下目标：

1. 支持新用户注册，新用户名和密码注册到字典中
2. 支持老用户登陆，用户名和密码正确提示登陆成功
3. 主程序通过循环询问进行何种操作，根据用户的选择，执行注册或是登陆操作

## 2.2 方案
创建空字典存储用户名、密码，用三个函数分别实现用户注册、用户登录以及判断调用函数这三个方法，完成模拟用户登录：

1. 调用show_menu()函数后，利用while循环交互端输出提示，请用户input0/1/2任意数值，如果输入的值不是0/1/2，打印选择无效请重新输入并重新开始循环，如果输入的值是2，停止整个循环，如果输入的值是0/1/2通过字典键值对关联关系，调用相对应函数

2. 如果输入的值是0，字典cmds中0键对应的值是register，register ()调用注册函数，函数利用if方法判断输入用户名是否存在，如果用户名在字典中，输出用户名已存在，否则用户输入密码，并将用户名与密码以键值对形式放入字典中

3. 如上，如果输入的值是1，调用登录函数login()，利用if方法判断输入的用户名的对应的密码是否和字典中存储用户对应密码相同，如果不同显示登录失败，否则登录成功，此函数中导入getpass模块使用方法，作用是输入密码不可见。

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：编写脚本**
```shell
[root@localhost day05]# vim login.py
#!/usr/bin/env python3
import getpass
userdb = {}
def register():
    username = input('username: ')
    if username in userdb:
        print('\033[31;1m%s already exists.\033[0m' % username)
    else:
        password = input('password: ')
        userdb[username] = password
def login():
    username = input('username: ')
    password = getpass.getpass('password: ')
    # if username not in userdb or userdb['username'] != password:
    if userdb.get(username) != password:
        print('\033[31;1mLogin incorrect\033[0m')
    else:
        print('\033[32;1mLogin successful\033[0m')
def show_menu():
    prompt = """(0) register
(1) login
(2) quit
Please input your choice(0/1/2): """
    cmds = {'0': register, '1': login}
    while True:
        choice = input(prompt).strip()[0]
        if choice not in '012':
            print('Invalid choice. Try again.')
            continue
        if choice == '2':
            break
        cmds[choice]()
if __name__ == '__main__':
    show_menu()
```
**步骤二：测试脚本执行**
```shell
[root@localhost day05]# python3 login.py 
(0) register
(1) login
(2) quit
Please input your choice(0/1/2): 0
username: a
password: 123
(0) register
(1) login
(2) quit
Please input your choice(0/1/2): 1
username: a
password: 
Login successful
(0) register
(1) login
(2) quit
Please input your choice(0/1/2): 1
username: b
password: 
Login incorrect
(0) register
(1) login
(2) quit
Please input your choice(0/1/2): 2
```
# 3. 比较文件内容
## 3.1 问题
编写程序，完成以下要求：

1. 有两个文件：a.log和b.log
2. 两个文件中有大量重复内容
3. 取出只有在b.log中存在的行

## 3.2 方案
使用集合去重效率高，操作简单。只要将两个文件内容转换成列表，再进行差补运算即可得到仅在b.log中存在的行。

**步骤一：准备两个文件**
```shell
[root@localhost day05]# cp /etc/passwd /tmp/a.log
[root@localhost day05]# cp /etc/passwd /tmp/b.log
# 修改b.log，使之与a.log有不同的行
[root@localhost day05]# vim /tmp/b.log
```
**步骤二：编写程序**
```shell
[root@localhost day05]# vim fdiff.py
with open('/tmp/a.log') as f1:
    aset = set(f1)
with open('/tmp/b.log') as f2:
    bset = set(f2)
with open('/tmp/result.txt', 'w') as f3:
     f3.writelines(bset - aset)
```
**步骤三：验证**
```shell
[root@localhost day05]# cat /tmp/result.txt
```
查看结果，result.txt中将是只有b.log中有，而a.log没有的行。

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
## 3 aset和bset是两个可变集合，举例说明什么是交集、并集和差补。
- 交集：aset & bset，取出两个集合中都包含的元素
- 并集：aset | bset，取出两个集合中所有的元素
- 差补：aset - bset，取出在第一个集合中有，而第二个集合中没有的元素

## 4 ('hello')是哪种数据类型
('hello')是元组。单元素元组需要注意，元素后面必须有个逗号，否则构不成元组。

## 5 列表根据不同的分类方式，都属于哪些类型？
列表按存储模型来分，属于容器类型；按更新模型来分，属于可变型；按访问模型来分，属于序列类型。

> 如有侵权，请联系作者删除
