# 集合set的操作
# 创建集合
set01 = {1, "hello", (1, 2, 3)}
set02 = set("abc")
print(len(set01))  # 3
print("hello" in set01)  # True
for item in set01:
    print(item)
# 添加元素 add(item)
# set01.add(100)
# 删除元素
# 1. set.discard(item)
print("*"*30)
# set01.discard(1)
# set01.discard(50)  # 删掉不存在的元素,不报错
# 2. set.remove(item)
# set01.remove(1)
# set01.remove(50)  # 删掉不存在的元素,报错

a = {"nn", "bb", "kk"}
b = {"dd", "gg", "nn"}
# 交集  &   s1.intersection(s2)
res = a & b  # 共同关注
print(res)
# 差集
res = a - b  # b同学可能认识的人
# a.difference(b)
res = b - a  # a同学可能认识的人
# b.difference(a)
# 并集
res = a | b  # a.union(b)
# 不能有重复的元素: 对列表去重  set(list)
list01 = [1, 1, 2, 2, 3, 3]
print("before:", list01)
print("after:", list(set(list01)))


