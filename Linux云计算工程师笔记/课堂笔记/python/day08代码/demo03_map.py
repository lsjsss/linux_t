# map: 统一加工
list01 = [1, 2, 3, 4, 5]  # 每个数求平方再加1
list02 = []
for item in list01:
    list02.append(item**2+1)
print(list02)

# map(func, seq)  seq表示序列  11:22 上课
# def func(my_item):
#     return my_item ** 2 + 1
res = map(lambda my_item: my_item**2+1, list01)
res1 = map(lambda my_item: True if my_item > 3 else False, list01)
print(list(res))
print(list(res1))

