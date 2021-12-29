# 字典
# 创建字典
# 1.常规，要求掌握
dict01 = {"name": "zs", "age": 18}
# 2. 骚操作，要求见过
dict02 = dict([["name", "ls"], ["age", 20]])
dict03 = {}.fromkeys(("ww", "zl"), 18)
# 查询
info = {"name": "nfx", "age": 18, "status": "lived"}
print(info["name"])  # nfx
print("age" in info)  # 判断某个key在不在字典当中
# print(info["sex"])  # 如果key不存在，则报错
# dict.get(key, default_value)
# 如果key不存在，则返回default_value,默认是None
print(info.get("sex", "ye men er"))
# 获取字典中所有的key  dict.keys()
print(info.keys())  # 10:05上课
for key in info:  # 相当于 for key in info.keys():
    print(key, info[key])
# 获取字典中所有的value  dict.values()
print(info.values())
# 获取字典中所有的 kv 对儿   dict.items()
print(info.items())
# [('name','nfx'),('age', 18),('status','lived')]
for item in info.items():
    print(item)
for k, v in info.items():
    print(k, v)
print("*" * 30)
# 更新/添加
# info = {"name": "nfx", "age": 18, "status": "lived"}
# 1. dict.update(字典):key如果在原字典中存在，则更新，不存在添加
# info.update({"age": 19, "sex": "nan"})
# 2. dict[key] = new_value, key不存在则新添加kv对
# info["age"] = 20
# 3. dict.setdefault(key, default)
# 如果字典中不存在key，由dict[key]=default为它赋值
# info.setdefault("sex", "nan")
# info.setdefault("age", 20)

# 删除
# 1. dict.pop(key) 根据key弹出元素并返回
# temp = info.pop("status")
# 2. del dict[key] 删除元素不返回
# del info["name"]
# 3. dict.clear()  清空字典元素
# info.clear()
# 其他
# 1. len(dict): 返回键值对的个数
# print(len(info))
# 2. hash(data): 可以判断是否可以作为字典的键
#   - 报错，data可变，不能作为字典的key
#   - 不报错，data不可变，能作为字典的key
# dict01[[1, 2, 3]] = ["a", "b"]  # 报错，列表可变
