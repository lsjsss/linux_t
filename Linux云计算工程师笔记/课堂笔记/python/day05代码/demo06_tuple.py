# 元组 tuple
tuple01 = (1, 2, 1, 4, 5)
# index(元素值) 求得某个元素的索引下标
print(tuple01.index(2))
# 如果元素重复出现多次，只会显示该元素第一次出现的索引位置
# 列表中同样适用
print(tuple01.index(1))  # 0
# 如果元组当中只有一个元素，那么在该元素后面必须加逗号
tuple02 = (1, )
print(type(tuple02))
