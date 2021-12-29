@[TOC]( OOP basics & OOP advanced & RE modules | Cloud computing )

---
# 1. 编写游戏人物
## 1.1 问题
创建程序，要求如下：

1. 创建游戏角色类
2. 游戏人物角色拥有名字、武器等属性
3. 游戏人物具有攻击和行走的方法
4. 武器通过武器类实现

## 1.2 方案
由于游戏角色和武器都由类实现，而这个两个类又完全不同，所以可以通过组合来实现。将武器类的一个实例作为游戏人物的一个属性。

## 1.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：编写脚本**
```shell
[root@localhost day07]# vim game_role.py
class Weapon:
    def __init__(self, wname, strength):
        self.wname = wname
        self.strength = strength
class Warrior:
    def __init__(self, name, weapon):
        self.name = name
        self.weapon = weapon
    def speak(self, words):
        print("I'm %s, %s" % (self.name, words))
    def show_me(self):
        print("我是%s, 我是一个战士。我用的武器是%s" % (self.name, self.weapon.wname))
if __name__ == '__main__':
    blade = Weapon('青龙偃月刀', 100)
    print(blade.wname, blade.strength)
    gy = Warrior('关羽', blade)
    gy.show_me()
    cz = Weapon('禅杖', 100)
    lzs = Warrior('鲁智深', cz)
    lzs.show_me()
```
**步骤二：测试脚本执行**
```shell
[root@localhost day07]# python3  game_role.py
青龙偃月刀 100
我是关羽, 我是一个战士。我用的武器是青龙偃月刀
我是鲁智深, 我是一个战士。我用的武器是禅杖
```
# 2. 出版商程序
## 2.1 问题
创建books.py文件，实现以下目标：

1. 为出版商编写一个Book类
2. Book类有书名、作者、页数等属性
3. 打印实例时，输出书名
4. 调用实例时，显示该书由哪个作者编写

## 2.2 方案
创建一个类，类中创建3种魔法方法：

1. __init__方法：__init__方法用于初始化实例属性，创建对象后会自动调用__init__方法，属于构造器方法，此处初始化了书名及作者两个属性

2. __str__方法：创建对象后，打印实例对象pybook，返回书名，打印出书名

3. __call__方法：创建对象后，可以像调用函数一样调用该方法，模拟函数的行为，打印出书名及作者

## 2.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：编写脚本**
```shell
[root@localhost day07] # vim books.py
#!/usr/bin/env python3
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
    def __str__(self):
        return '<Book: %s>' % self.title
    def __call__(self):
        print('《%s》 is written by %s.' % (self.title, self.author))
if __name__ == '__main__':
    pybook = Book('Core Python', 'Weysley')
    print(pybook)  # 调用__str__
    pybook()   # 调用__call__
```
**步骤二：测试脚本执行**
```shell
[root@localhost day07]# python3 books.py 
<Book: Core Python>
《Core Python》 is written by Weysley.
```
# 3. 分析apache访问日志
## 3.1 问题
编写count_patt.py脚本，实现一个apche日志分析脚本：

1. 统计每个客户端访问apache服务器的次数
2. 将统计信息通过字典的方式显示出来
3. 分别统计客户端是Firefox和MSIE的访问次数
4. 分别使用函数式编程和面向对象编程的方式实现
## 3.2 方案
collections是python内建的一个集合模块，模块中提供了许多有用的集合类,其中counter类 是一个简单的计数器，以字典的键值对形式储存，其中搜索的元素作为键，出现的次数作为值

实现过程：

1. 实例化一个计数器

2. 实例化正则表达式

3. 将文件以对象形式打开

4. 通过正则表达式查找文件每一行

5. 如果找到结果

6. 将结果添加到计数器，通过update方法更新原有数据

7. 返回计数器

8. 将文件地址和正则表达式作为实参传递给函数

## 3.3 步骤
实现此案例需要按照如下步骤进行。

**步骤一：编写脚本**
```shell
[root@localhost day08]# vim count_patt.py
#!/usr/bin/env python3
import re
import collections
#fname 文件地址  patt 正则表达式
def count_patt(fname,patt):
    
    counter = collections.Counter()
   
    cpatt = re.compile(patt)
        with open(fname) as fobj:
        for line in fobj:
           
            m = cpatt.search(line)
           
            if m:
              
                counter.update([m.group()])
  
    return counter
if __name__ == "__main__":
    fname = "access_log.txt"
    ip_patt = "^(\d+\.){3}\d+"
    a = count_patt(fname,ip_patt)
    print(a)
    br_patt = "Firefox|MSIE|Chrome"
    b = count_patt(fname,br_patt)
    print(b)
```
实现此案例还可通过面向对象方式实现：

实现过程：

1. 创建类CountPatt

2. 定义构造方法 创建正则对象

3. 定义类方法

4. 创建计数器对象

5. 打开文本文件

6. 通过正则表达式查找文件每一行

7. 如果找到结果

8. 将结果添加到计数器，通过update方法更新原有数据

9. 返回计数器

10. 将文件地址和正则表达式作为实参传递给函数
```shell
[root@localhost day08]# vim count_patt2.py
#!/usr/bin/env python3
import re
import collections
import re
import collections
class CountPatt:
    
    def __init__(self,patt):
        self.cpatt = re.compile(patt)
    
    def count_patt(self,fname):
        
        counter = collections.Counter()
       
        with open(fname) as fobj:
       
            for line in fobj:
       
                m = self.cpatt.search(line)
        
                if m:
        
                    counter.update([m.group()])
    
        return counter
if __name__ == "__main__":
    fname = "access_log.txt"
    ip_patt = "^(\d+\.){3}\d+"
    br_patt = "Firefox|MSIE|Chrome"
    ip = CountPatt(ip_patt)
    print(ip.count_patt(fname))
    br = CountPatt(br_patt)
    print(br.count_patt(fname))
```
步骤二：测试脚本执行
```shell
[root@localhost day08]# python3 count_patt.py 
Counter({‘172.40.0.54’：391，‘172.40.50.116’：244，‘201.1.1.254’：173，‘127.0.0.1’：121，‘201.1.2.254’：119})
Counter({‘Firefox’：870，‘MSIE’：391，‘Chrome’：24})
[root@localhost day08]# python3 count_patt2.py 
Counter({‘172.40.0.54’：391，‘172.40.50.116’：244，‘201.1.1.254’：173，‘127.0.0.1’：121，‘201.1.2.254’：119})
Counter({‘Firefox’：870，‘MSIE’：391，‘Chrome’：24})
```

# Exercise
## 1 在OOP编程时，常用的magic魔法方法有哪些？
- __init__：实例化类实例时默认会调用的方法
- __str__：打印/显示实例时调用方法
- __call__：用于创建可调用的实例

## 2 在OOP编程时，什么时候使用组合，什么时候使用派生？
- 当类之间有显著的不同，并且较小的类是较大的类所需要的组件时组合表现得很好
- 但当设计“相同的类但有一些不同的功能”时，使用派生

## 3 如何用正则表达式匹配全部是数字的字符串？
- '^\d+$'
- '^\[0-9]+$'

## 4 re.match和re.search的区别是什么？
- re.match只能从字符串的开头匹配
- re.search可以在字符串的任意位置匹配

## 5 通过什么方法可以将以下正则表达式匹配到的内容提取出来？
> ```shell
> m = re.search('f..', 'seafood')
> ```

```shell
m.group()
```

## 6 如何通过正则表达式匹配字符串中所有符合条件的子串。
- re.findall方法
- re.finditer方法

## 7 re.compile作用是什么？
- 对正则表达式模式进行编译，返回一个正则表达式对象
- 在大量匹配的情况下，可以提升效率


> 如有侵权，请联系作者删除
