# 正则: re.compile(正则表达式)
#     作用：将正则表达式进行编译
#     不是必须的方式，但是数据大量匹配可以提高效率
import re
# 正则表达式编译的过程: 匹配开头f的长度为3的字符串
patt = re.compile("f..")
# 用编译好的正则进行匹配
m = patt.search("seafood is food")
print(m)  # Match object
print(m.group())  # 获取到匹配的字符串


# re.match("\d{3}", "aaa333aaa")
# 1.现将正则表达式进行编译
# 2.使用编译好的正则进行数据匹配
# re.match("\d{3}", "bbb444bbb")
# 1.现将正则表达式进行编译
# 2.使用编译好的正则进行数据匹配
