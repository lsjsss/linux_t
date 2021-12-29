# range(start, end, step): 返回一个范围的整数们
# 1. 控制for循环的次数
for item in range(5):
    print("hello world")  # 打印5次hello world
# 2. 表示序列的索引值
# 拿到列表当中索引值为偶数的元素
list01 = ["zs", "ls", "ww", "zl"]
for i in range(4):  # i: 0 1 2 3
    if i % 2 == 0:  # 对2取余数为0的是偶数
        print(list01[i])
