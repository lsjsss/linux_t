# 匿名函数
import random
def add(a, b):
    return a + b
# print(add(1, 2))
myadd = lambda a, b: a + b
# print(myadd(10, 20))

list01=[random.randint(1, 100) for i in range(10)]
list02 = []
# 过滤出偶数，添加到新列表
for item in list01:
    if item % 2 == 0:
        list02.append(item)
print("list02:", list02)
# filter(func, seq): 过滤
# def func01(item):
#     return True if item % 2 == 0 else False
    # if item % 2 == 0:
    #     return True
    # return False
# lambda item: True if item % 2 == 0 else False
res = filter(lambda item: True if item % 2 == 0 else False, list01)
print("filter:", list(res))  # 将res转换成list的类型
