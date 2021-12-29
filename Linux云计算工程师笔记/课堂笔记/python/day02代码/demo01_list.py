# python中的数据类型: list
# 1. 序列(有序的 -> 索引 -> 有切片)
# 2. 可变
list01 = [10, 20, "zhangsan", "lisi", [1, 2]]
print(list01[-1][1])  # [1, 2][1]
print(len(list01))   # 10:10 上课
print(list01[2], list01[-2])  # 列表支持索引
print(list01[1:4], list01[::-1])  # 列表支持切片
list02 = list01 + [100]  # 创建了新列表
print(list01[-1])
list01[-1] = -100  # 更新元素，在列表本身操作
print(list01)
list01.append(100)  # append(): 尾部添加单个元素
print(list01)
print(-100 not in list01)  # 支持in 和not in 操作


