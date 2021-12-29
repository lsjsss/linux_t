# python中的数据类型: tuple(元组)
# 元组: 就是一个不可变的列表, 是一个序列
tuple01 = (1, 2, "zhangsan", "lisi", [1, 2])
print(tuple01[2], tuple01[-2])
print(tuple01[:3])
# 创建长度为1的元组，需要在元素后面加逗号
tuple02 = ("hello", )
# tuple01[-1] = 100  元组不支持修改操作, 因为不可变
tuple03 = tuple01 + (100, 200)
print(tuple03)