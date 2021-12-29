# 案例：计算列表中所有大于0的数字的和  continue
# [1, 2, 3, -4, 5, -6]
list01 = [1, 2, 3, -4, 5, -6]
sum_for = 0  # 用于求和
for item in list01:  # 拿出列表中每一个元素，赋值给item
    if item < 0:
        continue
    sum_for += item
print("sum:", sum_for)

