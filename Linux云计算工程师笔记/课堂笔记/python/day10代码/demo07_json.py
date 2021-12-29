# json: 高效的数据交互格式, 就是一个字符串
# 1. dict -> json
import json
dict01 = {"name": "zs", "age": 18}
# '{"name": "zs", "age": 18}'
res = json.dumps(dict01)  # dict -> json
print(res)
print(type(res))
# 2. json -> dict
tmp = json.loads(res)
print(type(tmp))
print(tmp["name"])
