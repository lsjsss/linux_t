# 可迭代对象: list str tuple dict
# 遍历元组
tuple01 = (1, 2, 3, 4, 5)
for item in tuple01:
    print("tuple item: " + str(item))
# 遍历字符串
str01 = "a bc"
for item in str01:
    print("str item: " + item)
# 遍历字典：默认遍历字典所有的key
dict01 = {"name": "zs", "age": 18}
for key in dict01:
    print(key, dict01[key])