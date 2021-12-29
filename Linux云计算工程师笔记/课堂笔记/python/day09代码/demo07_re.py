# Python使用正则  re
import re
# re.match(正则表达式, 目标字符串):
#       从头开始匹配,如果匹配成功，则返回一个匹配对象；
#       否则返回 None
res = re.match("foo", "food")
print(res)
print(res.group())  # 获取到匹配的字符串
# re.search(正则表达式, 目标字符串)
#   在字符串中查找正则表达式模式的第一次出现，
#   如果匹配成功，则返回一个匹配对象；否则返回 None
res = re.search("\d{3}", "aaa321bbb456vvv")
print(res)  # \d表示一个0~9的数字，{3}表示连续出现3次
print(res.group())
# re.findall(正则表达式, 目标字符串)
# 在字符串中查找正则表达式模式的所有（非重复）出现；
# 返回一个匹配对象的列表
res = re.findall("\d{3}", "aaa321bbb456vvv")
print(res)
print("*" * 30)
# finditer: 查找字符串中所有匹配字符【返回迭代器】
iter = re.finditer("\d{3}", "aaa321bbb456vvv")
for item in iter:
    print(item.group())
print("*" * 30)
# re.split(正则表达式, 目标字符串): 切割
str01 = "hello-world-how.tar.gz"
res = re.split("-|\.", str01)
print(res)
str02 = "aaa321bbb456vvv"
res = re.split("\d{3}", str02)
print(res)
# re.sub(正则, ): 替换
res = re.sub("\d{3}", "nfx",
             "Hi 333 , Nice to meet you!")
print(res)
