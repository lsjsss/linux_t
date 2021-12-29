# 生成器表达式
gen1 = (i+1 for i in range(5))
# print(next(gen1))
for item in gen1:
    print(item)

# 列表生成式
# [1, 2, 3, 4, 5]
list01 = [i+1 for i in range(5)]
# list02 = []
# for i in range(5):
#     list02.append(i+1)

# >>> sum((i for i in range(100000000)))
# 4999999950000000
# >>> sum([i for i in range(100000000)])
# kill



