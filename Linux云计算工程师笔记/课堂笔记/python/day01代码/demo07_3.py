# python中的数据类型: 字符串
# 切片: str[start:end:step], 含头去尾
# start默认值: 起始  end默认值: 结尾   step默认值: 1
str01 = "myname"
print(str01[0:4:1])  # myna获取前四个字符
print(str01[:4])  # 获取前四个字符
print(str01[:100])  # 100超过了6，所以获取的是整个字符串
print(str01[::3])  # ma
# =====================================
# 要保证获取元素的顺序和step的顺序要一致
print(str01[-1:-7:-1])  # emanym
print(str01[::-1])  # emanym

# >>> "*" * 30
# '******************************'
# >>> "123!" * 3
# '123!123!123!'
# >>> "hello" in "hello world"
# True
# >>> "aaa" in "hello world"
# False
# >>> "aaa" not in "hello world"
# True
print("*" * 30)
print(str01[-1:-7:1])
# 含头去尾，-1对应的是e，为什么输出为空