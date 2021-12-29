# 列表解析式: 了解  效率高，代码简洁
# list02 = [item for item in range(1, 6)]
# print(list02)
list03 = [item**2 for item in range(1, 6)]
print(list03)

list01 = []
for item in range(1, 6):  # 1 2 3 4 5
    list01.append(item**2)
print(list01)
