# 可迭代对象和迭代器
# 可迭代对象: 只要实现了__iter__()函数
# 迭代器: 既需要实现__iter__()函数, 有需要实现__next__()

# for item in 可迭代对象:
# str list tuple dict set range()
# 可迭代对象 iter(可迭代对象) -> 获取迭代器
list01 = [1, 2, 3]
# 用while去实现for循环的功能
# 1. 获取列表list01的迭代器  -> next(迭代器)
iterator_a = iter(list01)
# 2.(迭代)通过迭代器获取可迭代对象的每一个元素next(迭代器)
while True:
    try:
        print(next(iterator_a))
    except StopIteration:
        break  # 当列表元素获取完，表示while循环终止




# for 是对 while 的一层封装
# for item in list01:
#     print(item)

# >>> from collections.abc import Iterable
# >>> from collections.abc import Iterator
# >>> isinstance(1, int)
# True
# >>> isinstance([1, 2, 3], list)
# True
# >>> isinstance([1, 2, 3], Iterable)
# True
# >>> isinstance(iter([1, 2, 3]), Iterable)
# True
# >>> isinstance([1, 2, 3], Iterator)
# False
