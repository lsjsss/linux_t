# python中的数据类型: dict(字典)
# 每一个元素称为: 键值对儿(key-value)
# 特点：
#   - dict中的key不重复
#   - dict是无序的
# 1. 拼音   声母表  韵母表
# 2. 偏旁部首
#   - 具体的字    牛 ------- 10
dict01 = {"niu": 10, "wang": 100}
dict02 = {"niu": 10, "wang": 10}
# 查询是通过key获取到对应的value
print(dict01["niu"], dict01["wang"])
dict01["niu"] = 11  # 如果key存在，相当于是修改value
dict01["a"] = 1  # 如果key不存在，相当于添加kv对
print(dict01)
grades = {"yuwen": 80, "shuxue": 70, "yingyu": 0}
print(grades["yuwen"])
